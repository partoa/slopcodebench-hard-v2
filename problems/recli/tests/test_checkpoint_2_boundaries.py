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
