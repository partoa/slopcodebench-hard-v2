import json, tempfile,unittest
from pathlib import Path
from legacy_maintenance_sensor import project_snapshot
from feedback_loop import candidates
class FeedbackTests(unittest.TestCase):
 def test_ratio_dilution_triggers_investigation_not_auto_refactor(self):
  with tempfile.TemporaryDirectory() as root:
   p=Path(root);(p/'src').mkdir();(p/'src/a.py').write_text('def f(x):\n    if x:return 1\n    return 0\n')
   d=p/'records';d.mkdir()
   a=project_snapshot(p,['src'],'checkpoint-1',threshold=1)
   (p/'src/b.py').write_text('\n'.join('def f%s():return 1'%i for i in range(12)))
   b=project_snapshot(p,['src'],'checkpoint-2',threshold=1)
   (d/'stage_1_snapshot.json').write_text(json.dumps(a));(d/'stage_2_snapshot.json').write_text(json.dumps(b))
   (d/'trend.json').write_text(json.dumps({'checkpoints':[{'checkpoint':1},{'checkpoint':2}]}))
   result=candidates(d)
   self.assertTrue(any(i['kind']=='METRIC_RATIO_DILUTION' for i in result['issues']))
   self.assertFalse(result['automated_code_or_skill_change'])
