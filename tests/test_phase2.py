import copy
import json
import math
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.game_engine import GameEngine, RuleError
from core.save_manager import SaveManager
from core.phase2_content import validate_phase2

ROOT=Path(__file__).resolve().parents[1]
def sid(n): return f'phase2.skill.SKL{n:03}'
def eid(n): return f'phase2.event.EVT{n:03}'


class Phase2Tests(unittest.TestCase):
    def engine(self): return GameEngine(ROOT/'content',seed=20261016)

    def combat(self):
        e=self.engine(); e.p['level']=30; e.p['attributes']['int']=100
        for skill in e.content['skills']:
            if skill.get('phase2'): e.s['skills'][skill['id']]=1
        e.execute('enter'); e.start_combat(); e.p['mp']=e.derived()['mp']
        e.s['enemy'].update(hp=100000,max_hp=100000,atk=1,defense=0,evasion=0,accuracy=0,pattern=['defend'],on_hit_effects=[],effect_id=None)
        return e

    def event(self,n):
        e=self.engine(); e.p.update(level=100,gold=100000,hp=80,mp=10)
        e.s.update(mode='event',floor=20,highest=20,progress=0,event=copy.deepcopy(e.content.by_id[eid(n)]))
        e.s['items']['catalogue.v3.CON013']=2
        return e

    def reject(self,e,action,**args):
        old=copy.deepcopy(e.s); rng=e.rng.getstate()
        with self.assertRaises(RuleError): e.execute(action,**args)
        self.assertEqual(old,e.s); self.assertEqual(rng,e.rng.getstate())

    def test_pack_and_starting_state(self):
        e=self.engine(); self.assertFalse(e.content.errors)
        self.assertEqual((len(e.content['skills']),len(e.content['events'])),(13,30))
        self.assertEqual(e.s['game_version'],'1.2.0'); self.assertEqual(e.s['save_schema_version'],3)
        for r in e.content['skills']:
            self.assertEqual(e.s['skills'][r['id']],0 if r.get('phase2') else 1)
            if r['kind']=='active': self.assertEqual(e.s['skill_auto'][r['id']]['enabled'],not r.get('phase2',False))

    def test_all_skills_learn_and_upgrade_without_healing(self):
        e=self.engine(); e.p.update(level=30,skill_points=40,hp=50,mp=10)
        for n in (3,4,6,9,13,16,48,49):
            for level in range(1,6):
                e.execute('upgrade_skill',key=sid(n)); self.assertEqual(e.s['skills'][sid(n)],level)
                self.assertEqual((e.p['hp'],e.p['mp']),(50,10))
            self.reject(e,'upgrade_skill',key=sid(n))
        self.assertEqual(e.p['skill_points'],0)

    def test_unlock_and_point_failures_atomic(self):
        e=self.engine(); e.p['skill_points']=1; self.reject(e,'upgrade_skill',key=sid(3))
        e.p['level']=5; e.p['skill_points']=0; self.reject(e,'upgrade_skill',key=sid(3))
        e.p['skill_points']=1; e.execute('upgrade_skill',key=sid(3)); self.assertEqual(e.s['skills'][sid(3)],1)

    def test_skill_rejections_atomic(self):
        for reason in ('unlearned','locked','mp','silence','cooldown','legacy'):
            with self.subTest(reason=reason):
                e=self.combat()
                if reason=='unlearned': e.s['skills'][sid(3)]=0
                if reason=='locked': e.p['level']=1
                if reason=='mp': e.p['mp']=0
                if reason=='silence': e.s['statuses']=[dict(effect_number=6,turns=2,applied_at=0)]
                if reason=='cooldown': e.s['skill_cooldowns'][sid(3)]=1
                if reason=='legacy': e.s['phase2_legacy_combat']=True
                self.assertTrue(e.skill_reason(sid(3))); self.reject(e,'skill',key=sid(3))

    def test_cooldown_includes_blocked_turn_not_use_turn(self):
        e=self.combat(); e.execute('skill',key=sid(4)); self.assertEqual(e.s['skill_cooldowns'][sid(4)],2)
        self.reject(e,'skill',key=sid(4)); mp=e.p['mp']
        e.s['statuses']=[dict(effect_number=4,turns=1,applied_at=-1)]
        e.execute('skill',key=sid(3)); self.assertEqual(e.p['mp'],mp); self.assertNotIn(sid(3),e.s['skill_cooldowns'])
        self.assertEqual(e.s['skill_cooldowns'][sid(4)],1)
        e.execute('defend'); self.assertNotIn(sid(4),e.s['skill_cooldowns']); e.execute('skill',key=sid(4))

    def test_attack_buff_three_subsequent_actions(self):
        e=self.combat(); normal=e.derived()['atk']; e.execute('skill',key=sid(16))
        self.assertEqual(e.derived()['atk'],math.floor(normal*1.15)); self.assertEqual(e.s['skill_buffs'][sid(16)]['remaining'],3)
        for left in (2,1): e.execute('defend'); self.assertEqual(e.s['skill_buffs'][sid(16)]['remaining'],left)
        e.execute('defend'); self.assertEqual(e.derived()['atk'],normal)

    def test_reduction_two_enemy_actions_and_separate_multiplier(self):
        e=self.combat(); e.execute('skill',key=sid(6)); self.assertEqual(e.s['skill_buffs'][sid(6)]['remaining'],1)
        e.execute('defend'); self.assertNotIn(sid(6),e.s['skill_buffs'])
        e.s['enemy'].update(atk=100,accuracy=2); e.p['guard']=False
        stats=dict(e.derived()); stats.update(defense=0,evasion=0,reduction=.5,skill_reduction=.2,counter=0,reflect=0)
        enemy=dict(e.enemy_stats()); enemy.update(crit=0)
        with patch.object(e,'stats_for',side_effect=lambda side: stats if side=='player' else enemy),patch.object(e.rng,'uniform',return_value=1),patch.object(e.rng,'random',return_value=.5):
            before=e.p['hp']; e.direct_hit('enemy'); self.assertEqual(before-e.p['hp'],40)

    def test_damage_penetration_and_execute_boundary(self):
        e=self.combat(); e.s['enemy']['defense']=50
        with patch.object(e.rng,'random',return_value=.5),patch.object(e.rng,'uniform',return_value=1):
            before=e.s['enemy']['hp']; e.effects(e.content.by_id[sid(3)]['effects']); self.assertEqual(before-e.s['enemy']['hp'],max(1,math.floor(e.derived()['atk']*1.5-50*.6*.6)))
            e.s['enemy'].update(defense=0,hp=30000)
            before=e.s['enemy']['hp']; e.effects(e.content.by_id[sid(4)]['effects']); self.assertEqual(before-e.s['enemy']['hp'],math.floor(e.derived()['atk']*1.6*1.5-.6*e.enemy_stats()['defense']))
            e.s['enemy']['hp']=30001; before=e.s['enemy']['hp']; e.effects(e.content.by_id[sid(4)]['effects']); self.assertEqual(before-e.s['enemy']['hp'],math.floor(e.derived()['atk']*1.6-.6*e.enemy_stats()['defense']))

    def test_shield_refresh_and_cleanse(self):
        e=self.combat(); e.p['shield']=30; e.effects(e.content.by_id[sid(9)]['effects']); self.assertEqual(e.p['shield'],30)
        e.p['shield']=5; e.effects(e.content.by_id[sid(9)]['effects']); self.assertEqual(e.p['shield'],20)
        e.p['hp']=50; e.s['statuses']=[dict(effect_number=n,turns=3,applied_at=0,source_atk=10) for n in (1,2,3,6)]
        e.effects(e.content.by_id[sid(13)]['effects']); self.assertEqual(e.p['hp'],65); self.assertEqual([s['effect_number'] for s in e.s['statuses']],[6])

    def test_passives_and_repeated_reset_no_exploit(self):
        e=self.engine(); e.p.update(level=30,skill_points=12,hp=90,mp=20)
        for key in (sid(48),sid(49),'base.skill.strike'):
            for _ in range(2): e.execute('upgrade_skill',key=key)
        self.assertEqual((e.derived()['hp'],e.derived()['mp']),(106,32)); e.p['hp']=106; e.p['mp']=32
        e.execute('reset_skills'); self.assertEqual(e.p['skill_points'],12); self.assertEqual((e.p['hp'],e.p['mp']),(100,30))
        e.execute('reset_skills'); self.assertEqual(e.p['skill_points'],12)
        e.execute('enter'); self.reject(e,'reset_skills')

    def test_auto_rules_and_priority(self):
        e=self.combat()
        for n in (3,4,6,9,13,16): e.execute('skill_auto',key=sid(n),field='priority',value=9)
        self.reject(e,'skill_auto',key=sid(3),field='priority',value=10)
        self.assertFalse(e.auto_skill_allowed(e.content.by_id[sid(4)])); e.s['enemy']['hp']=30000; self.assertTrue(e.auto_skill_allowed(e.content.by_id[sid(4)]))
        self.assertFalse(e.auto_skill_allowed(e.content.by_id[sid(13)])); e.p['hp']=50; self.assertTrue(e.auto_skill_allowed(e.content.by_id[sid(13)]))
        e.p['hp']=100; e.s['statuses']=[dict(effect_number=1,turns=2,applied_at=0)]; self.assertTrue(e.auto_skill_allowed(e.content.by_id[sid(13)]))
        e.s['statuses']=[]; e.effects(e.content.by_id[sid(16)]['effects']); self.assertFalse(e.auto_skill_allowed(e.content.by_id[sid(16)]))
        e.p['shield']=1; self.assertFalse(e.auto_skill_allowed(e.content.by_id[sid(9)]))

    def test_auto_ties_use_id_order(self):
        e=self.combat(); e.content.balance['auto_turn_limit']=1
        for key in e.s['skill_auto']: e.s['skill_auto'][key].update(enabled=key in (sid(3),sid(4)),priority=1)
        e.s['enemy']['hp']=30000; e.execute('auto'); self.assertEqual(e.s['skill_usage'],{sid(3):1})

    def test_cooldowns_and_rng_survive_reload(self):
        e=self.combat(); e.execute('skill',key=sid(16)); clone=GameEngine(ROOT/'content',json.loads(json.dumps(e.s)))
        self.assertEqual(clone.s['skill_cooldowns'],e.s['skill_cooldowns'])
        e.execute('attack'); clone.execute('attack'); self.assertEqual(e.s,clone.s)

    def test_combat_end_resets_all_skill_state(self):
        for ending in ('victory','death','flee'):
            with self.subTest(ending=ending):
                e=self.combat(); e.execute('skill',key=sid(16)); e.p['shield']=20
                if ending=='victory': e.victory()
                elif ending=='death': e.death()
                else:
                    with patch.object(e.rng,'random',return_value=0): e.execute('flee')
                self.assertEqual(e.s['skill_cooldowns'],{}); self.assertEqual(e.s['skill_buffs'],{}); self.assertEqual(e.p['shield'],0)

    def test_all_event_choices_and_outcomes(self):
        initial=self.engine(); count=0
        for event in (r for r in initial.content['events'] if r.get('phase2')):
            n=int(event['source_id'][3:])
            for index,option in enumerate(event['options']):
                for branch in range(len(option['outcomes'])):
                    with self.subTest(event=n,choice=index,branch=branch):
                        e=self.event(n); opt=e.event_option(option); outcome=opt['outcomes'][branch]
                        weighted=e.weighted
                        with patch.object(e,'weighted',side_effect=lambda rows: outcome if 'effects' in rows[0] else weighted(rows)): e.execute('event',index=index)
                        self.assertIsNone(e.s['event']); self.assertTrue(e.s['event_result']['resolved']); SaveManager.validate(e.s)
                        self.assertEqual(e.s['progress'],0 if e.s['mode']=='combat' else 1)
                        before=copy.deepcopy(e.s); self.reject(e,'event',index=index)
                        e.execute('continue_event'); self.assertEqual(e.p,before['player']); self.reject(e,'continue_event')
                        count+=1
        self.assertGreaterEqual(count,50)

    def test_event_rewards_exact(self):
        e=self.event(1); gold=e.p['gold']; e.execute('event',index=0); self.assertEqual(e.p['gold']-gold,160)
        e=self.event(22); hp=e.p['hp']; xp=e.p['exp']; e.execute('event',index=0); self.assertEqual(hp-e.p['hp'],15); self.assertEqual(e.p['exp']-xp,500)
        e=self.event(11); e.execute('event',index=1); self.assertEqual(e.p['mp'],17)
        e=self.event(7); amount=e.s['items']['catalogue.v3.CON013']; e.execute('event',index=0); self.assertEqual(e.s['items']['catalogue.v3.CON013'],amount-1); self.assertEqual(e.p['exp'],400)

    def test_event_cost_rejections_atomic(self):
        e=self.event(2); e.p['gold']=0; self.reject(e,'event',index=0)
        e=self.event(22); e.p['hp']=15; self.assertTrue(e.event_option_reason(e.s['event']['options'][0])); self.reject(e,'event',index=0)
        e=self.event(7); e.s['items']['catalogue.v3.CON013']=0; self.reject(e,'event',index=0)
        self.reject(e,'event',index=-1)

    def test_event_previews_are_readonly(self):
        e=self.event(19); state=copy.deepcopy(e.s); rng=e.rng.getstate()
        for _ in range(3):
            for option in e.s['event']['options']: e.event_option(option); e.event_option_reason(option); e.event_option_description(option)
        self.assertEqual(e.s,state); self.assertEqual(e.rng.getstate(),rng)
        opt=e.event_option(e.s['event']['options'][0]); item=e.content.by_id['catalogue.v3.'+opt['outcomes'][0]['effects'][0]['catalogue_item']]
        self.assertEqual(opt['cost'],math.floor(item['price']*.8))

    def test_event_rewards_use_pending_queue(self):
        e=self.event(2)
        for _ in range(28): e.award_equipment()
        self.assertEqual(e.bag_used(),30); e.execute('event',index=0); self.assertTrue(e.s['pending_loot'])
        e=self.event(42); e.s['items']['catalogue.v3.CON005']=99; e.execute('event',index=0)
        self.assertEqual(e.s['items']['catalogue.v3.CON005'],99); self.assertEqual(e.s['pending_loot'][-1]['quantity'],1)

    def test_event_bonuses_replace_not_stack(self):
        e=self.event(21); e.s['exploration_bonuses']['rarity_pp']=5; e.execute('event',index=0); self.assertEqual(e.s['exploration_bonuses']['rarity_pp'],5)
        e=self.event(26); e.s['exploration_bonuses']['treasure_pp']=10; e.execute('event',index=1); self.assertEqual(e.s['exploration_bonuses']['treasure_pp'],10)

    def test_event_combat_progress_once_and_result_pause(self):
        e=self.event(37); e.execute('event',index=0); self.assertEqual(e.s['progress'],0); self.reject(e,'attack')
        e.execute('continue_event'); e.s['enemy']['hp']=0; e.resolve_deaths(); self.assertEqual(e.s['progress'],1)
        self.assertIsNone(e.s['event_result']); self.assertEqual(e.s['stats']['wins'],1)

    def test_event_fatal_damage_stops_following_rewards(self):
        e=self.event(6); e.p['hp']=1; xp=e.p['exp']; e.execute('event',index=1)
        self.assertEqual(e.s['mode'],'base'); self.assertEqual(e.p['exp'],xp); self.assertTrue(e.s['event_result'])

    def test_event_unlock_cooldown(self):
        e=self.engine(); event=e.content.by_id[eid(46)]; e.s['floor']=19; self.assertFalse(e.eligible(event))
        e.s['floor']=20; self.assertTrue(e.eligible(event)); e.s['event_seen'][event['id']]=10
        for step in (10,11,12,13): e.s['stats']['explorations']=step; self.assertFalse(e.eligible(event))
        e.s['stats']['explorations']=14; self.assertTrue(e.eligible(event))

    def test_migration_backup_and_preserved_states(self):
        (ROOT/'artifacts/tests').mkdir(parents=True,exist_ok=True)
        for mode in ('base','combat','event','result','pending'):
            with self.subTest(mode=mode),tempfile.TemporaryDirectory(dir=ROOT/'artifacts/tests') as folder:
                e=self.combat() if mode=='combat' else self.engine()
                if mode=='event': e.s.update(mode='event',event=copy.deepcopy(e.content['events'][0]))
                if mode=='result': e.s['event_result']=dict(title='기존 결과',description='설명',choice='선택',text='지급 완료')
                if mode=='pending':
                    e.s['items']['catalogue.v3.CON001']=99; e.grant_item('catalogue.v3.CON001',3)
                old=copy.deepcopy(e.s); old['save_schema_version']=2
                for key in list(old['skills']):
                    if key.startswith('phase2.'): old['skills'].pop(key); old['skill_auto'].pop(key,None)
                for key in ('skill_buffs','skill_cooldowns','skill_usage','phase2_legacy_combat'): old.pop(key,None)
                store=SaveManager(folder); store.save(1,old); original=store.path(1).read_bytes()
                loaded=store.load(1); clone=GameEngine(ROOT/'content',loaded)
                self.assertEqual(store.path(1).read_bytes(),original); self.assertEqual(store.path(1).with_suffix('.json.pre-v3.bak').read_bytes(),original)
                for key in ('player','inventory','event','event_result','pending_loot'): self.assertEqual(clone.s.get(key),old.get(key))
                self.assertEqual(clone.s['phase2_legacy_combat'],mode=='combat'); self.assertEqual(clone.s['skills'][sid(3)],0)
                if mode=='combat': clone.s['skills'][sid(3)]=1; self.reject(clone,'skill',key=sid(3))
                store.save(1,clone.s); SaveManager.validate(store.load(1))

    def test_invalid_phase2_definitions_rejected(self):
        e=self.engine(); source=e.content._phase2_source; selection=e.content._phase2_selection
        for change in ('unlock','cooldown','target','duration','condition','source','reference','effect'):
            with self.subTest(change=change):
                row=copy.deepcopy(e.content.by_id[sid(6)])
                if change=='unlock': row['unlock_level']=-1
                if change=='cooldown': row['cooldown_turns']=1.5
                if change=='target': row['effects'][0]['target']='everyone'
                if change=='duration': row['effects'][0]['duration']=0
                if change=='condition': row['auto_condition']='unknown'
                if change=='source': row['source_id']='SKL999'
                if change=='reference': row['effects'][0]=dict(type='catalogue_item',value=1,catalogue_item='CON999',target='player')
                if change=='effect': row['effects'][0]['type']='execute_python'
                with self.assertRaises(ValueError): validate_phase2(row,'skills',source,selection)

    def test_corrupt_skill_save_rejected(self):
        for field,value in (('skill_cooldowns',{sid(3):-1}),('skill_buffs',{sid(6):{'kind':'attack','remaining':0}}),('phase2_legacy_combat','false')):
            e=self.engine(); e.s[field]=value
            with self.assertRaises(ValueError): SaveManager.validate(e.s)


if __name__=='__main__': unittest.main()
