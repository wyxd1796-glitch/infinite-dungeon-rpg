"""Source-preserving adapter for explicitly selected definitions.

The original JSON is never rewritten. Textual operators are mapped by stable ID,
not evaluated or guessed from names at runtime.
"""
import copy
import hashlib
import json
import math
from .regions import Regions
from .phase3_effects import validate_definition, DESCRIPTIONS
from .high_floors import HighFloors, MECHANICS, PATTERNS

PREFIXES={'monsters':'MON','bosses':'BOS','prefixes':'PFX','equipment':'EQ','options':'OPT','consumables':'CON','materials':'MAT','environments':'ENV','floor_types':'FLR','effects':'EF'}
OPTION_STATS=['str','dex','vit','int','luk_pct','atk','defense','hp','mp','crit','crit_damage','evasion','hp_regen','mp_regen','kill_hp','kill_mp','leech','penetration','extra_damage','heavy_damage','normal_damage','reduction','crit_resist','status_resist','counter','shield','gold_bonus','exp_bonus','drop_bonus','rarity_bonus']
OPTION_NAMES=dict(zip(OPTION_STATS,['힘','민첩','체력','지능','행운 증가','공격력','방어력','최대 HP','최대 MP','치명타율','치명타 피해','회피율','HP 재생','MP 재생','처치 시 HP 회복','처치 시 MP 회복','흡혈','방어 무시','추가 피해','강공격 피해','일반 공격 피해','받는 피해 감소','치명타 저항','상태이상 저항','반격 확률','보호막','골드 획득','경험치 획득','장비 드롭률','희귀 등급 확률']))
PERCENT_STATS=set(OPTION_STATS)-{'str','dex','vit','int','atk','defense','hp','mp','luk'}
SUPPORTED_COUNTS=dict(monsters=150,bosses=40,prefixes=50,equipment=330,options=30,consumables=40,materials=60,environments=30,floor_types=5,effects=40)
def cid(source): return 'catalogue.v3.'+source

def option_slots(restriction):
    slots=['무기','투구','갑옷','장갑','신발','반지','목걸이']
    if not isinstance(restriction,str): raise ValueError('미지원 옵션 슬롯')
    result=[]
    for token in restriction.replace(',', '·').split('·'):
        token=token.strip()
        expanded=slots if token=='전체' else slots[1:5] if token=='방어구' else [token]
        if any(s not in slots for s in expanded): raise ValueError('미지원 옵션 슬롯')
        result.extend(s for s in expanded if s not in result)
    return result

def activate(content):
    root=content.root
    selection=json.loads((root/'catalogue/selection.json').read_text(encoding='utf-8'))
    high=json.loads((root/'catalogue/high_floors.json').read_text(encoding='utf-8'))
    if selection.get('selection_schema')!=2 or set(selection.get('active_ids',{}))!=set(PREFIXES): raise ValueError('잘못된 활성 목록 스키마')
    data=(root/'source/catalogue_v4.json').read_bytes()
    if hashlib.sha256(data).hexdigest()!=selection['source_sha256']: raise ValueError('원본 카탈로그 해시 불일치')
    source=json.loads(data)['base_catalogue_v3']['content']; chosen={}; ids={}
    for group,keys in selection['active_ids'].items():
        rows=source[group]; by_id={r['id']:r for r in rows}
        if len(by_id)!=len(rows): raise ValueError(f'{group}: 중복 ID')
        if not isinstance(keys,list) or not all(isinstance(k,str) for k in keys) or len(keys)!=len(set(keys)): raise ValueError(f'{group}: 잘못된 활성 ID 목록')
        supported={f'{PREFIXES[group]}{i:03}' for i in range(1,SUPPORTED_COUNTS[group]+1)}
        if group=='consumables': supported-={f'CON{i:03}' for i in range(26,36)}
        for key in keys:
            if key not in by_id: raise ValueError(f'{group}: 원본 부재 또는 종류 불일치 {key}')
            if key not in supported: raise ValueError(f'{group}: 미지원 실행 정의 {key}')
        chosen[group]=[copy.deepcopy(by_id[key]) for key in keys]
        for row in chosen[group]:
            if row['id'] in ids: raise ValueError('카탈로그 전역 ID 충돌')
            ids[row['id']]=row
    for group,rows in chosen.items():
        for row in rows:
            for field in ('effect_id','material_id'):
                if row.get(field) is not None and row[field] not in ids: raise ValueError(f"{row['id']}: 없는 참조 {row[field]}")
            for key in ('weight','base_hp','base_atk','base_def','buy_gold','sell_gold','min_floor','base_bonus','min_value','max_value'):
                if key in row and (not isinstance(row[key],(int,float)) or not math.isfinite(row[key]) or row[key]<0): raise ValueError(f"{row['id']}: 잘못된 {key}")
        if rows and all('weight' in r for r in rows) and sum(r['weight'] for r in rows)<=0: raise ValueError('빈 가중치 합')
    if not isinstance(selection['boss_monsters'],dict) or set(selection['boss_monsters'])!=set(selection['active_ids']['bosses']): raise ValueError('보스 연결 목록 불일치')
    for key in selection['boss_monsters'].values():
        if key not in selection['active_ids']['monsters']: raise ValueError('보스 원형 연결 누락')
    regions=Regions(json.loads((root/'catalogue/regions.json').read_text(encoding='utf-8')),chosen)
    from .monster_roles import validate_monsters
    roles=json.loads((root/'catalogue/monster_roles.json').read_text(encoding='utf-8'))
    validate_monsters(roles,chosen['monsters'],set(selection['active_ids']['effects']),set(selection['active_ids']['materials']))
    content.monster_roles=roles['monsters']
    if regions.cycle!=selection['cycle_floors']: raise ValueError('지역 반복 층수 불일치')
    normalized={}
    for group,rows in chosen.items():
        normalized[group]=[]
        for raw in rows:
            row=copy.deepcopy(raw); row.update(id=cid(raw['id']),source_id=raw['id'],catalogue=True)
            if group=='effects' and int(raw['id'][2:]) in DESCRIPTIONS:
                validate_definition(raw)
                row.update(polarity='debuff' if int(raw['id'][2:])<=28 else 'buff',description=DESCRIPTIONS[int(raw['id'][2:])])
            if group=='monsters':
                patterns={'기본 공격':['attack'],'공격→공격→특수공격':['attack','attack','special'],'기본 공격→방어':['attack','defend']}
                patterns.update({'기본→기본→특수':['attack','attack','special'],'기본→방어→특수':['attack','defend','special'],'기본→특수→기본':['attack','special','attack']})
                if raw['attack_pattern'] not in patterns: raise ValueError('미지원 몬스터 패턴')
                row.update(hp=raw['base_hp'],atk=raw['base_atk'],defense=raw['base_def'],accuracy=selection['defaults']['monster_accuracy'],evasion=selection['defaults']['monster_evasion'],abilities=[],pattern=patterns[raw['attack_pattern']])
            elif group=='bosses':
                if not raw['pattern'] or any(token not in PATTERNS for token in raw['pattern']): raise ValueError('미지원 보스 패턴')
                if int(raw['id'][3:])>10:
                    mechanic=high['boss_mechanics'].get(raw['id'])
                    if mechanic not in MECHANICS or mechanic!=raw.get('unique_mechanic'): raise ValueError('미지원 보스 기믹')
                    row['mechanic']=mechanic
                row.update(monster_id=cid(selection['boss_monsters'][raw['id']]),pattern=[PATTERNS[token] for token in raw['pattern']],phase2_multiplier=raw.get('phase2_multiplier',selection['defaults']['boss_phase2_multiplier']))
            elif group=='equipment':
                mapping={'ATK':'atk','DEF':'defense','HP':'hp','MP':'mp','EVA':'evasion','CRIT':'crit'}
                if raw['base_stat'] not in mapping: raise ValueError('미지원 장비 능력치')
                if raw['slot'] not in ('무기','투구','갑옷','장갑','신발','반지','목걸이'): raise ValueError('미지원 장비 슬롯')
                row['stat']=mapping[raw['base_stat']]; row['price']=raw['buy_gold']; row['sell_price']=raw['sell_gold']
                if int(raw['id'][2:])>90:
                    row['source_option_pool']=row['option_pool']; row['option_pool']=high['equipment_pools'].get(raw['id'],[])
                    categories={o['category'] for o in chosen['options']}
                    if not row['option_pool'] or set(row['option_pool'])-categories or set(row['option_pool'])-set(raw['option_pool']): raise ValueError('미지원 고층 장비 옵션 풀')
            elif group=='options':
                row['stat']=dict(zip((f'OPT{i:03}' for i in range(1,31)),OPTION_STATS))[raw['id']]
                restriction=raw['slot_restriction']
                if raw['unit'] not in ('점','%'): raise ValueError('미지원 옵션 단위')
                row['slots']=option_slots(restriction)
            elif group in ('consumables','materials'):
                row.update(category='소비품' if group=='consumables' else '재료',subtype=raw['category'],price=raw.get('buy_gold',raw['sell_gold']*2),sell_price=raw['sell_gold'],effects=[],description=raw.get('effect',raw.get('use','')))
                if group=='consumables':
                    number=int(raw['id'][3:]); row['use_number']=number
                    if number==13: row['description']+=' / 독성 폭발도 제거'
                    if number==16: row['description']+=' / 추가 해제: 감전·동상·부식·독성 폭발·암흑·무장 해제·혼란·속박·취약·둔화·마력 봉쇄·영혼 침식·정신 약화'
                    if not raw['use_context'] or set(raw['use_context'])-{'전투','탐험'}: raise ValueError('미지원 사용 상황')
                    if number<=8: row['effects']=[{'type':'heal_hp' if number<=4 else 'heal_mp','value':([50,120,260,550,25,60,130,260][number-1])}]
                    if 21<=number<=25:
                        spec=high['potions'].get(raw['id'],{})
                        if raw.get('operator')!='heal_both' or type(spec.get('unlock')) is not int or spec['unlock']<101 or type(spec.get('ratio')) not in (int,float) or not 0<spec['ratio']<=.5: raise ValueError('미지원 고층 회복 물약')
                        row.update(min_floor=spec['unlock'],effects=[dict(type='heal_'+k,value=spec['ratio'],fraction=True) for k in ('hp','mp')],description=f"최대 HP·MP 각각 {spec['ratio']:.0%} 회복 · {spec['unlock']}층 해금")
                    if 36<=number<=40:
                        if raw.get('operator')!='cleanse' or not raw.get('dispel_targets') or any(key not in selection['active_ids']['effects'] for key in raw['dispel_targets']): raise ValueError('미지원 고층 정화 물약')
                        row['description']='제거: '+', '.join(ids[key]['name'] for key in raw['dispel_targets'])
                    row['contexts']=['combat' if v=='전투' else 'explore' for v in raw['use_context']]
                else: row['upgrade_units']=selection['defaults']['material_upgrade_units'].get(raw['id'],0)
            normalized[group].append(row)
    for item in normalized['equipment']:
        if not any(item['slot'] in o['slots'] and o['category'] in item['option_pool'] for o in normalized['options']): raise ValueError('장비 옵션 풀 없음')
    # Legacy definitions remain addressable, but are not added to new spawn pools.
    for group,rows in normalized.items():
        for row in rows: content.by_id[row['id']]=row
        if group=='options': content.tables['affixes']=rows
        else: content.tables[group]=rows
    legacy_items=content.tables['items']
    for row in legacy_items: row.setdefault('stack_limit',99 if row['category']=='소비품' else 999)
    content.tables['items']=normalized['consumables']+normalized['materials']+legacy_items
    content.catalogue=selection; content.catalogue_counts={k:len(v) for k,v in chosen.items()}
    content.regions=regions
    from .prefixes import validate as validate_prefixes
    content.prefixes=json.loads((root/'catalogue/prefixes.json').read_text(encoding='utf-8'))
    validate_prefixes(content.prefixes,normalized['prefixes'])
    content.high_floors=HighFloors(high,content)
    content.packs.append({'id':'catalogue.phase1','version':selection['version']})
