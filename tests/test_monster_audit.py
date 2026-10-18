import copy
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from core.game_engine import GameEngine
from core.monster_roles import validate_monsters,effect_chance
from core.save_manager import SaveManager

ROOT=Path(__file__).resolve().parents[1]


class MonsterAuditTests(unittest.TestCase):
    def setUp(self):
        self.e=GameEngine(ROOT/'content',seed=20261018)

    def test_all_150_spawn_pattern_effect_reward_paths(self):
        e=self.e; clean=copy.deepcopy(e.s)
        for row in e.content['monsters']:
            with self.subTest(monster=row['source_id']):
                e.s=copy.deepcopy(clean); floor=row['min_floor']; e.s.update(floor=floor,highest=floor)
                e.p['attributes']['vit']=100000; e.p['hp']=e.derived()['hp']
                self.assertIn(row,e.content.regions.monsters(e.content,floor))
                with patch.object(e.rng,'choices',return_value=[row]),patch.object(e.rng,'random',return_value=.99): e.start_combat()
                enemy=e.s['enemy']; self.assertEqual(enemy['id'],row['id'])
                with patch.object(e,'direct_hit',return_value=1),patch.object(e,'apply_status',wraps=e.apply_status) as effect:
                    for _ in enemy['pattern']:
                        e.s['turn']+=1; e.counter()
                    if row['effect_id']:
                        self.assertTrue(effect.called)
                        self.assertEqual(effect.call_args.args[0],int(row['effect_id'][2:]))
                        self.assertEqual(effect.call_args.kwargs['chance'],effect_chance(enemy))
                self.assertEqual(enemy['pattern_index'],len(enemy['pattern']))
                before=e.s['progress']; gold=e.p['gold']
                with patch.object(e.rng,'random',return_value=0): e.victory()
                self.assertGreater(e.p['gold'],gold)
                key='catalogue.v3.'+row['material_id']; self.assertGreaterEqual(e.s['items'][key],1)
                self.assertEqual(e.s['progress'],before+1); self.assertEqual(e.s['stats']['wins'],1)
                SaveManager.validate(e.s)

    def test_existing_monster_effect_chance_survives_cycle(self):
        e=self.e; row=next(r for r in e.content['monsters'] if int(r['source_id'][3:])<=40 and r['effect_id'])
        e.s['floor']=400+row['min_floor']; e.p['attributes']['vit']=100000; e.p['hp']=e.derived()['hp']
        with patch.object(e.rng,'choices',return_value=[row]),patch.object(e.rng,'random',return_value=.99): e.start_combat()
        self.assertIsNone(effect_chance(e.s['enemy']))
        with patch.object(e,'direct_hit',return_value=1),patch.object(e.rng,'random',return_value=0):
            for _ in e.s['enemy']['pattern']: e.counter()
        self.assertTrue(e.s['statuses'] or e.s['enemy']['statuses'])

    def test_invalid_references_ranges_and_chances_rejected(self):
        data=json.loads((ROOT/'content/source/catalogue_v4.json').read_text(encoding='utf-8'))['base_catalogue_v3']['content']
        definition=json.loads((ROOT/'content/catalogue/monster_roles.json').read_text(encoding='utf-8'))
        for field,value in (('category',''),('max_floor',0),('weight',0),('special_proc_pct',101),('drop_material_pct',float('nan')),('material_id','MON001'),('effect_id','MAT001'),('ai_pattern_turns',99)):
            rows=copy.deepcopy(data['monsters']); rows[0][field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):
                validate_monsters(definition,rows,{r['id'] for r in data['effects']},{r['id'] for r in data['materials']})
        definition['monsters'].pop('MON150')
        with self.assertRaises(ValueError): validate_monsters(definition,data['monsters'],set(),set())

    def test_role_metadata_does_not_mutate_saved_enemy(self):
        e=self.e; e.start_combat(); before=copy.deepcopy(e.s['enemy'])
        restored=GameEngine(ROOT/'content',state=e.s)
        self.assertEqual(restored.s['enemy'],before); self.assertNotIn('role',before)

    def test_monster_gold_buff_is_paid_once_and_does_not_stack(self):
        e=self.e; clean=copy.deepcopy(e.s); gains=[]
        for both in (False,True):
            e.s=copy.deepcopy(clean); e.s['floor']=201; e.start_combat()
            e.s['enemy']['gold_multiplier']=1; e.s['statuses']=[]; e.s['enemy']['statuses']=[]
            e.apply_status(40,'enemy','enemy',1)
            if both: e.apply_status(31,'player','player',1)
            gold=e.p['gold']; e.s['enemy']['hp']=0
            with patch.object(e.rng,'random',return_value=.99): e.resolve_deaths(); e.resolve_deaths()
            gains.append(e.p['gold']-gold)
            self.assertEqual(e.s['stats']['wins'],1)
        self.assertEqual(gains[0],int((10+3*201)*1.27*1.25)); self.assertEqual(gains[0],gains[1])


if __name__=='__main__': unittest.main()
