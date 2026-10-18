"""Validated prefix operations; source prose is display-only."""
import math

STAT_FIELDS={'reflect','reduction','hp_regen','status_resist'}
SCALARS={'execute','kill_heal','survive','equipment_drop','material_drop','rarity_pp'}


def description(prefix,enemy=None,used=False):
    text={'PFX026':'공격 직전 대상 HP 30% 이하이면 직접 피해 +22%',
          'PFX031':'받는 직접 피해 -12% (지속/반사 피해 제외)',
          'PFX035':'플레이어 직접 처치 직후 HP 5% 회복 (패배 처리 전)',
          'PFX038':'전투당 1회 HP 1 생존 · 생존 효과와 횟수 공유'+(' [사용 완료]' if used else ''),
          'PFX045':'장비 드롭 확률 ×1.15 · 최대 100%',
          'PFX049':'기본 재료 드롭 확률 ×1.25 · 추가 재료 추첨 별도',
          'PFX050':'이번 처치 장비의 희귀 이상 등급 확률 +4%p'}.get(prefix['source_id'],prefix['effect'])
    return prefix['name']+' · '+text


def validate(definition,rows):
    if definition.get('version')!=1 or set(definition.get('effects',{}))!={r['source_id'] for r in rows}:
        raise ValueError('접두어 실행 목록 불일치')
    for row in rows:
        if row['category'] not in {'공격 강화','방어 강화','생존 강화','특수 공격','보상 강화'}: raise ValueError('접두어 범주 오류')
        if type(row.get('min_floor',1)) is not int or row.get('min_floor',1)<1 or row.get('duplicate_category_allowed',False) is not False: raise ValueError('접두어 해금/중복 규칙 오류')
        if type(row.get('weight')) not in (int,float) or not math.isfinite(row['weight']) or row['weight']<=0: raise ValueError('접두어 가중치 오류')
        effects=definition['effects'][row['source_id']]
        if not isinstance(effects,list) or not effects: raise ValueError('접두어 효과 누락')
        for effect in effects:
            kind=effect.get('type')
            if kind in ('hit','legacy_hit'):
                if set(effect)!={'type','effect','chance'} or type(effect['effect']) is not int or effect['effect'] not in range(1,29) or type(effect['chance']) not in (int,float) or not 0<=effect['chance']<=1: raise ValueError('접두어 상태효과 오류')
                if kind=='legacy_hit' and (effect['effect'] not in (1,2,9) or effect['chance']!=.15): raise ValueError('기존 접두어 효과 오류')
                continue
            fields={'multiply':{'atk','defense','hp','gold_multiplier','exp_multiplier'},'add':{'crit','evasion','leech'},'stat':STAT_FIELDS}
            if kind not in fields and kind not in SCALARS: raise ValueError('미지원 접두어 연산자')
            if set(effect)!=({'type','value','stat'} if kind in fields else {'type','value'}): raise ValueError('접두어 효과 필드 오류')
            value=effect['value']
            if type(value) not in (int,float) or not math.isfinite(value) or not (-.5<=value<=1 if kind in fields else 0<=value<=4 if kind=='rarity_pp' else 0<=value<=1): raise ValueError('접두어 수치 오류')
            if kind in fields and effect.get('stat') not in fields[kind]: raise ValueError('접두어 대상 능력치 오류')
            if kind=='survive' and value!=1: raise ValueError('접두어 생존 수치 오류')


def apply(enemy,prefix,definition):
    for effect in definition['effects'][prefix['source_id']]:
        kind=effect['type']; stat=effect.get('stat'); value=effect.get('value')
        if kind=='multiply':
            result=enemy[stat]*(1+value)
            enemy[stat]=result if stat.endswith('_multiplier') else math.floor(result)
        elif kind=='add': enemy[stat]=enemy.get(stat,0)+value
        elif kind=='legacy_hit': enemy.setdefault('on_hit_effects',[]).append(effect['effect'])
        else:
            runtime=enemy.setdefault('prefix_runtime',{'version':1,'stats':{},'hits':[]})
            if kind=='stat': runtime['stats'][stat]=runtime['stats'].get(stat,0)+value
            elif kind=='hit': runtime['hits'].append({'effect':effect['effect'],'chance':effect['chance']})
            else: runtime[kind]=value


def validate_saved(runtime):
    if not isinstance(runtime,dict) or type(runtime.get('version')) is not int or runtime['version']!=1 or set(runtime)-({'version','stats','hits'}|SCALARS): raise ValueError('접두어 저장 버전/필드 오류')
    stats=runtime.get('stats'); hits=runtime.get('hits')
    if not isinstance(stats,dict) or set(stats)-STAT_FIELDS or not isinstance(hits,list) or len(hits)>1: raise ValueError('접두어 저장 효과 오류')
    values=list(stats.values())+[v for k,v in runtime.items() if k in SCALARS-{'rarity_pp'}]
    if any(type(v) not in (int,float) or not math.isfinite(v) or not 0<=v<=1 for v in values): raise ValueError('접두어 저장 수치 오류')
    if type(runtime.get('rarity_pp',0)) not in (int,float) or not 0<=runtime.get('rarity_pp',0)<=4: raise ValueError('접두어 등급 확률 오류')
    for hit in hits:
        if not isinstance(hit,dict) or set(hit)!={'effect','chance'} or type(hit['effect']) is not int or hit['effect'] not in range(1,29) or type(hit['chance']) not in (int,float) or not 0<=hit['chance']<=1: raise ValueError('접두어 저장 타격 효과 오류')


def validate_ids(enemy):
    ids=enemy.get('prefix_ids',[])
    groups={f'catalogue.v3.PFX{i:03}':(i-1)//4 if i<=20 else (i-21)//6 for i in range(1,51)}
    if not isinstance(ids,list) or any(not isinstance(k,str) or k not in groups for k in ids): raise ValueError('저장 접두어 참조 오류')
    categories=[groups[k] for k in ids]
    if len(categories)!=len(set(categories)) or len(ids)>{'normal':1,'elite':2,'boss':0}.get(enemy.get('kind'),2): raise ValueError('저장 접두어 중복/개수 오류')
