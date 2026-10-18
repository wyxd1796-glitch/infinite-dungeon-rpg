"""03-12: all forty boss encounter contracts."""
import copy
import unittest
from pathlib import Path
from unittest.mock import patch
from core.game_engine import GameEngine
from core.catalogue import cid
from core.bosses import validate_boss, guidance

ROOT=Path(__file__).resolve().parents[1]

class BossTests(unittest.TestCase):
    def setUp(self):
        self.e=GameEngine(ROOT/'content',seed=312)

    def encounter(self, floor):
        e=self.e; e.s.update(floor=floor,highest=floor,floor_type='FLR005',statuses=[])
        e.p['attributes']['vit']=100000; e.p['hp']=e.derived()['hp']
        e.start_combat('boss'); e.s['statuses']=[]
        return e.s['enemy']

    def test_all_bosses_archetypes_patterns_phase_threshold_and_latch(self):
        e=self.e
        for row in e.content['bosses']:
            with self.subTest(boss=row['source_id']):
                enemy=self.encounter(row['first_floor'])
                self.assertEqual(enemy['source_id'],e.content.by_id[row['monster_id']]['source_id'])
                self.assertEqual(enemy['pattern'],row['pattern'])
                enemy.update(hp=enemy['max_hp'],atk=100)
                with patch.object(e,'direct_hit',return_value=0),patch.object(e,'apply_status',return_value=False):
                    for _ in row['pattern']: e.counter()
                    self.assertEqual(enemy['pattern_index'],len(row['pattern']))
                    self.assertFalse(enemy['phase2'])
                    enemy.update(hp=int(enemy['max_hp']*.4),statuses=[],pattern=['defend'])
                    e.counter(); self.assertTrue(enemy['phase2'])
                    self.assertEqual(e.enemy_stats()['atk'],int(100*row['phase2_multiplier']))
                    enemy['hp']=enemy['max_hp']; e.counter()
                    self.assertTrue(enemy['phase2'])

    def test_all_boss_rewards_first_clear_replay_and_next_cycle(self):
        e=self.e
        for floor in range(10,401,10):
            with self.subTest(floor=floor):
                for visit in range(2):
                    enemy=self.encounter(floor); e.s['items']={}
                    material=cid(enemy['material_id']); before=e.s['progress']
                    with patch.object(e,'award_equipment') as gear,patch.object(e.rng,'random',return_value=.999):
                        enemy['hp']=0; e.resolve_deaths(); e.resolve_deaths()
                        gear.assert_called_once()
                    self.assertEqual(e.s['progress'],before+1)
                    self.assertGreaterEqual(e.s['items'][cid('MAT018')],1)
                    self.assertEqual(e.s['items'].get(cid('MAT016'),0),3 if visit==0 else 0)
                    if floor>100: self.assertGreaterEqual(e.s['items'][material],2)
        enemy=self.encounter(410)
        self.assertEqual(enemy['boss_id'],cid('BOS001'))
        self.assertNotIn(410,e.s['boss_first'])
        enemy['hp']=0; e.resolve_deaths(); self.assertIn(410,e.s['boss_first'])

    def test_bad_boss_contracts_rejected(self):
        row=copy.deepcopy(self.e.content['bosses'][0]); row['id']=row['source_id']
        effects={r['source_id'] for r in self.e.content['effects']}
        for key,value in [('phase2_hp_pct',float('nan')),('phase2_hp_pct',100),('phase2_multiplier',True),('hp_multiplier',0),('atk_multiplier',float('inf')),('effect_id','MON001'),('first_floor',20),('escape_allowed',True)]:
            bad=dict(row); bad[key]=value
            with self.subTest(key=key,value=value),self.assertRaises(ValueError): validate_boss(bad,effects,1.25)

    def test_guidance_does_not_change_saved_encounter_or_rng(self):
        for floor in range(10,401,10):
            enemy=self.encounter(floor); before=copy.deepcopy(self.e.s); rng=self.e.rng.getstate()
            self.assertIn('40%',guidance(enemy)); self.assertIn('25%',guidance(enemy))
            self.assertEqual(self.e.s,before); self.assertEqual(self.e.rng.getstate(),rng)
