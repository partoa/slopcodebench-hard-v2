#!/usr/bin/env python3
"""Arm C retrospective: checkpoint snapshots + method/sensor evidence.

Uses ONLY commits of the current fresh local experiment and a version-pinned
sensor. Does not incorporate external grades, prior solutions, or hidden tests.
"""
from __future__ import annotations
import json,re,subprocess,tarfile,tempfile,io
from pathlib import Path
from maintenance_sensor import project_snapshot,compare
from change_impact import analyze


def own_history(repo:Path):
    cp={}
    lines=subprocess.check_output(['git','-C',str(repo),'log','--reverse','--format=%H %s'],text=True).splitlines()
    for line in lines:
        sha,subject=line.split(' ',1)
        match=re.search(r'Checkpoint ([1-8])\b',subject)
        if match:cp[int(match.group(1))]={'sha':sha,'subject':subject}
    if set(cp)!=set(range(1,9)):
        raise ValueError('Expected individually committed checkpoints 1–8; got '+repr(sorted(cp)))
    return cp


def unpack_checkout(repo,sha,dest):
    blob=subprocess.check_output(['git','-C',str(repo),'archive','--format=tar',sha])
    with tarfile.open(fileobj=io.BytesIO(blob)) as tar:
        for member in tar:
            resolved=(dest/member.name).resolve()
            if not resolved.is_relative_to(dest.resolve()):raise ValueError('Unsafe archive member')
        tar.extractall(dest,filter='data')


def main(repo:Path,output:Path):
    repo=repo.resolve();output=output.resolve();output.mkdir(parents=True,exist_ok=True)
    records=[];prior=None
    for cp,row in sorted(own_history(repo).items()):
        with tempfile.TemporaryDirectory() as tmp:
            d=Path(tmp);unpack_checkout(repo,row['sha'],d)
            snap=project_snapshot(d,['recli','appctl.py'],f'checkpoint-{cp}')
        if not snap['scope']['complete']:
            raise ValueError(f'Incomplete syntax coverage in checkpoint {cp}')
        record={**row,'checkpoint':cp,'summary':snap['summary'],
                'n_files':len(snap['scope']['requested_sources']),
                'sensor_version':snap['sensor_version']}
        (output/f'stage_{cp}_snapshot.json').write_text(json.dumps(snap,indent=2)+'\n')
        if prior is not None:
            assessment=analyze(prior,snap)
            (output/f'stage_{cp}_change.json').write_text(json.dumps(assessment,indent=2)+'\n')
            record['change_status']=assessment['structural']['status']
            record['added_files']=assessment['structural']['source_scope_evolution']['added_files']
            record['mass_delta']=assessment['structural']['deltas']['total_mass_proxy']
            record['high_mass_delta']=assessment['structural']['deltas']['high_mass_proxy']
            record['ratio_dilution_warning']=assessment['structural']['ratio_dilution_candidate']
        records.append(record);prior=snap
    report={'schema_version':1,'origin':'CLEAN_ARM_C_LOCAL_CHECKPOINTS',
            'provenance_limit':'Self-authored tests and public specification only; checkpoint code histories are those of this run.',
            'maintenance_ease':'NOT_MEASURED','causal_architecture_benefit':'NOT_ESTABLISHED',
            'sensor_completeness':'COMPLETE_FOR_DECLARED_PYTHON_SYNTAX_ONLY',
            'checkpoints':records}
    (output/'trend.json').write_text(json.dumps(report,indent=2)+'\n')
    return report

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path('.'));p.add_argument('--output',type=Path,default=Path('records/metrics'))
    args=p.parse_args();r=main(args.repo,args.output)
    for entry in r['checkpoints']:
        s=entry['summary']
        print(entry['checkpoint'],entry['n_files'],s['functions'],round(s['total_mass_proxy'],2),
              round(s['high_mass_proxy'],2),s['max_cc_proxy'],entry.get('change_status','baseline'))
