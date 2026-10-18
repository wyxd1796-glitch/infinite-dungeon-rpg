import copy
import json
import unittest
from collections import Counter
from pathlib import Path
from unittest.mock import patch
from core.game_engine import GameEngine
from core.environments import FLOOR_WEIGHTS, guidance, validate_environments

ROOT=Path(__file__).resolve().parents[1]

class EnvironmentTests(unittest.TestCase):
    def setUp(self):
        self.e=GameEngine(ROOT/'content',seed=313)

    def test_all_environment_boundaries_and_independent_cycles(self):
        e=self.e
        for floor in range(1,1201):
            e.s['floor']=floor
            self.assertEqual(e.environment()['source_id'],f'ENV{((floor-1)%300)//10+1:03}')
            self.assertTrue(e.content.regions.monsters(e.content,floor))
            if floor%10==0:
                self.assertEqual(e.content.regions.boss_id(floor),f'BOS{((floor-1)%400)//10+1:03}')

    def test_floor_distribution_100000_draws_and_boss_no_rng(self):
        e=self.e; e.s['floor']=1; counts=Counter()
        for _ in range(100000): e.roll_floor(); counts[e.s['floor_type']]+=1
        for key,percent in FLOOR_WEIGHTS.items(): self.assertLess(abs(counts[key]/100000-percent/100),.005)
        e.s['floor']=400; before=e.rng.getstate(); e.roll_floor()
        self.assertEqual(e.s['floor_type'],'FLR005'); self.assertEqual(before,e.rng.getstate())

    def test_every_environment_entry_effect_and_reload_no_repeat(self):
        e=self.e
        for n in range(1,31):
            e.s.update(floor=300+(n-1)*10+1,mode='explore',floor_type='FLR001')
            env=e.environment()
            with patch.object(e,'apply_status') as apply:
                e.start_combat()
                if env.get('floor_effect_id'):
                    number=int(env['floor_effect_id'][2:])
                    apply.assert_called_once_with(number,'enemy' if number>=29 else 'player','enemy',.1)
                else: apply.assert_not_called()
            state=copy.deepcopy(e.s); restored=GameEngine(ROOT/'content',state=state)
            self.assertEqual(restored.s['enemy'],e.s['enemy'])
            self.assertEqual(restored.environment(),env)

    def test_floor_encounter_modifiers_and_forced_boss(self):
        e=self.e
        for kind,elite,chest in [('FLR001',0,0),('FLR002',15,0),('FLR003',0,20),('FLR004',0,0)]:
            e.s.update(mode='explore',floor=1,floor_type=kind,progress=0)
            with patch.object(e.rng,'choices',return_value=['normal']) as roll,patch.object(e,'start_combat'):
                e.explore()
            args=roll.call_args; weights=dict(zip(args.args[0],args.kwargs['weights']))
            base=e.content.balance['encounters']
            self.assertEqual(weights['elite'],base['elite']+elite)
            self.assertEqual(weights['chest'],base['chest']+chest)
            self.assertEqual(weights['normal'],base['normal']-elite-chest)
            self.assertEqual(sum(weights.values()),sum(base.values()))
        e.s.update(mode='explore',floor=10,floor_type='FLR005',progress=2,boss_done=False)
        with patch.object(e,'start_combat') as start,patch.object(e.rng,'choices') as roll:
            e.explore(); start.assert_called_once_with('boss'); roll.assert_not_called()

    def test_danger_stats_and_gold_only_bonus(self):
        import math
        e=self.e
        for floor in (10,100,110,300,410):
            values=[]
            for kind in ('FLR005','FLR004'):
                e.s.update(floor=floor,highest=floor,floor_type=kind,statuses=[])
                e.start_combat('boss'); enemy=e.s['enemy']
                values.append((enemy['hp'],enemy['atk'],enemy['defense']))
            self.assertLessEqual(abs(values[1][0]-values[0][0]*1.2),5)
            self.assertLessEqual(abs(values[1][1]-values[0][1]*1.2),3)
            self.assertEqual(values[0][2],values[1][2])
        # Isolate rewards from level changes and random loot.
        rewards=[]
        for kind in ('FLR001','FLR004'):
            e.s.update(floor=110,floor_type=kind,statuses=[]); e.start_combat('boss')
            with patch.object(e,'gain_gold') as gold,patch.object(e,'gain_exp') as xp,patch.object(e,'award_equipment'),patch.object(e,'grant_item'):
                e.victory(); rewards.append((gold.call_args.args[0],xp.call_args.args[0]))
        self.assertEqual(rewards[0][1],rewards[1][1])
        self.assertLessEqual(abs(rewards[1][0]-rewards[0][0]*1.3),2)

    def test_bad_environment_definitions_fail_closed(self):
        source=json.loads((ROOT/'content/source/catalogue_v4.json').read_text(encoding='utf-8'))['base_catalogue_v3']['content']
        for field,value in [('risk_modifier_pct',float('nan')),('reward_modifier_pct',True),('floor_effect_id','MON001'),('floor_effect_id','EF001'),('first_floor',0),('primary_family','')]:
            rows=copy.deepcopy(source['environments']); rows[0][field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):
                validate_environments(rows,source['floor_types'],{r['id'] for r in source['effects']})

    def test_guidance_read_only_and_legacy_encounter_rules(self):
        e=self.e; e.s.update(floor=231,mode='explore',floor_type='FLR004')
        before=copy.deepcopy(e.s); rng=e.rng.getstate()
        self.assertIn('×1.27',guidance(e)); self.assertIn('경험치 제외',guidance(e))
        self.assertEqual(before,e.s); self.assertEqual(rng,e.rng.getstate())
        e.s['floor']=10; e.start_combat('boss'); e.s['floor']=231
        self.assertNotIn('×1.27',guidance(e)); self.assertIn('가중치 ×3',guidance(e))
