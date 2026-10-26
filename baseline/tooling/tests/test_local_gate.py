import sys,tempfile,unittest
from pathlib import Path
from local_gate import run
class GateTests(unittest.TestCase):
 def test_raw_failure_preserved(self):
  with tempfile.TemporaryDirectory() as root:
   p=Path(root);(p/'a.py').write_text('pass\n')
   z=run(p,p/'results',[sys.executable,'-c','import sys;print("reason",file=sys.stderr);sys.exit(3)'],sources=['a.py'])
   self.assertEqual(z['status'],'FAIL_EXIT_NONZERO')
   self.assertEqual(z['exit_code'],3)
   self.assertIn(b'reason',(p/'results/stderr.bin').read_bytes())
 def test_timeout_is_incomplete(self):
  with tempfile.TemporaryDirectory() as root:
   p=Path(root);(p/'a.py').write_text('pass\n')
   result=run(p,p/'results',[sys.executable,'-c','import time;time.sleep(2)'],timeout=.15,sources=['a.py'])
   self.assertEqual(result['status'],'TIMEOUT_INCOMPLETE')
   self.assertIsNone(result['exit_code'])
