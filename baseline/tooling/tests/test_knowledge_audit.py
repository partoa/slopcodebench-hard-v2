import importlib.util, json, sys, tempfile, unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('knowledge_audit',Path(__file__).resolve().parents[1]/'knowledge_audit.py')
k=importlib.util.module_from_spec(spec);sys.modules['knowledge_audit']=k;spec.loader.exec_module(k)
def q(id,scope,imp=2,estimate=2,anchored=False):
 return {'id':id,'kind':'question','status':'OPEN','statement':'Question '+id,
  'source':{'kind':'own','locator':'source'},'scope_refs':[scope] if scope else [],
  'scope_unknown_reason':'unknown' if not scope else '',
  'anchors':[{'path':'foo.py'}] if anchored else [],
  'retention':{'reason':'Useful to an engineering decision','value_if_retained':'Less risk',
               'maintenance_estimate_minutes':estimate,'review_trigger':'When related spec changes','why_not_existing':'Unique scope'},
  'priority':{'impact':imp,'uncertainty':3,'urgency':2},'last_review_stage':1}
class KnowledgeTests(unittest.TestCase):
 def test_no_fake_unknown_quota(self):
  self.assertTrue(k.audit({'records':[],'links':[]})['valid'])
 def test_entry_justification_required(self):
  x=q('Q-a','component:a');x.pop('retention')
  self.assertFalse(k.audit({'records':[x],'links':[]})['valid'])
 def test_duplicate_rejected(self):
  a=q('Q-a','component:a');b=q('Q-b','component:a');b['statement']=a['statement']
  self.assertFalse(k.audit({'records':[a,b],'links':[]})['valid'])
 def test_scoped_review_and_top_five(self):
  items=[q('Q-'+str(i),'folder:a' if i==9 else 'component:'+str(i),imp=0 if i==9 else 5) for i in range(10)]
  x=k.plan({'records':items,'links':[]},2,['file:a/demo.py'],30)
  self.assertEqual(x['selected'][0]['id'],'Q-9')
  self.assertTrue(x['selected'][0]['selection_reason']=='RELEVANT_UNBOUND')
  self.assertTrue(all(y['top_five'] for y in x['selected'][1:]))
  self.assertEqual(len(x['selected']),6)
 def test_budget_does_not_suppress_top_five(self):
  items=[q('Q-'+str(i),'domain:'+str(i),estimate=20) for i in range(7)]
  x=k.plan({'records':items,'links':[]},1,['domain:unrelated'],1)
  self.assertEqual(len(x['selected']),5)
  self.assertTrue(x['budget_exceeded'])
 def test_review_hash_invalidated_by_changed_question(self):
  items=[q('Q-one','domain:x')];led={'records':items,'links':[]}
  p=k.plan(led,1,['domain:x'],20)
  with tempfile.TemporaryDirectory() as tmp:
   file=Path(tmp)/'Q-one.json'
   file.write_text(json.dumps({'question_id':'Q-one','question_sha256':p['selected'][0]['question_sha256'],'independent_reasoning':'This review weighs the particular obligation and evidence.','evidence_examined':[]}))
   self.assertTrue(k.check_reviews(p,Path(tmp))['valid'])
   led['records'][0]['statement']='changed'
   p2=k.plan(led,1,['domain:x'],20)
   self.assertFalse(k.check_reviews(p2,Path(tmp))['valid'])
 def test_orphan_review_after_deletion(self):
  with tempfile.TemporaryDirectory() as tmp:
   (Path(tmp)/'Q-old.json').write_text('{}')
   self.assertFalse(k.check_reviews({'selected':[]},Path(tmp))['valid'])
if __name__=='__main__':unittest.main()
