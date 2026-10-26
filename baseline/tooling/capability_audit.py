#!/usr/bin/env python3
"""Conservative, offline engineering audit helpers. No access to hidden evaluations.

Methods are observations, not claims of complete binding, control flow or obligations.
"""
from __future__ import annotations
import argparse
import ast
import hashlib
import json
import os
import platform
import re
import subprocess
import sys
import time
from pathlib import Path

SCHEMA_VERSION = 1

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def contained(root: Path, name: str) -> Path:
    if not isinstance(name, str) or not name or Path(name).is_absolute() or '..' in Path(name).parts:
        raise ValueError(f"Unsafe relative path: {name!r}")
    dest = (root / name).resolve()
    if not dest.is_relative_to(root.resolve()) or not dest.is_file():
        raise ValueError(f"Missing or escaped file: {name!r}")
    return dest

def _call_name(n: ast.AST) -> str:
    try:
        return ast.unparse(n)
    except Exception:
        return "<unprintable>"

class ScopeVisitor(ast.NodeVisitor):
    """Local AST observations. Never descend into unrelated nested definitions."""
    def __init__(self):
        self.calls = []
        self.writes = []
        self.reads = []
    def visit_FunctionDef(self, n):
        return  # nested code is not executed merely by defining it
    visit_AsyncFunctionDef = visit_FunctionDef
    def visit_ClassDef(self, n):
        return
    def visit_Name(self, n):
        row = {"name": n.id, "line": n.lineno, "col": n.col_offset}
        if isinstance(n.ctx, (ast.Store, ast.Del)):
            self.writes.append(row)
        elif isinstance(n.ctx, ast.Load):
            self.reads.append(row)
    def visit_Call(self, n):
        self.calls.append({"callee_syntax": _call_name(n.func), "line": n.lineno,
                           "col": n.col_offset, "binding_status": "UNRESOLVED"})
        self.generic_visit(n)

def _scopes(root: ast.AST):
    yield "<module>", root.body
    def visit(items, prefix=""):
        for node in items:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                name = prefix + node.name
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    yield name, node.body
                yield from visit(node.body, name + ".")
            elif isinstance(node, (ast.If, ast.For, ast.AsyncFor, ast.While, ast.With, ast.AsyncWith, ast.Try)):
                for child in ast.iter_child_nodes(node):
                    if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                        yield from visit([child], prefix)
    yield from visit(root.body)

def scan(root: Path, include=None) -> dict:
    root = root.resolve()
    paths = sorted(root.rglob('*.py')) if include is None else [contained(root, p) for p in include]
    results, failures, excluded = [], [], []
    for file in paths:
        rel = str(file.relative_to(root))
        if file.is_symlink():
            excluded.append({"path": rel, "reason": "symlink"})
            continue
        raw = file.read_bytes()
        try:
            node = ast.parse(raw.decode('utf-8'), filename=rel)
        except (SyntaxError, UnicodeError, ValueError) as err:
            failures.append({"path": rel, "sha256": digest(raw), "type": type(err).__name__,
                             "line": getattr(err, 'lineno', None), "message": str(err)[:400]})
            continue
        entry = {"path": rel, "sha256": digest(raw), "scopes": []}
        for name, body in _scopes(node):
            visitor = ScopeVisitor()
            for stmt in body:
                visitor.visit(stmt)
            counts = {}
            for call in visitor.calls:
                counts[call['callee_syntax']] = counts.get(call['callee_syntax'], 0) + 1
            entry['scopes'].append({"name": name, "reads": visitor.reads,
                                    "writes": visitor.writes, "call_sites": visitor.calls,
                                    "repeated_callee_syntax": {k:v for k,v in counts.items() if v>1}})
        results.append(entry)
    return {"schema_version": SCHEMA_VERSION, "status": "PARTIAL" if failures or excluded else "COMPLETE_FOR_SYNTAX",
            "coverage": {"considered": len(paths), "parsed": len(results), "failed": len(failures),
                         "excluded": len(excluded), "language": "python", "frontend": "stdlib.ast",
                         "frontend_python": platform.python_version()},
            "files": results, "parse_failures": failures, "excluded_files": excluded,
            "semantic_limits": ["syntactic call-site only", "no binding or alias resolution",
                                "no interprocedural or path-feasibility proof", "not a safe caching recommendation"]}

def verify_evidence(root: Path, manifest: Path) -> dict:
    """Verify arbitrary referenced artifacts; no special case for released prompts."""
    root = root.resolve()
    data = json.loads(manifest.read_text(encoding='utf-8'))
    records = data.get('artifacts')
    if not isinstance(records, list):
        raise ValueError("Manifest requires artifacts array")
    checks=[]
    for r in records:
        if not isinstance(r, dict):
            checks.append({"ok": False, "error": "not an artifact object"}); continue
        name = r.get('path')
        want = r.get('sha256')
        try:
            if not isinstance(want, str) or re.fullmatch('[0-9a-f]{64}', want) is None:
                raise ValueError("Missing valid sha256")
            file = contained(root, name)
            got = digest(file.read_bytes())
            checks.append({"path": name, "ok": got == want, "expected": want, "observed": got})
        except (OSError, ValueError) as err:
            checks.append({"path": name, "ok": False, "error": str(err)})
    return {"valid": all(x['ok'] for x in checks), "count": len(checks),
            "checked": checks, "meaning": "byte integrity only, not contract truth or independent execution"}

def capture(root: Path, command: list[str], *, timeout: float, max_bytes: int) -> dict:
    if not command or timeout <= 0 or max_bytes < 1:
        raise ValueError('Capture needs command, positive timeout and max_bytes')
    start = time.monotonic()
    # File-backed capture prevents in-memory unbounded stdout/stderr. The output
    # cap is a retained-bytes cap, not a hard disk/producer output limit.
    from tempfile import TemporaryFile
    with TemporaryFile() as stdout, TemporaryFile() as stderr:
        p = subprocess.Popen(command, cwd=root, stdout=stdout, stderr=stderr,
                             stdin=subprocess.DEVNULL, start_new_session=True)
        timed_out = False
        try: p.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            import signal
            os.killpg(p.pid, signal.SIGKILL)
            p.wait()
        duration = time.monotonic() - start
        streams = {}
        for name, file in [('stdout', stdout), ('stderr', stderr)]:
            size = file.tell(); file.seek(0)
            payload = file.read(max_bytes + 1)[:max_bytes]
            streams[name] = {"bytes_total":size,"bytes_retained":len(payload),
                             "truncated":size>len(payload), "sha256_retained":digest(payload),
                             "text_retained":payload.decode('utf-8','replace')}
        return {"command_argv":command,"exit_code":p.returncode,"timed_out":timed_out,
                "duration_seconds":round(duration,5),"status": "TIMEOUT" if timed_out else
                "INCOMPLETE_OUTPUT" if any(v['truncated'] for v in streams.values()) else
                "PASS" if p.returncode==0 else "FAIL", "streams":streams,
                "python":platform.python_version(), "capture_limits": {"timeout_seconds":timeout,
                "max_retained_bytes_per_stream":max_bytes},
                "note":"bounded retention; producer output may consume more disk before timeout"}

def skill_index(root: Path) -> dict:
    entries=[]
    for path in sorted(root.rglob('SKILL.md')):
        text=path.read_text(encoding='utf-8')
        front=re.search(r'\A---\s*\n(.*?)\n---\s*\n',text,re.S)
        attrs={}
        if front:
            for line in front.group(1).splitlines():
                if ':' in line:
                    k,v=line.split(':',1)
                    if k.strip() in ('name','description'):attrs[k.strip()]=v.strip().strip('"\'')
        title=next((line.strip('# ').strip() for line in text.splitlines() if line.startswith('# ')), '')
        summary=attrs.get('description') or title
        entries.append({"path":str(path.relative_to(root)),"sha256":digest(path.read_bytes()),
                        "name":attrs.get('name') or path.parent.name,"description":summary,
                        "index_status":"CANDIDATE_FOR_CONTEXTUAL_REVIEW"})
    return {"skills":entries,"count":len(entries),"selector_limit":"heading-independent indexing; lexical matching alone does not prove applicability"}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest='mode', required=True)
    for name in ('scan','skills'):
        q=sub.add_parser(name);q.add_argument('--root',type=Path,required=True)
    q=sub.add_parser('verify');q.add_argument('--root',type=Path,required=True);q.add_argument('--manifest',type=Path,required=True)
    q=sub.add_parser('capture');q.add_argument('--root',type=Path,required=True);q.add_argument('--timeout',type=float,default=60);q.add_argument('--max-bytes',type=int,default=1048576);q.add_argument('command',nargs=argparse.REMAINDER)
    a=p.parse_args()
    try:
        if a.mode=='scan': result=scan(a.root)
        elif a.mode=='skills':result=skill_index(a.root)
        elif a.mode=='verify':result=verify_evidence(a.root,a.manifest)
        else:result=capture(a.root,a.command[1:] if a.command and a.command[0]=='--' else a.command,timeout=a.timeout,max_bytes=a.max_bytes)
        print(json.dumps(result,indent=2))
        if result.get('valid') is False or result.get('status') in ('PARTIAL','FAIL','TIMEOUT','INCOMPLETE_OUTPUT'):sys.exit(1)
    except (ValueError,OSError,subprocess.SubprocessError,json.JSONDecodeError) as e:
        p.error(str(e))
if __name__=='__main__':main()
