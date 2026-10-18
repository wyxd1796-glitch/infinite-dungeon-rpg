import copy
import json
import math
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from core.game_engine import GameEngine, RuleError
from core.phase3_effects import EFFECTS, validate_definition
from core.save_manager import SaveManager

ROOT=Path(__file__).resolve().parents[1]


class AdvancedEffectsTests(unittest.TestCase):
    def combat(self):
        e=GameEngine(ROOT/'content',seed=713); e.execute('enter'); e.start_combat()
        e.s['enemy'].update(hp=10000,max_hp=10000,atk=1,defense=0,evasion=0,accuracy=0,
                           pattern=['defend'],on_hit_effects=[],effect_id=None)
        e.p['level']=30
        return e

    def apply(self,e,n,side='player'):
        source=side if n>=29 else ('enemy' if side=='player' else 'player')
        self.assertTrue(e.apply_status(n,side,source,1))

    def roundtrip(self,e):
        with tempfile.TemporaryDirectory() as directory:
            store=SaveManager(directory); store.save(1,e.s)
            return GameEngine(ROOT/'content',state=store.load(1))

    def test_definitions_and_all_actor_expiries(self):
        for n in range(26,41):
            for side in ('player','enemy'):
                with self.subTest(n=n,side=side):
                    e=self.combat(); row=copy.deepcopy(e.content.by_id[f'catalogue.v3.EF{n:03}'])
                    row['id']=row['source_id']; validate_definition(row)
                    self.assertEqual(row['polarity'],'debuff' if n<=28 else 'buff')
                    self.apply(e,n,side); SaveManager.validate(e.s)
                    for _ in range(EFFECTS[n][3]):
                        e.s['turn']+=1; e.tick_start(side); e.tick_end(side)
                    self.assertFalse(e.actor_statuses(side))

    def test_effective_mp_cost_rejection_auto_reserve_and_payment(self):
        e=self.combat(); key='phase2.skill.SKL003'; e.s['skills'][key]=1; self.apply(e,26)
        self.assertEqual(e.skill_mp_cost(key),15)
        e.p['mp']=14; before=copy.deepcopy(e.s); rng=e.rng.getstate()
        self.assertEqual(e.skill_reason(key),'MP 부족')
        with self.assertRaises(RuleError): e.execute('skill',key=key)
        self.assertEqual(e.s,before); self.assertEqual(e.rng.getstate(),rng)
        for config in e.s['skill_auto'].values(): config['enabled']=False
        e.s['skill_auto'][key]['enabled']=True; e.p['mp']=20; e.s['settings']['mp_reserve']=6
        self.assertEqual(e.next_auto_action()['action'],'attack')
        e.s['settings']['mp_reserve']=5; self.assertEqual(e.next_auto_action()['key'],key)
        e.execute('skill',key=key); self.assertEqual(e.p['mp'],5)

    def test_max_mp_clamp_refresh_expire_and_load_no_gain(self):
        e=self.combat(); e.p['mp']=30; self.apply(e,27)
        self.assertEqual((e.derived()['mp'],e.p['mp']),(25,25))
        self.apply(e,27); self.assertEqual(e.derived()['mp'],25)
        e=self.roundtrip(e)
        for _ in range(3): e.execute('defend')
        self.assertEqual((e.derived()['mp'],e.p['mp']),(30,25))
        e=self.roundtrip(e); self.assertEqual(e.p['mp'],25)

    def test_skill_multiplier_excludes_basic_and_healing(self):
        e=self.combat(); self.apply(e,28); self.apply(e,32)
        with patch.object(e.rng,'random',return_value=.5),patch.object(e.rng,'uniform',return_value=1):
            normal=e.direct_hit('player',action='attack')
            skill=e.direct_hit('player',action='skill')
        self.assertEqual(normal,math.floor(e.derived()['atk']-.6*e.enemy_stats()['defense']))
        self.assertEqual(skill,math.floor(e.derived()['atk']*.8*1.2-.6*e.enemy_stats()['defense']))
        e.p['hp']=10; e.effects([dict(type='heal_hp',value=10)])
        self.assertEqual(e.p['hp'],20)

    def test_crit_reduction_counter_caps_and_defense(self):
        e=self.combat()
        for n in (29,30,33,36,38): self.apply(e,n)
        self.assertEqual(e.derived()['defense'],math.floor(5*1.25))
        d=dict(e.derived(),crit=.74,reduction=.69,counter=.39)
        result=e.apply_modifiers(d,e.s['statuses'])
        self.assertEqual((result['crit'],result['reduction'],result['counter']),(.75,.7,.4))
        self.assertEqual(e.derived()['crit_damage'],.25)
        self.assertEqual(e.damage_hp('player',10,'periodic'),10)

    def test_critical_damage_only_on_crit(self):
        e=self.combat(); self.apply(e,36)
        with patch.object(e.rng,'random',return_value=.5),patch.object(e.rng,'uniform',return_value=1):
            normal=e.direct_hit('player')
        with patch.object(e.rng,'random',return_value=0),patch.object(e.rng,'uniform',return_value=1):
            critical=e.direct_hit('player')
        self.assertEqual(critical,math.floor(normal*1.75))

    def test_healing_starts_next_turn_and_caps(self):
        e=self.combat(); e.p['hp']=50; self.apply(e,34)
        e.tick_start('player'); self.assertEqual(e.p['hp'],50)
        e.s['turn']+=1; e.tick_start('player'); self.assertEqual(e.p['hp'],56)
        e.p['hp']=99; e.tick_start('player'); self.assertEqual(e.p['hp'],100)

    def test_mp_leech_actual_damage_no_secondary_or_shield_gain(self):
        e=self.combat(); e.p['mp']=0; self.apply(e,35); e.s['enemy']['hp']=21
        with patch.object(e.rng,'random',return_value=.5),patch.object(e.rng,'uniform',return_value=1):
            actual=e.direct_hit('player',mult=100)
        self.assertEqual(actual,21); self.assertEqual(e.p['mp'],1)
        e.s['enemy']['hp']=10000; e.s['enemy']['shield']=10000
        with patch.object(e.rng,'random',return_value=.5): e.direct_hit('player')
        self.assertEqual(e.p['mp'],1)
        e.s['enemy']['shield']=0
        with patch.object(e.rng,'random',return_value=.5): e.direct_hit('player',mult=100,secondary=True)
        self.assertEqual(e.p['mp'],1)

    def test_barrier_once_refresh_save_and_reapplication(self):
        e=self.combat(); self.apply(e,37)
        self.assertEqual(e.damage_hp('player',20,'direct'),5)
        st=e.s['statuses'][0]; self.assertTrue(st['triggered'])
        self.apply(e,37); self.assertEqual(e.damage_hp('player',5,'direct'),5)
        e=self.roundtrip(e); self.assertEqual(e.damage_hp('player',5,'direct'),5)
        for _ in range(3): e.s['turn']+=1; e.tick_end('player')
        self.apply(e,37); self.assertEqual(e.damage_hp('player',5,'counter'),0)
        self.assertEqual(e.p['shield'],10)

    def test_barrier_not_additive_and_not_triggered_by_periodic(self):
        e=self.combat(); self.apply(e,37); e.p['shield']=30
        self.assertEqual(e.damage_hp('player',4,'periodic'),4)
        self.assertFalse(e.s['statuses'][0]['triggered'])
        self.assertEqual(e.damage_hp('player',10,'direct'),0)
        self.assertEqual(e.p['shield'],20)

    def test_survival_all_damage_types_once_per_battle(self):
        for kind in ('direct','counter','periodic','reflected'):
            with self.subTest(kind=kind):
                e=self.combat(); self.apply(e,39); e.p['hp']=10
                self.assertEqual(e.damage_hp('player',1000,kind),9); self.assertEqual(e.p['hp'],1)
                e.s['statuses']=[]; self.apply(e,39)
                e=self.roundtrip(e); self.assertEqual(e.damage_hp('player',1000,kind),1)
                self.assertEqual(e.p['hp'],0)
                e.resolve_deaths(); e.start_combat(); self.apply(e,39)
                e.damage_hp('player',1000,kind); self.assertEqual(e.p['hp'],1)

    def test_survival_does_not_heal_low_hp_and_shield_precedes_it(self):
        e=self.combat(); e.p['attributes']['vit']=100; self.apply(e,39)
        e.p.update(hp=1,shield=10)
        self.assertEqual(e.damage_hp('player',10,'direct'),0)
        self.assertFalse(e.s['effect_combat_state']['player']['survive_used'])
        self.assertEqual(e.damage_hp('player',1,'direct'),0); self.assertEqual(e.p['hp'],1)
        self.assertTrue(e.s['effect_combat_state']['player']['survive_used'])

    def test_enemy_survival_and_player_reflection_survival(self):
        e=self.combat(); self.apply(e,39,'enemy'); e.s['enemy']['hp']=10
        e.damage_hp('enemy',1000,'direct'); self.assertEqual(e.s['enemy']['hp'],10)
        self.assertTrue(e.s['effect_combat_state']['enemy']['survive_used'])
        e=self.combat(); self.apply(e,39); e.p['hp']=1; e.s['enemy']['hp']=10
        stats={'player':dict(e.derived(),atk=100,crit=0),'enemy':dict(e.enemy_stats(),reflect=1,counter=0)}
        with patch.object(e,'stats_for',side_effect=stats.__getitem__),patch.object(e.rng,'random',return_value=.5),patch.object(e.rng,'uniform',return_value=1): e.direct_hit('player')
        e.resolve_deaths(); self.assertEqual(e.s['stats']['wins'],1); self.assertEqual(e.s['stats']['deaths'],0)

    def test_gold_group_once_and_cap(self):
        rewards=[]
        for buffs in ((),(31,),(40,),(31,40)):
            e=self.combat()
            for n in buffs: self.apply(e,n)
            e.s['enemy']['hp']=0; e.resolve_deaths(); rewards.append(e.s['last_gold'])
            state=copy.deepcopy(e.s); e.resolve_deaths(); self.assertEqual(e.s,state)
        base=rewards[0]; self.assertEqual(rewards[1:], [math.floor(base*1.2),math.floor(base*1.25),math.floor(base*1.25)])
        e=self.combat(); self.apply(e,40); stats=dict(e.derived(),gold_bonus=2)
        with patch.object(e,'derived',return_value=stats): e.s['enemy']['hp']=0; e.resolve_deaths()
        self.assertEqual(e.s['last_gold'],base*3)

    def test_cure_preserves_buffs_and_no_mp_refill(self):
        e=self.combat(); self.apply(e,26); self.apply(e,27); self.apply(e,28); self.apply(e,29)
        e.s['items']['catalogue.v3.CON016']=1; e.consume('catalogue.v3.CON016')
        self.assertEqual([s['effect_number'] for s in e.s['statuses']],[29])
        self.assertEqual((e.derived()['mp'],e.p['mp']),(30,25))

    def test_save_flags_validation_and_old_v2_gate(self):
        e=self.combat(); self.apply(e,37); self.apply(e,39)
        for change in ('flag','trigger','version'):
            s=copy.deepcopy(e.s)
            if change=='flag': s['effect_combat_state']['player']['survive_used']='false'
            elif change=='trigger': s['statuses'][0]['triggered']=0
            else: s['battle_rules_version']=2
            with self.assertRaises(ValueError): SaveManager.validate(s)
        old=self.combat(); old.s['battle_rules_version']=2; old.s.pop('effect_combat_state')
        old=self.roundtrip(old); self.assertTrue(old.apply_status(16,'player','enemy',1))
        before=copy.deepcopy(old.s); rng=old.rng.getstate()
        self.assertFalse(old.apply_status(26,'player','enemy',1)); self.assertEqual(old.s,before); self.assertEqual(old.rng.getstate(),rng)

    def test_combined_effects_save_resume(self):
        e=self.combat()
        for n in range(26,41): self.apply(e,n); self.apply(e,n,'enemy')
        e.damage_hp('player',20,'direct')
        # Saves are taken after execute commits the RNG, never midway through helpers.
        e.execute('defend')
        restored=self.roundtrip(e)
        for _ in range(5):
            e.execute('defend'); restored.execute('defend')
            self.assertEqual(json.dumps(e.s,sort_keys=True),json.dumps(restored.s,sort_keys=True))

    def test_positive_effect_does_not_use_status_resistance(self):
        e=self.combat(); stats=dict(e.derived(),status_resist=.75)
        with patch.object(e,'stats_for',return_value=stats),patch.object(e.rng,'random',return_value=.5):
            self.assertTrue(e.apply_status(29,'player','player',1))
            self.assertFalse(e.apply_status(26,'player','enemy',1))
