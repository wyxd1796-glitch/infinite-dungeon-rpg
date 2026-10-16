"""Reproducible catalogue/economy audit; writes only under artifacts/."""
import collections
import json
import math
import random
from pathlib import Path
from core.game_engine import GameEngine, RuleError, SLOTS
from core.catalogue import cid
from core.save_manager import SaveManager

ROOT=Path(__file__).resolve().parents[1]

def run(output=None):
    e=GameEngine(ROOT/'content',seed=20261016); e.s['floor']=100
    gear_counts=collections.Counter(); rarities=collections.Counter(); option_counts=collections.Counter()
    for _ in range(100000):
        item=e.generate_equipment(); base=e.content.by_id[item['base_id']]
        assert base['min_floor']<=100 and item['slot']==base['slot']
        ids=[a['id'] for a in item['affixes']]; assert len(ids)==len(set(ids))
        for affix in item['affixes']:
            row=e.content.by_id[affix['id']]; assert item['slot'] in row['slots'] and row['category'] in base['option_pool']
            option_counts[row['source_id']]+=1
        gear_counts[base['source_id']]+=1; rarities[item['rarity']]+=1
    expected=dict(zip(e.content.balance['rarities'],e.rarity_weights()))
    assert len(gear_counts)==90 and len(option_counts)==30
    for rarity,pct in expected.items():
        sigma=math.sqrt(100000*pct/100*(1-pct/100)); assert abs(rarities[rarity]-pct*1000)<6*sigma
    monster_counts=collections.Counter(); depths=(1,10,30,50,100,101,200)
    for i in range(100000):
        floor=(i%100)+1; e.s['floor']=floor; e.start_combat('elite' if i%5==0 else 'normal')
        monster=e.s['enemy']; base=e.content.by_id[monster['id']]
        assert base['min_floor']<=floor<=base['max_floor']; monster_counts[base['source_id']]+=1
    assert len(monster_counts)==40

    encounters=[]
    for floor in depths:
        totals=collections.Counter()
        for trial in range(100):
            e=GameEngine(ROOT/'content',seed=floor*1000+trial); e.s.update(floor=floor,highest=floor,mode='explore')
            # Explicit fixture: level follows half-depth, all earned points split STR/VIT;
            # highest unlocked template per slot, randomly rolled rarity, +3 equipment.
            level=max(1,floor//2); points=3*(level-1); e.p['level']=level; e.p['attributes']['str']+=points*3//5; e.p['attributes']['vit']+=points-points*3//5
            for slot in SLOTS:
                base=max((r for r in e.content['equipment'] if r['slot']==slot and r['min_floor']<=floor),key=lambda r:r['min_floor'])
                gear=e.generate_equipment(base['id']); gear['enhance']=3; key=gear['instance_id']; e.s['inventory'][key]=gear; e.s['equipped'][slot]=key
            e.p.update(hp=e.derived()['hp'],mp=e.derived()['mp'],gold=10000)
            e.s['items']={cid('CON004'):20,cid('CON008'):10}; e.s['settings'].update(stop_danger=False)
            e.start_combat('boss' if floor%10==0 else 'normal'); e.execute('auto'); SaveManager.validate(e.s)
            totals['wins']+=e.s['stats']['wins']; totals['deaths']+=e.s['stats']['deaths']; totals['stalled']+=e.s['mode']=='combat'; totals['turns']+=e.s['combat_turn']
            potion_cost=(20-e.s['items'][cid('CON004')])*80+(10-e.s['items'][cid('CON008')])*160
            totals['potion_cost']+=potion_cost; totals['earned_gold']+=e.s['stats']['gold']; totals['equipment']+=e.s['stats']['equipment']; totals['net_gold']+=e.p['gold']-10000-potion_cost
            totals['rest_cost']+=(5*level if e.p['hp']<e.derived()['hp'] else 0)+(3*level if e.p['mp']<e.derived()['mp'] else 0)
        encounters.append(dict(floor=floor,trials=100,**totals))

    developed=[]
    for floor in (100,200):
        wins=0
        for trial in range(20):
            e=GameEngine(ROOT/'content',seed=trial); e.s.update(floor=floor,highest=floor,mode='explore')
            e.p['level']=floor; points=3*(floor-1); e.p['attributes']['str']+=points//2; e.p['attributes']['vit']+=points-points//2
            for slot in SLOTS:
                base=max((r for r in e.content['equipment'] if r['slot']==slot and r['min_floor']<=floor),key=lambda r:r['min_floor'])
                gear=e.generate_equipment(base['id']); gear['enhance']=15; key=gear['instance_id']; e.s['inventory'][key]=gear; e.s['equipped'][slot]=key
            e.p.update(hp=e.derived()['hp'],mp=e.derived()['mp']); e.s['items']={cid('CON004'):99}; e.s['settings']['stop_danger']=False
            e.start_combat('boss'); e.execute('auto'); wins+=e.s['stats']['wins']
        developed.append(dict(floor=floor,trials=20,wins=wins,level=floor,enhance=15,attribute_split='50% STR / 50% VIT'))

    # Real progression, no injected stats/currency/items. Sell bag items, equip better
    # base power, invest earned points, recover at hub, and retreat on danger.
    e=GameEngine(ROOT/'content',seed=20261016); commands=0
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
            for resource in ('hp','mp'):
                if e.p[resource]<e.derived()[resource]:
                    try: e.execute('rest',key=resource)
                    except RuleError: pass
            if not e.s['equipped'].get('무기') and e.p['gold']>=e.content.by_id[cid('EQ001')]['price']:
                e.execute('buy',key=cid('EQ001')); e.execute('equip',key=e.s['bag'][-1])
            # A few potions are budgeted, leaving gold for rest/equipment.
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
            options=e.s['event']['options']; index=next(i for i,o in enumerate(options) if not e.event_option_reason(o))
            e.execute('event',index=index)
        elif e.p['hp']<e.derived()['hp']*.6 or e.bag_used()>=28 or e.p['points']:
            e.execute('return')
        elif e.complete(): e.execute('next')
        else: e.execute('explore')
        commands+=1; SaveManager.validate(e.s); assert e.p['gold']>=0 and e.bag_used()<=30
        assert all(n<=e.content.by_id[k].get('stack_limit',999) for k,n in e.s['items'].items())
    report=dict(seed=20261016,catalogue_counts=e.content.catalogue_counts,gear_draws=100000,monster_draws=100000,gear_templates_seen=len(gear_counts),option_types_seen=len(option_counts),monster_types_seen=len(monster_counts),rarity_expected_pct=expected,rarity_observed=rarities,encounter_fixture='level=floor//2, earned points 60% STR/40% VIT, unlocked gear per slot +3, 20 CON004 and 10 CON008, auto danger stop off',encounters=encounters,developed_fixture=developed,progression=dict(decisions=commands,highest=e.s['highest'],level=e.p['level'],gold=e.p['gold'],stats=e.s['stats'],pending=len(e.s['pending_loot'])))
    output=Path(output) if output else ROOT/'artifacts/expansion_simulation.json'; output.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__': run()
