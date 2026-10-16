"""Source-preserving adapter for the explicitly selected 260 definitions.

The original JSON is never rewritten. Textual operators are mapped by stable ID,
not evaluated or guessed from names at runtime.
"""
import copy
import hashlib
import json
import math

PREFIXES={'monsters':'MON','bosses':'BOS','prefixes':'PFX','equipment':'EQ','options':'OPT','consumables':'CON','materials':'MAT','environments':'ENV','floor_types':'FLR','effects':'EF'}
OPTION_STATS=['str','dex','vit','int','luk_pct','atk','defense','hp','mp','crit','crit_damage','evasion','hp_regen','mp_regen','kill_hp','kill_mp','leech','penetration','extra_damage','heavy_damage','normal_damage','reduction','crit_resist','status_resist','counter','shield','gold_bonus','exp_bonus','drop_bonus','rarity_bonus']
OPTION_NAMES=dict(zip(OPTION_STATS,['힘','민첩','체력','지능','행운 증가','공격력','방어력','최대 HP','최대 MP','치명타율','치명타 피해','회피율','HP 재생','MP 재생','처치 시 HP 회복','처치 시 MP 회복','흡혈','방어 무시','추가 피해','강공격 피해','일반 공격 피해','받는 피해 감소','치명타 저항','상태이상 저항','반격 확률','보호막','골드 획득','경험치 획득','장비 드롭률','희귀 등급 확률']))
PERCENT_STATS=set(OPTION_STATS)-{'str','dex','vit','int','atk','defense','hp','mp','luk'}
SUPPORTED_COUNTS=dict(monsters=40,bosses=10,prefixes=20,equipment=90,options=30,consumables=20,materials=20,environments=10,floor_types=5,effects=15)
def cid(source): return 'catalogue.v3.'+source

def activate(content):
    root=content.root
    selection=json.loads((root/'catalogue/selection.json').read_text(encoding='utf-8'))
    if selection['counts']!=SUPPORTED_COUNTS: raise ValueError('검증되지 않은 활성 카탈로그 범위')
    data=(root/'source/catalogue_v4.json').read_bytes()
    if hashlib.sha256(data).hexdigest()!=selection['source_sha256']: raise ValueError('원본 카탈로그 해시 불일치')
    source=json.loads(data)['base_catalogue_v3']['content']; chosen={}; ids={}
    for group,count in selection['counts'].items():
        rows=source[group]; by_id={r['id']:r for r in rows}
        if len(by_id)!=len(rows): raise ValueError(f'{group}: 중복 ID')
        chosen[group]=[copy.deepcopy(by_id[f'{PREFIXES[group]}{i:03}']) for i in range(1,count+1)]
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
    for key in selection['boss_monsters']:
        if key not in ids: raise ValueError('보스 원형 연결 누락')
    normalized={}
    for group,rows in chosen.items():
        normalized[group]=[]
        for raw in rows:
            row=copy.deepcopy(raw); row.update(id=cid(raw['id']),source_id=raw['id'],catalogue=True)
            if group=='monsters':
                patterns={'기본 공격':['attack'],'공격→공격→특수공격':['attack','attack','special'],'기본 공격→방어':['attack','defend']}
                if raw['attack_pattern'] not in patterns: raise ValueError('미지원 몬스터 패턴')
                row.update(hp=raw['base_hp'],atk=raw['base_atk'],defense=raw['base_def'],accuracy=selection['defaults']['monster_accuracy'],evasion=selection['defaults']['monster_evasion'],abilities=[],pattern=patterns[raw['attack_pattern']])
            elif group=='bosses':
                index=int(raw['id'][3:])-1
                if raw['pattern']!=['공격','공격','특수공격']: raise ValueError('미지원 보스 패턴')
                row.update(monster_id=cid(selection['boss_monsters'][index]),pattern=['attack','attack','special'],phase2_multiplier=selection['defaults']['boss_phase2_multiplier'])
            elif group=='equipment':
                mapping={'ATK':'atk','DEF':'defense','HP':'hp','MP':'mp','EVA':'evasion','CRIT':'crit'}
                if raw['base_stat'] not in mapping: raise ValueError('미지원 장비 능력치')
                if raw['slot'] not in ('무기','투구','갑옷','장갑','신발','반지','목걸이'): raise ValueError('미지원 장비 슬롯')
                row['stat']=mapping[raw['base_stat']]; row['price']=raw['buy_gold']; row['sell_price']=raw['sell_gold']
            elif group=='options':
                index=int(raw['id'][3:])-1; row['stat']=OPTION_STATS[index]
                restriction=raw['slot_restriction']
                if raw['unit'] not in ('점','%'): raise ValueError('미지원 옵션 단위')
                row['slots']=['무기','투구','갑옷','장갑','신발','반지','목걸이'] if restriction=='전체' else ['투구','갑옷','장갑','신발','목걸이'] if restriction=='방어구·목걸이' else restriction.split('·')
            elif group in ('consumables','materials'):
                row.update(category='소비품' if group=='consumables' else '재료',subtype=raw['category'],price=raw.get('buy_gold',raw['sell_gold']*2),sell_price=raw['sell_gold'],effects=[],description=raw.get('effect',raw.get('use','')))
                if group=='consumables':
                    number=int(raw['id'][3:]); row['use_number']=number
                    if not raw['use_context'] or set(raw['use_context'])-{'전투','탐험'}: raise ValueError('미지원 사용 상황')
                    if number<=8: row['effects']=[{'type':'heal_hp' if number<=4 else 'heal_mp','value':([50,120,260,550,25,60,130,260][number-1])}]
                    row['contexts']=['combat' if v=='전투' else 'explore' for v in raw['use_context']]
                else: row['upgrade_units']=selection['defaults']['material_upgrade_units'].get(raw['id'],0)
            normalized[group].append(row)
    for floor in range(1,101):
        if not any(r['min_floor']<=floor<=r['max_floor'] and r['weight']>0 for r in normalized['monsters']): raise ValueError(f'{floor}층 출현 풀 없음')
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
    content.packs.append({'id':'catalogue.phase1','version':selection['version']})
    content.balance['evasion_cap']=.45
