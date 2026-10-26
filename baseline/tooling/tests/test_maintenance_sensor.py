"""Behavioral probes for scope honesty and misleading improvement signals."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).parents[1] / 'maintenance_sensor.py'
spec = importlib.util.spec_from_file_location('maintenance_sensor', SCRIPT)
sensor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sensor)


class MaintenanceSensorTests(unittest.TestCase):
    def profile(self, source):
        return {f['qualified_name']: f for f in sensor.inspect_source('fixture.py', source.encode())}

    def test_nested_decisions_and_calls_belong_to_nested_function(self):
        functions = self.profile('def outer():\n    def inner(x):\n        if x:\n            return parse(x)\n        return None\n    return inner\n')
        self.assertEqual(functions['outer']['cc_proxy'], 1)
        self.assertEqual(functions['outer']['call_sites'], [])
        self.assertEqual(functions['outer.inner']['cc_proxy'], 2)
        self.assertEqual(functions['outer']['code_lines'], 2)

    def test_short_circuits_comprehensions_and_mutually_exclusive_calls(self):
        functions = self.profile('def choose(x, a, b):\n    if a and b:\n        return parse(x)\n    return parse(x)\n\ndef collect(xs):\n    return [x for x in xs if x]\n')
        self.assertEqual(functions['choose']['cc_proxy'], 3)
        self.assertEqual(functions['collect']['cc_proxy'], 3)
        repeated = functions['choose']['repeated_call_syntax'][0]
        self.assertEqual(len(repeated['sites']), 2)
        self.assertEqual(repeated['status'], 'REQUIRES_VALUE_EFFECT_AND_EXECUTION_EVIDENCE')

    def test_parse_failure_cannot_appear_as_clean_improvement(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'source.py'
            path.write_text('def good():\n    return 1\n')
            before = sensor.snapshot(folder, ['source.py'], 'before')
            path.write_text('def broken(:\n')
            after = sensor.snapshot(folder, ['source.py'], 'after')
            result = sensor.compare(before, after)
            self.assertFalse(result['coverage_complete'])
            self.assertEqual(after['scope']['files'][0]['error_type'], 'SyntaxError')
            self.assertIsNone(after['summary']['high_mass_fraction_proxy'])

    def test_ratio_dilution_keeps_absolute_complexity_and_no_ease_verdict(self):
        source = 'def policy(x):\n' + ''.join(f'    if x == {i}:\n        return {i}\n' for i in range(11)) + '    return -1\n'
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'source.py'
            path.write_text(source)
            before = sensor.snapshot(folder, ['source.py'], 'before')
            path.write_text(source + ''.join(f'\ndef helper_{i}():\n    return {i}\n' for i in range(20)))
            after = sensor.snapshot(folder, ['source.py'], 'after')
            self.assertLess(after['summary']['high_mass_fraction_proxy'], before['summary']['high_mass_fraction_proxy'])
            self.assertEqual(after['summary']['high_mass_proxy'], before['summary']['high_mass_proxy'])
            result = sensor.compare(before, after)
            self.assertEqual(result['maintenance_difficulty'], 'NOT_MEASURED')
            self.assertEqual(next(f for f in result['functions'] if f['id'] == 'source.py:policy')['status'], 'UNCHANGED')

    def test_classes_and_async_names_are_not_collapsed(self):
        functions = self.profile('class A:\n    async def run(self):\n        return 1\nclass B:\n    def run(self):\n        return 2\n')
        self.assertEqual(set(functions), {'A.run', 'B.run'})


if __name__ == '__main__':
    unittest.main()
