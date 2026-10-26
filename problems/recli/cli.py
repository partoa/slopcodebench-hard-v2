"""Specification-derived hierarchical command-line dispatcher.

Commands are registered explicitly; no application-specific commands are assumed.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from difflib import get_close_matches
from typing import Callable, Optional
import os
import re
import sys


@dataclass
class Argument:
    name: str
    kind: str  # positional, keyed, flag, field
    required: bool = True
    repeated: bool = False
    default: object = None


@dataclass
class Command:
    name: str
    description: str = ""
    synopsis: str = ""
    handler: Optional[Callable] = None
    alias: Optional[str] = None
    children: dict[str, 'Command'] = field(default_factory=dict)
    defaults: dict[str, object] = field(default_factory=dict)


class SignatureError(ValueError):
    pass


def signature(synopsis: str) -> list[Argument]:
    """Parse supported synopsis tokens, rejecting malformed grammar."""
    result = []
    for raw in synopsis.split():
        required = not (raw.startswith('[') and raw.endswith(']'))
        token = raw if required else raw[1:-1]
        repeated = token.endswith('...')
        if repeated:
            token = token[:-3]
        if token == '--<field>=<value>':
            kind, name = 'field', 'field'
        elif re.fullmatch(r'<[A-Za-z][\w-]*>', token):
            kind, name = 'positional', token[1:-1]
        elif re.fullmatch(r'--\[no-\][A-Za-z][\w-]*', token):
            kind, name = 'flag', token[7:]
        elif re.fullmatch(r'--[A-Za-z][\w-]*', token):
            kind, name = 'flag', token[2:]
        elif re.fullmatch(r'--[A-Za-z][\w-]*=<[A-Za-z][\w-]*>', token):
            kind, name = 'keyed', token[2:].split('=', 1)[0]
        else:
            raise SignatureError('Malformed synopsis token: ' + raw)
        result.append(Argument(name, kind, required if kind in ('positional', 'keyed', 'field') else False, repeated))
    return result


def _sorted(values):
    return sorted(values, key=lambda c: (c.name.casefold(), c.name))


def _suggest(name: str, possibilities: list[str], synonyms: dict[str, str]):
    if name in synonyms and synonyms[name] in possibilities:
        return synonyms[name]
    choices = sorted(possibilities, key=lambda s: (s.casefold(), s))
    found = get_close_matches(name.casefold(), [s.casefold() for s in choices], n=1, cutoff=0.65)
    return next((c for c in choices if c.casefold() == found[0]), None) if found else None


class CLI:
    def __init__(self, executable='appctl', version='0.1.0', global_flags=None, synonyms=None):
        self.executable = executable
        self.version = version
        self.roots: dict[str, Command] = {}
        self.global_flags = set(global_flags or ())
        self.synonyms = dict(synonyms or {})
        self.register('help', 'Show command help', '[<command>...]', self._help_handler)
        self.register('cli version', 'Show CLI version', '', lambda _: self.version)

    def register(self, path, description='', synopsis='', handler=None, alias=None, defaults=None):
        segments = path.split()
        if not segments:
            raise ValueError('empty command path')
        roots = self.roots
        for i, part in enumerate(segments):
            node = roots.get(part)
            if node is None:
                node = Command(part)
                roots[part] = node
            if i == len(segments) - 1:
                node.description, node.synopsis, node.handler, node.alias = description, synopsis, handler, alias
                node.defaults = dict(defaults or {})
                signature(synopsis)
            roots = node.children
        return node

    def _resolve(self, parts):
        roots = self.roots
        current = None
        matched = []
        for index, part in enumerate(parts):
            target = roots.get(part) or next((v for v in roots.values() if v.alias == part), None)
            if target is None:
                if current is None:
                    return None, matched, parts[index:], ('top', part, '')
                if current.children and not part.startswith('-'):
                    return None, matched, parts[index:], ('sub', part, ' '.join(matched))
                break
            current = target
            matched.append(target.name)
            roots = target.children
        return current, matched, parts[len(matched):], None

    def help(self, command=None):
        if command:
            node, path, remaining, error = self._resolve(command.split())
            if node is None or remaining or error:
                return 'usage: ' + self.executable + ' help [<command>...]'
            prefix = ' '.join(path)
            heading = 'usage: ' + self.executable + ' ' + prefix + (' ' + node.synopsis if node.synopsis else '')
            children = _sorted(node.children.values())
        else:
            heading = 'usage: ' + self.executable + ' <command> [<args>] [--<flags>]'
            children = _sorted(self.roots.values())
        if children:
            width = max(len(c.name) for c in children)
            heading += '\nCommands:\n' + '\n'.join('  ' + ((prefix + ' ') if command else '') + c.name.ljust(width) + '  ' + c.description for c in children)
        return heading

    def _help_handler(self, values):
        args = values.get('command', [])
        if isinstance(args, str):
            args = [args]
        return self.help(' '.join(args) if args else None)

    def _parse(self, node, args):
        specs = signature(node.synopsis)
        positions = [s for s in specs if s.kind == 'positional']
        associative = {s.name: s for s in specs if s.kind in ('keyed', 'flag')}
        generic = next((s for s in specs if s.kind == 'field'), None)
        values = dict(node.defaults)
        errors = []
        positional = []
        for token in args:
            if token.startswith('--'):
                raw = token[2:]
                key, has_equal, value = raw.partition('=')
                negative = False
                if key.startswith('no-') and key[3:] in associative and associative[key[3:]].kind == 'flag':
                    key, negative = key[3:], True
                spec = associative.get(key)
                if spec is None and generic and has_equal and key:
                    values.setdefault('field', {})[key] = value
                    continue
                if spec is None or (spec.kind == 'keyed' and not has_equal) or (spec.kind == 'flag' and has_equal):
                    suggestion = _suggest(key, list(associative), {})
                    problem = f'unknown --{raw} parameter'
                    if suggestion:
                        problem += f"\nDid you mean '--{suggestion}'?"
                    errors.append(problem)
                    continue
                if spec.kind == 'keyed':
                    if not value:
                        errors.append(f'missing --{key} parameter')
                    else:
                        values[key] = value
                else:
                    values[key] = not negative
            elif token.startswith('-'):
                errors.append('unknown ' + token + ' parameter')
            else:
                positional.append(token)
        cursor = 0
        for s in positions:
            if s.repeated:
                if cursor < len(positional):
                    values[s.name] = positional[cursor:]
                    cursor = len(positional)
                elif s.required:
                    return None, 'usage'
                else:
                    values.setdefault(s.name, s.default if s.default is not None else [])
            elif cursor < len(positional):
                values[s.name] = positional[cursor]
                cursor += 1
            elif s.required:
                return None, 'usage'
            else:
                values.setdefault(s.name, s.default)
        if cursor < len(positional):
            return None, 'Error: Too many positional arguments: ' + ' '.join(positional[cursor:])
        for s in specs:
            if s.kind in ('keyed', 'field') and s.required and s.name not in values:
                errors.append('missing --' + s.name + ' parameter')
            if not s.required and s.name not in values:
                values[s.name] = s.default if s.default is not None else (False if s.kind == 'flag' else None)
        if errors:
            return None, 'Error: Parameter errors:\n' + '\n'.join(errors)
        return values, None

    def run(self, argv=None, stdout=None, stderr=None):
        argv = list(sys.argv[1:] if argv is None else argv)
        stdout = sys.stdout if stdout is None else stdout
        stderr = sys.stderr if stderr is None else stderr
        if not argv:
            print(self.help(), file=stdout)
            return 0
        if argv == ['--version']:
            argv = ['cli', 'version']
        elif '--help' in argv:
            idx = argv.index('--help')
            argv = ['help'] + argv[:idx] + argv[idx + 1:]
        # Strip only configured leading global flags; command-specific flags retain their meaning.
        global_config = {}
        while argv and argv[0].startswith('--') and argv[0].split('=', 1)[0][2:] in self.global_flags:
            token = argv.pop(0)[2:]
            key, _, value = token.partition('=')
            global_config[key] = value or True
        node, path, remaining, error = self._resolve(argv)
        if error:
            kind, name, parent = error
            if kind == 'top':
                msg = f"Error: '{name}' is not a registered appctl command. See 'appctl help' for available commands."
                possibilities = list(self.roots)
            else:
                msg = f"Error: '{name}' is not a registered subcommand of '{parent}'. See 'appctl help {parent}' for available subcommands."
                parent_node, _, _, _ = self._resolve(parent.split())
                possibilities = list(parent_node.children)
            suggestion = _suggest(name, possibilities, self.synonyms)
            if suggestion:
                msg += f"\nDid you mean '{suggestion}'?"
            print(msg, file=stderr)
            return 1
        if node is None:
            print(self.help(), file=stdout)
            return 0
        if node.handler is None and node.children and not remaining:
            print(self.help(' '.join(path)), file=stdout)
            return 0
        values, problem = self._parse(node, remaining)
        if problem:
            if problem == 'usage':
                print('usage: ' + self.executable + ' ' + ' '.join(path) + (' ' + node.synopsis if node.synopsis else ''), file=stdout)
            else:
                print(problem, file=stderr)
            return 1
        if node.handler is not None:
            result = node.handler(values)
            if result is not None:
                print(result, file=stdout)
        return 0


def main():
    return CLI().run()


if __name__ == '__main__':
    raise SystemExit(main())
