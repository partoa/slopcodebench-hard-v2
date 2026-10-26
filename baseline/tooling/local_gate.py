#!/usr/bin/env python3
"""Reproducible *authored* local check capture; not an official benchmark runner.

Timeouts are incomplete, not passes. Raw stdout and stderr are never interpreted
as semantic evidence of correctness by themselves.
"""
from __future__ import annotations
import argparse,hashlib,json,platform,subprocess,sys,time
from pathlib import Path


def run(repo, output, argv, *, timeout=50, sources=('appctl.py',), kind='authored_local'):
    repo=Path(repo).resolve();output=Path(output).resolve()
    output.mkdir(parents=True,exist_ok=True)
    source_hashes={}
    for item in sources:
        target=(repo/item).resolve()
        if not target.is_relative_to(repo) or not target.is_file():
            raise ValueError('missing or escaped declared source file: '+item)
        source_hashes[item]=hashlib.sha256(target.read_bytes()).hexdigest()
    start=time.monotonic()
    timed_out=False
    try:
        cp=subprocess.run(argv,cwd=repo,capture_output=True,timeout=timeout,check=False)
        stdout,stderr=cp.stdout,cp.stderr;exit_code=cp.returncode
    except subprocess.TimeoutExpired as err:
        stdout=err.stdout or b'';stderr=err.stderr or b''
        exit_code=None;timed_out=True
    elapsed=time.monotonic()-start
    (output/'stdout.bin').write_bytes(stdout)
    (output/'stderr.bin').write_bytes(stderr)
    report={'schema_version':1,'category':'AGENT_AUTHORED_NOT_OFFICIAL',
            'status':'TIMEOUT_INCOMPLETE' if timed_out else 'PASS_EXIT_ZERO' if exit_code==0 else 'FAIL_EXIT_NONZERO',
            'command':argv,'timeout_seconds':timeout,'elapsed_seconds':elapsed,
            'exit_code':exit_code,'python':platform.python_version(),
            'source_sha256':source_hashes,
            'stdout_sha256':hashlib.sha256(stdout).hexdigest(),
            'stderr_sha256':hashlib.sha256(stderr).hexdigest(),
            'cwd':str(repo),'kind':kind}
    (output/'results.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path('.'))
    p.add_argument('--output',type=Path,required=True);p.add_argument('--timeout',type=float,default=50)
    p.add_argument('--source',action='append',default=[])
    p.add_argument('argv',nargs=argparse.REMAINDER)
    a=p.parse_args();argv=a.argv
    if argv and argv[0]=='--':argv=argv[1:]
    if not argv:p.error('command required after --')
    r=run(a.repo,a.output,argv,timeout=a.timeout,sources=a.source or ['appctl.py'])
    print(json.dumps(r,indent=2))
    return 0 if r['status']=='PASS_EXIT_ZERO' else 2 if r['status']=='TIMEOUT_INCOMPLETE' else 1

if __name__=='__main__':raise SystemExit(main())
