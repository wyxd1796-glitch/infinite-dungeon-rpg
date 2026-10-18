"""Read-only source/runtime comparison. Textual effects are never executed."""
import collections
import hashlib
import json
import re
from pathlib import Path
from core.game_engine import GameEngine

ROOT=Path(__file__).resolve().parents[1]
ID=re.compile(r'[A-Z]{2,6}\d{3}\Z')


def inspect(root=ROOT):
    data=(root/'content/source/catalogue_v4.json').read_bytes()
    source=json.loads(data)
    groups=dict(source['base_catalogue_v3']['content'])
    groups.update(source['new_content_v4'])
    groups={k:v for k,v in groups.items() if isinstance(v,list) and all(isinstance(r,dict) and 'id' in r for r in v)}
    ids=[r['id'] for rows in groups.values() for r in rows]
    duplicates=[key for key,count in collections.Counter(ids).items() if count>1]
    all_ids=set(ids)
    engine=GameEngine(root/'content',seed=20261018)
    active=collections.defaultdict(list)
    for row in engine.content.by_id.values():
        if row.get('source_id') in all_ids: active[row['source_id']].append(row['id'])
    references=[]; empty_operators=[]; operators=collections.defaultdict(list)
    def walk(value,path,owner=None):
        if isinstance(value,dict):
            owner=value.get('id',owner)
            for key,child in value.items():
                field=f'{path}.{key}'
                if key in ('operator','op'):
                    if not isinstance(child,str) or not child.strip(): empty_operators.append(dict(owner=owner,path=field,value=child))
                    else: operators[child].append(field)
                if key!='id' and isinstance(child,str) and ID.fullmatch(child):
                    references.append(dict(owner=owner,path=field,target=child,exists=child in all_ids,active=child in active))
                elif isinstance(child,list):
                    for i,item in enumerate(child):
                        if isinstance(item,str) and ID.fullmatch(item): references.append(dict(owner=owner,path=f'{field}[{i}]',target=item,exists=item in all_ids,active=item in active))
                walk(child,field,owner)
        elif isinstance(value,list):
            for i,child in enumerate(value): walk(child,f'{path}[{i}]',owner)
    for name,rows in groups.items(): walk(rows,name)
    overrides=source['base_catalogue_v3'].get('event_runtime_overrides',{})
    for key,row in overrides.items(): walk(row,'event_runtime_overrides.'+key,key)
    events=[]
    for row in groups['events']:
        choices=overrides.get(row['id'],{}).get('choice_resolution_v3',row.get('choices',[]))
        missing=[]
        for i,choice in enumerate(choices):
            if 'success_effects' not in choice: missing.append(f'{i}:success_effects')
            for field in ('cost_effects','success_effects','failure_effects'):
                for j,effect in enumerate(choice.get(field,[])):
                    if not effect.get('op'): missing.append(f'{i}:{field}[{j}].op')
        events.append(dict(id=row['id'],runtime=active.get(row['id'],[]),override=row['id'] in overrides,
                           choice_count=len(choices),missing=missing,
                           planned_stage=3 if int(row['id'][3:])<=100 else 5 if int(row['id'][3:])<=150 else 7))
    empty_by_id={r['owner'] for r in empty_operators}
    records=[dict(id=r['id'],group=name,name=r.get('name'),runtime_ids=active.get(r['id'],[]),
                  explicit_empty_operator=r['id'] in empty_by_id)
             for name,rows in groups.items() for r in rows]
    selection=engine.content.catalogue
    return dict(source_sha256=hashlib.sha256(data).hexdigest(),expected_sha256=selection['source_sha256'],
                total=len(ids),duplicates=duplicates,loader_errors=engine.content.errors,
                groups={name:dict(source=len(rows),connected=sum(r['id'] in active for r in rows),
                                 unconnected_ids=[r['id'] for r in rows if r['id'] not in active]) for name,rows in groups.items()},
                records=records,references=references,missing_references=[r for r in references if not r['exists']],
                inactive_references=[r for r in references if r['exists'] and not r['active']],
                empty_operators=empty_operators,operator_occurrences=dict(operators),events=events,
                effects=[dict(id=r['id'],name=r['name'],operator=r.get('operator'),trigger=r.get('trigger'),
                              magnitude=r.get('magnitude'),duration=r['duration_turns'],stack=r['stack_rule'],connected=r['id'] in active) for r in groups['effects']],
                option_operators=dict(collections.Counter(r.get('operator','legacy-by-id') for r in groups['options'])),
                option_slots=dict(collections.Counter(r['slot_restriction'] for r in groups['options'])),
                phase2_overrides=[dict(source_id=r['source_id'],runtime=r) for kind in ('skills','events') for r in engine.content[kind] if r.get('phase2')])


def write_report(result,root=ROOT):
    (root/'artifacts/phase3_audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    lines=['# 3단계 원본·실행 정의 대조 결과','', '검사일: 2026-10-19. 03-11 구현 후 갱신. 생성 도구: `tests/audit_phase3.py`. 효과 문자열은 실행하거나 수치로 해석하지 않는다.', '',
           f"원본 {result['total']}개, 중복 ID {len(result['duplicates'])}개, 로더 오류 {len(result['loader_errors'])}개. SHA-256 `{result['source_sha256']}`.", '',
           '| 분류 | 원본 | 명시적 출처 연결 | 미연결 |', '|---|---:|---:|---:|']
    for name,row in result['groups'].items(): lines.append(f"| {name} | {row['source']} | {row['connected']} | {len(row['unconnected_ids'])} |")
    lines+=['', '명시적 출처 연결은 실행 정의가 있다는 뜻이며 각 후속 단계 검수의 완성을 뜻하지 않는다. 기존 스킬 5개는 원본 ID를 직접 쓰지 않아 이 수에 포함하지 않는다. 현재 카탈로그 765개와 phase2 28개, 총 793개다. 고층 조우·보상 경로는 HIGH_FLOORS.md를 따른다. 장비 옵션 확대·재료 제작은 후속 과제다.', '',
            '## 명시적인 빈 연산자와 참조','',
            f"`operator`/`op` 필드가 존재하지만 빈 항목: {len(result['empty_operators'])}개. 정확히 ID 형태인 문자열 참조 중 원본에 없는 대상: {len(result['missing_references'])}개, 원본에 있으나 실행 미연결 대상 참조: {len(result['inactive_references'])}개.", '',
            '검사 범위는 22개 콘텐츠 분류와 event_runtime_overrides다. 상위 운영 규칙·reference_index·메타데이터는 이 참조 집계에서 제외한다. 참조 검사는 ID 전체 문자열과 배열 항목만 검사한다. 설명 문장 안의 이름·ID나 모든 사용자 정의 의존성을 추론하지 않는다. 필드 자체가 없는 기존 텍스트 정의는 빈 연산자로 세지 않는다. 전수 경로와 ID는 JSON에 보존한다.']
    for row in result['empty_operators']: lines.append(f"- `{row['path']}` ({row['owner']})")
    for row in result['missing_references']: lines.append(f"- 없는 참조: `{row['path']}` → `{row['target']}`")
    lines+=['','## 현재 실행 미연결 효과','', '| ID | 이름 | 원본 연산자 | 시점 | 수치 | 기간 | 중첩 |', '|---|---|---|---|---:|---:|---|']
    for row in (r for r in result['effects'] if not r['connected']):
        lines.append(f"| {row['id']} | {row['name']} | {row['operator']} | {row['trigger']} | {row['magnitude']} | {row['duration']} | {row['stack']} |")
    lines+=['','EF001~015는 기존 ID 분기 처리다. EF016~040은 명시적 실행 정의와 저장 검증을 연결했다. 전체 효과는 [PHASE3_EFFECTS.md](PHASE3_EFFECTS.md)의 검증 범위를 따른다. 03-06~09에서 고층 몬스터·환경·보스 공급 경로를 연결했으며 옵션·스킬 공급 확대는 후속 작업이다.', '',
            '## 이벤트의 세 가지 실행 정의','',
            f"원본 이벤트 {len(result['events'])}개 중 runtime override {sum(r['override'] for r in result['events'])}개. override를 우선 적용해도 구조화된 성공 효과/연산자 점검에 걸리는 이벤트는 {sum(bool(r['missing']) for r in result['events'])}개다.", '',
            '- 원본 `choices` → 원본 `event_runtime_overrides` → 승인된 phase2 실행 팩을 별개로 비교한다. 현재 phase2 20개는 승인된 실행 팩을 우선 보존한다.',
            '- EVT001~100은 3단계, EVT101~150은 5단계, EVT151~200은 7단계다. 3단계 범위 100개를 원본 전체 개수로 오해하지 않는다.',
            '- 누락 검사 통과는 비용·보상 단위, 대상, 성공/실패 의미까지 승인됐다는 뜻이 아니다. 모든 선택의 비용·실패·진행도·지급 1회 처리는 별도 검증한다.', '',
            '## 옵션 데이터 형식','', '| 연산자 | 개수 |', '|---|---:|']
    for key,count in result['option_operators'].items(): lines.append(f'| {key or "(빈 값)"} | {count} |')
    lines+=['', '| 슬롯 원문 | 개수 |', '|---|---:|']
    for key,count in result['option_slots'].items(): lines.append(f'| {key} | {count} |')
    lines+=['', '현재 OPT001~030은 ID 순서에 따른 능력치 매핑이다. OPT031 이후는 operator만으로 대상 능력치·원소·발동 조건이 확정되지 않는다. 별도 명시적 매핑이 필요하다.', '',
            '## 검토 결정','', '[PHASE3_GAPS.md](PHASE3_GAPS.md)의 충돌·보완 규칙·담당 작업을 따른다. 이 감사는 콘텐츠 활성화나 게임 수치 변경을 수행하지 않는다.','']
    (root/'docs/PHASE3_AUDIT.md').write_text('\n'.join(lines),encoding='utf-8')


if __name__=='__main__':
    result=inspect(); write_report(result)
    print(json.dumps({k:result[k] for k in ('total','duplicates','loader_errors')},ensure_ascii=False))
    print('empty operators:',len(result['empty_operators']),'missing references:',len(result['missing_references']))
