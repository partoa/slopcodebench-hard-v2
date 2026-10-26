"""Original tests derived solely from the released checkpoint-2 specification."""
import io
import json
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cli import CLI
from configuration import (read_yaml, load_configuration, packages_directory,
                           expand_alias, project_config_path)


def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')


def test_config_precedence_and_nearest_project(tmp_path):
    root = tmp_path / 'root'
    project = tmp_path / 'project'
    nested = project / 'nested'
    nested.mkdir(parents=True)
    write(root / 'config/config.yml', 'locale: global\ninstaller_version: base\ncolor: green\n')
    write(project / 'appctl.yml', 'locale: project\ncolor: red\n')
    write(project / 'appctl.local.yml', 'locale: local\n')
    params, _ = load_configuration(cwd=nested, environ={'APPCTL_ROOT_DIR': str(root)})
    assert params['locale'] == 'local'
    assert params['color'] == 'green'
    assert project_config_path(nested).name == 'appctl.local.yml'


def test_inheritance_merge_and_cycle(tmp_path):
    write(tmp_path / 'base.yml', 'items: [a]\ncolor: blue\n')
    write(tmp_path / 'child.yml', '_:\n  inherit: base.yml\n  merge: true\nitems: [b, a]\ncolor: red\n')
    data = read_yaml(tmp_path / 'child.yml')
    assert data['items'] == ['a', 'b', 'a']
    assert data['color'] == 'red'
    write(tmp_path / 'base.yml', '_:\n  inherit: child.yml\n')
    with pytest.raises(ValueError, match='cycle'):
        read_yaml(tmp_path / 'child.yml')


def test_global_autocreate_and_packages(tmp_path):
    params, aliases = load_configuration(cwd=tmp_path, environ={'APPCTL_ROOT_DIR': str(tmp_path / 'home')})
    text = (tmp_path / 'home/config/config.yml').read_text()
    assert 'locale: en_US' in text and 'installer_version: stable' in text
    assert params['locale'] == 'en_US' and aliases == {}
    assert packages_directory({'APPCTL_ROOT_DIR': str(tmp_path)}) == tmp_path / 'packages'


def test_alias_validation_group_and_broadcast():
    aliases = {'@z': {'path': '/tmp/z'}, '@A': {'path': '/tmp/a'}, '@grp': ['@z', '@A', '@z']}
    assert expand_alias('@all', {'@z': {}, '@A': {}}) == ['@A', '@z']
    assert expand_alias('@grp', aliases) == ['@z', '@A']
    with pytest.raises(ValueError, match='invalid aliases'):
        expand_alias('@bad', {'@bad': ['@missing']})
    with pytest.raises(ValueError, match='no aliases'):
        expand_alias('@all', {})
    with pytest.raises(ValueError, match='Did you mean'):
        expand_alias('@Zx', aliases)


def test_runtime_alias_overrides_and_local_paths(tmp_path):
    write(tmp_path/'config.yml', '"@one":\n  path: relative\n')
    assert read_yaml(tmp_path/'config.yml')['@one']['path'] == str((tmp_path/'relative').resolve())
    params, aliases = load_configuration(cwd=tmp_path, environ={
        'APPCTL_CONFIG_PATH': str(tmp_path/'config.yml'),
        'APPCTL_RUNTIME_ALIAS': json.dumps({'@one': {'ssh': 'ssh://example'}})})
    assert aliases['@one']['ssh'] == 'ssh://example'


def test_dispatch_disabled_and_strict_mode(tmp_path, monkeypatch):
    global_path = tmp_path/'config.yml'
    write(global_path, 'disabled_commands: [blocked]\nlocale: en_US\ninstaller_version: stable\n')
    monkeypatch.setenv('APPCTL_CONFIG_PATH', str(global_path))
    monkeypatch.setenv('APPCTL_STRICT_ARGS_MODE', '1')
    cli = CLI()
    cli.register('blocked', handler=lambda _: 'should not run')
    cli.register('run', synopsis='[--color]', handler=lambda values: str(values['color']))
    out, err = io.StringIO(), io.StringIO()
    assert cli.run(['blocked'], out, err) == 1
    assert "has been disabled" in err.getvalue()
    out, err = io.StringIO(), io.StringIO()
    assert cli.run(['run', '--color'], out, err) == 0
    assert out.getvalue().strip() == 'True'
