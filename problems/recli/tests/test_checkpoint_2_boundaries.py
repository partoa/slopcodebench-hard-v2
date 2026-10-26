"""Additional contract tests: failures, propagation, and boundary behavior."""
import io
import os
import sys
from pathlib import Path
from unittest.mock import patch, Mock
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cli import CLI
from configuration import read_yaml, load_configuration, expand_alias, execute_remote


def run(cli, argv):
    out, err = io.StringIO(), io.StringIO()
    rc = cli.run(argv, out, err)
    return rc, out.getvalue(), err.getvalue()


def test_global_runtime_precedence_and_strict_mode(tmp_path, monkeypatch):
    cfg = tmp_path / 'config.yml'
    cfg.write_text('locale: de_DE\ninstaller_version: stable\ncolor: never\n')
    monkeypatch.setenv('APPCTL_CONFIG_PATH', str(cfg))
    monkeypatch.setenv('APPCTL_ROOT_DIR', str(tmp_path))
    monkeypatch.setenv('APPCTL_STRICT_ARGS_MODE', '1')
    cli = CLI()
    cli.register('run', synopsis='[--color]', handler=lambda args: str(args.get('color')))
    assert run(cli, ['run', '--color']) == (0, 'True\n', '')
    assert run(cli, ['--color=always', 'run'])[0] == 0
    assert cli.configuration['color'] == 'always'
    assert run(cli, ['run', '--color'])[0] == 0
    assert cli.configuration['color'] == 'never'


def test_global_file_only_not_runtime(tmp_path, monkeypatch):
    cfg = tmp_path / 'config.yml'
    cfg.write_text('locale: en_US\ninstaller_version: stable\n')
    monkeypatch.setenv('APPCTL_CONFIG_PATH', str(cfg))
    cli = CLI()
    cli.register('run', handler=lambda x:'ran')
    code, out, err = run(cli, ['run', '--locale=xx'])
    assert code == 1 and 'unknown --locale' in err
    assert cli.configuration['locale'] == 'en_US'


def test_remote_exit_255_and_precmd(tmp_path, monkeypatch):
    cfg = tmp_path / 'config.yml'
    cfg.write_text('locale: en_US\ninstaller_version: stable\n"@host":\n  ssh: ssh://user@example\n')
    monkeypatch.setenv('APPCTL_CONFIG_PATH', str(cfg))
    monkeypatch.setenv('APPCTL_SSH_PRE_CMD', 'echo prep')
    cli = CLI()
    cli.register('run', handler=lambda x:'local')
    completed = Mock(returncode=255, stdout='', stderr='connection refused')
    with patch('configuration.subprocess.run', return_value=completed) as proc:
        code, out, err = run(cli, ['@host','run'])
    assert code == 255
    assert 'Cannot connect over SSH using provided configuration' in err
    command = proc.call_args.args[0]
    assert command[:2] == ['ssh', 'user@example']
    assert command[2].startswith('echo prep && ')
    assert 'run' in command[2]


def test_broadcast_never_invokes_group_as_connection(tmp_path, monkeypatch):
    cfg = tmp_path / 'config.yml'
    cfg.write_text('locale: en_US\ninstaller_version: stable\n"@a": {path: .}\n"@group": ["@a"]\n')
    monkeypatch.setenv('APPCTL_CONFIG_PATH', str(cfg))
    cli = CLI()
    observed = []
    cli.register('run', handler=lambda x: observed.append(cli.active_alias))
    code, _, err = run(cli, ['@all','run'])
    assert code == 0 and observed == [{'path': str(tmp_path)}, {'path': str(tmp_path)}]


def test_unwritable_config_failure(tmp_path, monkeypatch):
    cfg = tmp_path / 'blocked'
    cfg.mkdir()
    monkeypatch.setenv('APPCTL_CONFIG_PATH', str(cfg))
    code, out, err = run(CLI(), ['cli','version'])
    assert code == 1 and 'Error:' in err


def test_invalid_alias_and_duplicate_group(tmp_path, monkeypatch):
    cfg=tmp_path/'config.yml'
    cfg.write_text('locale: en_US\ninstaller_version: stable\n"@first": {path: .}\n"@group": ["@first", "@first", "@missing"]\n')
    monkeypatch.setenv('APPCTL_CONFIG_PATH',str(cfg))
    code, out, err=run(CLI(), ['@group','help'])
    assert code==1 and "invalid aliases: @missing" in err

def test_no_args_populates_global_config(tmp_path, monkeypatch):
    cfg = tmp_path / 'new.yml'
    monkeypatch.setenv('APPCTL_CONFIG_PATH', str(cfg))
    code, out, err = run(CLI(), [])
    assert code == 0 and 'Commands:' in out and cfg.exists()


def test_explicit_no_color_runtime(tmp_path, monkeypatch):
    cfg = tmp_path / 'cfg.yml'
    cfg.write_text('locale: en_US\ninstaller_version: stable\ncolor: always\n')
    monkeypatch.setenv('APPCTL_CONFIG_PATH', str(cfg))
    cli = CLI()
    cli.register('ping', handler=lambda _: None)
    assert run(cli, ['--no-color', 'ping'])[0] == 0
    assert cli.configuration['color'] is False


def test_alias_cycle_rejected():
    with pytest.raises(ValueError, match='cycle'):
        expand_alias('@a', {'@a': ['@b'], '@b': ['@a']})

def test_deprecated_global_warns_but_remains_usable(tmp_path, monkeypatch):
    cfg = tmp_path / 'c.yml'
    cfg.write_text('locale: en_US\ninstaller_version: stable\n')
    monkeypatch.setenv('APPCTL_CONFIG_PATH', str(cfg))
    cli = CLI(global_flags={'legacy'})
    cli.deprecated_globals.add('legacy')
    cli.register('ping', handler=lambda _: 'ok')
    rc, out, err = run(cli, ['--legacy=on', 'ping'])
    assert rc == 0 and out == 'ok\n'
    assert 'Warning: The --legacy global parameter is deprecated.' in err
    assert cli.configuration['legacy'] == 'on'


def test_runtime_alias_has_priority_over_file_alias(tmp_path, monkeypatch):
    cfg = tmp_path / 'c.yml'
    cfg.write_text('locale: en_US\ninstaller_version: stable\n"@remote": {path: ./old}\n')
    monkeypatch.setenv('APPCTL_CONFIG_PATH', str(cfg))
    monkeypatch.setenv('APPCTL_RUNTIME_ALIAS', json.dumps({'@remote': {'path': '/new'}}))
    cli = CLI()
    seen = []
    cli.register('ping', handler=lambda _: seen.append(cli.active_alias))
    rc, out, err = run(cli, ['@remote', 'ping'])
    assert rc == 0 and seen == [{'path': '/new'}]
