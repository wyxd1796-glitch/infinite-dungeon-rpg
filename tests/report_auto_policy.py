"""Render the recorded policy experiment without rerunning the simulation."""
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def run():
    report=json.loads((ROOT/'artifacts/auto_policy_simulation.json').read_text(encoding='utf-8'))
    lines=['# 자동 전투 정책 다중 시드 보고서','',
           '2026-10-17 · 준비 조건과 목표: [BALANCE_SPEC.md](BALANCE_SPEC.md).', '',
           '20시드, 전투 5,400회 및 초기 진행 18,000결정. 아래 승률 구간은 표본 이항 Wilson 95% 구간이며 동일 시드 반복과 준비 조건에 따른 상관·모형 편향을 제거한 보장은 아니다.', '',
           '| 빌드 | 정책 | 적 | 승률 (95% 구간) | 턴 P50/P90 | 물약 합계 | MP 감소 합계 | 미종료 |',
           '|---|---|---|---|---|---:|---:|---:|']
    for row in report['encounters']:
        p,n=row['win_rate'],row['n']; z=1.96
        center=(p+z*z/(2*n))/(1+z*z/n)
        radius=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/(1+z*z/n)
        lines.append(f"| {row['build']} | {row['policy']} | {row['kind']} | {p:.1%} ({center-radius:.1%}~{center+radius:.1%}) | {row['p50']}/{row['p90']} | {row['potions']} | {row['mp_spent']} | {row['stalls']} |")
    lines+=['','## 초기 진행','', '| 빌드 | 정책 | 승리/전투 | 턴 P50/P90 | 물약 | MP 감소 | 귀환 | 골드 순증감 | 장비 드롭 | 사망 |', '|---|---|---|---|---:|---:|---:|---:|---:|---:|']
    for row in report['progression']:
        samples=row['samples']
        def total(key): return sum(r[key] for r in samples)
        lines.append(f"| {row['build']} | {row['policy']} | {total('wins')}/{total('battles')} | {row['p50']}/{row['p90']} | {total('potions_used')} | {total('mp_spent')} | {total('returns')} | {total('gold_net')} | {total('drops')} | {total('deaths')} |")
    lines+=['','## 목표 대조','', '| 표본 | 목표 | 실측 범위 |', '|---|---|---|']
    for kind,target in [('normal','P50 2~5'),('elite','P50 4~9'),('boss','P50 8~18 / 승률 60~85%')]:
        rows=[r for r in report['encounters'] if r['kind']==kind]
        lines.append(f"| {kind} | {target} | P50 {min(r['p50'] for r in rows)}~{max(r['p50'] for r in rows)} / 승률 {min(r['win_rate'] for r in rows):.1%}~{max(r['win_rate'] for r in rows):.1%} |")
    lines+=['', '## 해석과 다음 판단','',
            '- 위 표는 정책과 빌드를 같은 준비로 비교한 결과다. 모든 목표를 달성했다는 판정은 하지 않는다. 30레벨·30층 준비의 적절성부터 자연 진행 표본과 대조해야 한다.',
            '- 기본값은 호환성을 위해 물약 우선·예약 0을 유지한다. 실험의 예약 16은 비교 조건이며 기본값으로 강제하지 않는다. 정책은 사용자가 선택한다.',
            '- 초기 100결정 표본은 장기 보급 간격·10층 장비 갱신 주기·20레벨 이후 빌드 성장 확정에 부족하다. 관련 목표는 미확정으로 유지한다.',
            '- 고층 난이도와 장비 성장 수치는 이번 결과만으로 조정하지 않는다. 3단계 설계 전 장기 진행과 적정 장비 예산 검증을 추가한다.',
            '- 세부 사망층·스킬별 사용 횟수·비중과 시드별 결과는 `artifacts/auto_policy_simulation.json`에 보존한다. MP는 재생을 차감한 행동별 양수 감소량이다.', '']
    (ROOT/'docs/AUTO_POLICY_REPORT.md').write_text('\n'.join(lines),encoding='utf-8')
    print('\n'.join(lines[-14:]))

if __name__=='__main__': run()
