"""Development-only synthetic tests. Not evidence that this improves maintainability."""
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest

HERE = Path(__file__).parents[1]
sys.path.insert(0, str(HERE))
import change_impact as ci
import maintenance_sensor as ms


def trial(task_id='T1', family='add-step', criterion='published-contract'):
    return {'record_status': 'OBSERVED_TRIAL',
            'task': {'id': task_id, 'family': family, 'released_requirement': 'Public contract',
                     'external_acceptance_criterion': criterion},
            'conditions': {'source_commit': 'fake-example-commit'},
            'task_observations': {'attempts': 2, 'rework': 1, 'regressions': 0,
                                  'coordinated_semantic_edit_sites': 3, 'elapsed_seconds': 12,
                                  'tool_wait_seconds': 2, 'tokens': None,
                                  'tool_and_investigation_cost': None,
                                  'responsibilities_touched': ['parse', 'execute'],
                                  'evidence': ['own_test_stdout_sha256:123']},
            'verification': {'contract_checks': ['own tests PASS'],
                             'acceptance_status': 'NOT_VERIFIED', 'independent_evidence': []}}


class ChangeImpactTests(unittest.TestCase):
    def snapshots(self, old, new):
        d = tempfile.TemporaryDirectory()
        self.addCleanup(d.cleanup)
        path = Path(d.name) / 'code.py'
        path.write_text(old)
        before = ms.snapshot(d.name, ['code.py'], 'before')
        path.write_text(new)
        after = ms.snapshot(d.name, ['code.py'], 'after')
        return before, after

    def test_proxy_dilution_is_not_maintainability_gain(self):
        src = 'def run(x):\n' + ''.join(f'    if x == {i}:\n        return {i}\n' for i in range(11)) + '    return None\n'
        before, after = self.snapshots(src, src + ''.join(f'\ndef noop_{i}():\n    pass\n' for i in range(20)))
        result = ci.analyze(before, after)
        self.assertTrue(result['structural']['ratio_dilution_candidate'])
        self.assertEqual(result['overall_maintenance_conclusion'], 'UNESTABLISHED')
        self.assertEqual(result['work']['status'], 'NOT_MEASURED')

    def test_actual_work_requires_provenance_and_does_not_claim_cause(self):
        b, a = self.snapshots('def f():\n    pass\n', 'def f():\n    return 3\n')
        result = ci.analyze(b, a, trial())
        self.assertEqual(result['work']['status'], 'OBSERVED_SINGLE_TASK_NOT_CAUSAL')
        self.assertFalse(result['structural']['complexity_is_maintainability'])

    def test_task_family_mismatch_not_comparable(self):
        result = ci.trial_pair(trial(family='a'), trial(family='b'))
        self.assertEqual(result['status'], 'NOT_COMPARABLE')

    def test_matching_tasks_give_descriptive_delta_not_causality(self):
        before, after = trial(), trial(task_id='T2')
        after['task_observations']['rework'] = 0
        result = ci.trial_pair(before, after)
        self.assertEqual(result['deltas']['rework'], -1)
        self.assertFalse(result['causal_improvement_established'])

    def test_invalid_attempts_or_wait_times_rejected(self):
        t = trial()
        t['task_observations']['attempts'] = -1
        with self.assertRaises(ValueError): ci.assess_trial(t)
        t = trial()
        t['task_observations']['tool_wait_seconds'] = 99
        with self.assertRaises(ValueError): ci.assess_trial(t)

    def test_unscanned_file_blocks_comparisons(self):
        b, a = self.snapshots('def f():\n    return 1\n', 'def broken(:\n')
        result = ci.analyze(b, a)
        self.assertEqual(result['structural']['status'], 'INCOMPARABLE_SCOPE_COVERAGE_OR_THRESHOLD')
        self.assertIsNone(result['structural']['deltas']['total_mass_proxy'])

    def test_template_is_not_a_measured_trial(self):
        self.assertEqual(ci.assess_trial({'record_status':'TEMPLATE_NOT_AN_EXECUTED_TRIAL'})['status'],
                         'NOT_MEASURED_TEMPLATE_ONLY')

if __name__ == '__main__': unittest.main()
