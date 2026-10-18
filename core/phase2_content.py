"""Validation for the declarative phase-two pack, before any game effects run."""
import math

PHASE2_EFFECTS={'tactical_damage','skill_buff','skill_shield','cleanse','exploration_bonus','catalogue_item','phase2_combat'}

def has_phase2_effect(obj):
    if isinstance(obj,dict): return obj.get('type') in PHASE2_EFFECTS or any(has_phase2_effect(v) for v in obj.values())
    if isinstance(obj,list): return any(has_phase2_effect(v) for v in obj)
    return False

def number(value,label,minimum=0,maximum=None,integer=False):
    if type(value) not in ((int,) if integer else (int,float)) or not math.isfinite(value) or value<minimum or (maximum is not None and value>maximum):
        raise ValueError('잘못된 콘텐츠 수치: '+label)

def validate_phase2(row,kind,source,selection):
    rows={r['id']:r for r in source[kind]}
    raw=rows.get(row.get('source_id'))
    if not raw or raw['name']!=row.get('name',row.get('title')): raise ValueError('2차 콘텐츠 출처 불일치')
    if kind=='skills':
        number(row.get('unlock_level'),'unlock_level',1,integer=True)
        number(row.get('cooldown_turns'),'cooldown_turns',0,integer=True)
        number(row.get('mp'),'mp',0,integer=True)
        if row.get('max_level')!=5 or row.get('initial_level')!=0 or row.get('auto_enabled') is not False: raise ValueError('신규 스킬 기본값 오류')
        if row.get('auto_condition') not in ('always','execute','unbuffed','unshielded','emergency'): raise ValueError('자동 스킬 조건 오류')
        if not row.get('effects') or not row.get('description'): raise ValueError('스킬 효과·설명 누락')
        for effect in row['effects']:
            expected='enemy' if effect['type']=='tactical_damage' else 'player'
            if effect.get('target')!=expected: raise ValueError('스킬 효과 대상 오류')
        if row['kind']=='passive' and any(e['type']!='modify_stat' or e.get('stat') not in ('hp','mp') for e in row['effects']): raise ValueError('패시브 효과 오류')
    else:
        number(row.get('cooldown_encounters'),'cooldown_encounters',0,integer=True)
        for opt in row['options']:
            for field in ('gold_per_floor','cost'): number(opt.get(field,0),field,0,integer=True)
            number(opt.get('hp_cost',0),'hp_cost',0,1)
            if opt.get('shop_potion') not in (None,'hp','mp'): raise ValueError('물약 선택 오류')
            if not opt.get('description'): raise ValueError('선택지 설명 누락')
        if not any(not o.get('cost') and not o.get('gold_per_floor') and not o.get('hp_cost') and not o.get('cost_item') and not o.get('shop_potion') and all(not x['effects'] for x in o['outcomes']) for o in row['options']): raise ValueError('무료 지나가기 누락')

    items={key for group in ('consumables','materials') for key in selection['active_ids'][group]}
    def walk(obj):
        if isinstance(obj,list):
            for value in obj: walk(value)
        elif isinstance(obj,dict):
            for field in ('catalogue_item','cost_item'):
                if field in obj and obj[field] not in items: raise ValueError('미활성 아이템 참조: '+str(obj[field]))
            if 'type' in obj:
                t=obj['type']; number(obj.get('value',0),'value'); number(obj.get('growth',0),'growth')
                allowed={'tactical_damage','skill_buff','skill_shield','cleanse','exploration_bonus','catalogue_item','phase2_combat','heal_hp','heal_mp','hurt','grant_gold','grant_exp','equipment','modify_stat'}
                if t not in allowed: raise ValueError('2차 콘텐츠 미지원 효과')
                if t=='tactical_damage':
                    number(obj.get('penetration',0),'penetration',0,1)
                    if 'execute_threshold' in obj:
                        number(obj['execute_threshold'],'execute_threshold',0,1); number(obj.get('execute_multiplier'),'execute_multiplier',1)
                if t=='skill_buff':
                    if obj.get('buff') not in ('attack','reduction') or obj.get('skill_id')!=row['id']: raise ValueError('버프 정의 오류')
                    number(obj.get('duration'),'duration',1,integer=True)
                    number(obj['value']+obj.get('growth',0)*4,'최대 버프',0,.99)
                if t=='exploration_bonus' and obj.get('bonus') not in ('treasure_pp','rarity_pp'): raise ValueError('탐험 보너스 오류')
                if t=='phase2_combat' and obj.get('encounter') not in ('normal','elite'): raise ValueError('이벤트 전투 오류')
                if t=='catalogue_item' and 'catalogue_item' not in obj: raise ValueError('아이템 참조 누락')
            for value in obj.values(): walk(value)
    walk(row)
