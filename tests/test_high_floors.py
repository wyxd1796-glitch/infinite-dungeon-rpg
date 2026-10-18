"""03-06..09 routing, growth, mechanics and saved encounter contracts."""
import copy
import math
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from core.catalogue import cid
from core.game_engine import GameEngine
from core.high_floors import MECHANICS, HighFloors
from core.save_manager import SaveManager

ROOT=Path(__file__).resolve().parents[1]


class HighFloorTests(unittest.TestCase):
    def setUp(self):
        self.e=GameEngine(ROOT/'content',seed=713)

    def battle(self,floor=160):
        e=self.e; e.s.update(floor=floor,highest=floor,statuses=[],floor_type='FLR001')
        e.p['attributes']['vit']=1000; e.p['hp']=e.derived()['hp']
        e.start_combat('boss'); e.s['statuses']=[]
        e.s['enemy'].update(atk=1,effect_id=None,statuses=[],on_hit_effects=[])
        return e

    def test_all_pools_bosses_and_independent_cycles(self):
        e=self.e; found=set(); bosses=set()
        for floor in range(1,401):
            rows=e.content.regions.monsters(e.content,floor)
            self.assertTrue(rows); found.update(r['source_id'] for r in rows)
            if floor%10==0: bosses.add(e.content.regions.boss_id(floor))
        self.assertEqual(len(found),150); self.assertEqual(len(bosses),40)
        for floor in (101,200,201,300,301,400,401,800,1000,10000):
            e.s.update(floor=floor,mode='explore',enemy=None)
            self.assertEqual(e.environment()['source_id'],f'ENV{((floor-1)%300)//10+1:03}')
            self.assertEqual(e.content.regions.boss_id(floor+400),e.content.regions.boss_id(floor))
            e.start_combat('normal')
            self.assertEqual(e.s['enemy']['level'],floor)
            self.assertTrue(all(type(e.s['enemy'][s]) is int and e.s['enemy'][s]>0 for s in ('hp','atk','defense')))

    def test_average_growth_and_boss_continuity(self):
        e=self.e; high=e.content.high_floors
        for left,right in ((100,101),(199,201),(299,301),(399,401),(799,801),(999,1001)):
            means=[]
            for floor in (left,right):
                env=e.content.by_id[cid(e.content.regions.at(floor)['environment_id'])]
                rows=e.content.regions.monsters(e.content,floor); weights=high.weights(rows,env,floor)
                means.append({s:sum(high.stats(r,floor,env)[s]*w for r,w in zip(rows,weights))/sum(weights) for s in high.anchor})
            for s in high.anchor:
                self.assertGreaterEqual(means[1][s],means[0][s]*.99)
                self.assertLess(means[1][s]/means[0][s],1.2)
        previous=None
        for floor in (100,110,200,210,300,310,400,410,800,1000,10000):
            e.s['floor']=floor; e.start_combat('boss'); stats=[e.s['enemy'][s] for s in ('hp','atk','defense')]
            if previous: self.assertTrue(all(a>b for a,b in zip(stats,previous)))
            previous=stats

    def test_family_share_and_missing_family_fallback(self):
        e=self.e; high=e.content.high_floors; rows=e.content.regions.monsters(e.content,200)
        env={'primary_family':rows[0]['category']}; weights=high.weights(rows,env,200)
        self.assertAlmostEqual(sum(w for r,w in zip(rows,weights) if r['category']==env['primary_family'])/sum(weights),.7)
        self.assertEqual(high.weights(rows,{'primary_family':'absent'},200),[r['weight'] for r in rows])

    def test_growth_configuration_rejects_invalid_numbers(self):
        for group,key,value in (('normal_growth','hp',float('nan')),('gear_growth','hp',-1),('normal_growth','atk',True)):
            config=copy.deepcopy(self.e.content.high_floors.definition); config[group][key]=value
            with self.assertRaises(ValueError): HighFloors(config,self.e.content)

    def test_gear_grows_and_existing_rolls_stay_fixed(self):
        e=self.e; e.s['floor']=400
        for stat in ('atk','defense','hp','mp'):
            base=next(r for r in e.content['equipment'] if int(r['source_id'][2:])>90 and r['stat']==stat)
            self.assertGreater(e.equipment_base_stats(base,800)[stat],e.equipment_base_stats(base,400)[stat])
        item=e.generate_equipment(cid('EQ091')); before=e.gear_stats(item)
        new=e.content.by_id[cid('EQ091')]
        self.assertGreater(e.equipment_base_stats(new,99)['atk'],new['base_bonus']+151)
        e.s['floor']=10000; self.assertEqual(e.gear_stats(item),before)
        self.assertEqual(item['generation_rules_version'],1)
        old=e.content.by_id[cid('EQ001')]
        self.assertEqual(e.equipment_base_stats(old,200)['atk'],old['base_bonus']+303)

    def test_potion_unlock_fraction_and_cleanse_targets(self):
        e=self.e
        for number,floor in ((21,101),(22,151),(23,201),(24,301),(25,401)):
            key=cid(f'CON{number:03}')
            e.s['highest']=floor-1; e.refresh_shop(); self.assertNotIn(key,e.s['shop_stock'])
            e.s['highest']=floor; e.refresh_shop(); self.assertIn(key,e.s['shop_stock'])
            e.s.update(mode='explore',enemy=None); e.p.update(hp=1,mp=0); e.s['items'][key]=1
            e.consume(key); ratio=e.content.by_id[key]['effects'][0]['value']
            self.assertEqual(e.p['hp'],1+math.floor(e.derived()['hp']*ratio))
            self.assertEqual(e.p['mp'],math.floor(e.derived()['mp']*ratio))
        for number in range(36,41):
            e=self.battle(); key=cid(f'CON{number:03}'); row=e.content.by_id[key]
            for target in row['dispel_targets']: e.apply_status(int(target[2:]),'player','enemy',1)
            e.apply_status(1,'player','enemy',1); e.s['items'][key]=1; e.consume(key)
            self.assertEqual([s['effect_number'] for s in e.s['statuses']],[1])

    def test_all_six_mechanics_and_heavy_trigger(self):
        for mechanic in MECHANICS:
            e=self.battle(); enemy=e.s['enemy']; enemy.update(mechanic=mechanic,pattern=['special'])
            e.p['shield']=100
            with patch.object(e,'direct_hit',return_value=0) as hit,patch.object(e.rng,'random',return_value=0): e.counter()
            if mechanic=='보호막 파괴': self.assertEqual(e.p['shield'],0)
            if mechanic=='단일 강타': self.assertEqual(hit.call_args.args[1],2)
            if mechanic=='연속 공격': self.assertEqual(hit.call_count,2)
            if mechanic=='특수 소환':
                self.assertEqual(hit.call_count,2); self.assertEqual(enemy['summon_turns'],1)
                self.assertEqual(enemy['shield'],math.floor(enemy['max_hp']*.08))
            if mechanic=='회복 억제': self.assertEqual(enemy['healing_suppression'],2)
            if mechanic=='추가 상태이상': self.assertIn(24,[s['effect_number'] for s in e.s['statuses']])
        e=self.battle(310); e.s['enemy'].update(pattern=['heavy'],mechanic='보호막 파괴'); e.p['shield']=100
        with patch.object(e,'direct_hit',return_value=0): e.counter()
        self.assertEqual(e.p['shield'],0)

    def test_silence_stun_summon_duration_and_death_order(self):
        e=self.battle(); enemy=e.s['enemy']; enemy.update(pattern=['special'],mechanic='회복 억제')
        e.apply_status(6,'enemy','player',1)
        with patch.object(e,'direct_hit',return_value=0): e.counter()
        self.assertEqual(enemy['healing_suppression'],0)
        enemy.update(statuses=[],summon_turns=2,pattern=['defend']); e.apply_status(4,'enemy','player',1)
        with patch.object(e,'direct_hit',return_value=0) as hit: e.counter(); hit.assert_not_called()
        self.assertEqual(enemy['summon_turns'],2)
        enemy['statuses']=[]
        with patch.object(e,'direct_hit',return_value=0) as hit: e.counter(); e.counter(); e.counter()
        self.assertEqual(hit.call_count,2); self.assertEqual(enemy['summon_turns'],0)
        enemy.update(pattern=['special'],mechanic='연속 공격'); e.p['hp']=1
        def kill(*args,**kwargs): e.p['hp']=0; return 1
        with patch.object(e,'direct_hit',side_effect=kill) as hit: e.counter()
        self.assertEqual(hit.call_count,1); self.assertEqual(e.s['stats']['deaths'],1)

    def test_boss_status_action_uses_effect_polarity_and_heal_is_silenceable(self):
        e=self.battle(250); enemy=e.s['enemy']; enemy.update(pattern=['debuff'],effect_id='EF030')
        with patch.object(e.rng,'random',return_value=0): e.counter()
        self.assertIn(30,[s['effect_number'] for s in enemy['statuses']]); self.assertFalse(e.s['statuses'])
        enemy.update(pattern=['heal'],statuses=[],hp=enemy['max_hp']//2)
        before=enemy['hp']; e.counter(); self.assertEqual(enemy['hp']-before,math.floor(enemy['max_hp']*.04))
        e.apply_status(6,'enemy','player',1); before=enemy['hp']
        with patch.object(e,'direct_hit',return_value=0): e.counter()
        self.assertEqual(enemy['hp'],before)

    def test_suppression_duration_healing_and_save_resume(self):
        e=self.battle(); enemy=e.s['enemy']; enemy.update(pattern=['defend'],healing_suppression=2,suppression_at=e.s['turn'])
        e.p.update(hp=1,mp=0)
        e.effects([dict(type='heal_hp',value=20),dict(type='heal_mp',value=20)])
        self.assertEqual((e.p['hp'],e.p['mp']),(11,20))
        e.p['hp']=e.derived()['hp']; e.s['skill_cooldowns']['phase2.skill.SKL003']=2
        with tempfile.TemporaryDirectory() as directory:
            store=SaveManager(directory); store.save(1,e.s)
            restored=GameEngine(ROOT/'content',state=store.load(1),seed=713)
        self.assertEqual(restored.s['enemy'],e.s['enemy'])
        self.assertEqual(restored.s['skill_cooldowns'],e.s['skill_cooldowns'])
        restored.execute('defend'); self.assertEqual(restored.s['enemy']['healing_suppression'],1)
        restored.execute('defend'); self.assertEqual(restored.s['enemy']['healing_suppression'],0)

    def test_old_high_battle_snapshot_rewards_and_gear(self):
        e=self.e; e.s['floor']=10; e.start_combat('boss')
        old=copy.deepcopy(e.s['enemy']); e.s.update(floor=410,highest=410)
        restored=GameEngine(ROOT/'content',state=e.s,seed=713)
        self.assertEqual(restored.s['enemy'],old)
        self.assertEqual(restored.environment()['source_id'],'ENV001')
        for _ in range(50): self.assertLessEqual(int(restored.generate_equipment()['base_id'][-3:]),90)
        restored.s['enemy']['hp']=0; restored.victory(); restored.start_combat('boss')
        self.assertEqual(restored.s['enemy']['depth_rules_version'],1)
        self.assertEqual(restored.environment()['source_id'],'ENV011')

    def test_saved_version_and_mechanic_validation(self):
        e=self.battle()
        for key,value in (('depth_rules_version',2),('mechanic','unknown'),('summon_turns',3),('healing_suppression',-1),('suppression_at',999),('reward_factor',float('inf')),('environment_snapshot',None)):
            state=copy.deepcopy(e.s); state['enemy'][key]=value
            with self.subTest(key=key),self.assertRaises(ValueError): SaveManager.validate(state)
        state=copy.deepcopy(e.s); state['enemy']['environment_snapshot']['risk_modifier_pct']=float('nan')
        with self.assertRaises(ValueError): SaveManager.validate(state)

    def test_reloaded_boss_continuation_matches_state_and_rng(self):
        e=self.battle(); e.s['enemy']['effect_id']='EF021'; e.p['hp']=e.derived()['hp']; e.execute('defend')
        with tempfile.TemporaryDirectory() as directory:
            store=SaveManager(directory); store.save(1,e.s)
            restored=GameEngine(ROOT/'content',state=store.load(1))
        e.execute('defend'); restored.execute('defend')
        # JSON serializes tuples in rng_state as arrays; compare after normalization.
        import json
        self.assertEqual(json.loads(json.dumps(e.s)),json.loads(json.dumps(restored.s)))
        self.assertEqual(e.rng.getstate(),restored.rng.getstate())

    def test_every_high_material_can_be_sold_without_turn_cost(self):
        e=self.e
        for number in range(21,61):
            key=cid(f'MAT{number:03}'); e.s['items'][key]=1; gold=e.p['gold']; turn=e.s['turn']
            e.execute('sell',key=key,quantity=1)
            self.assertEqual(e.s['items'][key],0); self.assertGreater(e.p['gold'],gold)
            self.assertEqual(e.s['turn'],turn)

    def test_new_gear_pending_save_and_boss_materials(self):
        e=self.battle(200); material=cid(e.s['enemy']['material_id'])
        e.s['items']={r['id']:1 for r in e.content['materials'][:30]}
        e.award_equipment(); pending=copy.deepcopy(e.s['pending_loot'])
        self.assertEqual(pending[0]['equipment']['generation_rules_version'],1)
        with tempfile.TemporaryDirectory() as directory:
            store=SaveManager(directory); store.save(1,e.s); restored=store.load(1)
        self.assertEqual(restored['pending_loot'],pending)
        e.s['items']={}; before=e.s['progress']; e.s['enemy']['hp']=0; e.resolve_deaths(); e.resolve_deaths()
        self.assertGreaterEqual(e.s['items'][material],2); self.assertEqual(e.s['progress'],before+1)


if __name__=='__main__': unittest.main()
