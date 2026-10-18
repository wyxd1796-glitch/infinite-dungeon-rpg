"""Validate the full experiment matrix and publish compact, reproducible evidence."""
import collections
import json
import math
import statistics
import zipfile
from tests.simulate_phase2 import ROOT, BUILDS
from tests.simulate_long_term import source_fingerprints


def percentile(values,p):
    return sorted(values)[max(0,math.ceil(len(values)*p)-1)] if values else None


def summarize(rows):
    turns=[x for r in rows for x in r['combat_turn_samples']]
    trips=[t for r in rows for t in r['long_term']['trips']]
    returns=[t for t in trips if t['reason']=='return']
    spent=collections.Counter(); earned=collections.Counter(); uses=collections.Counter(); death_floors=collections.Counter()
    for row in rows:
        spent.update(row['long_term']['spent']); earned.update(row['long_term']['earned'])
        uses.update(row['skill_uses']); death_floors.update(row['death_floors'])
    wins=sum(r['wins'] for r in rows); battles=sum(r['battles'] for r in rows)
    return dict(samples=len(rows),decisions=sum(r['decisions'] for r in rows),wins=wins,battles=battles,
                win_rate=wins/max(1,battles),turn_p50=percentile(turns,.5),turn_p90=percentile(turns,.9),
                highest_min=min(r['highest'] for r in rows),highest_median=statistics.median(r['highest'] for r in rows),highest_max=max(r['highest'] for r in rows),
                level_median=statistics.median(r['level'] for r in rows),potions=sum(r['potions_used'] for r in rows),mp_spent=sum(r['mp_spent'] for r in rows),
                spent=dict(spent),earned=dict(earned),gold_net=sum(r['gold_net'] for r in rows),
                returns=len(returns),deaths=sum(r['deaths'] for r in rows),death_floors=dict(death_floors),
                return_floor_advance_p50=percentile([t['completed_floors'] for t in returns],.5),
                return_floor_advance_p90=percentile([t['completed_floors'] for t in returns],.9),
                return_new_floor_p50=percentile([t['new_floors'] for t in returns],.5),
                replaces=sum(sum(r['long_term']['replacements_by_highest_band'].values()) for r in rows),
                replacement_counts=[sum(r['long_term']['replacements_by_highest_band'].values()) for r in rows],
                replacement_bands=[r['long_term']['replacements_by_highest_band'] for r in rows],
                drops=sum(r['drops'] for r in rows),skill_uses=dict(uses),
                skill_shares={k:v/max(1,sum(uses.values())) for k,v in uses.items()},
                unfinished_trips=sum(r['long_term']['unfinished_trip'] is not None for r in rows))


def run():
    folder=ROOT/'artifacts/long_term'; all_rows=[]; paths=[]; groups=[]
    for prepared in (False,True):
        for build in BUILDS:
            for policy in (('efficient',) if prepared else ('potion_first','skill_first','efficient')):
                rows=[]
                for seed in range(20261017,20261037):
                    path=folder/f'{"funded_" if prepared else ""}{build}_{policy}_{seed}_3000.json'
                    row=json.loads(path.read_text(encoding='utf-8'))
                    assert row['seed']==seed and row['build']==build and row['policy']==policy and row['decisions']==3000
                    assert row['long_term']['gold_reconciliation']
                    assert row['gold_net']==sum(row['long_term']['earned'].values())-sum(row['long_term']['spent'].values())
                    rows.append(row); paths.append(path)
                groups.append(dict(preparation='funded' if prepared else 'legacy',build=build,policy=policy,**summarize(rows)))
                all_rows+=rows
    manifest=source_fingerprints()
    manifest_path=folder/'manifest.json'
    if manifest_path.exists():
        assert json.loads(manifest_path.read_text(encoding='utf-8'))==manifest, '측정 코드와 출처 해시 불일치'
    else:
        # Initial audit added provenance guarding after identical-rule samples started.
        manifest_path.write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    result=dict(seeds=20,decisions_per_sample=3000,total_samples=len(all_rows),total_decisions=sum(r['decisions'] for r in all_rows),groups=groups,source_sha256=manifest)
    (ROOT/'artifacts/long_term_summary.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    with zipfile.ZipFile(ROOT/'artifacts/long_term_samples.zip','w',zipfile.ZIP_DEFLATED) as archive:
        for path in paths: archive.write(path,path.name)
        archive.write(manifest_path,'manifest.json')
    lines=['# 장기 진행 측정과 2단계 수치 결정','', '2026-10-17 · 20시드 × 3빌드 × 기존 준비 3정책 및 자금 기반 준비 1정책 × 3,000결정 = **240회 실행, 720,000결정**. 모든 표본의 골드 흐름을 잔액과 대조했다.', '',
           '## 전투·성장 결과','', '| 준비 | 빌드 | 정책 | 최고층 최소/중앙/최대 | 레벨 중앙 | 승률 | 턴 P50/P90 | 물약 | 사망 |', '|---|---|---|---|---:|---|---|---:|---:|']
    for r in groups:
        lines.append(f"| {r['preparation']} | {r['build']} | {r['policy']} | {r['highest_min']}/{r['highest_median']:g}/{r['highest_max']} | {r['level_median']:g} | {r['wins']}/{r['battles']} ({r['win_rate']:.1%}) | {r['turn_p50']}/{r['turn_p90']} | {r['potions']} | {r['deaths']} |")
    lines+=['','## 준비 비용·보급·교체','', '| 준비 | 빌드 | 정책 | 구매 G | 휴식 G | 강화 G | 순증감 G | 귀환 | 귀환 간 층 이동 P50/P90 | 실제 교체 |', '|---|---|---|---:|---:|---:|---:|---:|---|---:|']
    for r in groups:
        s=r['spent']
        lines.append(f"| {r['preparation']} | {r['build']} | {r['policy']} | {s.get('buy',0)} | {s.get('rest',0)} | {s.get('enhance',0)} | {r['gold_net']} | {r['returns']} | {r['return_floor_advance_p50']}/{r['return_floor_advance_p90']} | {r['replaces']} |")
    lines+=['','## 測정 정의와 한계'.replace('測','측'),'',
            '- 비용과 수량은 20시드 합계다. 구매·휴식·강화 비용은 성공한 실제 명령의 골드 감소다. 전투/이벤트 중 획득과 사망 손실은 명령 단위 순변화로 분류되므로 전체 수입·손실의 총액과 혼동하지 않는다.',
            '- 층 이동은 출발 후 `next`로 이동한 횟수다. 같은 층에서 싸우다 돌아오면 0이며, 마지막 완료 층에서 바로 귀환하면 그 층은 이동 횟수에 포함되지 않는다. 사망으로 끝난 여정과 실험 종료 시 미완료 여정은 귀환 주기에서 제외한다.',
            '- 장비 교체는 기존 착용 슬롯이 있는 상태에서 다른 장비를 실제 장착한 횟수다. 최초 장착은 제외한다. 장비 가치 함수로 선택한 대용 지표이며, 사람의 빌드 선택 가치나 최초 10층 구간 내 교체 달성률을 뜻하지 않는다. 최고 도달층 구간별 횟수는 원자료에 있다.',
            '- 기존 준비는 레벨업 포인트가 생겨도 귀환하고 강화 재료를 판매한다. 자금 기반 준비는 포인트만으로 귀환하지 않고, 보유 재료와 실제 잔액으로 +3까지 강화하며 100G를 남긴다. 상점에서 해금된 HP/MP 물약을 최대 3개까지 보충한다. 무료 장비·재화·경험치는 지급하지 않는다.',
            '- 자금 기반 장비 점수는 공격/방어 1, HP 0.1, MP 0.2, STR 2, VIT 1.5, INT 1, DEX/LUK 0.2, 기타 비율 옵션 20의 가중합이다. 최적 빌드 판정기가 아니다. 비교군은 준비 행동 여러 가지가 함께 달라져 원인을 하나로 단정할 수 없다.',
            '- 자동 중단 뒤 보스전에서 수동 공격을 이어가는 기존 시험 운용을 유지했다. 실제 사용자의 안전 중단·귀환 성향과 다르다. 모든 승률은 해당 운용에 대한 값이다.',
            '- 물약 소비·MP 감소·사망층·스킬 사용률·여정별 원자료는 ZIP에, 집계와 소스 해시는 JSON에 저장한다. 실사용 저장과 설정은 접근하지 않는다.', '',
            '## 재현','', '```powershell', '.\\.venv\\Scripts\\python.exe -m tests.simulate_long_term --all', '.\\.venv\\Scripts\\python.exe -m tests.report_long_term', '```','',
            '완료 표본은 `artifacts/long_term/`에서 재사용한다. 게임 규칙이나 시험 준비를 바꾸어 비교할 때에는 이 폴더를 별도 이름으로 보존한 뒤 새로운 폴더에서 실행한다. 결과 집계는 240개 파일의 시드·정책·빌드·결정 수·골드 보존을 모두 검사한다.','']
    (ROOT/'docs/LONG_TERM_REPORT.md').write_text('\n'.join(lines),encoding='utf-8')
    print(json.dumps({'samples':len(all_rows),'decisions':result['total_decisions'],'groups':len(groups)},ensure_ascii=False))


if __name__=='__main__': run()
