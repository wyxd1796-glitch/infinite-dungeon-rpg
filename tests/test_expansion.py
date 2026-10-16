import copy
import hashlib
import json
import math
import unittest
from pathlib import Path
from unittest.mock import patch

from core.game_engine import GameEngine, RuleError
from core.legacy_engine import GameEngine as LegacyEngine
from core.catalogue import cid, OPTION_STATS
from core.save_manager import SaveManager

ROOT=Path(__file__).resolve().parents[1]

class ExpansionTests(unittest.TestCase):
    def setUp(self): self.e=GameEngine(ROOT/'content',seed=713)

    def combat(self):
        self.e.execute('enter'); self.e.start_combat()
        self.e.s['enemy'].update(hp=10000,max_hp=10000,atk=10,defense=0,evasion=0,accuracy=2,pattern=['attack'])
        return self.e

    def gear(self,**stats):
        e=self.e; gear=e.generate_equipment(cid('EQ001')); gear.update(rolled_stats=stats,affixes=[])
        key=gear['instance_id']; e.s['inventory'][key]=gear; e.s['equipped'][gear['slot']]=key
        return gear

    def test_exact_catalogue_and_original(self):
        e=self.e
        self.assertEqual(sum(e.content.catalogue_counts.values()),260)
        self.assertEqual(e.content.catalogue_counts,dict(monsters=40,bosses=10,prefixes=20,equipment=90,options=30,consumables=20,materials=20,environments=10,floor_types=5,effects=15))
        self.assertEqual(hashlib.sha256((ROOT/'content/source/catalogue_v4.json').read_bytes()).hexdigest(),e.content.catalogue['source_sha256'])
        self.assertEqual([len(e.content[t]) for t in ('skills','events','achievements')],[5,10,7])
        self.assertEqual(len({r['id'] for r in e.content.by_id.values() if r.get('catalogue')}),260)

    def test_all_depth_pools_and_cycle(self):
        e=self.e
        for floor in (1,10,30,50,100,101,200):
            e.s['floor']=floor; e.s['floor_type']='FLR001'
            for _ in range(50):
                e.start_combat(); monster=e.content.by_id[e.s['enemy']['id']]; zone=(floor-1)%100+1
                self.assertLessEqual(monster['min_floor'],zone); self.assertGreaterEqual(monster['max_floor'],zone)
                self.assertEqual(e.s['enemy']['level'],floor)
                gear=e.generate_equipment(); self.assertLessEqual(e.content.by_id[gear['base_id']]['min_floor'],floor)
        e.s['floor']=1; env=e.environment()['id']; e.s['floor']=101; self.assertEqual(e.environment()['id'],env)

    def test_boss_order_and_absolute_scaling(self):
        e=self.e
        for i in range(1,11):
            e.s['floor']=i*10; e.start_combat('boss'); first=copy.deepcopy(e.s['enemy'])
            self.assertEqual(first['boss_id'],cid(f'BOS{i:03}'))
            e.s['floor']+=100; e.start_combat('boss')
            self.assertEqual(first['boss_id'],e.s['enemy']['boss_id']); self.assertGreater(e.s['enemy']['hp'],first['hp'])

    def test_prefix_category_exclusion(self):
        e=self.e
        for _ in range(500):
            e.start_combat('elite'); ids=e.s['enemy']['prefix_ids']; cats=[e.content.by_id[k]['category'] for k in ids]
            self.assertIn(len(ids),(1,2)); self.assertEqual(len(cats),len(set(cats)))

    def test_all_gear_and_option_constraints(self):
        e=self.e; seen=set()
        for base in e.content['equipment']:
            e.s['floor']=max(100,base['min_floor'])
            for _ in range(15):
                item=e.generate_equipment(base['id']); self.assertEqual(item['slot'],base['slot'])
                ids=[a['id'] for a in item['affixes']]; self.assertEqual(len(ids),len(set(ids)))
                for affix in item['affixes']:
                    row=e.content.by_id[affix['id']]; seen.add(affix['id'])
                    self.assertIn(base['slot'],row['slots']); self.assertIn(row['category'],base['option_pool'])
                    scale=(item['level']//10)*row['per_10_levels']; divisor=1 if row['unit']=='점' else 100
                    self.assertGreaterEqual(affix['value']+.00005,(row['min_value']+scale)/divisor)
                    self.assertLessEqual(affix['value']-.00005,(row['max_value']+scale)/divisor)
        self.assertEqual(len(seen),30)

    def test_all_options_feed_derived_stats(self):
        before=self.e.derived()
        for stat in OPTION_STATS:
            with self.subTest(stat=stat):
                gear=self.gear(**{stat:1 if stat in ('str','dex','vit','int','atk','defense','hp','mp') else .1})
                after=self.e.derived(); target='luk' if stat=='luk_pct' else stat
                self.assertGreater(after[target],before.get(target,0)); self.e.s['equipped'].clear()

    def test_shop_unlock_and_refresh_without_rng(self):
        e=self.e; stock=e.s['shop_stock'][:]; rng=e.rng.getstate(); before=copy.deepcopy(e.s)
        for row in e.shop_stock(): e.shop_description(row['id'])
        self.assertEqual(before,e.s); self.assertEqual(rng,e.rng.getstate())
        with self.assertRaises(RuleError): e.execute('buy',key=cid('EQ090'))
        e.s['highest']=100; self.assertEqual(stock,e.s['shop_stock']); e.execute('enter'); e.execute('return')
        self.assertIn(cid('EQ090'),e.s['shop_stock'])

    def test_pending_stacks_partial_receive_and_discard(self):
        e=self.e; e.s['items'][cid('CON001')]=98; e.grant_item(cid('CON001'),10)
        self.assertEqual(e.s['items'][cid('CON001')],99); row=e.s['pending_loot'][0]; self.assertEqual(row['quantity'],9)
        with self.assertRaises(RuleError): e.execute('claim_loot',key=row['pending_id'])
        e.s['items'][cid('CON001')]=95; e.execute('claim_loot',key=row['pending_id'])
        self.assertEqual(e.s['items'][cid('CON001')],99); self.assertEqual(e.s['pending_loot'][0]['quantity'],5)
        e.execute('discard_loot',key=row['pending_id']); self.assertFalse(e.s['pending_loot'])
        e.grant_item(cid('MAT001'),1001); self.assertEqual(e.s['items'][cid('MAT001')],999); self.assertEqual(e.s['pending_loot'][0]['quantity'],2)

    def test_full_bag_gear_preserves_roll_and_no_gold(self):
        e=self.e; e.s['items']={}
        for _ in range(30): e.award_equipment()
        gold=e.p['gold']; e.award_equipment(); row=copy.deepcopy(e.s['pending_loot'][0]); self.assertEqual(e.p['gold'],gold)
        e.execute('discard',key=e.s['bag'][0]); e.execute('claim_loot',key=row['pending_id'])
        self.assertEqual(e.s['inventory'][row['equipment']['instance_id']],row['equipment']); self.assertFalse(e.s['pending_loot'])

    def test_auto_smallest_available_heal(self):
        e=self.e; e.s['items']={cid('CON004'):1,cid('CON002'):1,cid('CON013'):5}
        self.assertEqual(e.automatic_potion(),cid('CON002')); e.s['items'][cid('CON002')]=0
        self.assertEqual(e.automatic_potion(),cid('CON004'))

    def test_consumable_context_and_exploration_turn(self):
        e=self.e; before=copy.deepcopy(e.s)
        with self.assertRaises(RuleError): e.execute('use',key=cid('CON001'))
        self.assertEqual(e.s,before); e.execute('enter'); turn=e.s['turn']; progress=e.s['progress']; e.p['hp']=10
        e.execute('use',key=cid('CON001')); self.assertEqual(e.p['hp'],60); self.assertEqual(e.s['turn'],turn+1); self.assertEqual(e.s['progress'],progress)
        e.s['items'][cid('CON018')]=1; turn=e.s['turn']; e.execute('use',key=cid('CON018')); self.assertEqual(e.s['turn'],turn)
        self.assertEqual(e.s['exploration_bonuses']['treasure_pp'],10)

    def test_all_consumables_execute(self):
        for number in range(1,21):
            with self.subTest(number=number):
                e=GameEngine(ROOT/'content',seed=1); e.execute('enter'); key=cid(f'CON{number:03}'); e.s['items'][key]=1; e.p['hp']=20; e.p['mp']=0
                e.execute('use',key=key); self.assertEqual(e.s['items'][key],0)
                self.assertEqual(e.s['mode'],'base' if number==17 else 'explore')

    def test_all_effects_both_sides_expire(self):
        for side in ('player','enemy'):
            for number in range(1,16):
                with self.subTest(side=side,number=number):
                    e=GameEngine(ROOT/'content',seed=1); e.execute('enter'); e.start_combat(); e.s['enemy'].update(hp=1000,max_hp=1000)
                    self.assertTrue(e.apply_status(number,side,side,chance=1)); self.assertEqual(e.actor_statuses(side)[0]['effect_number'],number)
                    for _ in range(6): e.s['turn']+=1; e.tick_start(side); e.tick_end(side)
                    self.assertFalse(any(st.get('effect_number')==number for st in e.actor_statuses(side)))

    def test_dot_stack_damage_and_lethal(self):
        e=self.combat()
        for _ in range(5): e.apply_status(1,'player','player',1)
        self.assertEqual(e.s['statuses'][0]['stacks'],3); e.s['turn']+=1; e.tick_end('player'); self.assertEqual(e.p['hp'],91)
        e.p['hp']=1; e.execute('defend'); self.assertEqual(e.s['mode'],'base'); self.assertEqual(e.s['stats']['deaths'],1)

    def test_burn_and_bleed_damage(self):
        e=self.combat(); e.apply_status(2,'enemy','player',1); e.apply_status(3,'enemy','player',1)
        before=e.s['enemy']['hp']; e.s['turn']+=1; e.tick_end('enemy')
        self.assertEqual(before-e.s['enemy']['hp'],1+200)

    def test_cc_skips_one_action_and_grants_immunity(self):
        e=self.combat(); e.apply_status(4,'player','enemy',1); mp=e.p['mp']; hp=e.s['enemy']['hp']
        e.execute('skill',key='base.skill.strike'); self.assertEqual(e.p['mp'],mp); self.assertEqual(e.s['enemy']['hp'],hp)
        self.assertFalse(e.apply_status(4,'player','enemy',1)); e.execute('attack'); self.assertLess(e.s['enemy']['hp'],hp)

    def test_enemy_cc_skips_exactly_once(self):
        e=self.combat(); e.apply_status(5,'enemy','player',1); hp=e.p['hp']; e.counter(); self.assertEqual(e.p['hp'],hp)
        self.assertFalse(any(st.get('effect_number')==5 for st in e.s['enemy']['statuses'])); e.s['turn']+=1; e.counter(); self.assertLess(e.p['hp'],hp)

    def test_silence_rejection_is_atomic(self):
        e=self.combat(); e.apply_status(6,'player','enemy',1); old=copy.deepcopy(e.s)
        with self.assertRaises(RuleError): e.execute('skill',key='base.skill.strike')
        self.assertEqual(old,e.s); e.execute('attack'); self.assertEqual(e.s['turn'],1)

    def test_cures_preserve_positive_effects(self):
        e=self.combat()
        for n in (1,2,7,9,10): e.apply_status(n,'player','player',1)
        e.s['items'][cid('CON016')]=1; e.execute('use',key=cid('CON016'))
        self.assertEqual([s['effect_number'] for s in e.s['statuses']],[10])

    def test_reflection_no_recursion_and_leech_cap(self):
        e=self.combat(); e.s['enemy'].update(defense=0,evasion=0); self.gear(atk=100,leech=1); e.p['hp']=20
        e.apply_status(15,'enemy','enemy',1); e.apply_status(15,'player','player',1)
        with patch.object(e.rng,'random',return_value=.1),patch.object(e.rng,'uniform',return_value=1):
            damage=e.direct_hit('player',accuracy=2)
        self.assertEqual(e.p['hp'],20+math.floor(damage*.25)-math.floor(damage*.1)); self.assertEqual(e.s['stats']['damage'],damage)

    def test_enemy_regeneration_and_player_regeneration(self):
        e=self.combat(); e.apply_status(14,'enemy','enemy',1); e.s['enemy']['hp']=100
        e.tick_start('enemy'); self.assertEqual(e.s['enemy']['hp'],100)
        e.s['turn']+=1; e.tick_start('enemy'); self.assertEqual(e.s['enemy']['hp'],500)
        self.gear(hp_regen=.1,mp_regen=.2); e.p.update(hp=10,mp=0); e.tick_start('player'); self.assertEqual((e.p['hp'],e.p['mp']),(20,6))

    def test_pattern_sequence_and_phase2(self):
        e=self.combat(); e.s['enemy'].update(pattern=['defend','attack','special'],effect_id='EF010',phase2=False,phase2_hp_pct=40,phase2_multiplier=1.25,hp=3000)
        e.counter(); self.assertTrue(e.s['enemy']['guard']); self.assertTrue(e.s['enemy']['phase2'])
        e.counter(); self.assertFalse(e.s['enemy']['guard']); e.counter()
        self.assertEqual(e.s['enemy']['pattern_index'],3); self.assertEqual(e.s['enemy']['statuses'][0]['effect_number'],10)

    def test_basic_pattern_effect_not_silently_skipped(self):
        e=self.combat(); e.s['enemy'].update(effect_id='EF007')
        with patch.object(e.rng,'random',return_value=0): e.counter()
        self.assertEqual(e.s['statuses'][0]['effect_number'],7)

    def test_enemy_silence_prevents_special(self):
        e=self.combat(); e.s['enemy'].update(pattern=['special'],effect_id='EF010'); e.apply_status(6,'enemy','player',1)
        e.counter(); self.assertFalse(any(st.get('effect_number')==10 for st in e.s['enemy']['statuses']))

    def test_saved_malformed_pattern_rejected(self):
        e=self.combat(); e.s['enemy']['pattern_index']=-1
        with self.assertRaises(ValueError): SaveManager.validate(e.s)

    def test_pity_and_boss_material(self):
        e=self.e; e.s['elite_misses']=10; e.start_combat('elite')
        with patch.object(e.rng,'random',return_value=.99): e.victory()
        self.assertEqual(e.s['elite_misses'],0); self.assertEqual(e.s['stats']['equipment'],1)
        e.s['floor']=10; e.start_combat('boss'); e.victory(); self.assertEqual(e.s['items'][cid('MAT018')],1)
        self.assertEqual(e.s['items'][cid('MAT016')],3)

    def test_shield_reduces_damage_and_resets(self):
        e=self.e; self.gear(shield=.5); e.start_combat(); self.assertEqual(e.p['shield'],50)
        e.s['enemy'].update(atk=10,accuracy=2)
        with patch.object(e.rng,'random',return_value=.5): e.direct_hit('enemy',accuracy=2)
        self.assertEqual(e.p['hp'],100); self.assertLess(e.p['shield'],50)
        e.victory(); self.assertEqual(e.p['shield'],0)

    def test_save_old_snapshots_all_slots_and_pending(self):
        folder=ROOT/'artifacts/tests/migration'; store=SaveManager(folder)
        for slot,mode in enumerate(('base','combat','event'),1):
            old=LegacyEngine(ROOT/'content',seed=1); old.execute('buy',key='base.equipment.0'); old.s['items']['base.item.hp']=120
            if mode=='combat': old.execute('enter'); old.start_combat(); old.execute('defend')
            if mode=='event': old.s.update(mode='event',event=copy.deepcopy(old.content['events'][0]))
            original=copy.deepcopy(old.s); store.save(slot,old.s); saved_bytes=store.path(slot).read_bytes()
            loaded=store.load(slot); new=GameEngine(ROOT/'content',loaded)
            self.assertEqual(new.s['inventory'],original['inventory']); self.assertEqual(new.s['enemy'],original['enemy']); self.assertEqual(new.s['event'],original['event'])
            self.assertEqual(new.s['items']['base.item.hp'],99); self.assertEqual(new.s['pending_loot'][0]['quantity'],21)
            self.assertEqual(store.path(slot).read_bytes(),saved_bytes); self.assertTrue(store.path(slot).with_suffix('.json.pre-v2.bak').exists())
            store.save(slot,new.s); clone=GameEngine(ROOT/'content',store.load(slot)); self.assertEqual(clone.s['pending_loot'],new.s['pending_loot'])
            if mode=='combat':
                new.s['enemy'].update(hp=1,evasion=-1); new.execute('attack'); self.assertFalse(new.s['legacy_pending'])
            if mode=='event': new.execute('event',index=1); self.assertFalse(new.s['legacy_pending'])

    def test_migration_failure_preserves_original(self):
        store=SaveManager(ROOT/'artifacts/tests/migration_failure'); old=LegacyEngine(ROOT/'content',seed=1); store.save(1,old.s); original=store.path(1).read_bytes()
        with patch('core.migrations.migrate_v1_to_v2',side_effect=ValueError('forced migration failure')):
            with self.assertRaises(ValueError): store.load(1)
        self.assertEqual(store.path(1).read_bytes(),original)

    def test_state_roundtrip_with_statuses_pattern_and_pending(self):
        e=self.combat(); e.apply_status(1,'player','enemy',1); e.grant_item(cid('CON001'),110); e.execute('defend')
        clone=GameEngine(ROOT/'content',json.loads(json.dumps(e.s))); e.execute('attack'); clone.execute('attack')
        self.assertEqual(e.s,clone.s)

    def test_unowned_starter_items_not_added_on_load(self):
        e=self.e; e.s['items']={}; clone=GameEngine(ROOT/'content',e.s); self.assertEqual(clone.s['items'],{})

    def test_event_receipt_blocks_progress_and_survives_save(self):
        e=self.e; e.s.update(mode='event',event=copy.deepcopy(e.content['events'][0])); e.execute('event',index=1)
        self.assertIn('지나갔습니다',e.s['event_result']['text']); old=copy.deepcopy(e.s); rng=e.rng.getstate()
        for action in ('event','explore','return','buy'):
            with self.assertRaises(RuleError): e.execute(action)
            self.assertEqual(old,e.s); self.assertEqual(rng,e.rng.getstate())
        store=SaveManager(ROOT/'artifacts/tests/event_result'); store.save(1,e.s)
        restored=GameEngine(ROOT/'content',store.load(1)); self.assertEqual(restored.s['event_result'],e.s['event_result'])
        turn=restored.s['turn']; gold=restored.p['gold']; rng=restored.rng.getstate()
        restored.execute('continue_event'); self.assertIsNone(restored.s['event_result'])
        self.assertEqual((turn,gold,rng),(restored.s['turn'],restored.p['gold'],restored.rng.getstate()))
        with self.assertRaises(RuleError): restored.execute('continue_event')

    def test_event_reward_battle_and_death_wait_for_confirmation(self):
        for effect,mode in [({'type':'grant_gold','value':35},'explore'),({'type':'start_combat'},'combat'),({'type':'hurt','value':1000},'base')]:
            e=GameEngine(ROOT/'content',seed=1); event=copy.deepcopy(e.content['events'][0]); event['options'][0]['outcomes']=[dict(weight=1,effects=[effect])]
            e.s.update(mode='event',event=event); e.execute('event',index=0)
            self.assertEqual(e.s['mode'],mode); self.assertTrue(e.s['event_result']['text'])
            if mode=='explore': self.assertIn('35 G를 얻었습니다',e.s['event_result']['text'])
            before=copy.deepcopy(e.s); e.execute('continue_event'); before['event_result']=None; self.assertEqual(before,e.s)

    def test_old_battle_keeps_old_evasion_cap_until_completion(self):
        old=LegacyEngine(ROOT/'content',seed=7); old.execute('buy',key='base.equipment.0'); key=old.s['bag'][0]
        old.s['inventory'][key]['rolled_stats']={'evasion':.7}; old.execute('equip',key=key)
        old.execute('enter'); old.start_combat(); old.execute('defend'); new=GameEngine(ROOT/'content',old.s)
        self.assertEqual(old.derived()['evasion'],new.derived()['evasion'])
        old.execute('defend'); new.execute('defend'); self.assertEqual(old.p['hp'],new.p['hp'])
        new.s.update(mode='explore',enemy=None,legacy_pending=False); self.assertEqual(new.derived()['evasion'],.45)

if __name__=='__main__': unittest.main()
