"""Formatting of command results according to checkpoint 3."""
import csv
import io
import json
import yaml


class FormatError(ValueError):
    pass


def _text(value):
    return json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else '' if value is None else str(value)


def render(data, fmt='table', field=None, fields=None, prefix=''):
    rows = data if isinstance(data, list) else ([] if data is None else [data])
    rows = [v if isinstance(v, dict) else {'value': v} for v in rows]
    keys = list(rows[0]) if rows else []

    def lookup(name):
        target = (prefix + name).casefold()
        key = next((k for k in keys if k.casefold() == target), None)
        if key is None:
            raise FormatError('Error: Invalid field: ' + name + '.')
        return key

    if field is not None:
        key = lookup(field)
        return '\n'.join(_text(row.get(key)) for row in rows)
    if fields is not None:
        keys = [lookup(name.strip()) for name in (fields.split(',') if isinstance(fields, str) else fields)]
    selected = [{key: row.get(key) for key in keys} for row in rows]
    if fmt == 'count':
        return str(len(rows))
    if fmt == 'ids':
        key = lookup('id')
        return ' '.join(_text(row.get(key)) for row in rows)
    if fmt == 'json':
        return json.dumps(selected, indent=4, ensure_ascii=False)
    if fmt == 'yaml':
        return yaml.safe_dump(selected, default_flow_style=False, sort_keys=False, allow_unicode=True).rstrip('\n')
    if fmt == 'csv':
        output = io.StringIO(newline='')
        writer = csv.writer(output, lineterminator='\n')
        writer.writerow(keys)
        writer.writerows([_text(row[key]) for key in keys] for row in selected)
        return output.getvalue().rstrip('\n')
    if fmt != 'table':
        raise FormatError('Error: Invalid format: ' + str(fmt) + '.')
    if not rows:
        return ''
    if len(rows) == 1:
        return '\n'.join(str(key) + ': ' + _text(selected[0][key]) for key in keys)
    widths = {key: max(len(str(key)), *(len(_text(row[key])) for row in selected)) for key in keys}
    return '\n'.join(['  '.join(str(k).ljust(widths[k]) for k in keys)] +
                     ['  '.join(_text(row[k]).ljust(widths[k]) for k in keys) for row in selected])
