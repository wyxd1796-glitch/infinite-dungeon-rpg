"""Versioned high-floor routing and absolute-depth normalization.

The first 100 floors retain their original distributions and formulas.
"""
import math

MECHANICS={'특수 소환','추가 상태이상','보호막 파괴','단일 강타','연속 공격','회복 억제'}
MECHANIC_DESCRIPTIONS={
    '특수 소환':'최대 HP 8% 보호막(누적 없음), 발동 행동부터 적이 행동할 때 2회 공격력 25% 보조 공격',
    '추가 상태이상':'공격 후 30% 확률로 취약 부여(받는 피해 +15%)',
    '보호막 파괴':'공격 직전 플레이어 보호막 제거',
    '단일 강타':'공격력 200% 단일 공격',
    '연속 공격':'첫 공격 후 공격력 70% 추가 공격',
    '회복 억제':'이후 플레이어 2행동 동안 HP 회복 50% 감소(MP 제외)',
}
PATTERNS={'공격':'attack','특수공격':'special','방어':'defend','강공격':'heavy','회복':'heal','디버프':'debuff'}


class HighFloors:
    def __init__(self,definition,content):
        self.definition=definition; self.content=content; self.cache={}
        if definition.get('version')!=1: raise ValueError('미지원 고층 규칙 버전')
        for group in ('normal_growth','gear_growth'):
            for value in definition[group].values():
                if type(value) not in (int,float) or not math.isfinite(value) or value<=0: raise ValueError('고층 성장 수치 오류')
        if set(definition['normal_growth'])!={'hp','atk','defense'} or set(definition['gear_growth'])!={'atk','defense','hp','mp'}: raise ValueError('고층 성장 키 오류')
        if definition['role_bounds']!=[.8,1.2] or definition['family_share']!=.7: raise ValueError('미검증 고층 역할/종족 분포')
        rows=content.regions.monsters(content,100)
        env=content.by_id['catalogue.v3.ENV010']
        weights=[r['weight']*(3 if r['category']==env['primary_family'] else 1) for r in rows]
        self.anchor={stat:sum(math.floor(math.floor(r[stat]*(1+rate*99))*(1+env['risk_modifier_pct']/100) if stat!='defense' else math.floor(r[stat]*(1+rate*99)))*w for r,w in zip(rows,weights))/sum(weights) for stat,rate in (('hp',.12),('atk',.08),('defense',.06))}
        boss=content.by_id['catalogue.v3.BOS010']; base=content.by_id[boss['monster_id']]
        self.boss_anchor={}
        for stat,rate,mult in (('hp',.12,'hp_multiplier'),('atk',.08,'atk_multiplier'),('defense',.06,'def_multiplier')):
            value=math.floor(base[stat]*(1+rate*99))
            if stat!='defense': value=math.floor(value*(1+env['risk_modifier_pct']/100))
            self.boss_anchor[stat]=math.floor(value*boss[mult])

    def weights(self,rows,environment,floor):
        if floor<=100: return [r['weight']*(3 if r['category']==environment['primary_family'] else 1) for r in rows]
        primary=[r['category']==environment['primary_family'] for r in rows]
        totals={flag:sum(r['weight'] for r,p in zip(rows,primary) if p==flag) for flag in (False,True)}
        if not all(totals.values()): return [r['weight'] for r in rows]
        share=self.definition['family_share']
        return [r['weight']*(share if p else 1-share)/totals[p] for r,p in zip(rows,primary)]

    def stats(self,base,floor,environment,boss=False):
        if boss:
            return {key:max(1,math.floor(value*(floor/100)**self.definition['normal_growth'][key])) for key,value in self.boss_anchor.items()}
        cache_key=(self.content.regions.zone(floor),environment['id'])
        if cache_key not in self.cache:
            rows=self.content.regions.monsters(self.content,floor); weights=self.weights(rows,environment,floor)
            ratios={r['id']:{} for r in rows}
            for stat in self.anchor:
                mean=sum(r[stat]*w for r,w in zip(rows,weights))/sum(weights)
                raw=[max(.8,min(1.2,r[stat]/mean)) for r in rows]
                center=sum(v*w for v,w in zip(raw,weights))/sum(weights)
                for r,value in zip(rows,raw): ratios[r['id']][stat]=value/center
            self.cache[cache_key]=ratios
        ratios=self.cache[cache_key][base['id']]
        return {key:max(1,math.floor(value*(floor/100)**self.definition['normal_growth'][key]*ratios[key])) for key,value in self.anchor.items()}
