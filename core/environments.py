"""Explicit environment/floor contracts; source prose is never executed."""
import math

FLOOR_WEIGHTS = {'FLR001':75, 'FLR002':10, 'FLR003':10, 'FLR004':5}
FLOOR_GUIDANCE = {
    'FLR001':'기본 조우 확률 · 탐험 결과 3회 완료 후 이동',
    'FLR002':'정예 조우 +15%p · 일반 조우 -15%p',
    'FLR003':'보물 조우 +20%p · 일반 조우 -20%p',
    'FLR004':'적 HP·공격력 +20% · 전투 골드 +30% (경험치 제외)',
    'FLR005':'탐험 결과 2회 완료 후 다음 탐험에서 보스 확정 · 처치 후 이동',
}


def validate_environments(rows, floors, effects):
    for row in rows:
        number=int(row['id'][3:])
        if type(row.get('first_floor')) is not int or type(row.get('last_floor')) is not int or (row['first_floor'],row['last_floor']) != ((number-1)*10+1,number*10):
            raise ValueError('환경 층 범위 오류')
        if not isinstance(row.get('primary_family'),str) or not row['primary_family'].strip():
            raise ValueError('환경 주 종족 누락')
        for key in ('risk_modifier_pct','reward_modifier_pct'):
            value=row.get(key)
            if type(value) not in (int,float) or not math.isfinite(value) or value<0:
                raise ValueError('환경 보정 수치 오류')
        effect=row.get('floor_effect_id')
        if effect is not None and effect not in effects: raise ValueError('환경 효과 참조 오류')
        if effect is not None and not 16<=int(effect[2:])<=40: raise ValueError('미지원 환경 효과')
    if {r['id'] for r in floors} != set(FLOOR_WEIGHTS)|{'FLR005'}:
        raise ValueError('층 유형 목록 오류')
    for row in floors:
        if type(row.get('explorations')) is not int or row['explorations']!=(2 if row['id']=='FLR005' else 3):
            raise ValueError('층 탐험 횟수 오류')


def guidance(engine):
    env=engine.environment(); enemy=engine.s.get('enemy')
    high=bool(enemy.get('depth_rules_version')) if engine.s['mode']=='combat' and enemy else engine.s['floor']>100
    if high:
        text='고층 절대층 성장 적용 · 전투 골드·경험치 ×1.27\n주 종족 70% / 기타 30% (한쪽이 없으면 원래 가중치)'
    else:
        text=f"적 HP·공격력 +{env['risk_modifier_pct']:g}% · 전투 골드·경험치 +{env['reward_modifier_pct']:g}%\n주 종족 출현 가중치 ×3"
    text=f"주 종족: {env['primary_family']}\n"+text
    effect=env.get('floor_effect_id') if high else None
    if effect:
        definition=engine.content.by_id['catalogue.v3.'+effect]
        target='적 강화' if int(effect[2:])>=29 else '플레이어 약화'
        text+=f"\n새 전투 시작 시 {target}: {definition['name']} · 기본 확률 10% (저항 적용)"
    return text+'\n'+FLOOR_GUIDANCE[engine.s['floor_type']]
