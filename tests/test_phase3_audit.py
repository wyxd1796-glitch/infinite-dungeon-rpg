import hashlib
import unittest
from tests.audit_phase3 import ROOT, inspect


class Phase3AuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.audit=inspect()

    def test_inventory_exact_and_source_untouched(self):
        a=self.audit
        self.assertEqual(a['total'],1305); self.assertEqual(len(a['groups']),22)
        self.assertEqual(len({r['id'] for r in a['records']}),1305)
        self.assertEqual(sum(r['connected'] for r in a['groups'].values()),793)
        self.assertEqual(a['duplicates'],[]); self.assertEqual(a['loader_errors'],[])
        self.assertEqual(a['source_sha256'],a['expected_sha256'])
        self.assertEqual(hashlib.sha256((ROOT/'content/source/catalogue_v4.json').read_bytes()).hexdigest(),a['source_sha256'])

    def test_missing_implementation_not_classified_as_missing_source(self):
        a=self.audit
        self.assertEqual(a['missing_references'],[])
        self.assertGreater(len(a['inactive_references']),0)
        self.assertTrue(all(r['exists'] and not r['active'] for r in a['inactive_references']))
        self.assertTrue(all(r['connected'] for r in a['effects'][15:40]))
        self.assertEqual([r['id'] for r in a['effects']],[f'EF{i:03}' for i in range(1,41)])
        self.assertTrue(all(r['operator'] for r in a['effects'][15:]))

    def test_events_stages_and_approved_overrides(self):
        a=self.audit
        self.assertEqual(len(a['events']),200)
        for stage,count in ((3,100),(5,50),(7,50)):
            self.assertEqual(sum(r['planned_stage']==stage for r in a['events']),count)
        self.assertEqual(len(a['phase2_overrides']),28)
        self.assertEqual(sum(bool(r['runtime']) for r in a['events']),20)
        event=next(r for r in a['phase2_overrides'] if r['source_id']=='EVT001')
        self.assertEqual(event['runtime']['options'][0]['outcomes'][0]['effects'][0]['type'],'grant_gold')
