import copy
import json
import shutil
import unittest
from pathlib import Path
from core.game_engine import GameEngine,RuleError
from core.save_manager import SaveManager
from core.content import Content

ROOT=Path(__file__).resolve().parents[1]

class EngineTests(unittest.TestCase):
    def setUp(self): self.e=GameEngine(ROOT/'content',seed=7)
    def combat(self,kind='normal'):
        self.e.execute('enter'); self.e.start_combat(kind)
    def test_initial_template(self):
        d=self.e.derived(); self.assertEqual([d[k] for k in ('hp','mp','atk','defense')],[100,30,15,5])
    def test_invalid_is_atomic(self):
        old=copy.deepcopy(self.e.s)
        with self.assertRaises(RuleError): self.e.execute('attack')
        self.assertEqual(old,self.e.s)
    def test_no_counter_on_kill(self):
        self.combat(); e=self.e; e.s['enemy']['hp']=1; e.s['enemy']['evasion']=-1
        hp=e.p['hp']; e.execute('attack'); self.assertEqual(e.s['mode'],'explore'); self.assertEqual(e.p['hp'],hp); self.assertEqual(e.s['progress'],1)
    def test_potion_counter(self):
        self.combat(); e=self.e; e.p['hp']=40; e.s['enemy']['accuracy']=2
        e.execute('use',key='catalogue.v3.CON001'); self.assertLess(e.p['hp'],90); self.assertEqual(e.s['turn'],1); self.assertEqual(e.s['items']['catalogue.v3.CON001'],2)
    def test_boss_gate_and_flee(self):
        e=self.e; e.s['highest']=10; e.execute('enter',floor=10); e.s['progress']=2; e.execute('explore')
        self.assertEqual(e.s['enemy']['kind'],'boss'); old=copy.deepcopy(e.s)
        with self.assertRaises(RuleError): e.execute('flee')
        self.assertEqual(e.s,old); e.s['enemy']['hp']=1; e.s['enemy']['evasion']=-1; e.execute('attack'); self.assertTrue(e.complete()); self.assertEqual(e.s['items']['catalogue.v3.MAT016'],3)
    def test_death_preserves_progression(self):
        self.combat(); e=self.e; e.p.update(hp=1,gold=205,exp=23); e.s['enemy'].update(accuracy=2,atk=100)
        e.execute('defend'); self.assertEqual(e.s['mode'],'base'); self.assertEqual(e.p['gold'],185); self.assertEqual(e.p['exp'],23); self.assertGreater(e.p['hp'],0)
    def test_level_points(self):
        e=self.e; e.gain_exp(100); self.assertEqual(e.p['level'],2); self.assertEqual(e.p['points'],3); e.execute('invest',key='vit'); self.assertEqual(e.derived()['hp'],110)
    def test_auto_danger_stops(self):
        self.combat(); e=self.e; e.p['hp']=30; turn=e.s['turn']; e.execute('auto'); self.assertEqual(e.s['turn'],turn); self.assertEqual(e.s['mode'],'combat')
    def test_equipment_identity(self):
        e=self.e; e.execute('buy',key='catalogue.v3.EQ001'); iid=e.s['bag'][0]; e.execute('equip',key=iid)
        with self.assertRaises(RuleError): e.execute('sell',key=iid)
        e.execute('unequip',key='무기'); e.execute('deposit',key=iid); e.execute('withdraw',key=iid); self.assertEqual(e.s['bag'],[iid]); self.assertEqual(len(e.s['inventory']),1)
    def test_enhance_guaranteed_then_failure(self):
        e=self.e; e.execute('buy',key='catalogue.v3.EQ001'); iid=e.s['bag'][0]; e.p['gold']=100000; e.s['items']['catalogue.v3.MAT016']=100
        for _ in range(3): e.execute('enhance',key=iid)
        item=e.s['inventory'][iid]; self.assertEqual(item['enhance'],3)
        e.rng.random=lambda: .99; before=e.p['gold']; e.execute('enhance',key=iid); self.assertEqual(item['enhance'],3); self.assertLess(e.p['gold'],before)
    def test_event_lock_and_resolution(self):
        e=self.e; e.execute('enter'); e.s['mode']='event'; e.s['event']=copy.deepcopy(e.content['events'][0]); old=copy.deepcopy(e.s)
        with self.assertRaises(RuleError): e.execute('return')
        self.assertEqual(e.s,old); e.execute('event',index=1); self.assertEqual(e.s['progress'],1)
    def test_achievement_once(self):
        e=self.e; e.s['highest']=10; e.execute('claim',key='base.achievement.0'); before=e.p['gold']
        with self.assertRaises(RuleError): e.execute('claim',key='base.achievement.0')
        self.assertEqual(e.p['gold'],before)
    def test_bag_capacity_atomic_purchase(self):
        e=self.e; e.p['gold']=100000
        for _ in range(28): e.execute('buy',key='catalogue.v3.EQ001')
        self.assertEqual(e.bag_used(),30); before=copy.deepcopy(e.s)
        with self.assertRaises(RuleError): e.execute('buy',key='catalogue.v3.MAT016')
        self.assertEqual(e.s,before)
    def test_low_floor_exp(self):
        self.combat(); e=self.e; e.p['level']=11; e.s['enemy']['hp']=1; e.s['enemy']['evasion']=-1; e.execute('attack'); self.assertEqual(e.s['last_exp'],6); self.assertEqual(e.s['last_gold'],13)
    def test_three_slots_and_corruption(self):
        folder=ROOT/'artifacts/tests/save'; folder.mkdir(parents=True,exist_ok=True); store=SaveManager(folder); self.combat(); e=self.e
        for slot in (1,2,3):
            store.save(slot,e.s); loaded=store.load(slot); clone=GameEngine(ROOT/'content',loaded); self.assertEqual(clone.s['enemy'],e.s['enemy'])
        store.save(1,e.s); store.path(1).write_text('{bad',encoding='utf-8'); loaded=store.load(1); self.assertEqual(loaded['mode'],'combat'); self.assertTrue(store.notice); self.assertTrue(store.path(1).with_suffix('.json.corrupt').exists())
    def test_rng_resume(self):
        self.combat(); e=self.e; e.execute('defend'); clone=GameEngine(ROOT/'content',json.loads(json.dumps(e.s)))
        e.execute('attack'); clone.execute('attack'); self.assertEqual(json.dumps(e.s,sort_keys=True),json.dumps(clone.s,sort_keys=True))
    def test_all_events_resolve(self):
        for event in self.e.content['events']:
            for index in range(len(event['options'])):
                e=GameEngine(ROOT/'content',seed=index); e.execute('enter'); e.s.update(mode='event',event=copy.deepcopy(event)); e.execute('event',index=index); self.assertIn(e.s['mode'],('base','explore','combat'))
    def test_all_skills(self):
        for skill in self.e.content['skills']:
            e=GameEngine(ROOT/'content',seed=1); e.p['skill_points']=1; e.execute('upgrade_skill',key=skill['id']); self.assertEqual(e.s['skills'][skill['id']],2)
            if skill['kind']=='active': e.execute('enter'); e.start_combat(); e.execute('skill',key=skill['id']); self.assertEqual(e.p['mp'],30-skill['mp'])
    def test_unknown_equipment_preserved(self):
        e=self.e; e.execute('buy',key='catalogue.v3.EQ001'); iid=e.s['bag'][0]; e.s['inventory'][iid]['base_id']='missing.item'; old=copy.deepcopy(e.s)
        with self.assertRaises(RuleError): e.execute('equip',key=iid)
        self.assertEqual(e.s,old)
    def test_content_invalid_pack_isolated(self):
        root=ROOT/'artifacts/tests/content'; shutil.copytree(ROOT/'content/base',root/'base',dirs_exist_ok=True)
        pack=root/'packs/bad'; pack.mkdir(parents=True,exist_ok=True)
        (pack/'manifest.json').write_text(json.dumps(dict(pack_id='bad',version='1',schema_version=1,dependencies=['base'],content_files=['monsters.json'])),encoding='utf-8')
        (pack/'monsters.json').write_text(json.dumps([{'id':'base.monster.slime'}]),encoding='utf-8')
        content=Content(root); self.assertEqual(len(content['monsters']),8); self.assertEqual(len(content.errors),1)
    def test_save_additive_defaults(self):
        state=copy.deepcopy(self.e.s); del state['event_seen']; del state['settings']['stop_danger']; state['inventory']['legacy']={'opaque':'preserve'}
        restored=GameEngine(ROOT/'content',state); self.assertTrue(restored.s['settings']['stop_danger']); self.assertEqual(restored.s['inventory']['legacy'],{'opaque':'preserve'})
    def test_event_conditions(self):
        e=self.e
        self.assertFalse(e.eligible({'min_floor':20})); self.assertTrue(e.eligible({'conditions':[{'type':'gold_at_least','value':200}]}))
        self.assertFalse(e.eligible({'conditions':[{'type':'boss_defeated','value':10}]}))
        e.s['boss_first']=[10]; self.assertTrue(e.condition({'type':'boss_defeated','value':10}))
    def test_invalid_settings_rejected(self):
        old=copy.deepcopy(self.e.s)
        with self.assertRaises(RuleError): self.e.execute('setting',key='font_size',value=1000)
        self.assertEqual(old,self.e.s)
    def test_shop_preview_matches_generation_range(self):
        e=self.e; old=copy.deepcopy(e.s); rng=e.rng.getstate()
        self.assertIn('HP 50 회복',e.shop_description('catalogue.v3.CON001')); self.assertIn('강화',e.shop_description('catalogue.v3.MAT016'))
        for base in e.content['equipment']:
            text=e.shop_description(base['id']); self.assertIn('장비 레벨 1~3',text)
        self.assertEqual(old,e.s); self.assertEqual(rng,e.rng.getstate())
        for base in e.content['equipment']:
            minimum=e.equipment_base_stats(base,1); maximum=e.equipment_base_stats(base,3)
            for _ in range(20):
                item=e.generate_equipment(base['id'])
                for stat,value in item['rolled_stats'].items(): self.assertTrue(minimum[stat]<=value<=maximum[stat])

if __name__=='__main__': unittest.main()
