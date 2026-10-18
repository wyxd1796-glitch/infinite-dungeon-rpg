"""Explicit EF016–040 execution definitions; source text is never evaluated."""
import math

BATTLE_RULES_VERSION = 3
# operator, trigger, magnitude (% or percentage points), duration, stack limit
EFFECTS = {
    16: ('dot_atk_pct', 'turn_end', 6, 3, 1),
    17: ('dot_maxhp_pct', 'turn_end', 1.5, 4, 2),
    18: ('dot_maxhp_pct', 'turn_end', 2.5, 3, 1),
    19: ('dot_maxhp_pct', 'turn_end', 4, 2, 1),
    20: ('accuracy_down_pp', 'on_attack', 15, 2, 1),
    21: ('basic_damage_down_pct', 'on_attack', 30, 2, 1),
    22: ('skip_chance_pct', 'turn_start', 25, 2, 1),
    23: ('evade_down_pp', 'on_evade', 12, 2, 1),
    24: ('damage_taken_up_pct', 'on_hit', 15, 3, 1),
    25: ('evade_down_pp', 'on_evade', 8, 3, 1),
    26: ('mp_cost_up_pct', 'on_spell', 30, 3, 1),
    27: ('maxmp_down_pct', 'turn_end', 15, 3, 1),
    28: ('skill_damage_down_pct', 'on_spell', 20, 3, 1),
    29: ('crit_up_pp', 'on_attack', 10, 3, 1),
    30: ('damage_taken_down_pct', 'on_damage', 12, 3, 1),
    31: ('gold_up_pct', 'on_drop', 20, 3, 1),
    32: ('skill_damage_up_pct', 'on_spell', 20, 3, 1),
    33: ('def_up_pct', 'on_damage', 25, 3, 1),
    34: ('heal_maxhp_pct', 'turn_start', 6, 2, 1),
    35: ('mp_leech_pct', 'on_hit', 5, 3, 1),
    36: ('crit_damage_up_pct', 'on_crit', 25, 3, 1),
    37: ('barrier_maxhp_pct', 'on_damage', 15, 3, 1),
    38: ('counter_chance_pct', 'on_hit', 15, 3, 1),
    39: ('survive_once_hp_pct', 'on_lethal', 1, 99, 1),
    40: ('gold_up_pct', 'on_reward', 25, 5, 1),
}
DESCRIPTIONS = {
    16: '부여자 공격력 6% 지속 피해', 17: '최대 HP 1.5% 지속 피해·최대 2중첩',
    18: '최대 HP 2.5% 지속 피해', 19: '최대 HP 4% 지속 피해',
    20: '명중 -15%p', 21: '일반·강공격 피해 -30%',
    22: '행동 25% 취소·MP/아이템 소모 없음', 23: '회피 -12%p',
    24: '받는 직접 피해 +15%', 25: '회피 -8%p',
    26: '스킬 MP 비용 +30%·올림', 27: '최대 MP -15%', 28: '공격 스킬 피해 -20%',
    29: '치명 +10%p', 30: '직접 피해 감소 +12%p', 31: '전투 골드 +20%·황금 축복과 큰 값 적용',
    32: '공격 스킬 피해 +20%', 33: '방어력 +25%', 34: '턴 시작 최대 HP 6% 회복',
    35: '실제 직접 피해 5% MP 회복', 36: '치명 피해 배율 +0.25',
    37: '첫 직접 피격에 HP 15% 보호막·갱신으로 재발동 불가', 38: '반격 +15%p',
    39: '전투당 1회 치명 피해 생존', 40: '전투 골드 +25%·행운과 큰 값 적용',
}


def required_version(number):
    return 2 if number <= 25 else 3


def validate_definition(row):
    number = int(row['id'][2:])
    expected = EFFECTS[number]
    fields = ('operator', 'trigger', 'magnitude', 'duration_turns', 'stack_limit')
    if tuple(row.get(key) for key in fields) != expected or row.get('resist_type') != ('debuff' if number <= 28 else 'none'):
        raise ValueError('미지원 효과 실행 정의: ' + row['id'])
    chance = row.get('base_chance_pct')
    if type(chance) not in (int, float) or not math.isfinite(chance) or not 0 <= chance <= 100:
        raise ValueError('잘못된 효과 부여 확률')


def validate_status(status, state):
    n = status['effect_number']
    if state.get('battle_rules_version', 1) < required_version(n) or state['mode'] != 'combat':
        raise ValueError('이전 규칙 또는 전투 밖 신규 효과')
    if status.get('effect_id') != f'catalogue.v3.EF{n:03}' or status.get('source_side') not in ('player', 'enemy'):
        raise ValueError('효과 출처 오류')
    if status.get('runtime_version') != required_version(n):
        raise ValueError('효과 실행 버전 오류')
    if type(status.get('stacks')) is not int or not 1 <= status['stacks'] <= EFFECTS[n][4]:
        raise ValueError('효과 중첩 오류')
    if type(status.get('turns')) is not int or not 1 <= status['turns'] <= EFFECTS[n][3]:
        raise ValueError('효과 기간 오류')
    for key in ('eligible_turn', 'applied_at'):
        if type(status.get(key)) is not int or not 0 <= status[key] <= state.get('turn', 0) + 1:
            raise ValueError('효과 시점 오류')
    if type(status.get('source_atk')) not in (int, float) or not math.isfinite(status['source_atk']) or status['source_atk'] < 0:
        raise ValueError('효과 공격력 스냅샷 오류')
    if n == 37 and type(status.get('triggered')) is not bool:
        raise ValueError('보호 결계 발동 기록 오류')
