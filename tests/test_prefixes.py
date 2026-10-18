import copy
import itertools
import math
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from core.game_engine import GameEngine
from core.prefixes import apply,validate,validate_saved
from core.save_manager import SaveManager

ROOT=Path(__file__).resolve().parents[1]


class PrefixTests(unittest.TestCase):
    def setUp(self):
        self.e=GameEngine(ROOT/'content',seed=713)
        e=self.e; e.s.update(floor=400,highest=400)
        with patch.object(e.rng,'random',return_value=.99): e.start_combat()
        e.s['statuses']=[]
        e.s['enemy'].update(hp=1000,max_hp=1000,atk=100,defense=100,evasion=.1,crit=.05,
                           pattern=['attack'],statuses=[],effect_id=None,on_hit_effects=[],prefix_ids=[])

    def add(self,number):
        enemy=self.e.s['enemy']; row=self.e.content.by_id[f'catalogue.v3.PFX{number:03}']
        apply(enemy,row,self.e.content.prefixes); enemy['prefix_ids'].append(row['id']); enemy['max_hp']=enemy['hp']
        return enemy

    def test_all_50_definitions_and_scalar_effects(self):
        e=self.e; self.assertEqual(len(e.content['prefixes']),50); original=copy.deepcopy(e.s['enemy'])
        expected={21:('atk',117),22:('crit',.12),23:('atk',122),24:('atk',127),25:('leech',.03),27:('defense',118),28:('defense',124),29:('reflect',.06),30:('defense',128),31:('reduction',.12),32:('defense',108),33:('hp',1180),34:('hp_regen',.02),36:('hp',1250),37:('status_resist',.15),46:('gold_multiplier',1.25),47:('exp_multiplier',1.25),48:('exp_multiplier',1.35)}
        for n in range(1,51):
            e.s['enemy']=copy.deepcopy(original); enemy=self.add(n); SaveManager.validate(e.s)
            if n in expected:
                key,value=expected[n]; actual=enemy[key] if key in ('gold_multiplier','exp_multiplier') else e.enemy_stats()[key]
                self.assertAlmostEqual(actual,value,msg=str(n))
        e.s['enemy']=copy.deepcopy(original); self.add(24); self.assertEqual(e.s['enemy']['defense'],92)
        e.s['enemy']=copy.deepcopy(original); self.add(30); self.assertAlmostEqual(e.enemy_stats()['evasion'],.07)
        e.s['enemy']=copy.deepcopy(original); self.add(36); self.assertAlmostEqual(e.enemy_stats()['evasion'],.05)

    def test_category_pairs_and_no_resource_or_rng_on_apply(self):
        e=self.e; original=copy.deepcopy(e.s['enemy']); count=0
        for a,b in itertools.combinations(e.content['prefixes'],2):
            if a['category']==b['category']: continue
            e.s['enemy']=copy.deepcopy(original); e.s['enemy']['kind']='elite'; rng=e.rng.getstate()
            for row in (a,b): apply(e.s['enemy'],row,e.content.prefixes); e.s['enemy']['prefix_ids'].append(row['id'])
            e.s['enemy']['max_hp']=e.s['enemy']['hp']; SaveManager.validate(e.s)
            self.assertEqual(e.rng.getstate(),rng); count+=1
        self.assertEqual(count,1000)

    def test_unlock_weighted_selection_and_boss_exclusion(self):
        e=self.e; seen=set()
        for floor in (1,100,101,130,131,160,161,190,191,220,221,400,401,800):
            e.s['floor']=floor
            for _ in range(100):
                e.start_combat('elite'); ids=e.s['enemy']['prefix_ids']; seen.update(ids)
                rows=[e.content.by_id[k] for k in ids]
                self.assertTrue(1<=len(rows)<=2); self.assertEqual(len(rows),len({r['category'] for r in rows}))
                self.assertTrue(all(r.get('min_floor',1)<=floor for r in rows))
            e.start_combat('boss'); self.assertEqual(e.s['enemy']['prefix_ids'],[])
        self.assertEqual(len(seen),50)

    def test_execute_threshold_and_damage_reduction(self):
        e=self.e; self.add(26)
        e.p['hp']=30
        with patch.object(e.rng,'random',return_value=.5),patch.object(e.rng,'uniform',return_value=1):
            # Use a harmless attack to compare without killing the player.
            e.s['enemy']['atk']=10; low=e.direct_hit('enemy'); e.p['hp']=31; high=e.direct_hit('enemy')
        self.assertGreater(low,high)
        e=self.e; e.s['enemy']['prefix_ids']=[]; e.s['enemy'].pop('prefix_runtime'); self.add(31)
        with patch.object(e.rng,'random',return_value=.5),patch.object(e.rng,'uniform',return_value=1):
            e.s['enemy']['defense']=0; actual=e.direct_hit('player')
        self.assertEqual(actual,math.floor(math.floor(e.derived()['atk']-.6)*.88))

    def test_reflection_regeneration_and_resistance(self):
        e=self.e; self.add(29); e.s['enemy']['defense']=0; e.p['attributes']['str']=100
        with patch.object(e.rng,'random',return_value=.5),patch.object(e.rng,'uniform',return_value=1):
            hp=e.p['hp']; damage=e.direct_hit('player')
        self.assertEqual(hp-e.p['hp'],math.floor(damage*.06))
        self.add(34); e.s['enemy']['hp']=100; e.tick_start('enemy'); self.assertEqual(e.s['enemy']['hp'],100+math.floor(e.s['enemy']['max_hp']*.02))
        e.s['enemy']['prefix_ids']=[]; self.add(37)
        with patch.object(e.rng,'random',return_value=.1): self.assertFalse(e.apply_status(1,'enemy','player',.2))

    def test_on_hit_six_effects_and_no_proc_on_absorption(self):
        e=self.e; original=copy.deepcopy(e.s['enemy'])
        for n,number,chance in ((39,5,.1),(40,16,.15),(41,18,.12),(42,20,.15),(43,22,.1),(44,9,.2)):
            e.s['enemy']=copy.deepcopy(original); self.add(n)
            with patch.object(e,'direct_hit',return_value=1),patch.object(e,'apply_status') as proc: e.counter()
            self.assertEqual(proc.call_args.args,(number,'player')); self.assertEqual(proc.call_args.kwargs,{'chance':chance})
            with patch.object(e,'direct_hit',return_value=0),patch.object(e,'apply_status') as proc: e.counter(); proc.assert_not_called()

    def test_survival_once_across_save_and_with_status(self):
        e=self.e; self.add(38)
        e.damage_hp('enemy',2000,'periodic'); self.assertEqual(e.s['enemy']['hp'],1)
        with tempfile.TemporaryDirectory() as directory:
            store=SaveManager(directory); store.save(1,e.s); restored=GameEngine(ROOT/'content',state=store.load(1))
        self.assertEqual(restored.s['enemy'],e.s['enemy'])
        restored.apply_status(39,'enemy','enemy',1); restored.damage_hp('enemy',100,'direct')
        self.assertEqual(restored.s['enemy']['hp'],0)

    def test_kill_heal_happens_only_on_actual_kill(self):
        e=self.e; enemy=self.add(35); enemy.update(hp=500,defense=0); e.p['hp']=1
        with patch.object(e.rng,'random',return_value=.5),patch.object(e.rng,'uniform',return_value=1): e.direct_hit('enemy')
        self.assertEqual(enemy['hp'],550); e.direct_hit('enemy'); self.assertEqual(enemy['hp'],550)

    def test_drop_bonuses_and_rarity_are_local_to_reward(self):
        e=self.e; original=copy.deepcopy(e.s)
        e.s['floor']=221; self.add(45)
        with patch.object(e.rng,'random',return_value=.16),patch.object(e,'award_equipment') as award: e.victory()
        award.assert_called_once()
        e.s=copy.deepcopy(original); self.add(49); e.s['enemy']['drop_material_pct']=20; material='catalogue.v3.'+e.s['enemy']['material_id']
        with patch.object(e.rng,'random',return_value=.24),patch.object(e,'grant_item',wraps=e.grant_item) as grant: e.victory()
        self.assertIn(((material,1),{}),[(c.args,c.kwargs) for c in grant.call_args_list])
        e.s=copy.deepcopy(original); self.add(50)
        with patch.object(e.rng,'random',return_value=0),patch.object(e,'award_equipment') as award: e.victory()
        award.assert_called_once_with(rarity_bonus=4)
        self.assertNotIn('rarity_pp',e.s['exploration_bonuses'])
        weights=e.rarity_weights(luck=0,bonus=4); self.assertAlmostEqual(sum(weights[2:]),19)

    def test_reject_invalid_definitions_and_saved_state(self):
        e=self.e
        for effect in ({'type':'execute','value':float('nan')},{'type':'multiply','stat':'mp','value':.1},{'type':'hit','effect':999,'chance':.1},{'type':'code','value':1}):
            data=copy.deepcopy(e.content.prefixes); data['effects']['PFX021']=[effect]
            with self.assertRaises(ValueError): validate(data,e.content['prefixes'])
        self.add(38)
        for value in (float('nan'),-1,2):
            data=copy.deepcopy(e.s['enemy']['prefix_runtime']); data['survive']=value
            with self.assertRaises(ValueError): validate_saved(data)
        e.s['enemy']['prefix_ids']=['catalogue.v3.PFX001','catalogue.v3.PFX021']; e.s['enemy']['kind']='elite'
        with self.assertRaises(ValueError): SaveManager.validate(e.s)


if __name__=='__main__': unittest.main()
