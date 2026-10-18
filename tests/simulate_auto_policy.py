"""20-seed paired policy comparison, using isolated synthetic states."""
import collections
import json
import math
from tests.simulate_phase2 import AuditEngine, ROOT, BUILDS, invest_skills, progression, SLOTS
from core.catalogue import cid

POLICIES=('potion_first','skill_first','efficient')

def percentile(values,p):
    return sorted(values)[max(0,math.ceil(len(values)*p)-1)] if values else None

def run():
    report={'seeds':list(range(20261017,20261037)), 'encounters':[], 'progression':[]}
    for build in BUILDS:
        for policy in POLICIES:
            for kind in ('normal','elite','boss'):
                turns=[]; wins=potions=mp=stalls=0; uses=collections.Counter()
                for seed in report['seeds']:
                    for repeat in range(10):
                        e=AuditEngine(ROOT/'content',seed=seed*10+repeat)
                        e.s.update(floor=30,highest=30); e.p.update(level=30,skill_points=6,gold=10000)
                        e.p['attributes']['str']+=52; e.p['attributes']['vit']+=35
                        invest_skills(e,build)
                        for slot in SLOTS:
                            row=max((r for r in e.content['equipment'] if r['slot']==slot and r['min_floor']<=30),key=lambda r:r['min_floor'])
                            gear=e.generate_equipment(row['id']); gear['enhance']=3
                            e.s['inventory'][gear['instance_id']]=gear; e.s['equipped'][slot]=gear['instance_id']
                        e.p.update(hp=e.derived()['hp'],mp=e.derived()['mp'])
                        # Fixed finite potion budget; 30-floor unlocked HP potion.
                        e.s['items']={cid('CON002'):5}
                        e.s['settings'].update(stop_danger=False,recovery_policy=policy,mp_reserve=16)
                        e.start_combat(kind); e.execute('auto')
                        wins+=e.s['stats']['wins']; potions+=e.potions; mp+=e.mp_spent
                        turns.append(e.s['combat_turn']); uses.update(e.s['skill_usage']); stalls+=e.s['mode']=='combat'
                rate=wins/200
                report['encounters'].append(dict(build=build,policy=policy,kind=kind,n=200,win_rate=rate,
                    approximate_95_margin=1.96*math.sqrt(rate*(1-rate)/200),p50=percentile(turns,.5),p90=percentile(turns,.9),
                    potions=potions,mp_spent=mp,skill_uses=dict(uses),stalls=stalls))
            samples=[progression(build,seed,100,policy,16) for seed in report['seeds']]
            turns=[turn for sample in samples for turn in sample['combat_turn_samples']]
            report['progression'].append(dict(build=build,policy=policy,decisions_per_seed=100,
                p50=percentile(turns,.5),p90=percentile(turns,.9),samples=samples))
            print(build,policy,'complete',flush=True)
    target=ROOT/'artifacts/auto_policy_simulation.json'
    target.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(str(target),flush=True)

if __name__=='__main__': run()
