"""Boss source contracts and read-only encounter guidance."""
import math

COUNTERS = {
    '특수 소환': '소환 보호막을 먼저 소모시키고 보조 공격 2회 동안 HP를 확보하세요.',
    '추가 상태이상': '취약 상태에서는 방어하고 치료 수단을 준비하세요.',
    '보호막 파괴': '보호막에만 의존하지 말고 강공격 순서에 방어하세요.',
    '단일 강타': '특수공격 순서에 방어하고 미리 HP를 회복하세요.',
    '연속 공격': '두 번의 공격을 버틸 HP를 확보하고 방어하세요.',
    '회복 억제': '강공격 전에 HP를 회복하세요. 억제 중에는 HP 회복량이 절반입니다.',
}


def validate_boss(row, effects, default_multiplier):
    for field in ('hp_multiplier', 'atk_multiplier', 'def_multiplier', 'phase2_multiplier'):
        value = row.get(field, default_multiplier if field == 'phase2_multiplier' else None)
        if type(value) not in (int, float) or not math.isfinite(value) or value <= 0:
            raise ValueError(f"{row['id']}: 잘못된 보스 배율 {field}")
    threshold = row.get('phase2_hp_pct')
    if type(threshold) not in (int, float) or not 0 < threshold < 100:
        raise ValueError(f"{row['id']}: 잘못된 보스 단계 조건")
    if row.get('effect_id') not in effects:
        raise ValueError(f"{row['id']}: 보스 효과 종류 오류")
    if type(row.get('first_floor')) is not int or row['first_floor'] != int(row['id'][3:]) * 10:
        raise ValueError(f"{row['id']}: 보스 등장층 오류")
    if row.get('escape_allowed', False) is not False:
        raise ValueError(f"{row['id']}: 미지원 보스 도주 규칙")


def guidance(enemy):
    phase = '2단계 진행 중' if enemy.get('phase2') else '1단계'
    increase = (enemy.get('phase2_multiplier', 1.25) - 1) * 100
    return (f"{phase} · HP {enemy.get('phase2_hp_pct',40):g}% 이하에서 적 행동 시작 시 2단계"
            f"\n2단계 공격력 +{increase:g}% · 회복해도 단계 유지 · 도주 불가\n"
            + COUNTERS.get(enemy.get('mechanic'), '특수공격 순서에 방어하고 상태효과에 맞는 치료 수단을 준비하세요.'))
