"""Regenerate the 150-row runtime encounter catalogue without touching saves."""
from collections import Counter
from pathlib import Path
from core.game_engine import GameEngine
from core.monster_roles import effect_chance

ROOT=Path(__file__).resolve().parents[1]


def run():
    e=GameEngine(ROOT/'content'); roles=Counter(r['role'] for r in e.content.monster_roles.values())
    lines=['# 03-10 몬스터 150종 전수 검수','',
           '2026-10-18. 원본 150종과 실행 출현·패턴·효과·보상을 전수 대조했다. 역할은 원본에 없어 별도 monster_roles.json에 명시했다. 기존 전투 스냅샷과 수치는 바꾸지 않는다.', '',
           '역할 집계: '+', '.join(f'{k} {v}종' for k,v in sorted(roles.items()))+'.', '',
           '방어 행동이 있는 경우 방어형을 주 역할로 표시한다. 나머지는 실제 지속 피해/제어/자기 강화 효과, 특수공격 유무에 따라 분류했다. 표의 효과 열로 복합 역할을 확인할 수 있다. 이름·설명 문자열을 실행해 역할 효과를 추정하지 않는다.', '',
           '## 구현과 수정','',
           '- 종족·출현층·양수 가중치·효과/재료의 종류·0~100% 확률·선언된 패턴 길이를 로딩 시 검증한다. 전투 화면에 종족·역할·기본 재료 확률을 줄바꿈 표시한다.',
           '- MON001~040은 special_proc_pct가 원본에 없다. 401층 이후 재등장 시 이를 0%로 처리하던 오류를 수정하여 효과 자체의 기본 확률을 사용한다. 수치가 있는 MON041~150은 해당 확률을 사용한다. 보스와 진행 중 기존 전투의 기본 확률 경로는 유지한다.',
           '- 적에게 걸린 EF031/040 골드 강화는 처치 골드에 반영한다. 플레이어의 같은 계열 효과와 최댓값 하나만 적용하고 기존 골드 보너스 상한을 유지한다. 처치 확정 경로에서 한 번만 지급한다.',
           '- EF035 MP 흡수는 현재 150종의 effect_id에 없다. 이번 몬스터 검수에서 새 MP 소비 규칙을 만들지 않는다. 원소와 마력 체계의 추가 설계는 별도 과제다.',
           '- 개별 재료 드롭과 추가 재료 추첨, 골드/경험치, 장비 보상은 공통 처치 경로를 따른다. 모든 재료의 현행 사용처는 판매 또는 기존 강화 대체이고 제작은 후속이다.',
           '- 원본 element/reward_tier는 출처 메타데이터다. 현재 원소 상성이나 등급별 보상 계수로 실행하지 않는다. 원소 시스템을 이번 완료 범위로 주장하지 않는다.',
           '- 도감은 6단계다. 이번 화면은 현재 전투의 적 정보이며 미보유 소지품/미학습 스킬을 사용 목록에 노출하지 않는다.', '',
           '## 전수 연결표','',
           '층 범위는 400층 원형 순환 안의 실제 유효 범위다. 효과 확률은 상태 저항 차감 전이며 디버프는 유효 피해 이후, 버프는 자신에게 적용한다. 특수 행동이 있는 패턴에서는 해당 순서에만 발동한다. 재료 확률은 1~100층 20%, 고층은 명시값 또는 20%다.', '',
           '| ID | 이름 | 종족 | 역할 | 원형 층 | 가중치 | 실행 패턴 | 효과/확률 | 재료/고층 확률 |',
           '|---|---|---|---|---|---:|---|---|---|']
    for r in e.content['monsters']:
        effect=e.content.by_id.get('catalogue.v3.'+str(r['effect_id']))
        chance=effect_chance(dict(r,depth_rules_version=1))
        if effect and chance is None: chance=effect['base_chance_pct']/100
        label=f"{r['effect_id']} {chance:.0%}" if effect else '없음'
        lines.append(f"| {r['source_id']} | {r['name']} | {r['category']} | {e.content.monster_roles[r['source_id']]['role']} | {r['min_floor']}~{min(400,r['max_floor'])} | {r['weight']} | {' → '.join(r['pattern'])} | {label} | {r['material_id']} {r.get('drop_material_pct',20)}% |")
    lines+=['','검증: test_monster_audit.py가 150종 각각의 출현·패턴 한 주기·효과 호출·골드/재료 지급·진행도·저장 유효성을 검사한다. 별도 순환 재등장 확률 회귀, 잘못된 데이터 거절, 기존 적 스냅샷 보존 검사를 포함한다. 기존 03-06~09 대량 측정은 당시 결과로 보존하며 이번 수정으로 그 원자료를 새로 측정한 것으로 표시하지 않는다.', '',
            '최종 전체 검사: `QT_QPA_PLATFORM=offscreen`에서 `python -m unittest discover -s tests -p test_*.py`, 199개 통과(53.749초). 신규 엔진 검사 5개와 좁은 창 UI 검사 1개를 기존 193개에 추가했다. 1~100층 추첨 상태·난수 해시와 기존 48행동 전투 해시도 유지했다. 268×861/250×400의 역할·재료 안내 줄바꿈, 조회의 상태/난수 불변성을 확인했다.', '',
            '재생성: `python -m tests.report_monsters`. 다음 작업은 03-11 접두어 50종이다. 보스 개별 대응/경제/자연 고층 진행은 기존 후속 단계에서 검증한다.','']
    (ROOT/'docs/MONSTER_AUDIT.md').write_text('\n'.join(lines),encoding='utf-8')


if __name__=='__main__': run()
