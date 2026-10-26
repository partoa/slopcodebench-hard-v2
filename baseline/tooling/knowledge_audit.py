#!/usr/bin/env python3
"""Bounded active-knowledge and independent-question review scheduler.

A source/scope index is not a proof of relevance or completeness. Uses no Git state.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path

VALID_SCOPES = {'file', 'folder', 'obligation', 'component', 'domain', 'node'}
OPEN = {'OPEN', 'CANDIDATE', 'PROVISIONAL', 'INCONCLUSIVE'}

def canonical(value):return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()
def fingerprint(value):return hashlib.sha256(canonical(value)).hexdigest()
def checked_scope(x):
    if not isinstance(x,str) or ':' not in x:return False
    kind,val=x.split(':',1)
    return kind in VALID_SCOPES and bool(val.strip()) and not val.startswith('/') and '..' not in val.split('/')
def linked(a,b):
    if a==b:return True
    ka,pa=a.split(':',1);kb,pb=b.split(':',1)
    if ka=='folder' and kb in {'file','folder'}:return pb.startswith(pa.rstrip('/')+'/')
    if kb=='folder' and ka in {'file','folder'}:return pa.startswith(pb.rstrip('/')+'/')
    return False

def audit(ledger:dict):
    issues=[];ids=set();seen={}
    if not isinstance(ledger.get('records'),list) or not isinstance(ledger.get('links'),list):
        return {'valid':False,'errors':['records and links must be arrays']}
    for row in ledger['records']:
        if not isinstance(row,dict):issues.append('non-object record');continue
        rid=row.get('id')
        if not isinstance(rid,str) or not re.fullmatch('[A-Za-z][A-Za-z0-9._-]{2,79}',rid) or rid in ids:
            issues.append('duplicate or invalid record id: '+str(rid));continue
        ids.add(rid)
        ret=row.get('retention')
        if not isinstance(ret,dict):issues.append(rid+': no retention justification');continue
        for k in ('reason','value_if_retained','review_trigger','why_not_existing'):
            if not isinstance(ret.get(k),str) or not ret[k].strip():issues.append(rid+': empty '+k)
        estimate=ret.get('maintenance_estimate_minutes')
        if type(estimate) not in (float,int) or estimate<0:issues.append(rid+': bad maintenance estimate')
        refs=row.get('scope_refs',[])
        if not isinstance(refs,list) or not all(checked_scope(x) for x in refs):
            issues.append(rid+': malformed scopes');refs=[]
        if not refs and not row.get('anchors') and not row.get('scope_unknown_reason'):
            issues.append(rid+': unbound/no scope must explain the gap')
        dup=(row.get('kind'), ' '.join(str(row.get('statement','')).lower().split()),tuple(sorted(refs)))
        if dup[1] and dup in seen:issues.append(rid+': duplicates '+seen[dup])
        seen[dup]=rid
        if row.get('kind')=='question':
            if row.get('status') not in OPEN:issues.append(rid+': resolved question must be removed from active records')
            p=row.get('priority')
            if not isinstance(p,dict) or any(type(p.get(k)) is not int or not 0<=p[k]<=5 for k in ('impact','uncertainty','urgency')):
                issues.append(rid+': priority needs impact/uncertainty/urgency 0..5')
    for link in ledger['links']:
        if not isinstance(link,dict) or link.get('from') not in ids or link.get('to') not in ids:
            issues.append('dangling link: '+str(link))
    return {'valid':not issues,'errors':issues,'total_records':len(ids),
            'meaning':'shape, uniqueness and maintenance contract only; obligations can be missing'}

def plan(ledger, stage:int, new_scopes:list[str], budget_minutes:float):
    check=audit(ledger)
    if not check['valid']:raise ValueError('; '.join(check['errors']))
    if any(not checked_scope(s) for s in new_scopes):raise ValueError('Invalid evidence scope')
    q=[r for r in ledger['records'] if r.get('kind')=='question' and r.get('status') in OPEN]
    def rank(r):
        p=r['priority'];return 4*p['impact']+3*p['uncertainty']+2*p['urgency']+min(5,max(0,stage-r.get('last_review_stage',stage)))
    top=sorted(q,key=lambda r:(-rank(r),-int(not r.get('anchors')),r['id']))[:5]
    top_ids={r['id'] for r in top}
    selected=[];deferred=[]
    for r in q:
        refs=list(r.get('scope_refs') or [])
        for a in r.get('anchors') or []:
            if isinstance(a,dict) and a.get('path'):refs.append('file:'+a['path'])
        match=bool(new_scopes) and any(linked(a,b) for a in refs for b in new_scopes)
        if not match and r['id'] not in top_ids:continue
        selected.append({'id':r['id'],'question_sha256':fingerprint(r),
                         'selection_reason':'RELEVANT_UNBOUND' if match and not r.get('anchors') else
                          'RELEVANT_BOUND' if match else 'TOP_FIVE',
                         'score':rank(r),'estimated_minutes':r['retention']['maintenance_estimate_minutes'],
                         'top_five':r['id'] in top_ids})
    selected.sort(key=lambda r:({'RELEVANT_UNBOUND':0,'RELEVANT_BOUND':1,'TOP_FIVE':2}[r['selection_reason']],-r['score'],r['id']))
    total=sum(r['estimated_minutes'] for r in selected)
    return {'stage':stage,'existing_open_questions':len(q),'top_five':[r['id'] for r in top],
            'selected':selected,'skipped_irrelevant':len(q)-len(selected),
            'estimated_minutes':total,'budget_minutes':budget_minutes,'budget_exceeded':total>budget_minutes,
            'unscoped_questions':[r['id'] for r in q if not r.get('scope_refs') and not r.get('anchors')],
            'scope_unknown':len(new_scopes)==0,
            'warning':'Scope filtering is incomplete; investigate unknown scope; top five are not waived by budget.'}

def check_reviews(plan_data:dict, directory:Path):
    errors=[];seen=set();expected={r['id']:r for r in plan_data['selected']}
    for rid,row in expected.items():
        path=directory/(rid+'.json')
        try:
            r=json.loads(path.read_text())
            if r.get('question_id')!=rid or r.get('question_sha256')!=row['question_sha256']:
                raise ValueError('question changed since review or wrong question')
            why=r.get('independent_reasoning','')
            if not isinstance(why,str) or len(why.strip())<25:raise ValueError('missing question-specific reasoning')
            normalized=' '.join(why.lower().split())
            if normalized in seen:raise ValueError('duplicated review content')
            seen.add(normalized)
            if not isinstance(r.get('evidence_examined'),list):raise ValueError('evidence list required')
        except (OSError,ValueError,json.JSONDecodeError) as e:errors.append({'question':rid,'error':str(e)})
    for p in directory.glob('*.json') if directory.exists() else []:
        if p.stem not in expected:errors.append({'question':p.stem,'error':'orphan active review; remove with Git history'})
    return {'valid':not errors,'reviewed':len(expected)-len([x for x in errors if x['question'] in expected]),
            'required':len(expected),'errors':errors}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('command',choices=['audit','plan','reviews'])
    p.add_argument('--ledger',type=Path,required=True)
    p.add_argument('--stage',type=int,default=1)
    p.add_argument('--scope',action='append',default=[])
    p.add_argument('--budget-minutes',type=float,default=30)
    p.add_argument('--reviews',type=Path)
    a=p.parse_args()
    try:
        ledger=json.loads(a.ledger.read_text())
        if a.command=='audit':out=audit(ledger)
        elif a.command=='plan':out=plan(ledger,a.stage,a.scope,a.budget_minutes)
        else:
            if not a.reviews:p.error('--reviews required')
            out=check_reviews(plan(ledger,a.stage,a.scope,a.budget_minutes),a.reviews)
        print(json.dumps(out,indent=2))
        if out.get('valid') is False:raise SystemExit(1)
    except (OSError,ValueError,json.JSONDecodeError) as e:p.error(str(e))
if __name__=='__main__':main()
