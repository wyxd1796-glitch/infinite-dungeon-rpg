"""Reproducible gameplay and distribution checks; writes measured results."""
import json
from collections import Counter
from pathlib import Path
from core.legacy_engine import GameEngine,RuleError

ROOT=Path(__file__).resolve().parents[1]
def run():
    result={}
    e=GameEngine(ROOT/'content',seed=20261015)
    counts=Counter(e.generate_equipment()['rarity'] for _ in range(10000))
    result['rarity_10000']=dict(counts)
    for name,expected in e.content.balance['rarities'].items():
        assert abs(counts[name]/100-expected)<2,(name,counts)
    e=GameEngine(ROOT/'content',seed=100)
    e.execute('buy',key='base.equipment.0'); e.execute('equip',key=e.s['bag'][0]); e.execute('enter')
    for step in range(3000):
        s=e.s; p=e.p; mode=s['mode']
        if mode=='combat':
            if p['hp']<e.derived()['hp']*.5 and s['items'].get('base.item.hp',0)>0: e.execute('use',key='base.item.hp')
            elif p['mp']>=8: e.execute('skill',key='base.skill.strike')
            else: e.execute('attack')
        elif mode=='event':
            options=s['event']['options']; index=next((i for i,o in enumerate(options) if not o['cost'] and not o['outcomes'][0]['effects']),0)
            if p['gold']<options[index]['cost']: index=len(options)-1
            e.execute('event',index=index)
        else:
            if p['points']:
                e.execute('invest',key='vit' if p['attributes']['str']>p['attributes']['vit']*1.8 else 'str'); continue
            if p['skill_points']:
                skill=next((r for r in e.content['skills'] if s['skills'][r['id']]<5),None)
                if skill: e.execute('upgrade_skill',key=skill['id']); continue
            if mode=='base':
                for iid in list(s['bag']):
                    item=s['inventory'][iid]; current=s['equipped'].get(item['slot'])
                    if not current or sum(e.gear_stats(item).values())>sum(e.gear_stats(s['inventory'][current]).values()): e.execute('equip',key=iid)
                for iid in list(s['bag']): e.execute('sell',key=iid)
                for resource in ('hp','mp'):
                    cost=e.content.balance['rest_'+resource]*p['level']
                    if p[resource]<e.derived()[resource] and p['gold']>=cost: e.execute('rest',key=resource)
                if s['items'].get('base.item.hp',0)<3 and p['gold']>=30: e.execute('buy',key='base.item.hp')
                e.execute('enter',floor=max(1,s['highest']-int(p['hp']<e.derived()['hp']*.5)))
            elif p['hp']<e.derived()['hp']*.4: e.execute('return')
            elif e.complete(): e.execute('next')
            else: e.execute('explore')
        assert 0<=p['hp']<=e.derived()['hp'] and p['gold']>=0
        assert e.bag_used()<=30
        ids=s['bag']+s['storage']+list(s['equipped'].values()); assert len(ids)==len(set(ids))
    result['gameplay_3000_commands']={'highest':e.s['highest'],'level':e.p['level'],'gold':e.p['gold'],**e.s['stats']}
    result['scaling']={}
    for floor in (10,20,50,100,500,10000):
        e=GameEngine(ROOT/'content',seed=4); e.s['floor']=floor; e.start_combat('boss'); result['scaling'][floor]={k:e.s['enemy'][k] for k in ('hp','atk','defense')}; assert e.s['enemy']['hp']>0
    (ROOT/'artifacts/simulation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__': run()
