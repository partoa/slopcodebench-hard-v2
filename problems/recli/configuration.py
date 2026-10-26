"""Configuration and alias resolution for the appctl command dispatcher."""
from __future__ import annotations

import json
import os
from pathlib import Path
import re
import subprocess

import yaml

GLOBAL_DEFAULTS = {
    'disabled_commands': [], 'projects_path': None, 'locale': 'en_US',
    'cert-email': None, 'env': None, 'admin-email': None,
    'sysctl': None, 'skip-tty': False, 'custom-compose': None,
    'installer_version': 'stable', 'color': 'auto',
    'debug': False, 'quiet': False,
}
RUNTIME_PARAMS = {'color', 'debug', 'quiet'}
ALIAS_PATTERN = re.compile(r'^@[A-Za-z0-9_.\\-]+$')


def root_directory(environ=None):
    env = os.environ if environ is None else environ
    return Path(env.get('APPCTL_ROOT_DIR', str(Path.home() / '.appctl')))


def global_config_path(environ=None):
    env = os.environ if environ is None else environ
    return Path(env['APPCTL_CONFIG_PATH']) if env.get('APPCTL_CONFIG_PATH') else root_directory(env) / 'config' / 'config.yml'


def packages_directory(environ=None):
    env = os.environ if environ is None else environ
    return Path(env['APPCTL_PACKAGES_DIR']) if env.get('APPCTL_PACKAGES_DIR') else root_directory(env) / 'packages'


def project_config_path(cwd=None):
    directory = Path(cwd or os.getcwd()).resolve()
    for base in (directory, *directory.parents):
        for name in ('appctl.local.yml', 'appctl.yml'):
            path = base / name
            if path.is_file():
                return path
    return None


def merge_config(base, derived, append_arrays=False):
    result = dict(base)
    for key, value in derived.items():
        if key == '_':
            continue
        if append_arrays and isinstance(result.get(key), list) and isinstance(value, list):
            result[key] = list(result[key]) + value
        elif append_arrays and isinstance(result.get(key), dict) and isinstance(value, dict):
            result[key] = merge_config(result[key], value, True)
        else:
            result[key] = value
    return result


def read_yaml(path, seen=None):
    path = Path(path).expanduser().resolve()
    seen = set() if seen is None else seen
    if path in seen:
        raise ValueError('Configuration inheritance cycle: ' + str(path))
    seen.add(path)
    try:
        with path.open(encoding='utf-8') as handle:
            data = yaml.safe_load(handle) or {}
        if not isinstance(data, dict):
            raise ValueError('Configuration must be a mapping: ' + str(path))
        meta = data.get('_') or {}
        if not isinstance(meta, dict):
            raise ValueError('Invalid configuration metadata: ' + str(path))
        inherited = {}
        if meta.get('inherit'):
            inherited = read_yaml(path.parent / str(meta['inherit']), seen)
        # A local alias path belongs to the definition file, not the caller's CWD.
        for key, value in list(data.items()):
            if key.startswith('@') and isinstance(value, dict) and 'path' in value and 'ssh' not in value:
                copy = dict(value)
                copy['path'] = str((path.parent / str(copy['path'])).resolve())
                data[key] = copy
        return merge_config(inherited, data, bool(meta.get('merge')))
    finally:
        seen.remove(path)


def load_configuration(cwd=None, environ=None):
    env = dict(os.environ if environ is None else environ)
    global_path = global_config_path(env)
    if global_path.exists():
        global_data = read_yaml(global_path)
    else:
        global_data = {}
    missing = [k for k in ('locale', 'installer_version') if k not in global_data]
    if missing:
        global_path.parent.mkdir(parents=True, exist_ok=True)
        global_data.update({k: GLOBAL_DEFAULTS[k] for k in missing})
        with global_path.open('w', encoding='utf-8') as out:
            yaml.safe_dump(global_data, out, sort_keys=False)
    project_path = project_config_path(cwd)
    project_data = read_yaml(project_path) if project_path else {}
    data = merge_config(global_data, project_data)
    aliases = {k: v for k, v in data.items() if isinstance(k, str) and k.startswith('@') and ALIAS_PATTERN.fullmatch(k)}
    runtime = env.get('APPCTL_RUNTIME_ALIAS')
    if runtime:
        additions = json.loads(runtime)
        if not isinstance(additions, dict):
            raise ValueError('APPCTL_RUNTIME_ALIAS must be a JSON object')
        for key, value in additions.items():
            if not ALIAS_PATTERN.fullmatch(key):
                raise ValueError('Invalid alias name: ' + key)
            aliases[key] = value
    params = {key: data.get(key, default) for key, default in GLOBAL_DEFAULTS.items()}
    return params, aliases


def levenshtein(a, b):
    a, b = a.casefold(), b.casefold()
    previous = list(range(len(b) + 1))
    for i, char in enumerate(a, 1):
        current = [i]
        for j, other in enumerate(b, 1):
            current.append(min(current[-1] + 1, previous[j] + 1, previous[j-1] + (char != other)))
        previous = current
    return previous[-1]


def expand_alias(name, aliases):
    def unknown(alias):
        choices = sorted((v for v in aliases if levenshtein(alias, v) <= 2),
                         key=lambda v: (levenshtein(alias, v), v.casefold(), v))
        message = f"Error: Alias '{alias}' not found."
        if choices:
            message += f"\nDid you mean '{choices[0]}'?"
        raise ValueError(message)

    if name == '@all' and name not in aliases:
        if not aliases:
            raise ValueError("Error: Cannot use '@all' when no aliases are registered.")
        requested = sorted(aliases, key=lambda v: (v.casefold(), v))
    else:
        if name not in aliases:
            unknown(name)
        requested = [name]

    ordered = []
    seen = set()

    def visit(alias, stack):
        if alias in stack:
            raise ValueError('Error: Alias group cycle: ' + ' -> '.join(stack + [alias]))
        members = aliases[alias]
        if not isinstance(members, list):
            if alias not in seen:
                seen.add(alias)
                ordered.append(alias)
            return
        invalid = [str(member) for member in members
                   if not isinstance(member, str) or member not in aliases]
        if invalid:
            raise ValueError(f"Error: Group '{alias}' contains one or more invalid aliases: {', '.join(invalid)}.")
        for member in members:
            visit(member, stack + [alias])

    for alias in requested:
        if name == '@all':
            seen.clear()
        visit(alias, [])
    return ordered


def execute_remote(alias, args, environ=None):
    env = os.environ if environ is None else environ
    ssh = alias['ssh']
    if isinstance(ssh, str) and ssh.startswith('ssh://'):
        ssh = ssh[6:]
    pre = env.get('APPCTL_SSH_PRE_CMD')
    import shlex
    command = ' '.join(shlex.quote(arg) for arg in args)
    if pre:
        command = pre + ' && ' + command
    return subprocess.run(['ssh', ssh, command], capture_output=True, text=True)
