"""Seeded phase-two build comparison. Never opens the user's saves directory."""
import collections
import json
from pathlib import Path

from core.game_engine import GameEngine, RuleError, SLOTS
from core.catalogue import cid
from core.save_manager import SaveManager

ROOT=Path(__file__).resolve().parents[1]
BUILDS={'attack':(3,4),'defense':(6,9),'recovery':(13,49)}


class AuditEngine(GameEngine):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.potions=0; self.death_floors=[]; self.finished_turns=[]

    def consume(self,key):
        result=super().consume(key)
        if self.content.by_id[key].get('use_number',99)<=8: self.potions+=1
        return result

    def death(self):
        self.death_floors.append(self.s['floor']); return super().death()

    def battle(self,action,key=None):
        result=super().battle(action,key)
        if self.s['mode']!='combat': self.finished_turns.append(self.s['combat_turn'])
        return result


def invest_skills(e,build):
    keys=[f'phase2.skill.SKL{n:03}' for n in BUILDS[build]]
    while e.p['skill_points']:
        candidates=[k for k in keys if not e.skill_reason(k,learning=True)]
        if not candidates: break
        key=min(candidates,key=lambda k:(e.s['skills'][k],keys.index(k)))
        e.execute('upgrade_skill',key=key)
    for key in e.s['skill_auto']:
        if key.startswith('phase2.'):
            e.execute('skill_auto',key=key,field='enabled',value=key in keys)
        e.execute('skill_auto',key=key,field='priority',value=1 if key in keys else 9)


def report(e):
    total=sum(e.s.get('skill_usage',{}).values())
    return dict(highest=e.s['highest'],level=e.p['level'],battles=e.s['stats']['battles'],wins=e.s['stats']['wins'],
                win_rate=e.s['stats']['wins']/max(1,e.s['stats']['battles']),
                mean_finished_combat_turns=sum(e.finished_turns)/max(1,len(e.finished_turns)),
                potions_used=e.potions,deaths=e.s['stats']['deaths'],death_floors=dict(collections.Counter(e.death_floors)),
                skills=e.s['skills'],skill_uses=e.s['skill_usage'],
                skill_usage_share={k:v/max(1,total) for k,v in e.s['skill_usage'].items()},
                skill_uses_per_player_combat_action=total/max(1,sum(e.finished_turns)+(e.s['combat_turn'] if e.s['mode']=='combat' else 0)))


def progression(build):
    e=AuditEngine(ROOT/'content',seed=20261016)
    for _ in range(3000):
        if e.s.get('event_result'): e.execute('continue_event')
        mode=e.s['mode']
        if mode=='base':
            for key in e.s['bag'][:]:
                item=e.s['inventory'][key]; old=e.s['equipped'].get(item['slot'])
                if not old or sum(e.gear_stats(item).values())>sum(e.gear_stats(e.s['inventory'][old]).values()): e.execute('equip',key=key)
            for key in e.s['bag'][:]: e.execute('sell',key=key)
            for key,quantity in list(e.s['items'].items()):
                if quantity and e.content.by_id[key]['category']=='재료': e.execute('sell',key=key,quantity=quantity)
            for row in e.s['pending_loot'][:]:
                try: e.execute('claim_loot',key=row['pending_id'])
                except RuleError: break
            while e.p['points']: e.execute('invest',key='vit' if e.p['points']%3==0 else 'str')
            invest_skills(e,build)
            for resource in ('hp','mp'):
                if e.p[resource]<e.derived()[resource]:
                    try: e.execute('rest',key=resource)
                    except RuleError: pass
            if not e.s['equipped'].get('무기') and e.p['gold']>=e.content.by_id[cid('EQ001')]['price']:
                e.execute('buy',key=cid('EQ001')); e.execute('equip',key=e.s['bag'][-1])
            if e.s['items'].get(cid('CON001'),0)<3 and e.p['gold']>=60:
                try: e.execute('buy',key=cid('CON001'),quantity=3)
                except RuleError: pass
            e.execute('enter',floor=max(1,e.s['highest']-1 if e.s['stats']['deaths'] else e.s['highest']))
        elif mode=='combat':
            if e.p['hp']/e.derived()['hp']<=.3 and e.s['enemy']['kind']!='boss': e.execute('flee')
            else:
                turn=e.s['turn']; e.execute('auto')
                if e.s['mode']=='combat' and turn==e.s['turn']: e.execute('attack')
        elif mode=='event':
            index=next(i for i,o in enumerate(e.s['event']['options']) if not e.event_option_reason(o)); e.execute('event',index=index)
        elif e.p['hp']<e.derived()['hp']*.6 or e.bag_used()>=28 or e.p['points']: e.execute('return')
        elif e.complete(): e.execute('next')
        else: e.execute('explore')
        SaveManager.validate(e.s)
        assert e.p['gold']>=0 and e.bag_used()<=30
    return dict(decisions=3000,**report(e))


def encounters(build):
    rows=[]
    for floor in (10,30,50,100,101,200):
        totals=collections.Counter(); skills=collections.Counter(); deaths=collections.Counter()
        for trial in range(50):
            e=AuditEngine(ROOT/'content',seed=floor*1000+trial); level=max(30,floor//2)
            e.s.update(floor=floor,highest=floor); e.p.update(level=level,skill_points=level//5,gold=10000)
            points=3*(level-1); e.p['attributes']['str']+=points*3//5; e.p['attributes']['vit']+=points-points*3//5
            invest_skills(e,build)
            for slot in SLOTS:
                base=max((r for r in e.content['equipment'] if r['slot']==slot and r['min_floor']<=floor),key=lambda r:r['min_floor'])
                gear=e.generate_equipment(base['id']); gear['enhance']=3; key=gear['instance_id']; e.s['inventory'][key]=gear; e.s['equipped'][slot]=key
            e.p.update(hp=e.derived()['hp'],mp=e.derived()['mp']); e.s['items']={cid('CON004'):20,cid('CON008'):10}
            e.s['settings']['stop_danger']=False; e.start_combat('boss' if floor%10==0 else 'normal'); e.execute('auto'); SaveManager.validate(e.s)
            totals.update(wins=e.s['stats']['wins'],deaths=e.s['stats']['deaths'],turns=e.s['combat_turn'],potions=e.potions,stalled=int(e.s['mode']=='combat'))
            skills.update(e.s['skill_usage']); deaths.update(e.death_floors)
        uses=sum(skills.values())
        rows.append(dict(floor=floor,trials=50,win_rate=totals['wins']/50,mean_combat_turns=totals['turns']/50,potions_used=totals['potions'],deaths=totals['deaths'],death_floors=dict(deaths),stalled=totals['stalled'],skill_uses=dict(skills),skill_usage_share={k:v/max(1,uses) for k,v in skills.items()},skill_uses_per_player_combat_action=uses/max(1,totals['turns'])))
    return rows


def run():
    results=dict(seed=20261016,fixture='Same seeds and gear per build; level=max(30,floor//2), earned skill points=level//5, STR/VIT=60/40, gear +3, 20 CON004/10 CON008; auto danger stop disabled only in encounter fixtures.',builds={})
    for build in BUILDS:
        print('Simulating '+build,flush=True)
        results['builds'][build]=dict(progression=progression(build),encounters=encounters(build))
        print(build+' complete',flush=True)
    (ROOT/'artifacts/phase2_build_simulation.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Saved artifacts/phase2_build_simulation.json',flush=True)


if __name__=='__main__': run()
