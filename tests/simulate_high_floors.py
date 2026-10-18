"""Reproducible 03-06..09 audit. Writes artifacts only, never user saves."""
import collections
import copy
import hashlib
import json
import math
from pathlib import Path

from core.catalogue import cid
from core.game_engine import GameEngine, SLOTS
from core.save_manager import SaveManager
from tests.simulate_phase2 import BUILDS, invest_skills, progression

ROOT=Path(__file__).resolve().parents[1]
SEED=20261018


def quantile(values,p):
    ordered=sorted(values)
    return ordered[max(0,math.ceil(len(ordered)*p)-1)]


def distribution(e,floor):
    c=e.content; env=c.by_id[cid(c.regions.at(floor)['environment_id'])]
    rows=c.regions.monsters(c,floor); weights=c.high_floors.weights(rows,env,floor)
    stats=[]
    for row in rows:
        if floor<=100:
            value={k:math.floor(row[k]*(1+rate*(floor-1))) for k,rate in (('hp',.12),('atk',.08),('defense',.06))}
            for k in ('hp','atk'): value[k]=math.floor(value[k]*(1+env['risk_modifier_pct']/100))
        else: value=c.high_floors.stats(row,floor,env)
        stats.append(value)
    result={}
    for key in ('hp','atk','defense'):
        average=sum(v[key]*w for v,w in zip(stats,weights))/sum(weights)
        cumulative=0
        for value,weight in sorted((v[key],w) for v,w in zip(stats,weights)):
            cumulative+=weight
            if cumulative>=sum(weights)*.9: break
        result[key]=dict(mean=average,p90=value)
    reward=1+env['reward_modifier_pct']/100 if floor<=100 else 1.27
    result['normal_gold']=math.floor((10+3*floor)*reward)
    result['normal_xp']=math.floor((25+8*floor)*reward)
    return result


def draws(e,count=100000):
    monsters=collections.Counter(); gears=collections.Counter(); digest=hashlib.sha256()
    for i in range(count):
        floor=i%400+1 if i%1000<800 else (401,800,1000,10000)[i%4]
        e.s.update(floor=floor,mode='explore',enemy=None,statuses=[])
        item=e.generate_equipment(); base=e.content.by_id[item['base_id']]
        assert base['min_floor']<=floor and all(math.isfinite(v) for v in item['rolled_stats'].values())
        assert len({a['id'] for a in item['affixes']})==len(item['affixes'])
        for a in item['affixes']:
            option=e.content.by_id[a['id']]
            assert item['slot'] in option['slots'] and option['category'] in base['option_pool']
        gears[base['source_id']]+=1
        e.start_combat('elite' if i%5==0 else 'normal'); enemy=e.s['enemy']; row=e.content.by_id[enemy['id']]
        assert row['min_floor']<=e.content.regions.zone(floor)<=row['max_floor']
        assert all(type(enemy[k]) is int and enemy[k]>0 for k in ('hp','atk','defense'))
        monsters[row['source_id']]+=1
        digest.update(json.dumps([floor,item,enemy],sort_keys=True,ensure_ascii=False).encode())
        if (i+1)%20000==0: print('draws',i+1,flush=True)
    assert len(monsters)==150 and len(gears)==330
    return dict(count_each=count,monsters=dict(sorted(monsters.items())),equipment=dict(sorted(gears.items())),sha256=digest.hexdigest())


def encounters(e):
    clean=copy.deepcopy(e.s); results=[]
    for floor in (101,110,199,200,201,210,299,300,301,310,399,400,401,410,800,1000,10000):
        for build in BUILDS:
            turns=[]; costs=[]; potions=[]; wins=0; stalls=0; skills=collections.Counter(); death_floors=collections.Counter()
            for trial in range(20):
                e.s=copy.deepcopy(clean); e.rng.seed(SEED+floor*100+trial)
                e.s.update(floor=floor,highest=floor,mode='base')
                level=max(30,floor//2); points=3*(level-1)
                e.p.update(level=level,skill_points=level//5)
                # Equal earned point budgets and gear across builds; only skill allocation differs.
                e.p['attributes']['str']+=points*3//5; e.p['attributes']['vit']+=points-points*3//5
                invest_skills(e,build)
                for slot in SLOTS:
                    base=max((r for r in e.content['equipment'] if r['slot']==slot and r['min_floor']<=floor),key=lambda r:r['min_floor'])
                    item=e.generate_equipment(base['id']); item['enhance']=3; key=item['instance_id']
                    e.s['inventory'][key]=item; e.s['equipped'][slot]=key
                potion=max((r for r in e.content['consumables'] if 21<=r['use_number']<=25 and r['min_floor']<=floor),key=lambda r:r['min_floor'])
                e.s['items']={potion['id']:10}; e.p.update(hp=e.derived()['hp'],mp=e.derived()['mp'])
                e.s['settings'].update(stop_danger=False,recovery_policy='efficient')
                e.start_combat('boss' if floor%10==0 else 'normal'); e.execute('auto'); SaveManager.validate(e.s)
                used=10-e.s['items'].get(potion['id'],0)
                wins+=e.s['stats']['wins']; stalls+=int(e.s['mode']=='combat'); turns.append(e.s['combat_turn'])
                potions.append(used); costs.append(used*potion['price']); skills.update(e.s['skill_usage'])
                if e.s['stats']['deaths']: death_floors[floor]+=1
            results.append(dict(floor=floor,build=build,trials=20,wins=wins,win_rate=wins/20,stalls=stalls,
                                turns_mean=sum(turns)/20,turns_p50=quantile(turns,.5),turns_p90=quantile(turns,.9),
                                potions_mean=sum(potions)/20,potion_cost_mean=sum(costs)/20,
                                skills=dict(skills),death_floors=dict(death_floors)))
        print('encounters',floor,[(r['build'],r['wins'],r['stalls']) for r in results[-3:]],flush=True)
    return results


def run():
    e=GameEngine(ROOT/'content',seed=SEED)
    boundaries={str(f):distribution(e,f) for f in (99,100,101,199,200,201,299,300,301,399,400,401,799,800,801,999,1000,1001,10000)}
    result=dict(seed=SEED,source_sha256=hashlib.sha256((ROOT/'content/source/catalogue_v4.json').read_bytes()).hexdigest(),
                fixture='20 seeds/build/floor; level=max(30,F//2); earned STR/VIT 60/40, skill points=level//5; highest unlocked gear per slot +3, 10 best unlocked mixed potions, efficient policy. Prepared fixtures are not evidence of natural progression.',
                boundaries=boundaries,draws=draws(e))
    # Discard every synthetic encounter before preparing controlled combat fixtures.
    e=GameEngine(ROOT/'content',seed=SEED); result['encounters']=encounters(e)
    result['progression']={}
    for build in BUILDS:
        print('progression',build,flush=True)
        result['progression'][build]=progression(build,seed=SEED,decisions=3000)
    path=ROOT/'artifacts/high_floors_simulation.json'
    path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Saved',path,flush=True)


if __name__=='__main__': run()
