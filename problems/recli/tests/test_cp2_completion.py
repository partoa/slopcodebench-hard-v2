"""Completion gates derived from released checkpoint 2; never benchmark evaluator tests."""
import io
import sys
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from configuration import load_configuration
from cli import CLI

def test_invalid_file_alias_is_rejected(tmp_path):
    cfg = tmp_path / 'config.yml'
    cfg.write_text('"@oops!": {path: .}\n')
    with pytest.raises(ValueError, match='Invalid alias name'):
        load_configuration(cwd=tmp_path, environ={'APPCTL_CONFIG_PATH': str(cfg)})

def test_metadata_hidden_and_deprecated(tmp_path, monkeypatch):
    cfg = tmp_path / 'config.yml'
    cfg.write_text('locale: en_US\ninstaller_version: stable\n')
    monkeypatch.setenv('APPCTL_CONFIG_PATH', str(cfg))
    cli = CLI()
    cli.register_global_parameter('old', deprecated=True)
    cli.register_global_parameter('secret', hidden=True)
    cli.register('run', handler=lambda _: 'ok')
    output, errors = io.StringIO(), io.StringIO()
    assert cli.run(['--old=x', '--secret=y', 'run'], output, errors) == 0
    assert cli.configuration['old'] == 'x' and cli.configuration['secret'] == 'y'
    assert 'deprecated' in errors.getvalue()
    assert 'secret' not in cli.help()

def test_multi_global_flags_and_strict_command_scope(tmp_path, monkeypatch):
    cfg = tmp_path / 'config.yml'
    cfg.write_text('locale: en_US\ninstaller_version: stable\n')
    monkeypatch.setenv('APPCTL_CONFIG_PATH', str(cfg))
    monkeypatch.setenv('APPCTL_STRICT_ARGS_MODE', '1')
    cli = CLI()
    cli.register('run', synopsis='[--color]', handler=lambda v: str(v['color']))
    out, err = io.StringIO(), io.StringIO()
    assert cli.run(['--no-color', 'run', '--color'], out, err) == 0
    assert cli.configuration['color'] is False
    assert out.getvalue() == 'True\n'
