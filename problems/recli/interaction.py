"""User-facing messages, interaction and append-only logging."""
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

COLORS = {'Error:': 31, 'Warning:': 33, 'Success:': 32, 'Debug:': 36}


def enabled_color(mode='auto', stream=None, platform=None):
    if mode is True or str(mode).lower() in ('on', 'yes', 'true', 'always'):
        return True
    if mode is False or str(mode).lower() in ('off', 'no', 'false', 'never'):
        return False
    stream = sys.stdout if stream is None else stream
    return (os.name if platform is None else platform) != 'nt' and bool(getattr(stream, 'isatty', lambda: False)())


def tint(message, enabled):
    if enabled:
        for label, color in COLORS.items():
            if message.startswith(label):
                return f'\x1b[{color}m{label}\x1b[0m' + message[len(label):]
    return message


def log_file(environ=None):
    env = os.environ if environ is None else environ
    return Path(env.get('APPCTL_ROOT_DIR', str(Path.home() / '.appctl'))) / 'logs/appctl.log'


def log_line(message, environ=None):
    path = log_file(environ)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a', encoding='utf-8') as f:
        f.write(message.rstrip('\n') + '\n')


def log_invocation(argument_count, environ=None):
    stamp = datetime.now(timezone.utc).isoformat(timespec='microseconds').replace('+00:00', 'Z')
    log_line('--- invocation ---\n' + stamp + ' argc=' + str(argument_count), environ)


class Reporter:
    def __init__(self, stdout=None, stderr=None, quiet=False, debug=False, color='auto', environ=None, logging=True):
        self.stdout = sys.stdout if stdout is None else stdout
        self.stderr = sys.stderr if stderr is None else stderr
        self.quiet, self.debug_mode, self.color = quiet, debug, color
        self.environ, self.logging = environ, logging
        self.started = time.monotonic()

    def _write(self, category, message, stream, persist=True, sensitive=False):
        line = f'{category}: {message}' if category else str(message)
        print(tint(line, enabled_color(self.color, stream)), file=stream)
        if persist and not sensitive and self.logging:
            log_line(line, self.environ)

    def error(self, message, code=1, sensitive=False):
        if '\n' in str(message):
            lines = str(message).splitlines()
            width = max(map(len, lines))
            message = '+' + '-' * (width + 2) + '+\n' + '\n'.join('| ' + line.ljust(width) + ' |' for line in lines) + '\n+' + '-' * (width + 2) + '+'
        self._write('Error', message, self.stderr, sensitive=sensitive)
        return code

    def warning(self, message):
        self._write('Warning', message, self.stderr)

    def success(self, message):
        if not self.quiet:
            self._write('Success', message, self.stdout, persist=False)

    def info(self, message, sensitive=False):
        if not self.quiet:
            self._write('', message, self.stdout, sensitive=sensitive)

    def debug(self, message, group=None):
        if not self.debug_mode:
            return
        if isinstance(self.debug_mode, str) and self.debug_mode not in ('true', 'True', '1') and self.debug_mode != group:
            return
        suffix = (' [' + group + ']') if group else ''
        self._write('Debug', f'{time.monotonic() - self.started:.3f}s{suffix} {message}', self.stderr)


def ask(question, stdin=None, stdout=None):
    stdin = sys.stdin if stdin is None else stdin
    stdout = sys.stdout if stdout is None else stdout
    print(question, end='', flush=True, file=stdout)
    return stdin.readline().strip().lower()


def confirm(question, yes=False, stdin=None, stdout=None, reporter=None):
    if yes:
        return True
    if ask(question + ' [y/n] ', stdin, stdout) == 'y':
        return True
    (reporter or Reporter(stdout=stdout)).warning('Operation cancelled.')
    return False


def input_value(stdin=None, json_mode=False):
    stdin = sys.stdin if stdin is None else stdin
    raw = stdin.readline()
    if not raw:
        return None
    if json_mode:
        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError('Error: Invalid JSON: ' + raw.rstrip('\n')) from exc
    return raw.rstrip('\n')
