import copy
import tempfile
import unittest
from core.game_engine import GameEngine, RuleError
from core.save_manager import SaveManager
from core.expansion_engine import GameEngine as PreviousEngine
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class AutoPolicyTests(unittest.TestCase):
    def engine(self):
        e=GameEngine(ROOT/'content',seed=17)
        e.execute('enter'); e.start_combat()
        e.s['settings']['stop_danger']=False
        e.p.update(hp=40,mp=30)
        return e

    def test_policies_and_preview_read_only(self):
        e=self.engine()
        for policy,action in [('potion_first','potion'),('skill_first','skill'),('efficient','potion')]:
            e.execute('setting',key='recovery_policy',value=policy)
            before=copy.deepcopy(e.s); rng=e.rng.getstate()
            self.assertEqual(e.next_auto_action()['action'],action)
            self.assertEqual(e.s,before); self.assertEqual(e.rng.getstate(),rng)

    def test_reserve_attacks_and_healing_exception(self):
        e=self.engine(); e.p['hp']=100; e.execute('setting',key='mp_reserve',value=30)
        self.assertEqual(e.next_auto_action()['action'],'attack')
        e.p['hp']=40; e.s['settings'].update(auto_potion=False,recovery_policy='skill_first')
        self.assertEqual(e.next_auto_action()['key'],'base.skill.heal')
        e.p['level']=30; e.s['skills']['phase2.skill.SKL003']=1
        e.s['skill_auto']['phase2.skill.SKL003'].update(enabled=True,priority=1)
        e.p['hp']=100
        self.assertEqual(e.next_auto_action()['action'],'attack')

    def test_silence_cooldowns_and_no_resources(self):
        e=self.engine(); e.s['items']={}; e.s['settings']['recovery_policy']='skill_first'
        e.s['statuses']=[dict(effect_number=6,turns=2)]
        self.assertEqual(e.next_auto_action()['action'],'attack')
        e.s['statuses']=[]
        e.s['skill_cooldowns']={k:2 for k in e.s['skill_auto']}
        self.assertEqual(e.next_auto_action()['action'],'attack')
        e.s['skill_cooldowns']={}; e.p['mp']=0
        self.assertEqual(e.next_auto_action()['action'],'attack')

    def test_danger_boundary_and_full_health_no_waste(self):
        e=self.engine(); e.s['settings'].update(stop_danger=True,recovery_policy='efficient')
        e.p['hp']=30
        self.assertEqual(e.next_auto_action()['action'],'stop')
        e.p['hp']=31
        self.assertNotEqual(e.next_auto_action()['action'],'stop')
        e.p['hp']=100
        self.assertNotEqual(e.next_auto_action()['key'],'base.skill.heal')

    def test_blocked_turn_preview_and_consumption(self):
        e=self.engine(); e.s['statuses']=[dict(effect_number=4,turns=1,applied_at=-1)]
        decision=e.next_auto_action(); self.assertIn('행동불가',decision['reason'])
        mp=e.p['mp']; items=copy.deepcopy(e.s['items']); turn=e.s['turn']
        e.battle(decision['action'],decision['key'])
        self.assertEqual(e.p['mp'],mp); self.assertEqual(e.s['items'],items)
        self.assertEqual(e.s['turn'],turn+1)

    def test_version_profile_preserves_previous_balance_values(self):
        import json
        e=self.engine()
        original=json.loads((ROOT/'content/base/balance.json').read_text(encoding='utf-8'))
        self.assertEqual(e.content.balance,original)

    def test_cleanse_and_efficiency_tie(self):
        e=self.engine(); e.s['settings']['recovery_policy']='efficient'
        e.p.update(level=20,hp=100); key='phase2.skill.SKL013'
        e.s['skills'][key]=1; e.s['skill_auto'][key]['enabled']=True
        e.s['statuses']=[dict(effect_number=1,turns=2)]
        self.assertEqual(e.next_auto_action()['key'],key)
        e.s['statuses']=[]; e.p['hp']=70; e.s['settings']['potion_threshold']=.7
        e.s['skills']['base.skill.heal']=5
        self.assertEqual(e.next_auto_action()['key'],'base.skill.heal')

    def test_settings_roundtrip_defaults_and_rejection(self):
        e=self.engine(); old=copy.deepcopy(e.s)
        del old['settings']['recovery_policy']; del old['settings']['mp_reserve']
        loaded=GameEngine(ROOT/'content',old)
        self.assertEqual(loaded.s['settings']['recovery_policy'],'potion_first')
        self.assertEqual(loaded.s['settings']['mp_reserve'],0)
        for key,value in [('mp_reserve',-1),('mp_reserve',True),('recovery_policy','unknown')]:
            before=copy.deepcopy(e.s); rng=e.rng.getstate()
            with self.assertRaises(RuleError): e.execute('setting',key=key,value=value)
            self.assertEqual(e.s,before); self.assertEqual(e.rng.getstate(),rng)
        e.execute('setting',key='mp_reserve',value=16)
        e.execute('setting',key='recovery_policy',value='efficient')
        with tempfile.TemporaryDirectory() as folder:
            store=SaveManager(folder); store.save(1,e.s)
            saved=GameEngine(ROOT/'content',store.load(1))
            self.assertEqual(saved.s['settings'],e.s['settings'])

    def test_default_matches_previous_loop(self):
        for seed in range(20):
            e=GameEngine(ROOT/'content',seed=seed); e.execute('enter'); e.start_combat()
            other=GameEngine(ROOT/'content',copy.deepcopy(e.s))
            other.rng.setstate(e.rng.getstate())
            e.execute('auto'); PreviousEngine.auto_battle(other)
            # Both runs consume the same actions and random draws.
            for key in ('player','enemy','skills','items','stats','mode','turn'):
                self.assertEqual(e.s[key],other.s[key])
            self.assertEqual(e.rng.getstate(),other.rng.getstate())
