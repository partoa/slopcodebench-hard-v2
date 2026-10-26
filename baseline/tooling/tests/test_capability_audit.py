import importlib.util
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

name = Path(__file__).resolve().parents[1] / 'capability_audit.py'
spec = importlib.util.spec_from_file_location('capability_audit', name)
a = importlib.util.module_from_spec(spec)
sys.modules['capability_audit'] = a
spec.loader.exec_module(a)

class CapabilityTests(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.TemporaryDirectory()
        self.root = Path(self.t.name)
    def tearDown(self):self.t.cleanup()
    def write(self,name,text):
        p=self.root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text);return p
    def test_syntax_coverage_includes_failure(self):
        self.write('good.py','def go():\n return 1\n')
        self.write('bad.py','def f(: pass')
        d=a.scan(self.root)
        self.assertEqual(d['status'],'PARTIAL')
        self.assertEqual(d['coverage']['failed'],1)
        self.assertEqual(d['parse_failures'][0]['path'],'bad.py')
    def test_nested_not_inherited_and_module_work(self):
        self.write('scope.py','count=1\ndef outer():\n def inner():\n  global count\n  count=3\n return 0\n')
        s=a.scan(self.root)['files'][0]['scopes']
        out=next(x for x in s if x['name']=='outer')
        ins=next(x for x in s if x['name']=='outer.inner')
        self.assertFalse(any(x['name']=='count' for x in out['writes']))
        self.assertTrue(any(x['name']=='count' for x in ins['writes']))
        self.assertTrue(any(x['name']=='count' for x in s[0]['writes']))
    def test_call_sites_not_deduplicated(self):
        self.write('calls.py','def f(x):\n int(x)\n int(x)\n')
        f=a.scan(self.root)['files'][0]['scopes'][1]
        self.assertEqual(len(f['call_sites']),2)
        self.assertEqual(f['repeated_callee_syntax'],{'int':2})
        self.assertTrue(all(x['binding_status']=='UNRESOLVED' for x in f['call_sites']))
    def test_manifest_checks_all_artifacts(self):
        self.write('spec.md','spec')
        self.write('evidence.txt','bad')
        p=self.write('manifest.json',json.dumps({'artifacts':[{'path':'spec.md','sha256':a.digest(b'spec')},{'path':'evidence.txt','sha256':a.digest(b'good')}]}))
        r=a.verify_evidence(self.root,p)
        self.assertFalse(r['valid'])
        self.assertEqual([x['ok'] for x in r['checked']],[True,False])
    def test_manifest_rejects_escape(self):
        m=self.write('manifest.json',json.dumps({'artifacts':[{'path':'../secret','sha256':'0'*64}]}))
        self.assertFalse(a.verify_evidence(self.root,m)['valid'])
    def test_capture_failure_exit(self):
        r=a.capture(self.root,[sys.executable,'-c','import sys; sys.exit(3)'],timeout=2,max_bytes=100)
        self.assertEqual(r['status'],'FAIL')
        self.assertEqual(r['exit_code'],3)
    def test_capture_timeout(self):
        r=a.capture(self.root,[sys.executable,'-c','import time; time.sleep(5)'],timeout=0.15,max_bytes=100)
        self.assertEqual(r['status'],'TIMEOUT')
    def test_capture_retention_limit(self):
        r=a.capture(self.root,[sys.executable,'-c',"print('a'*1000)"],timeout=3,max_bytes=25)
        self.assertEqual(r['status'],'INCOMPLETE_OUTPUT')
        self.assertEqual(r['streams']['stdout']['bytes_retained'],25)
    def test_skill_discovery_ordinary_heading(self):
        self.write('skills/a/SKILL.md','---\nname: filter-hazards\ndescription: Detect incorrect filters.\n---\n# Methods\nDo work.')
        self.write('skills/b/SKILL.md','# Everyday skill\nFocus on scope.')
        r=a.skill_index(self.root)
        self.assertEqual(r['count'],2)
        self.assertEqual(r['skills'][0]['name'],'filter-hazards')
        self.assertIn('Everyday skill',[s['description'] for s in r['skills']])
if __name__=='__main__':unittest.main()
