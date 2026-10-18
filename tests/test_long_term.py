import unittest
from tests.simulate_phase2 import progression
from tests.simulate_long_term import EconomyAudit, FundedPreparation, ROOT


class LongTermAuditTests(unittest.TestCase):
    def test_instrumentation_does_not_change_outcome(self):
        original=progression('attack',seed=17,decisions=100)
        audited=progression('attack',seed=17,decisions=100,engine_type=EconomyAudit)
        audit=audited.pop('long_term')
        self.assertEqual(original,audited)
        self.assertTrue(audit['gold_reconciliation'])
        self.assertTrue(audit['trips'])
        self.assertGreater(audit['spent'].get('rest',0),0)

    def test_funded_preparation_only_spends_available_gold(self):
        e=FundedPreparation(ROOT/'content',seed=17)
        original_gold=e.p['gold']
        e.prepare_base('recovery')
        self.assertGreaterEqual(e.p['gold'],0)
        audit=e.audit_report()
        self.assertTrue(audit['gold_reconciliation'])
        self.assertEqual(original_gold-e.p['gold'],sum(audit['spent'].values())-sum(audit['earned'].values()))
        self.assertLessEqual(e.p['level'],1)
        for item in e.s['inventory'].values(): self.assertLessEqual(item['enhance'],3)

    def test_return_and_death_trips_are_distinct(self):
        e=EconomyAudit(ROOT/'content',seed=1)
        e.execute('enter'); e.execute('return')
        self.assertEqual(e.audit_report()['trips'][0]['reason'],'return')
        e.execute('enter'); e.start_combat(); e.p['hp']=1
        e.s['enemy'].update(atk=100000,accuracy=2,pattern=['attack'],evasion=0)
        e.execute('defend')
        self.assertEqual(e.audit_report()['trips'][1]['reason'],'death')
