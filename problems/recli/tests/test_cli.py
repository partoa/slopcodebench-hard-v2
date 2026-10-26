"""Original checkpoint-1 contract tests; no evaluator data used."""
import io
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cli import CLI, signature, SignatureError


def invoke(cli, *args):
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(list(args), out, err)
    return code, out.getvalue(), err.getvalue()


def test_real_entrypoint_help_and_version():
    root = Path(__file__).resolve().parents[1]
    for args in ([], ['--version'], ['help']):
        p = subprocess.run([sys.executable, str(root/'appctl'), *args], capture_output=True, text=True, timeout=5)
        assert p.returncode == 0 and p.stdout and not p.stderr


def test_tree_alias_and_help_order():
    cli = CLI()
    cli.register('Zebra', 'last', '', lambda x: 'z')
    cli.register('alpha', 'first', '', lambda x: 'a', alias='a')
    cli.register('site create', 'Create site', '<name>', lambda x: x['name'], alias='new')
    cli.register('site delete', 'Delete site', '<name>', lambda x: x['name'])
    code, out, err = invoke(cli)
    assert code == 0 and out.index('alpha') < out.index('cli') < out.index('Zebra')
    assert invoke(cli, 'a')[1] == 'a\n'
    assert invoke(cli, 'site', 'new', 'abc')[1] == 'abc\n'
    assert 'site create' in invoke(cli, 'site', '--help')[1]
    assert 'site delete' in invoke(cli, 'site')[1]


def test_arguments_and_rejection():
    cli = CLI()
    observed = []
    cli.register('run', 'run', '<target> [<files>...] --type=<type> [--force] [--[no-]color] [--<field>=<value>]', lambda x: observed.append(x))
    assert invoke(cli, 'run', 'a', 'b', 'c', '--type=fast', '--no-color', '--owner=me')[0] == 0
    assert observed[-1]['files'] == ['b', 'c'] and observed[-1]['color'] is False
    assert observed[-1]['field'] == {'owner': 'me'}
    assert invoke(cli, 'run')[1].startswith('usage: appctl run')
    assert 'Too many positional' not in invoke(cli, 'run', 'a', 'b', '--type=x')[2]
    assert 'Parameter errors:' in invoke(cli, 'run', 'a', '--typo=y')[2]
    assert 'missing --type parameter' in invoke(cli, 'run', 'a')[2]
    strict = CLI()
    strict.register('run', 'run', '<target> --type=<type>', lambda x: None)
    assert 'Did you mean' in invoke(strict, 'run', 'a', '--tyoe=x')[2]


def test_missing_and_extra_positional_and_keyed():
    cli = CLI()
    cli.register('send', 'send', '<recipient> --subject=<subject> [--force]', lambda _: None)
    assert invoke(cli, 'send')[0] == 1
    assert 'Too many positional arguments: b' in invoke(cli, 'send', 'a', 'b', '--subject=x')[2]
    assert 'missing --subject parameter' in invoke(cli, 'send', 'a')[2]
    assert 'missing --subject parameter' in invoke(cli, 'send', 'a', '--subject=')[2]
    assert 'unknown --typo parameter' in invoke(cli, 'send', 'a', '--subject=x', '--typo')[2]


def test_command_errors_and_suggestions():
    cli = CLI(synonyms={'remove': 'delete'})
    cli.register('delete', 'delete', '', lambda _: None, alias='del')
    cli.register('site create', 'create', '', lambda _: None)
    assert "not a registered appctl command" in invoke(cli, 'missing')[2]
    assert "Did you mean 'delete'?" in invoke(cli, 'remove')[2]
    assert invoke(cli, 'del')[0] == 0
    assert "not a registered subcommand of 'site'" in invoke(cli, 'site', 'creat')[2]
    assert "Did you mean 'create'?" in invoke(cli, 'site', 'creat')[2]


def test_defaults_and_signature_safety():
    cli = CLI()
    seen = []
    cli.register('task', 'task', '[<job>] [--timeout=<seconds>]', lambda v: seen.append(v.copy()), defaults={'timeout': '10'})
    assert invoke(cli, 'task')[0] == 0
    assert seen[-1]['timeout'] == '10'
    try:
        signature('random')
    except SignatureError:
        pass
    else:
        raise AssertionError('malformed synopsis accepted')
