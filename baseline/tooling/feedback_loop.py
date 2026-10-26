#!/usr/bin/env python3
"""Evidence-to-investigation planner for growing codebases.

Produces bounded candidates for contemplation; does not automatically replace
skills, suppress tests, grade architecture, or mutate production code.
"""
from __future__ import annotations
import json
from collections import defaultdict
from pathlib import Path


def candidates(records_dir):
    root=Path(records_dir)
    trend=json.loads((root/'trend.json').read_text())
    snapshots=[json.loads((root/f"stage_{row['checkpoint']}_snapshot.json").read_text())
               for row in trend['checkpoints']]
    issues=[]
    for idx, snap in enumerate(snapshots):
        if not snap['scope']['complete']:
            issues.append({'kind':'TOOL_COVERAGE_GAP','stage':idx+1,
                           'observation':'One or more source files were not scanned',
                           'action':'Repair coverage before interpreting change'})
    if len(snapshots)>=2:
        for previous,current in zip(snapshots,snapshots[1:]):
            p,c=previous['summary'],current['summary']
            if (p['high_mass_fraction_proxy'] is not None and
                    c['high_mass_fraction_proxy'] < p['high_mass_fraction_proxy'] and
                    c['high_mass_proxy'] >= p['high_mass_proxy']):
                issues.append({'kind':'METRIC_RATIO_DILUTION','stage':int(current['label'].split('-')[-1]),
                               'observation':'High-mass fraction fell while absolute high mass did not',
                               'action':'Do not infer improved maintainability from fraction'})
    longevity=defaultdict(list)
    for s in snapshots:
        for function in s['functions']:
            if function['cc_proxy']>s['summary']['threshold']:
                longevity[function['id']].append({'stage':s['label'],'cc_proxy':function['cc_proxy'],
                                                   'mass_proxy':function['mass_proxy']})
    for name, series in sorted(longevity.items()):
        if len(series)<3:continue
        severity=series[-1]['mass_proxy']-series[0]['mass_proxy']
        if severity<=0:continue
        issues.append({'kind':'PERSISTENT_GROWING_HOTSPOT','source':name,'observations':series,
                       'action':'Investigate concrete edit costs, responsibility boundaries, and known tests before refactor'})
    return {'schema_version':1,'type':'CANDIDATES_NOT_OBLIGATIONS',
            'reference':'Current clean local run only',
            'issues':issues,'retention_note':'Only promote candidates with evidence and prospective value. Delete unjustified records.',
            'automated_code_or_skill_change':False}

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--metrics-dir',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();result=candidates(a.metrics_dir);a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,indent=2)+'\n');print(len(result['issues']),'candidates (not obligations)')
