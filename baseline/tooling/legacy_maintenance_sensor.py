#!/usr/bin/env python3
"""Explicit-scope Python structural observations, never a maintenance verdict.

snapshot --root ROOT --label REV --source file.py [--source another.py]
compare BEFORE.json AFTER.json
Uses no external packages and never imports or executes inspected code.
"""
import argparse
import ast
from collections import Counter, defaultdict
import hashlib
import io
import json
import math
from pathlib import Path
import tokenize

VERSION = '1.1'
# Versioned to avoid comparing incompatible output without an explicit re-scan.
FUNCTIONS = (ast.FunctionDef, ast.AsyncFunctionDef)
SCOPES = FUNCTIONS + (ast.ClassDef, ast.Lambda)
CONTROL = (ast.If, ast.For, ast.AsyncFor, ast.While, ast.Try, ast.Match)
LIMITS = [
    'Python named functions only; module execution and lambda bodies are not profiled.',
    'CC is the documented AST decision proxy, not exact scb-check compatibility.',
    'Calls are lexical sites, not resolved dependencies or runtime execution counts.',
    'Repeated syntax does not establish stable values, purity, reachability or safe reuse.',
    'Comparison matches file and qualified name; renames/moves appear as removals/additions.',
    'Duplicate qualified names use source-order ordinals; their cross-version identity is uncertain.',
    'No maintenance effort, domain necessity, semantic coupling or defect is inferred.',
]


def digest(value):
    return hashlib.sha256(value).hexdigest()


def owned_nodes(node, depth=0):
    """Do not attribute nested scopes or their definition-time expressions to this body."""
    if isinstance(node, SCOPES):
        return
    yield node, depth
    next_depth = depth + isinstance(node, CONTROL)
    for child in ast.iter_child_nodes(node):
        if not isinstance(child, SCOPES):
            yield from owned_nodes(child, next_depth)


def decisions(node):
    if isinstance(node, (ast.If, ast.For, ast.AsyncFor, ast.While,
                         ast.ExceptHandler, ast.IfExp, ast.Assert)):
        return 1
    if isinstance(node, ast.BoolOp):
        return len(node.values) - 1
    if isinstance(node, ast.comprehension):
        return 1 + len(node.ifs)
    if isinstance(node, ast.match_case):
        wildcard = isinstance(node.pattern, ast.MatchAs) and node.pattern.pattern is None
        return int(not wildcard or node.guard is not None)
    return 0


def function_profile(path, qualname, ordinal, func, code_lines):
    nodes = [pair for statement in func.body for pair in owned_nodes(statement)]
    # Nested scope ranges are removed from the parent's source-line measure.
    excluded = set()
    for node, _ in nodes:
        for child in ast.iter_child_nodes(node):
            if isinstance(child, FUNCTIONS + (ast.ClassDef,)):
                start = min([child.lineno] + [d.lineno for d in getattr(child, 'decorator_list', [])])
                excluded.update(range(start, child.end_lineno + 1))
    # A nested scope can itself be a direct statement.
    for statement in func.body:
        if isinstance(statement, FUNCTIONS + (ast.ClassDef,)):
            start = min([statement.lineno] + [d.lineno for d in getattr(statement, 'decorator_list', [])])
            excluded.update(range(start, statement.end_lineno + 1))
    nodes = [(node, depth) for node, depth in nodes if not isinstance(node, SCOPES)]
    cc = 1 + sum(decisions(node) for node, _ in nodes)
    sloc = len((code_lines & set(range(func.lineno, func.end_lineno + 1))) - excluded)
    calls = []
    repeats = defaultdict(list)
    for node, _ in nodes:
        if isinstance(node, ast.Call):
            expression = ast.unparse(node)
            calls.append({'line': node.lineno, 'column': node.col_offset,
                          'callee': ast.unparse(node.func), 'expression': expression})
            repeats[expression].append({'line': node.lineno, 'column': node.col_offset})
    return {
        'id': f'{path}:{qualname}' + (f'#{ordinal}' if ordinal > 1 else ''),
        'qualified_name': qualname, 'definition_ordinal': ordinal,
        'line': func.lineno, 'end_line': func.end_lineno,
        'ast_sha256': digest(ast.dump(func, include_attributes=False).encode()),
        'code_lines': sloc, 'cc_proxy': cc, 'mass_proxy': cc * math.sqrt(max(1, sloc)),
        'max_control_nesting': max((depth + isinstance(node, CONTROL) for node, depth in nodes), default=0),
        'decision_sources': dict(Counter(type(node).__name__ for node, _ in nodes if decisions(node))),
        'call_sites': calls,
        'repeated_call_syntax': [{'expression': expression, 'sites': sites,
                                  'status': 'REQUIRES_VALUE_EFFECT_AND_EXECUTION_EVIDENCE'}
                                 for expression, sites in sorted(repeats.items()) if len(sites) > 1],
    }


def inspect_source(path, raw):
    # tokenize.open-style encoding recognition, without importing the target.
    encoding, _ = tokenize.detect_encoding(io.BytesIO(raw).readline)
    source = raw.decode(encoding)
    tree = ast.parse(source)
    code_lines = set()
    ignored = {tokenize.ENCODING, tokenize.ENDMARKER, tokenize.NEWLINE, tokenize.NL,
               tokenize.INDENT, tokenize.DEDENT, tokenize.COMMENT}
    for token in tokenize.generate_tokens(io.StringIO(source).readline):
        if token.type not in ignored:
            code_lines.update(range(token.start[0], token.end[0] + 1))
    profiles = []
    seen = Counter()

    class Discover(ast.NodeVisitor):
        def __init__(self):
            self.scope = []

        def visit_ClassDef(self, node):
            self.scope.append(node.name)
            for statement in node.body:
                self.visit(statement)
            self.scope.pop()

        def visit_FunctionDef(self, node):
            qualname = '.'.join(self.scope + [node.name])
            seen[qualname] += 1
            profiles.append(function_profile(path, qualname, seen[qualname], node, code_lines))
            self.scope.append(node.name)
            for statement in node.body:
                self.visit(statement)
            self.scope.pop()

        visit_AsyncFunctionDef = visit_FunctionDef

    Discover().visit(tree)
    return profiles


def snapshot(root, sources, label, threshold=10, *, project_roots=None):
    root = Path(root).resolve()
    files, functions = [], []
    for relative in sorted(set(sources)):
        target = (root / relative).resolve()
        target.relative_to(root)  # Fail explicit requests outside the declared scope.
        path = target.relative_to(root).as_posix()
        info = {'path': path}
        try:
            raw = target.read_bytes()
            info['sha256'] = digest(raw)
            found = inspect_source(path, raw)
            info.update(status='SCANNED', functions=len(found))
            functions.extend(found)
        except (OSError, SyntaxError, UnicodeError, LookupError, tokenize.TokenError) as exc:
            info.update(status='UNSCANNED', error_type=type(exc).__name__, error=str(exc))
        files.append(info)
    mass = sum(f['mass_proxy'] for f in functions)
    high = [f for f in functions if f['cc_proxy'] > threshold]
    high_mass = sum(f['mass_proxy'] for f in high)
    return {
        'schema_version': 1, 'sensor_version': VERSION, 'label': label,
        'sensor_sha256': digest(Path(__file__).read_bytes()),
        'scope': {'requested_sources': sorted(set(sources)),
                  'policy': 'project_recursive' if project_roots is not None else 'explicit',
                  'project_roots': sorted(set(project_roots or [])), 'files': files,
                  'complete': all(f['status'] == 'SCANNED' for f in files) and bool(files)},
        'definition': 'CC proxy = 1 + if/loop/except/ternary/assert + boolean extra operands + comprehension generators/filters + non-default or guarded match cases. Nested scopes excluded. Code lines contain non-comment tokens, including docstrings; nested definitions excluded. Definition-time expressions on nested scopes are not attributed.',
        'limitations': LIMITS,
        'summary': {'functions': len(functions), 'threshold': threshold,
                    'total_mass_proxy': mass, 'high_mass_proxy': high_mass,
                    'high_mass_fraction_proxy': high_mass / mass if mass else None,
                    'high_cc_functions': len(high),
                    'max_cc_proxy': max((f['cc_proxy'] for f in functions), default=None)},
        'functions': functions,
    }


def project_snapshot(root, project_roots, label, threshold=10):
    """A versioned project-wide source scope that permits deliberate file additions.

    Only declared source roots are inspected; tests/tooling do not silently enter
    the maintenance denominator. Rename and deletion remain unresolved identities.
    """
    base = Path(root).resolve()
    roots = sorted(set(project_roots))
    sources = []
    for relative in roots:
        target = (base / relative).resolve()
        target.relative_to(base)
        if target.is_file() and target.suffix == '.py':
            sources.append(target.relative_to(base).as_posix())
        elif target.is_dir():
            sources.extend(p.relative_to(base).as_posix() for p in target.rglob('*.py')
                           if '__pycache__' not in p.parts)
        else:
            raise ValueError('Declared project source root missing: ' + relative)
    return snapshot(base, sources, label, threshold, project_roots=roots)


def compare(before, after):
    for snapshot_ in (before, after):
        if snapshot_['schema_version'] != 1 or snapshot_['sensor_version'] != VERSION:
            raise ValueError('Incompatible sensor versions')
    old, new = ({f['id']: f for f in s['functions']} for s in (before, after))
    rows = []
    for identity in sorted(old.keys() | new.keys()):
        a, b = old.get(identity), new.get(identity)
        status = 'ADDED' if a is None else 'REMOVED' if b is None else 'UNCHANGED' if a['ast_sha256'] == b['ast_sha256'] else 'CHANGED'
        rows.append({'id': identity, 'status': status,
                     'delta': {key: b[key] - a[key] for key in ('cc_proxy', 'code_lines', 'mass_proxy', 'max_control_nesting')} if a and b else None})
    project_scope = (before['scope'].get('policy') == 'project_recursive' and
                     after['scope'].get('policy') == 'project_recursive' and
                     before['scope'].get('project_roots') == after['scope'].get('project_roots'))
    oldfiles, newfiles = (set(x['scope']['requested_sources']) for x in (before, after))
    return {'schema_version': 1, 'before': before['label'], 'after': after['label'],
            'coverage_complete': before['scope']['complete'] and after['scope']['complete'],
            'same_requested_scope': before['scope']['requested_sources'] == after['scope']['requested_sources'],
            'comparable_project_scope': project_scope and before['scope']['complete'] and after['scope']['complete'],
            'scope_evolution': {'added_files': sorted(newfiles-oldfiles), 'removed_files': sorted(oldfiles-newfiles)},
            'scope_caveat': 'Source-file additions or removals are intentional coverage changes only when project roots match; semantic identity and total effort remain unresolved.',
            'same_threshold': before['summary']['threshold'] == after['summary']['threshold'],
            'summaries': {'before': before['summary'], 'after': after['summary']},
            'matching': 'Exact file/qualified-name/source-order ordinal; renames, moves and duplicate-name reordering are unresolved.',
            'functions': rows, 'maintenance_difficulty': 'NOT_MEASURED',
            'interpretation': 'A change in structural measurements is not evidence that maintenance became easier or harder. Inspect additions/removals, absolute mass, denominator, call sites, source and task evidence.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    scan = commands.add_parser('snapshot')
    scan.add_argument('--root', type=Path, required=True)
    scan.add_argument('--label', required=True)
    scan.add_argument('--source', action='append')
    scan.add_argument('--project-root', action='append', help='Explicit source root for recursive project scope')
    scan.add_argument('--threshold', type=int, default=10)
    diff = commands.add_parser('compare')
    diff.add_argument('before', type=Path)
    diff.add_argument('after', type=Path)
    args = parser.parse_args()
    if args.command == 'snapshot':
        if bool(args.source) == bool(args.project_root):
            parser.error('snapshot requires either --source or --project-root, not both')
        result = (project_snapshot(args.root, args.project_root, args.label, args.threshold)
                  if args.project_root else snapshot(args.root, args.source, args.label, args.threshold))
        code = 0 if result['scope']['complete'] else 2
    else:
        result = compare(json.loads(args.before.read_text()), json.loads(args.after.read_text()))
        code = 0 if result['coverage_complete'] else 2
    print(json.dumps(result, indent=2))
    return code


if __name__ == '__main__':
    raise SystemExit(main())
