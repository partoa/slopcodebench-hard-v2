import unittest
from tooling.requirements_gate import inspect

BASE = {"id":"R1","source":"released/checkpoint_1.md","criterion":"entrypoint returns specified JSON","boundary":"CLI","implementation":"problems/x/app.py","evidence":"evidence/run.json","status":"VERIFIED_LOCAL"}

class RequirementGateTests(unittest.TestCase):
    def test_complete(self):
        self.assertEqual(inspect({"requirements":[BASE]}), [])
    def test_missing_requirement_list_fails(self):
        self.assertTrue(inspect({"requirements":[]}))
    def test_missing_evidence_fails(self):
        self.assertTrue(inspect({"requirements":[{**BASE,"evidence":""}]}))
    def test_blocked_requirement_fails_engineering_acceptance(self):
        self.assertTrue(inspect({"requirements":[{**BASE,"status":"BLOCKED"}]}))
    def test_duplicate_id_fails(self):
        self.assertTrue(inspect({"requirements":[BASE,BASE]}))
    def test_unsupported_status_fails(self):
        self.assertTrue(inspect({"requirements":[{**BASE,"status":"PASS"}]}))

if __name__ == "__main__":
    unittest.main()
