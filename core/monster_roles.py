"""Explicit encounter roles; metadata never rewrites saved enemy snapshots."""
import math

ROLES={'일반형','공격형','방어형','지속피해형','제어형','강화형'}


def validate_monsters(definition,monsters,effects,materials):
    if definition.get('version')!=1 or set(definition.get('monsters',{}))!={r['id'] for r in monsters}:
        raise ValueError('몬스터 역할 목록 누락/중복 참조')
    for row in monsters:
        if definition['monsters'][row['id']].get('role') not in ROLES: raise ValueError('미지원 몬스터 역할')
        if not isinstance(row.get('category'),str) or not row['category'].strip(): raise ValueError('몬스터 종족 누락')
        for key in ('base_hp','base_atk','weight'):
            if type(row.get(key)) not in (int,float) or not math.isfinite(row[key]) or row[key]<=0: raise ValueError('몬스터 능력치/가중치 오류')
        if any(type(row.get(k)) is not int for k in ('min_floor','max_floor')) or not 1<=row['min_floor']<=row['max_floor']:
            raise ValueError('몬스터 출현 범위 오류')
        if row.get('material_id') not in materials or (row.get('effect_id') is not None and row['effect_id'] not in effects):
            raise ValueError('몬스터 효과/재료 종류 불일치')
        for key in ('special_proc_pct','drop_material_pct'):
            if key in row and (type(row[key]) not in (int,float) or not math.isfinite(row[key]) or not 0<=row[key]<=100):
                raise ValueError('몬스터 확률 오류')
        if 'ai_pattern_turns' in row and (type(row['ai_pattern_turns']) is not int or row['ai_pattern_turns']!=len(row['attack_pattern'].split('→'))):
            raise ValueError('몬스터 패턴 길이 불일치')


def effect_chance(enemy):
    if enemy.get('depth_rules_version') and not enemy.get('boss_id') and 'special_proc_pct' in enemy:
        return enemy['special_proc_pct']/100
    return None  # The effect's base chance, including legacy monsters on later cycles.
