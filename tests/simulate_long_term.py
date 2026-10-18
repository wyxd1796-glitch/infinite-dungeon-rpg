"""Instrument existing progression without injecting resources or altering RNG."""
import argparse
import collections
import json
import hashlib
from concurrent.futures import ProcessPoolExecutor, as_completed
from tests.simulate_phase2 import AuditEngine, ROOT, BUILDS, progression, invest_skills, RuleError


class EconomyAudit(AuditEngine):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.spent=collections.Counter(); self.earned=collections.Counter()
        self.replacements=collections.Counter(); self.first_equips=0
        self.trips=[]; self.trip=None; self.rejections=collections.Counter()

    def execute(self,action,**kwargs):
        gold=self.p['gold']; old_mode=self.s['mode']; old_highest=self.s['highest']
        old_floor=self.s['floor']; old_slot=None
        if action=='equip':
            item=self.s['inventory'][kwargs['key']]
            old_slot=self.s['equipped'].get(item['slot'])
        before_turns=self.s['turn']
        try: result=super().execute(action,**kwargs)
        except Exception:
            self.rejections[action]+=1
            raise
        delta=self.p['gold']-gold
        if delta<0: self.spent[action]+=-delta
        elif delta>0: self.earned[action]+=delta
        if action=='equip':
            if old_slot: self.replacements[str((self.s['highest']-1)//10*10+1)]+=1
            else: self.first_equips+=1
        if action=='enter':
            self.trip=dict(start_floor=self.s['floor'],start_highest=self.s['highest'],completed_floors=0,new_floors=0,actions=0)
        elif self.trip:
            self.trip['actions']+=self.s['turn']-before_turns
            if action=='next': self.trip['completed_floors']+=1
            self.trip['new_floors']+=max(0,self.s['highest']-old_highest)
            if old_mode!='base' and self.s['mode']=='base':
                self.trip.update(end_floor=old_floor,reason='return' if action=='return' else 'death')
                self.trips.append(self.trip); self.trip=None
        return result

    def audit_report(self):
        return dict(spent=dict(self.spent),earned=dict(self.earned),
                    gold_reconciliation=200+sum(self.earned.values())-sum(self.spent.values())==self.p['gold'],
                    replacements_by_highest_band=dict(self.replacements),first_equips=self.first_equips,
                    trips=self.trips,unfinished_trip=self.trip,rejections=dict(self.rejections))


class FundedPreparation(EconomyAudit):
    return_for_points=False

    def prepare_base(self,build):
        def score(item):
            weights={'atk':1,'defense':1,'hp':.1,'mp':.2,'str':2,'vit':1.5,'int':1,'dex':.2,'luk':.2}
            return sum(value*weights.get(stat,20) for stat,value in self.gear_stats(item).items())
        for row in self.s['pending_loot'][:]:
            try: self.execute('claim_loot',key=row['pending_id'])
            except RuleError: break
        for key in self.s['bag'][:]:
            item=self.s['inventory'][key]; old=self.s['equipped'].get(item['slot'])
            if not old or score(item)>score(self.s['inventory'][old]): self.execute('equip',key=key)
        for key in self.s['bag'][:]: self.execute('sell',key=key)
        while self.p['points']: self.execute('invest',key='vit' if self.p['points']%3==0 else 'str')
        invest_skills(self,build)
        for resource in ('hp','mp'):
            if self.p[resource]<self.derived()[resource]:
                try: self.execute('rest',key=resource)
                except RuleError: pass
        if not self.s['equipped'].get('무기'):
            try:
                self.execute('buy',key='catalogue.v3.EQ001'); self.execute('equip',key=self.s['bag'][-1])
            except RuleError: pass
        for resource in ('hp','mp'):
            rows=[r for r in self.shop_stock() if r.get('category')=='소비품' and any(x['type']=='heal_'+resource for x in r.get('effects',[]))]
            if not rows: continue
            def effective(row):
                return min(self.derived()[resource],sum(x['value']*(self.derived()[resource] if x.get('fraction') else 1) for x in row['effects'] if x['type']=='heal_'+resource))
            item=max(rows,key=lambda r:(effective(r),-r['price'],r['id']))
            count=max(0,3-self.s['items'].get(item['id'],0))
            if count:
                try: self.execute('buy',key=item['id'],quantity=count)
                except RuleError: pass
        for key in list(self.s['equipped'].values()):
            while self.s['inventory'][key]['enhance']<3:
                cost,units,_=self.enhance_cost(self.s['inventory'][key])
                if self.p['gold']-cost<100: break
                materials=[(k,u) for k,_,u in self.upgrade_materials() if self.s['items'].get(k,0)*u>=units]
                if not materials: break
                try: self.execute('enhance',key=key,material=materials[0][0])
                except RuleError: break


def trial(job):
    build,policy,seed,decisions,prepared=job
    folder=ROOT/'artifacts/long_term'; folder.mkdir(parents=True,exist_ok=True)
    name=folder/f'{"funded_" if prepared else ""}{build}_{policy}_{seed}_{decisions}.json'
    if name.exists():
        try:
            saved=json.loads(name.read_text(encoding='utf-8'))
            if saved['long_term']['gold_reconciliation'] and saved['decisions']==decisions: return name.name
        except (ValueError,KeyError): pass
    row=progression(build,seed,decisions,policy,0,FundedPreparation if prepared else EconomyAudit)
    row.update(build=build,policy=policy,seed=seed,reserve=0,preparation='funded' if prepared else 'legacy')
    assert row['long_term']['gold_reconciliation']
    temporary=name.with_suffix('.tmp')
    temporary.write_text(json.dumps(row,ensure_ascii=False,indent=2),encoding='utf-8')
    temporary.replace(name)
    return name.name


def source_fingerprints():
    sources=list((ROOT/'core').glob('*.py'))+list((ROOT/'content').rglob('*.json'))+[ROOT/'tests/simulate_phase2.py',ROOT/'tests/simulate_long_term.py']
    return {str(p.relative_to(ROOT)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(sources)}


def run(seeds=20,decisions=3000,prepared=False,workers=4,all_groups=False):
    folder=ROOT/'artifacts/long_term'; folder.mkdir(parents=True,exist_ok=True)
    manifest=folder/'manifest.json'; current=source_fingerprints()
    if manifest.exists():
        if json.loads(manifest.read_text(encoding='utf-8'))!=current:
            raise ValueError('측정 코드가 변경됐습니다. artifacts/long_term 폴더를 별도 보존한 뒤 재실행하세요.')
    elif any(folder.glob('*.json')):
        raise ValueError('출처 정보 없는 캐시입니다. 기존 결과를 별도 폴더로 보존하세요.')
    else: manifest.write_text(json.dumps(current,indent=2),encoding='utf-8')
    jobs=[(build,policy,20261017+offset,decisions,mode)
          for mode in ((False,True) if all_groups else (prepared,)) for build in BUILDS
          for policy in (('efficient',) if mode else ('potion_first','skill_first','efficient')) for offset in range(seeds)]
    with ProcessPoolExecutor(max_workers=workers) as pool:
        futures=[pool.submit(trial,job) for job in jobs]
        for i,future in enumerate(as_completed(futures),1):
            name=future.result()
            if i%10==0 or i==len(jobs): print(f'{i}/{len(jobs)} complete: {name}',flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--seeds',type=int,default=20); parser.add_argument('--decisions',type=int,default=3000); parser.add_argument('--prepared',action='store_true')
    parser.add_argument('--workers',type=int,default=4); parser.add_argument('--all',action='store_true')
    args=parser.parse_args(); run(args.seeds,args.decisions,args.prepared,args.workers,args.all)
