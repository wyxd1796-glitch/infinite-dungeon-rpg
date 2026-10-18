"""Render the checked-in high-floor simulation into a readable report."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def run():
    result=json.loads((ROOT/'artifacts/high_floors_simulation.json').read_text(encoding='utf-8'))
    initial=json.loads((ROOT/'artifacts/high_floors_initial_simulation.json').read_text(encoding='utf-8'))
    lines=['# 03-06~09 고층 측정 결과','',f"시드 {result['seed']}. 원본 SHA-256 `{result['source_sha256']}`.",'',
           '장비 100,000개와 몬스터 100,000회 생성. 장비 330종·몬스터 150종 모두 출현했고, 원형 출현층·양수 유한 능력치·옵션 슬롯/범주·옵션 중복 금지 검사를 통과했다.',
           f"생성 결과 SHA-256: `{result['draws']['sha256']}`.",'',
           '## 일반 적 경계 비교','',
           '접두어·정예·재앙 보정을 제외한 일반 적 풀의 정확한 가중 평균과 P90이다. 일반전이 가능한 인접 비보스 층을 비교한다. 100/200/300/400층의 이론적 일반 풀 수치는 JSON에 별도로 남겼다. 정수 내림 때문에 평균의 미세 감소는 가능하다.', '',
           '| 경계 | HP 평균 변화 | ATK 평균 변화 | DEF 평균 변화 | HP P90 변화 | ATK P90 변화 | DEF P90 변화 |',
           '|---|---:|---:|---:|---:|---:|---:|']
    for a,b in ((99,101),(199,201),(299,301),(399,401),(799,801),(999,1001)):
        values=[result['boundaries'][str(b)][k][metric]/result['boundaries'][str(a)][k][metric]-1 for metric in ('mean','p90') for k in ('hp','atk','defense')]
        lines.append(f'| {a}→{b} | '+' | '.join(f'{v:+.2%}' for v in values)+' |')
    lines+=['','## 준비된 전투 표본','',
            '17개 층 × 공격·방어·회복 3빌드 × 20시드 = 1,020전. 레벨 max(30,층수÷2 내림), 레벨당 획득 가능한 능력치 3P를 STR/VIT 60/40에 투자, 스킬 포인트 레벨÷5. 같은 층·시드는 동일 장비 굴림/예산을 사용하고 스킬 투자만 달리했다. 각 슬롯 최고 해금 원형 +3과 최고 해금 복합 물약 10개, 효율 우선 정책, 위험 중단 해제. 조건을 주입한 준비 표본이며 자연 등반으로 그 장비를 확보했다는 뜻은 아니다.', '',
            '| 층 | 빌드 | 승리/20 | 승률 | 평균 턴 | 턴 P50/P90 | 평균 물약 | 평균 물약비 G | 500턴 중단 |',
            '|---:|---|---:|---:|---:|---|---:|---:|---:|']
    names={'attack':'공격','defense':'방어','recovery':'회복'}
    for r in result['encounters']:
        lines.append(f"| {r['floor']} | {names[r['build']]} | {r['wins']} | {r['win_rate']:.0%} | {r['turns_mean']:.2f} | {r['turns_p50']}/{r['turns_p90']} | {r['potions_mean']:.2f} | {r['potion_cost_mean']:.2f} | {r['stalls']} |")
    lines+=['','20시드의 승률은 5%p 단위다. 20/20 승리의 Wilson 95% 구간은 약 83.9~100%, 19/20은 약 76.4~99.1%로 표본 오차가 크다. 스킬별 사용 횟수와 사망층은 JSON에 보존한다.', '',
            '## 초기 안과 보정','',
            '초기 안은 신규 장비 추가 성장에 `(레벨-100)`을 사용했다. 최초 고층 진입 시 방어구·HP 성장이 거의 없어 110층 보스가 막혔다. 적의 100층 기준값을 낮추지 않고 신규 장비만 `계수×장비 레벨`로 보정했다. 101층 드롭이 -2레벨로 굴러도 신규 성장식을 적용한다. 기존 저장 장비의 rolled_stats는 변경하지 않는다.', '',
            '| 구간 | 초기 승리/60 | 보정 후 승리/60 |', '|---|---:|---:|']
    for floor in (110,200):
        a=sum(r['wins'] for r in initial['encounters'] if r['floor']==floor)
        b=sum(r['wins'] for r in result['encounters'] if r['floor']==floor)
        lines.append(f'| {floor}층 보스 | {a} | {b} |')
    lines+=['','초기 원자료는 탐색용 결과로 별도 보존한다. 최종판에는 보스 상태효과의 강화/약화 대상 교정도 포함된다. 이후 변경은 같은 표본을 재실행한다.', '',
            '## 실제 3,000결정 진행','',
            '시작 자원 이외 추가 장비·능력치를 주입하지 않은 기존 진행 정책을 빌드마다 3,000결정 실행했다. 이 정책이 도달한 층까지만 자연 성장 근거로 사용한다.', '',
            '| 빌드 | 최고층 | 레벨 | 승리/전투 | 사망 | 평균 완료 전투 턴 | 물약 소비 |', '|---|---:|---:|---|---:|---:|---:|']
    for build,r in result['progression'].items():
        lines.append(f"| {names[build]} | {r['highest']} | {r['level']} | {r['wins']}/{r['battles']} | {r['deaths']} | {r['mean_finished_combat_turns']:.2f} | {r['potions_used']} |")
    lines+=['','## 판정과 한계','',
            '- 03-06~09의 콘텐츠 연결·순환 성장·저장 재개·생성 유효성 기준을 검증했다. 고층 전투 전체 빌드의 준비 표본에서 진행 불가를 해소했다.',
            '- 상위 구간의 승률이 목표 60~85%보다 높다. 이는 난이도 최종 승인이나 무한 층수의 안전 보장이 아니다. 800·1,000·10,000층은 유한 수치/진행 중단 검사 표본이다.',
            '- 장비·회복 자원의 실제 확보 비용, 3~8층 보급 주기, 보스별 대응 차이와 자연 등반의 고층 도달은 03-10/12/14/16/22/23 및 경제 단계에서 이어서 검증한다.',
            '- 기본 자동 회복 정책과 보유 목록 정책은 유지했다. 신규 장비 옵션은 지원되는 OPT001~030의 슬롯·범주 교집합이며 전체 옵션 확대는 03-15다.', '',
            '재현: `.venv\\Scripts\\python.exe -m tests.simulate_high_floors`, 이어서 `.venv\\Scripts\\python.exe -m tests.report_high_floors`. UI는 오프스크린 268×861/250×400 검사다. 실제 Windows 배율·다중 모니터 수동 검수는 별개다.','']
    (ROOT/'docs/HIGH_FLOORS_REPORT.md').write_text('\n'.join(lines),encoding='utf-8')


if __name__=='__main__': run()
