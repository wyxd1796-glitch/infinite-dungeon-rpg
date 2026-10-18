# INFINITE 전체 콘텐츠 대장 — 원본 1,305개

작성일: 2026-10-17 · 현재 기준: 게임 1.2.0 · 관련 문서: [상세 기획](MASTER_ROADMAP.md), [실행 체크리스트](ROADMAP_TASKS.md)

원본 파일의 모든 정의를 ID별로 열거한 기획 대장이다. 현재 연결은 selection.json과 phase2 실행 정의의 source_id를 대조했다. 원본 스킬 5개는 별도의 기존 구현과 이름·역할이 대응하므로 원본 수치까지 동일하다는 뜻으로 표시하지 않는다.

기획 단계는 구현 착수 순서다. 후속 기능에 의존하는 항목은 해당 의존 기능이 끝나기 전 활성화하지 않는다. 연결 상태가 이미 있는 항목도 뒤 단계의 성장·조합 회귀 검수가 필요하다. 최종 판정 칸은 향후 실행 연결/통합/제외 및 증빙 링크를 작성하는 칸이며 현재는 미판정이다.

원본 SHA-256: `01034289e9549a23416d085480c667ef84097d772b4a7a293a0e8559f33ed7eb`. 원본 JSON은 수정하지 않았다.

2026-10-18 03-01 감사에서 22분류·1,305개와 명시적 연결 288개를 재확인했다. [전수 대조](PHASE3_AUDIT.md)와 [충돌·보완 규칙](PHASE3_GAPS.md)에 실행 미연결 효과·옵션·참조를 기록했다. 이번 감사로 미연결 항목이 활성화되거나 최종 구현 판정이 바뀌지는 않는다.

## 분류별 합계

| 분류 | 원본 개수 | 현재 원본 ID 연결 | 기존 별도 대응 | 주요 후속 단계 |
|---|---:|---:|---:|---|
| 공통 효과 | 40 | 40 | 0 | 3 |
| 몬스터 | 150 | 150 | 0 | 3 |
| 보스 | 40 | 40 | 0 | 3 |
| 접두어 | 50 | 20 | 0 | 3 |
| 장비 | 330 | 330 | 0 | 3 |
| 장비 옵션 | 100 | 30 | 0 | 3 |
| 소비품 | 50 | 30 | 0 | 3 |
| 재료 | 60 | 60 | 0 | 3·4 |
| 이벤트 | 200 | 20 | 0 | 3→5→7 |
| 환경 | 30 | 30 | 0 | 3 |
| 층 유형 | 5 | 5 | 0 | 3 |
| 스킬 | 70 | 8 | 5 | 5 |
| 유물 | 24 | 0 | 0 | 6 |
| 현상금 | 24 | 0 | 0 | 7 |
| 직업 트리 | 45 | 0 | 0 | 5 |
| 직업 | 5 | 0 | 0 | 5 |
| 전직 | 10 | 0 | 0 | 5 |
| 계승 | 10 | 0 | 0 | 8 |
| 특수 던전 | 6 | 0 | 0 | 7 |
| 시설 | 6 | 0 | 0 | 7 |
| 칭호 | 20 | 0 | 0 | 7 |
| 도전 | 30 | 0 | 0 | 7 |
| **합계** | **1305** | **763** | **5** | 1~10단계에서 검수 |

현재 원본 ID 연결 313개 = 최초 카탈로그 260개 + 추가 공통 효과 25개 + 2차 스킬 8개 + 2차 이벤트 20개. 이 집계에 기존 독립 이벤트 10개·업적 7개는 포함하지 않는다. 남은 원본 992개에는 기존 별도 스킬 대응 5개가 포함된다.

## 공통 효과 — 40개

| 원본 ID | 이름 | 현재 상태·연결 ID | 예정 단계 | 필수 연결·검수 | 최종 판정/증빙 |
|---|---|---|---|---|---|
| EF001 | 중독 | 1차 연결: catalogue.v3.EF001 | 3 | 효과 시점·중첩·상한·복원 | [효과·고층 공급 연결](HIGH_FLOORS.md) |
| EF002 | 화상 | 1차 연결: catalogue.v3.EF002 | 3 | 효과 시점·중첩·상한·복원 | [효과·고층 공급 연결](HIGH_FLOORS.md) |
| EF003 | 출혈 | 1차 연결: catalogue.v3.EF003 | 3 | 효과 시점·중첩·상한·복원 | [효과·고층 공급 연결](HIGH_FLOORS.md) |
| EF004 | 기절 | 1차 연결: catalogue.v3.EF004 | 3 | 효과 시점·중첩·상한·복원 | [효과·고층 공급 연결](HIGH_FLOORS.md) |
| EF005 | 빙결 | 1차 연결: catalogue.v3.EF005 | 3 | 효과 시점·중첩·상한·복원 | [효과·고층 공급 연결](HIGH_FLOORS.md) |
| EF006 | 침묵 | 1차 연결: catalogue.v3.EF006 | 3 | 효과 시점·중첩·상한·복원 | [효과·고층 공급 연결](HIGH_FLOORS.md) |
| EF007 | 공격력 감소 | 1차 연결: catalogue.v3.EF007 | 3 | 효과 시점·중첩·상한·복원 | [효과·고층 공급 연결](HIGH_FLOORS.md) |
| EF008 | 방어력 감소 | 1차 연결: catalogue.v3.EF008 | 3 | 효과 시점·중첩·상한·복원 | [효과·고층 공급 연결](HIGH_FLOORS.md) |
| EF009 | 저주 | 1차 연결: catalogue.v3.EF009 | 3 | 효과 시점·중첩·상한·복원 | [효과·고층 공급 연결](HIGH_FLOORS.md) |
| EF010 | 공격력 증가 | 1차 연결: catalogue.v3.EF010 | 3 | 효과 시점·중첩·상한·복원 | [효과·고층 공급 연결](HIGH_FLOORS.md) |
| EF011 | 방어력 증가 | 1차 연결: catalogue.v3.EF011 | 3 | 효과 시점·중첩·상한·복원 | [효과·고층 공급 연결](HIGH_FLOORS.md) |
| EF012 | 신속 | 1차 연결: catalogue.v3.EF012 | 3 | 효과 시점·중첩·상한·복원 | [효과·고층 공급 연결](HIGH_FLOORS.md) |
| EF013 | 흡혈 | 1차 연결: catalogue.v3.EF013 | 3 | 효과 시점·중첩·상한·복원 | [효과·고층 공급 연결](HIGH_FLOORS.md) |
| EF014 | 재생 | 1차 연결: catalogue.v3.EF014 | 3 | 효과 시점·중첩·상한·복원 | [효과·고층 공급 연결](HIGH_FLOORS.md) |
| EF015 | 피해 반사 | 1차 연결: catalogue.v3.EF015 | 3 | 효과 시점·중첩·상한·복원 | [효과·고층 공급 연결](HIGH_FLOORS.md) |
| EF016 | 감전 | 실행 연결: catalogue.v3.EF016 | 3 | 효과 시점·중첩·상한·복원 | [효과·고층 공급 연결](HIGH_FLOORS.md) |
| EF017 | 동상 | 실행 연결: catalogue.v3.EF017 | 3 | 효과 시점·중첩·상한·복원 | [효과·고층 공급 연결](HIGH_FLOORS.md) |
| EF018 | 부식 | 실행 연결: catalogue.v3.EF018 | 3 | 효과 시점·중첩·상한·복원 | [효과·고층 공급 연결](HIGH_FLOORS.md) |
| EF019 | 독성 폭발 | 실행 연결: catalogue.v3.EF019 | 3 | 효과 시점·중첩·상한·복원 | [효과·고층 공급 연결](HIGH_FLOORS.md) |
| EF020 | 암흑 | 실행 연결: catalogue.v3.EF020 | 3 | 효과 시점·중첩·상한·복원 | [효과·고층 공급 연결](HIGH_FLOORS.md) |
| EF021 | 무장 해제 | 실행 연결: catalogue.v3.EF021 | 3 | 효과 시점·중첩·상한·복원 | [효과·고층 공급 연결](HIGH_FLOORS.md) |
| EF022 | 혼란 | 실행 연결: catalogue.v3.EF022 | 3 | 효과 시점·중첩·상한·복원 | [효과·고층 공급 연결](HIGH_FLOORS.md) |
| EF023 | 속박 | 실행 연결: catalogue.v3.EF023 | 3 | 효과 시점·중첩·상한·복원 | [효과·고층 공급 연결](HIGH_FLOORS.md) |
| EF024 | 취약 | 실행 연결: catalogue.v3.EF024 | 3 | 효과 시점·중첩·상한·복원 | [효과·고층 공급 연결](HIGH_FLOORS.md) |
| EF025 | 둔화 | 실행 연결: catalogue.v3.EF025 | 3 | 효과 시점·중첩·상한·복원 | [효과·고층 공급 연결](HIGH_FLOORS.md) |
| EF026 | 마력 봉쇄 | 실행 연결: catalogue.v3.EF026 | 3 | 효과 시점·중첩·상한·복원 | [효과·고층 공급 연결](HIGH_FLOORS.md) |
| EF027 | 영혼 침식 | 실행 연결: catalogue.v3.EF027 | 3 | 효과 시점·중첩·상한·복원 | [효과·고층 공급 연결](HIGH_FLOORS.md) |
| EF028 | 정신 약화 | 실행 연결: catalogue.v3.EF028 | 3 | 효과 시점·중첩·상한·복원 | [효과·고층 공급 연결](HIGH_FLOORS.md) |
| EF029 | 집중 강화 | 실행 연결: catalogue.v3.EF029 | 3 | 효과 시점·중첩·상한·복원 | [효과·고층 공급 연결](HIGH_FLOORS.md) |
| EF030 | 강인함 | 실행 연결: catalogue.v3.EF030 | 3 | 효과 시점·중첩·상한·복원 | [효과·고층 공급 연결](HIGH_FLOORS.md) |
| EF031 | 행운 | 실행 연결: catalogue.v3.EF031 | 3 | 효과 시점·중첩·상한·복원 | [효과·고층 공급 연결](HIGH_FLOORS.md) |
| EF032 | 마력 증폭 | 실행 연결: catalogue.v3.EF032 | 3 | 효과 시점·중첩·상한·복원 | [효과·고층 공급 연결](HIGH_FLOORS.md) |
| EF033 | 철갑 보호 | 실행 연결: catalogue.v3.EF033 | 3 | 효과 시점·중첩·상한·복원 | [효과·고층 공급 연결](HIGH_FLOORS.md) |
| EF034 | 급속 치유 | 실행 연결: catalogue.v3.EF034 | 3 | 효과 시점·중첩·상한·복원 | [효과·고층 공급 연결](HIGH_FLOORS.md) |
| EF035 | 마나 흡수 | 실행 연결: catalogue.v3.EF035 | 3 | 효과 시점·중첩·상한·복원 | [효과·고층 공급 연결](HIGH_FLOORS.md) |
| EF036 | 치명 집중 | 실행 연결: catalogue.v3.EF036 | 3 | 효과 시점·중첩·상한·복원 | [효과·고층 공급 연결](HIGH_FLOORS.md) |
| EF037 | 보호 결계 | 실행 연결: catalogue.v3.EF037 | 3 | 효과 시점·중첩·상한·복원 | [효과·고층 공급 연결](HIGH_FLOORS.md) |
| EF038 | 응보 | 실행 연결: catalogue.v3.EF038 | 3 | 효과 시점·중첩·상한·복원 | [효과·고층 공급 연결](HIGH_FLOORS.md) |
| EF039 | 최후의 저항 | 실행 연결: catalogue.v3.EF039 | 3 | 효과 시점·중첩·상한·복원 | [효과·고층 공급 연결](HIGH_FLOORS.md) |
| EF040 | 황금 축복 | 실행 연결: catalogue.v3.EF040 | 3 | 효과 시점·중첩·상한·복원 | [효과·고층 공급 연결](HIGH_FLOORS.md) |

## 몬스터 — 150개

| 원본 ID | 이름 | 현재 상태·연결 ID | 예정 단계 | 필수 연결·검수 | 최종 판정/증빙 |
|---|---|---|---|---|---|
| MON001 | 슬라임 | 실행 연결: catalogue.v3.MON001 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON002 | 늑대 | 실행 연결: catalogue.v3.MON002 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON003 | 박쥐 | 실행 연결: catalogue.v3.MON003 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON004 | 거대쥐 | 실행 연결: catalogue.v3.MON004 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON005 | 그림자 표범 | 실행 연결: catalogue.v3.MON005 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON006 | 고블린 | 실행 연결: catalogue.v3.MON006 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON007 | 고블린 궁수 | 실행 연결: catalogue.v3.MON007 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON008 | 오크 | 실행 연결: catalogue.v3.MON008 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON009 | 오크 전사 | 실행 연결: catalogue.v3.MON009 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON010 | 트롤 | 실행 연결: catalogue.v3.MON010 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON011 | 해골 병사 | 실행 연결: catalogue.v3.MON011 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON012 | 좀비 | 실행 연결: catalogue.v3.MON012 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON013 | 망령 | 실행 연결: catalogue.v3.MON013 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON014 | 구울 | 실행 연결: catalogue.v3.MON014 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON015 | 리치의 하수인 | 실행 연결: catalogue.v3.MON015 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON016 | 거대 거미 | 실행 연결: catalogue.v3.MON016 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON017 | 독전갈 | 실행 연결: catalogue.v3.MON017 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON018 | 식인꽃 | 실행 연결: catalogue.v3.MON018 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON019 | 가시 덩굴 | 실행 연결: catalogue.v3.MON019 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON020 | 맹독 벌레 | 실행 연결: catalogue.v3.MON020 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON021 | 화염 정령 | 실행 연결: catalogue.v3.MON021 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON022 | 물 정령 | 실행 연결: catalogue.v3.MON022 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON023 | 얼음 정령 | 실행 연결: catalogue.v3.MON023 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON024 | 바람 정령 | 실행 연결: catalogue.v3.MON024 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON025 | 대지 정령 | 실행 연결: catalogue.v3.MON025 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON026 | 돌 골렘 | 실행 연결: catalogue.v3.MON026 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON027 | 철 골렘 | 실행 연결: catalogue.v3.MON027 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON028 | 마력 인형 | 실행 연결: catalogue.v3.MON028 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON029 | 고대 파수병 | 실행 연결: catalogue.v3.MON029 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON030 | 수정 골렘 | 실행 연결: catalogue.v3.MON030 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON031 | 임프 | 실행 연결: catalogue.v3.MON031 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON032 | 하급 악마 | 실행 연결: catalogue.v3.MON032 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON033 | 마족 전사 | 실행 연결: catalogue.v3.MON033 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON034 | 서큐버스 | 실행 연결: catalogue.v3.MON034 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON035 | 지옥 사냥개 | 실행 연결: catalogue.v3.MON035 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON036 | 심연 촉수 | 실행 연결: catalogue.v3.MON036 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON037 | 공허 추적자 | 실행 연결: catalogue.v3.MON037 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON038 | 타락한 기사 | 실행 연결: catalogue.v3.MON038 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON039 | 혼돈의 눈 | 실행 연결: catalogue.v3.MON039 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON040 | 심연 포식자 | 실행 연결: catalogue.v3.MON040 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON041 | 늑대인간 정찰병 | 실행 연결: catalogue.v3.MON041 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON042 | 곰전사 | 실행 연결: catalogue.v3.MON042 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON043 | 호랑이 주술사 | 실행 연결: catalogue.v3.MON043 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON044 | 여우 암살자 | 실행 연결: catalogue.v3.MON044 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON045 | 멧돼지 투사 | 실행 연결: catalogue.v3.MON045 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON046 | 표범 추격자 | 실행 연결: catalogue.v3.MON046 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON047 | 매눈 궁수 | 실행 연결: catalogue.v3.MON047 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON048 | 사자 수호병 | 실행 연결: catalogue.v3.MON048 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON049 | 하이에나 약탈자 | 실행 연결: catalogue.v3.MON049 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON050 | 수인 대전사 | 실행 연결: catalogue.v3.MON050 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON051 | 검은 신도 | 실행 연결: catalogue.v3.MON051 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON052 | 가면 제사장 | 실행 연결: catalogue.v3.MON052 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON053 | 이단 사냥꾼 | 실행 연결: catalogue.v3.MON053 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON054 | 금기술사 | 실행 연결: catalogue.v3.MON054 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON055 | 광신도 전사 | 실행 연결: catalogue.v3.MON055 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON056 | 기도하는 광인 | 실행 연결: catalogue.v3.MON056 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON057 | 피의 집행자 | 실행 연결: catalogue.v3.MON057 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON058 | 봉인 해제자 | 실행 연결: catalogue.v3.MON058 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON059 | 부패한 사제 | 실행 연결: catalogue.v3.MON059 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON060 | 심판의 전도자 | 실행 연결: catalogue.v3.MON060 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON061 | 새끼 와이번 | 실행 연결: catalogue.v3.MON061 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON062 | 비늘 파수꾼 | 실행 연결: catalogue.v3.MON062 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON063 | 화염 드레이크 | 실행 연결: catalogue.v3.MON063 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON064 | 서리 드레이크 | 실행 연결: catalogue.v3.MON064 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON065 | 폭풍 비룡 | 실행 연결: catalogue.v3.MON065 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON066 | 흑비늘 사냥꾼 | 실행 연결: catalogue.v3.MON066 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON067 | 용혈 광전사 | 실행 연결: catalogue.v3.MON067 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON068 | 고대 도마뱀 | 실행 연결: catalogue.v3.MON068 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON069 | 수정 와이번 | 실행 연결: catalogue.v3.MON069 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON070 | 황혼 용기사 | 실행 연결: catalogue.v3.MON070 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON071 | 고철 파수기 | 실행 연결: catalogue.v3.MON071 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON072 | 증기 보병 | 실행 연결: catalogue.v3.MON072 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON073 | 톱날 인형 | 실행 연결: catalogue.v3.MON073 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON074 | 강철 수색기 | 실행 연결: catalogue.v3.MON074 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON075 | 전격 포탑 | 실행 연결: catalogue.v3.MON075 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON076 | 자동 수리기 | 실행 연결: catalogue.v3.MON076 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON077 | 마도 장갑병 | 실행 연결: catalogue.v3.MON077 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON078 | 분쇄 기갑 | 실행 연결: catalogue.v3.MON078 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON079 | 시계태엽 처형자 | 실행 연결: catalogue.v3.MON079 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON080 | 제어핵 수호병 | 실행 연결: catalogue.v3.MON080 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON081 | 깊은 물 해파리 | 실행 연결: catalogue.v3.MON081 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON082 | 산호 전사 | 실행 연결: catalogue.v3.MON082 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON083 | 아귀 사냥꾼 | 실행 연결: catalogue.v3.MON083 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON084 | 거대 갯지렁이 | 실행 연결: catalogue.v3.MON084 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON085 | 심해 문어 | 실행 연결: catalogue.v3.MON085 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON086 | 해골 어인 | 실행 연결: catalogue.v3.MON086 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON087 | 심연 해마 | 실행 연결: catalogue.v3.MON087 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON088 | 조개 포식자 | 실행 연결: catalogue.v3.MON088 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON089 | 파도 정령수 | 실행 연결: catalogue.v3.MON089 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON090 | 바다 무덤지기 | 실행 연결: catalogue.v3.MON090 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON091 | 포자 벌레 | 실행 연결: catalogue.v3.MON091 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON092 | 버섯 투사 | 실행 연결: catalogue.v3.MON092 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON093 | 균사 추적자 | 실행 연결: catalogue.v3.MON093 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON094 | 부패 이끼수 | 실행 연결: catalogue.v3.MON094 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON095 | 포자 투척자 | 실행 연결: catalogue.v3.MON095 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON096 | 감염된 곰 | 실행 연결: catalogue.v3.MON096 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON097 | 독버섯 기사 | 실행 연결: catalogue.v3.MON097 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON098 | 균핵 수호자 | 실행 연결: catalogue.v3.MON098 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON099 | 잠복 포식균 | 실행 연결: catalogue.v3.MON099 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON100 | 군락 지배체 | 실행 연결: catalogue.v3.MON100 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON101 | 모래 도적 | 실행 연결: catalogue.v3.MON101 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON102 | 사막 맹독뱀 | 실행 연결: catalogue.v3.MON102 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON103 | 먼지 정령 | 실행 연결: catalogue.v3.MON103 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON104 | 유리 전갈 | 실행 연결: catalogue.v3.MON104 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON105 | 사구 방랑자 | 실행 연결: catalogue.v3.MON105 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON106 | 모래 미이라 | 실행 연결: catalogue.v3.MON106 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON107 | 바람 모래벌레 | 실행 연결: catalogue.v3.MON107 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON108 | 태양 이교도 | 실행 연결: catalogue.v3.MON108 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON109 | 메마른 기사 | 실행 연결: catalogue.v3.MON109 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON110 | 사막의 매복자 | 실행 연결: catalogue.v3.MON110 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON111 | 광석 구더기 | 실행 연결: catalogue.v3.MON111 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON112 | 수정 박쥐 | 실행 연결: catalogue.v3.MON112 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON113 | 철광 파먹이 | 실행 연결: catalogue.v3.MON113 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON114 | 보석 지네 | 실행 연결: catalogue.v3.MON114 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON115 | 마력 광부 | 실행 연결: catalogue.v3.MON115 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON116 | 암석 소환사 | 실행 연결: catalogue.v3.MON116 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON117 | 광맥 수호자 | 실행 연결: catalogue.v3.MON117 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON118 | 동굴 석화수 | 실행 연결: catalogue.v3.MON118 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON119 | 빛나는 수정인형 | 실행 연결: catalogue.v3.MON119 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON120 | 심층 파쇄자 | 실행 연결: catalogue.v3.MON120 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON121 | 별빛 망령 | 실행 연결: catalogue.v3.MON121 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON122 | 천문 파수병 | 실행 연결: catalogue.v3.MON122 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON123 | 유성 추적자 | 실행 연결: catalogue.v3.MON123 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON124 | 시간 사냥꾼 | 실행 연결: catalogue.v3.MON124 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON125 | 월식 기사 | 실행 연결: catalogue.v3.MON125 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON126 | 태양 잔영 | 실행 연결: catalogue.v3.MON126 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON127 | 별무리 정령 | 실행 연결: catalogue.v3.MON127 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON128 | 은하 맹수 | 실행 연결: catalogue.v3.MON128 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON129 | 궤도 감시자 | 실행 연결: catalogue.v3.MON129 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON130 | 공전 인형 | 실행 연결: catalogue.v3.MON130 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON131 | 일그러진 살점 | 실행 연결: catalogue.v3.MON131 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON132 | 기억 포식자 | 실행 연결: catalogue.v3.MON132 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON133 | 뒤틀린 뼈수 | 실행 연결: catalogue.v3.MON133 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON134 | 혼돈 모사체 | 실행 연결: catalogue.v3.MON134 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON135 | 허공 절단자 | 실행 연결: catalogue.v3.MON135 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON136 | 불규칙 감시자 | 실행 연결: catalogue.v3.MON136 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON137 | 타락한 원소수 | 실행 연결: catalogue.v3.MON137 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON138 | 악몽 찌꺼기 | 실행 연결: catalogue.v3.MON138 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON139 | 역행 포식자 | 실행 연결: catalogue.v3.MON139 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON140 | 무형 변이체 | 실행 연결: catalogue.v3.MON140 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON141 | 울부짖는 시종 | 실행 연결: catalogue.v3.MON141 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON142 | 고독한 감시자 | 실행 연결: catalogue.v3.MON142 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON143 | 혼령 재판관 | 실행 연결: catalogue.v3.MON143 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON144 | 유령 기병 | 실행 연결: catalogue.v3.MON144 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON145 | 전장 원혼 | 실행 연결: catalogue.v3.MON145 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON146 | 망각의 악사 | 실행 연결: catalogue.v3.MON146 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON147 | 빛바랜 귀부인 | 실행 연결: catalogue.v3.MON147 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON148 | 허무의 무희 | 실행 연결: catalogue.v3.MON148 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON149 | 영혼 구속자 | 실행 연결: catalogue.v3.MON149 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MON150 | 망령 황실근위 | 실행 연결: catalogue.v3.MON150 | 3 | 출현·패턴·드롭·도감 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |

## 보스 — 40개

| 원본 ID | 이름 | 현재 상태·연결 ID | 예정 단계 | 필수 연결·검수 | 최종 판정/증빙 |
|---|---|---|---|---|---|
| BOS001 | 고블린 왕 | 실행 연결: catalogue.v3.BOS001 | 3 | 원형·단계·패턴·최초 보상 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| BOS002 | 거대 거미 여왕 | 실행 연결: catalogue.v3.BOS002 | 3 | 원형·단계·패턴·최초 보상 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| BOS003 | 해골 군주 | 실행 연결: catalogue.v3.BOS003 | 3 | 원형·단계·패턴·최초 보상 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| BOS004 | 트롤 족장 | 실행 연결: catalogue.v3.BOS004 | 3 | 원형·단계·패턴·최초 보상 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| BOS005 | 얼음의 수호자 | 실행 연결: catalogue.v3.BOS005 | 3 | 원형·단계·패턴·최초 보상 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| BOS006 | 지옥의 기사 | 실행 연결: catalogue.v3.BOS006 | 3 | 원형·단계·패턴·최초 보상 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| BOS007 | 타락한 대사제 | 실행 연결: catalogue.v3.BOS007 | 3 | 원형·단계·패턴·최초 보상 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| BOS008 | 고대 골렘 | 실행 연결: catalogue.v3.BOS008 | 3 | 원형·단계·패턴·최초 보상 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| BOS009 | 심연의 감시자 | 실행 연결: catalogue.v3.BOS009 | 3 | 원형·단계·패턴·최초 보상 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| BOS010 | 심연의 군주 | 실행 연결: catalogue.v3.BOS010 | 3 | 원형·단계·패턴·최초 보상 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| BOS011 | 야수왕 바르칸 | 실행 연결: catalogue.v3.BOS011 | 3 | 원형·단계·패턴·최초 보상 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| BOS012 | 피의 고위사제 | 실행 연결: catalogue.v3.BOS012 | 3 | 원형·단계·패턴·최초 보상 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| BOS013 | 황혼의 용왕자 | 실행 연결: catalogue.v3.BOS013 | 3 | 원형·단계·패턴·최초 보상 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| BOS014 | 강철 군단장 | 실행 연결: catalogue.v3.BOS014 | 3 | 원형·단계·패턴·최초 보상 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| BOS015 | 심해의 대왕오징어 | 실행 연결: catalogue.v3.BOS015 | 3 | 원형·단계·패턴·최초 보상 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| BOS016 | 포자 군주 | 실행 연결: catalogue.v3.BOS016 | 3 | 원형·단계·패턴·최초 보상 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| BOS017 | 사막의 망령왕 | 실행 연결: catalogue.v3.BOS017 | 3 | 원형·단계·패턴·최초 보상 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| BOS018 | 수정 핵심체 | 실행 연결: catalogue.v3.BOS018 | 3 | 원형·단계·패턴·최초 보상 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| BOS019 | 성좌의 집행관 | 실행 연결: catalogue.v3.BOS019 | 3 | 원형·단계·패턴·최초 보상 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| BOS020 | 혼돈의 복제왕 | 실행 연결: catalogue.v3.BOS020 | 3 | 원형·단계·패턴·최초 보상 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| BOS021 | 영혼 궁정의 섭정 | 실행 연결: catalogue.v3.BOS021 | 3 | 원형·단계·패턴·최초 보상 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| BOS022 | 불멸의 용아귀 | 실행 연결: catalogue.v3.BOS022 | 3 | 원형·단계·패턴·최초 보상 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| BOS023 | 폭풍의 원시신 | 실행 연결: catalogue.v3.BOS023 | 3 | 원형·단계·패턴·최초 보상 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| BOS024 | 검은 태엽군주 | 실행 연결: catalogue.v3.BOS024 | 3 | 원형·단계·패턴·최초 보상 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| BOS025 | 심해의 노래꾼 | 실행 연결: catalogue.v3.BOS025 | 3 | 원형·단계·패턴·최초 보상 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| BOS026 | 균사 여왕 | 실행 연결: catalogue.v3.BOS026 | 3 | 원형·단계·패턴·최초 보상 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| BOS027 | 황금 사막의 수호신 | 실행 연결: catalogue.v3.BOS027 | 3 | 원형·단계·패턴·최초 보상 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| BOS028 | 심층 광산의 거인 | 실행 연결: catalogue.v3.BOS028 | 3 | 원형·단계·패턴·최초 보상 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| BOS029 | 월식 대장군 | 실행 연결: catalogue.v3.BOS029 | 3 | 원형·단계·패턴·최초 보상 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| BOS030 | 무형의 지배자 | 실행 연결: catalogue.v3.BOS030 | 3 | 원형·단계·패턴·최초 보상 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| BOS031 | 기억을 거두는 왕 | 실행 연결: catalogue.v3.BOS031 | 3 | 원형·단계·패턴·최초 보상 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| BOS032 | 심연의 거대뱀 | 실행 연결: catalogue.v3.BOS032 | 3 | 원형·단계·패턴·최초 보상 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| BOS033 | 천공의 파수룡 | 실행 연결: catalogue.v3.BOS033 | 3 | 원형·단계·패턴·최초 보상 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| BOS034 | 쇠사슬 처형왕 | 실행 연결: catalogue.v3.BOS034 | 3 | 원형·단계·패턴·최초 보상 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| BOS035 | 파도의 폭군 | 실행 연결: catalogue.v3.BOS035 | 3 | 원형·단계·패턴·최초 보상 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| BOS036 | 부패의 정령수 | 실행 연결: catalogue.v3.BOS036 | 3 | 원형·단계·패턴·최초 보상 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| BOS037 | 사구의 침묵왕 | 실행 연결: catalogue.v3.BOS037 | 3 | 원형·단계·패턴·최초 보상 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| BOS038 | 마석의 제왕 | 실행 연결: catalogue.v3.BOS038 | 3 | 원형·단계·패턴·최초 보상 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| BOS039 | 시간의 감시자 | 실행 연결: catalogue.v3.BOS039 | 3 | 원형·단계·패턴·최초 보상 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| BOS040 | 균열 너머의 절대자 | 실행 연결: catalogue.v3.BOS040 | 3 | 원형·단계·패턴·최초 보상 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |

## 접두어 — 50개

| 원본 ID | 이름 | 현재 상태·연결 ID | 예정 단계 | 필수 연결·검수 | 최종 판정/증빙 |
|---|---|---|---|---|---|
| PFX001 | 흉포한 | 1차 연결: catalogue.v3.PFX001 | 3 | 범주·중복 제한·수치/발동 | 미판정 |
| PFX002 | 난폭한 | 1차 연결: catalogue.v3.PFX002 | 3 | 범주·중복 제한·수치/발동 | 미판정 |
| PFX003 | 광기에 찬 | 1차 연결: catalogue.v3.PFX003 | 3 | 범주·중복 제한·수치/발동 | 미판정 |
| PFX004 | 살육의 | 1차 연결: catalogue.v3.PFX004 | 3 | 범주·중복 제한·수치/발동 | 미판정 |
| PFX005 | 견고한 | 1차 연결: catalogue.v3.PFX005 | 3 | 범주·중복 제한·수치/발동 | 미판정 |
| PFX006 | 철갑의 | 1차 연결: catalogue.v3.PFX006 | 3 | 범주·중복 제한·수치/발동 | 미판정 |
| PFX007 | 불굴의 | 1차 연결: catalogue.v3.PFX007 | 3 | 범주·중복 제한·수치/발동 | 미판정 |
| PFX008 | 수호하는 | 1차 연결: catalogue.v3.PFX008 | 3 | 범주·중복 제한·수치/발동 | 미판정 |
| PFX009 | 거대한 | 1차 연결: catalogue.v3.PFX009 | 3 | 범주·중복 제한·수치/발동 | 미판정 |
| PFX010 | 재생하는 | 1차 연결: catalogue.v3.PFX010 | 3 | 범주·중복 제한·수치/발동 | 미판정 |
| PFX011 | 불사의 | 1차 연결: catalogue.v3.PFX011 | 3 | 범주·중복 제한·수치/발동 | 미판정 |
| PFX012 | 생명력이 넘치는 | 1차 연결: catalogue.v3.PFX012 | 3 | 범주·중복 제한·수치/발동 | 미판정 |
| PFX013 | 맹독의 | 1차 연결: catalogue.v3.PFX013 | 3 | 범주·중복 제한·수치/발동 | 미판정 |
| PFX014 | 불타는 | 1차 연결: catalogue.v3.PFX014 | 3 | 범주·중복 제한·수치/발동 | 미판정 |
| PFX015 | 흡혈하는 | 1차 연결: catalogue.v3.PFX015 | 3 | 범주·중복 제한·수치/발동 | 미판정 |
| PFX016 | 저주받은 | 1차 연결: catalogue.v3.PFX016 | 3 | 범주·중복 제한·수치/발동 | 미판정 |
| PFX017 | 황금의 | 1차 연결: catalogue.v3.PFX017 | 3 | 범주·중복 제한·수치/발동 | 미판정 |
| PFX018 | 축복받은 | 1차 연결: catalogue.v3.PFX018 | 3 | 범주·중복 제한·수치/발동 | 미판정 |
| PFX019 | 고대의 | 1차 연결: catalogue.v3.PFX019 | 3 | 범주·중복 제한·수치/발동 | 미판정 |
| PFX020 | 보물을 품은 | 1차 연결: catalogue.v3.PFX020 | 3 | 범주·중복 제한·수치/발동 | 미판정 |
| PFX021 | 잔혹한 | 미연결 | 3 | 범주·중복 제한·수치/발동 | 미판정 |
| PFX022 | 날카로운 | 미연결 | 3 | 범주·중복 제한·수치/발동 | 미판정 |
| PFX023 | 맹렬한 | 미연결 | 3 | 범주·중복 제한·수치/발동 | 미판정 |
| PFX024 | 광폭한 | 미연결 | 3 | 범주·중복 제한·수치/발동 | 미판정 |
| PFX025 | 피에 굶주린 | 미연결 | 3 | 범주·중복 제한·수치/발동 | 미판정 |
| PFX026 | 처형자의 | 미연결 | 3 | 범주·중복 제한·수치/발동 | 미판정 |
| PFX027 | 철벽의 | 미연결 | 3 | 범주·중복 제한·수치/발동 | 미판정 |
| PFX028 | 단단한 | 미연결 | 3 | 범주·중복 제한·수치/발동 | 미판정 |
| PFX029 | 가시 갑옷의 | 미연결 | 3 | 범주·중복 제한·수치/발동 | 미판정 |
| PFX030 | 무쇠의 | 미연결 | 3 | 범주·중복 제한·수치/발동 | 미판정 |
| PFX031 | 방패를 든 | 미연결 | 3 | 범주·중복 제한·수치/발동 | 미판정 |
| PFX032 | 수호자의 | 미연결 | 3 | 범주·중복 제한·수치/발동 | 미판정 |
| PFX033 | 끈질긴 | 미연결 | 3 | 범주·중복 제한·수치/발동 | 미판정 |
| PFX034 | 회복하는 | 미연결 | 3 | 범주·중복 제한·수치/발동 | 미판정 |
| PFX035 | 생명을 탐하는 | 미연결 | 3 | 범주·중복 제한·수치/발동 | 미판정 |
| PFX036 | 거목의 | 미연결 | 3 | 범주·중복 제한·수치/발동 | 미판정 |
| PFX037 | 정화된 | 미연결 | 3 | 범주·중복 제한·수치/발동 | 미판정 |
| PFX038 | 부활의 | 미연결 | 3 | 범주·중복 제한·수치/발동 | 미판정 |
| PFX039 | 서릿발의 | 미연결 | 3 | 범주·중복 제한·수치/발동 | 미판정 |
| PFX040 | 번개의 | 미연결 | 3 | 범주·중복 제한·수치/발동 | 미판정 |
| PFX041 | 부식의 | 미연결 | 3 | 범주·중복 제한·수치/발동 | 미판정 |
| PFX042 | 암흑의 | 미연결 | 3 | 범주·중복 제한·수치/발동 | 미판정 |
| PFX043 | 혼란스러운 | 미연결 | 3 | 범주·중복 제한·수치/발동 | 미판정 |
| PFX044 | 불길한 | 미연결 | 3 | 범주·중복 제한·수치/발동 | 미판정 |
| PFX045 | 진귀한 | 미연결 | 3 | 범주·중복 제한·수치/발동 | 미판정 |
| PFX046 | 보석을 품은 | 미연결 | 3 | 범주·중복 제한·수치/발동 | 미판정 |
| PFX047 | 지식의 | 미연결 | 3 | 범주·중복 제한·수치/발동 | 미판정 |
| PFX048 | 대가의 | 미연결 | 3 | 범주·중복 제한·수치/발동 | 미판정 |
| PFX049 | 풍요로운 | 미연결 | 3 | 범주·중복 제한·수치/발동 | 미판정 |
| PFX050 | 별의 | 미연결 | 3 | 범주·중복 제한·수치/발동 | 미판정 |

## 장비 — 330개

| 원본 ID | 이름 | 현재 상태·연결 ID | 예정 단계 | 필수 연결·검수 | 최종 판정/증빙 |
|---|---|---|---|---|---|
| EQ001 | 낡은 장검 | 실행 연결: catalogue.v3.EQ001 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ002 | 철 장검 | 실행 연결: catalogue.v3.EQ002 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ003 | 강철 장검 | 실행 연결: catalogue.v3.EQ003 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ004 | 은빛 장검 | 실행 연결: catalogue.v3.EQ004 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ005 | 미스릴 장검 | 실행 연결: catalogue.v3.EQ005 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ006 | 심연의 장검 | 실행 연결: catalogue.v3.EQ006 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ007 | 나무 손도끼 | 실행 연결: catalogue.v3.EQ007 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ008 | 철 손도끼 | 실행 연결: catalogue.v3.EQ008 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ009 | 전투 도끼 | 실행 연결: catalogue.v3.EQ009 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ010 | 양날 도끼 | 실행 연결: catalogue.v3.EQ010 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ011 | 처형 도끼 | 실행 연결: catalogue.v3.EQ011 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ012 | 파멸의 도끼 | 실행 연결: catalogue.v3.EQ012 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ013 | 나무 몽둥이 | 실행 연결: catalogue.v3.EQ013 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ014 | 철퇴 | 실행 연결: catalogue.v3.EQ014 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ015 | 돌망치 | 실행 연결: catalogue.v3.EQ015 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ016 | 전쟁망치 | 실행 연결: catalogue.v3.EQ016 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ017 | 파쇄망치 | 실행 연결: catalogue.v3.EQ017 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ018 | 별무리 망치 | 실행 연결: catalogue.v3.EQ018 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ019 | 녹슨 단검 | 실행 연결: catalogue.v3.EQ019 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ020 | 사냥 단검 | 실행 연결: catalogue.v3.EQ020 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ021 | 암살 단검 | 실행 연결: catalogue.v3.EQ021 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ022 | 맹독 단검 | 실행 연결: catalogue.v3.EQ022 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ023 | 그림자 단검 | 실행 연결: catalogue.v3.EQ023 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ024 | 공허 단검 | 실행 연결: catalogue.v3.EQ024 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ025 | 짧은 창 | 실행 연결: catalogue.v3.EQ025 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ026 | 철 창 | 실행 연결: catalogue.v3.EQ026 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ027 | 장창 | 실행 연결: catalogue.v3.EQ027 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ028 | 관통창 | 실행 연결: catalogue.v3.EQ028 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ029 | 용병의 창 | 실행 연결: catalogue.v3.EQ029 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ030 | 천공의 창 | 실행 연결: catalogue.v3.EQ030 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ031 | 천 투구 | 실행 연결: catalogue.v3.EQ031 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ032 | 가죽 투구 | 실행 연결: catalogue.v3.EQ032 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ033 | 모험가 투구 | 실행 연결: catalogue.v3.EQ033 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ034 | 철 투구 | 실행 연결: catalogue.v3.EQ034 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ035 | 강철 투구 | 실행 연결: catalogue.v3.EQ035 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ036 | 기사 투구 | 실행 연결: catalogue.v3.EQ036 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ037 | 미스릴 투구 | 실행 연결: catalogue.v3.EQ037 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ038 | 룬 투구 | 실행 연결: catalogue.v3.EQ038 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ039 | 고대 투구 | 실행 연결: catalogue.v3.EQ039 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ040 | 심연 투구 | 실행 연결: catalogue.v3.EQ040 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ041 | 천 갑옷 | 실행 연결: catalogue.v3.EQ041 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ042 | 가죽 갑옷 | 실행 연결: catalogue.v3.EQ042 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ043 | 모험가 갑옷 | 실행 연결: catalogue.v3.EQ043 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ044 | 철 갑옷 | 실행 연결: catalogue.v3.EQ044 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ045 | 강철 갑옷 | 실행 연결: catalogue.v3.EQ045 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ046 | 기사 갑옷 | 실행 연결: catalogue.v3.EQ046 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ047 | 미스릴 갑옷 | 실행 연결: catalogue.v3.EQ047 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ048 | 룬 갑옷 | 실행 연결: catalogue.v3.EQ048 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ049 | 고대 갑옷 | 실행 연결: catalogue.v3.EQ049 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ050 | 심연 갑옷 | 실행 연결: catalogue.v3.EQ050 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ051 | 천 장갑 | 실행 연결: catalogue.v3.EQ051 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ052 | 가죽 장갑 | 실행 연결: catalogue.v3.EQ052 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ053 | 모험가 장갑 | 실행 연결: catalogue.v3.EQ053 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ054 | 철 장갑 | 실행 연결: catalogue.v3.EQ054 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ055 | 강철 장갑 | 실행 연결: catalogue.v3.EQ055 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ056 | 기사 장갑 | 실행 연결: catalogue.v3.EQ056 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ057 | 미스릴 장갑 | 실행 연결: catalogue.v3.EQ057 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ058 | 룬 장갑 | 실행 연결: catalogue.v3.EQ058 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ059 | 고대 장갑 | 실행 연결: catalogue.v3.EQ059 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ060 | 심연 장갑 | 실행 연결: catalogue.v3.EQ060 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ061 | 천 신발 | 실행 연결: catalogue.v3.EQ061 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ062 | 가죽 신발 | 실행 연결: catalogue.v3.EQ062 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ063 | 모험가 신발 | 실행 연결: catalogue.v3.EQ063 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ064 | 철 신발 | 실행 연결: catalogue.v3.EQ064 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ065 | 강철 신발 | 실행 연결: catalogue.v3.EQ065 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ066 | 기사 신발 | 실행 연결: catalogue.v3.EQ066 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ067 | 미스릴 신발 | 실행 연결: catalogue.v3.EQ067 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ068 | 룬 신발 | 실행 연결: catalogue.v3.EQ068 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ069 | 고대 신발 | 실행 연결: catalogue.v3.EQ069 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ070 | 심연 신발 | 실행 연결: catalogue.v3.EQ070 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ071 | 낡은 반지 | 실행 연결: catalogue.v3.EQ071 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ072 | 구리 반지 | 실행 연결: catalogue.v3.EQ072 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ073 | 힘의 반지 | 실행 연결: catalogue.v3.EQ073 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ074 | 민첩의 반지 | 실행 연결: catalogue.v3.EQ074 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ075 | 수호의 반지 | 실행 연결: catalogue.v3.EQ075 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ076 | 행운의 반지 | 실행 연결: catalogue.v3.EQ076 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ077 | 피의 반지 | 실행 연결: catalogue.v3.EQ077 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ078 | 별의 반지 | 실행 연결: catalogue.v3.EQ078 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ079 | 고대의 반지 | 실행 연결: catalogue.v3.EQ079 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ080 | 심연의 반지 | 실행 연결: catalogue.v3.EQ080 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ081 | 나무 목걸이 | 실행 연결: catalogue.v3.EQ081 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ082 | 뼈 목걸이 | 실행 연결: catalogue.v3.EQ082 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ083 | 생명의 목걸이 | 실행 연결: catalogue.v3.EQ083 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ084 | 마력 목걸이 | 실행 연결: catalogue.v3.EQ084 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ085 | 수호의 목걸이 | 실행 연결: catalogue.v3.EQ085 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ086 | 정령의 목걸이 | 실행 연결: catalogue.v3.EQ086 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ087 | 용기의 목걸이 | 실행 연결: catalogue.v3.EQ087 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ088 | 왕가의 목걸이 | 실행 연결: catalogue.v3.EQ088 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ089 | 고대의 목걸이 | 실행 연결: catalogue.v3.EQ089 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ090 | 심연의 목걸이 | 실행 연결: catalogue.v3.EQ090 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ091 | 황혼의 대검 | 실행 연결: catalogue.v3.EQ091 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ092 | 전격의 월도 | 실행 연결: catalogue.v3.EQ092 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ093 | 수호자의 철퇴 | 실행 연결: catalogue.v3.EQ093 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ094 | 바람을 가르는 쌍날검 | 실행 연결: catalogue.v3.EQ094 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ095 | 용린 작살창 | 실행 연결: catalogue.v3.EQ095 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ096 | 별무리 쐐기창 | 실행 연결: catalogue.v3.EQ096 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ097 | 불꽃의 파쇄도끼 | 실행 연결: catalogue.v3.EQ097 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ098 | 마석 전투망치 | 실행 연결: catalogue.v3.EQ098 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ099 | 공허의 톱날검 | 실행 연결: catalogue.v3.EQ099 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ100 | 심연왕의 장창 | 실행 연결: catalogue.v3.EQ100 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ101 | 잿빛 투구 | 실행 연결: catalogue.v3.EQ101 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ102 | 황혼 투구 | 실행 연결: catalogue.v3.EQ102 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ103 | 흑철 투구 | 실행 연결: catalogue.v3.EQ103 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ104 | 바람무늬 투구 | 실행 연결: catalogue.v3.EQ104 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ105 | 용린 투구 | 실행 연결: catalogue.v3.EQ105 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ106 | 성좌 투구 | 실행 연결: catalogue.v3.EQ106 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ107 | 마나 투구 | 실행 연결: catalogue.v3.EQ107 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ108 | 수정 투구 | 실행 연결: catalogue.v3.EQ108 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ109 | 정화 투구 | 실행 연결: catalogue.v3.EQ109 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ110 | 잔혹 투구 | 실행 연결: catalogue.v3.EQ110 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ111 | 태양 투구 | 실행 연결: catalogue.v3.EQ111 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ112 | 월식 투구 | 실행 연결: catalogue.v3.EQ112 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ113 | 은하 투구 | 실행 연결: catalogue.v3.EQ113 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ114 | 파동 투구 | 실행 연결: catalogue.v3.EQ114 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ115 | 군단 투구 | 실행 연결: catalogue.v3.EQ115 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ116 | 신성 투구 | 실행 연결: catalogue.v3.EQ116 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ117 | 공허 투구 | 실행 연결: catalogue.v3.EQ117 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ118 | 혼돈 투구 | 실행 연결: catalogue.v3.EQ118 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ119 | 영혼 투구 | 실행 연결: catalogue.v3.EQ119 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ120 | 초월 투구 | 실행 연결: catalogue.v3.EQ120 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ121 | 어둠 투구 | 실행 연결: catalogue.v3.EQ121 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ122 | 시공 투구 | 실행 연결: catalogue.v3.EQ122 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ123 | 영겁 투구 | 실행 연결: catalogue.v3.EQ123 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ124 | 창세 투구 | 실행 연결: catalogue.v3.EQ124 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ125 | 결계 투구 | 실행 연결: catalogue.v3.EQ125 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ126 | 불멸 투구 | 실행 연결: catalogue.v3.EQ126 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ127 | 심판 투구 | 실행 연결: catalogue.v3.EQ127 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ128 | 무한 투구 | 실행 연결: catalogue.v3.EQ128 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ129 | 잿빛 갑옷 | 실행 연결: catalogue.v3.EQ129 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ130 | 황혼 갑옷 | 실행 연결: catalogue.v3.EQ130 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ131 | 흑철 갑옷 | 실행 연결: catalogue.v3.EQ131 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ132 | 바람무늬 갑옷 | 실행 연결: catalogue.v3.EQ132 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ133 | 용린 갑옷 | 실행 연결: catalogue.v3.EQ133 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ134 | 성좌 갑옷 | 실행 연결: catalogue.v3.EQ134 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ135 | 마나 갑옷 | 실행 연결: catalogue.v3.EQ135 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ136 | 수정 갑옷 | 실행 연결: catalogue.v3.EQ136 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ137 | 정화 갑옷 | 실행 연결: catalogue.v3.EQ137 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ138 | 잔혹 갑옷 | 실행 연결: catalogue.v3.EQ138 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ139 | 태양 갑옷 | 실행 연결: catalogue.v3.EQ139 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ140 | 월식 갑옷 | 실행 연결: catalogue.v3.EQ140 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ141 | 은하 갑옷 | 실행 연결: catalogue.v3.EQ141 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ142 | 파동 갑옷 | 실행 연결: catalogue.v3.EQ142 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ143 | 군단 갑옷 | 실행 연결: catalogue.v3.EQ143 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ144 | 신성 갑옷 | 실행 연결: catalogue.v3.EQ144 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ145 | 공허 갑옷 | 실행 연결: catalogue.v3.EQ145 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ146 | 혼돈 갑옷 | 실행 연결: catalogue.v3.EQ146 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ147 | 영혼 갑옷 | 실행 연결: catalogue.v3.EQ147 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ148 | 초월 갑옷 | 실행 연결: catalogue.v3.EQ148 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ149 | 어둠 갑옷 | 실행 연결: catalogue.v3.EQ149 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ150 | 시공 갑옷 | 실행 연결: catalogue.v3.EQ150 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ151 | 영겁 갑옷 | 실행 연결: catalogue.v3.EQ151 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ152 | 창세 갑옷 | 실행 연결: catalogue.v3.EQ152 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ153 | 결계 갑옷 | 실행 연결: catalogue.v3.EQ153 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ154 | 불멸 갑옷 | 실행 연결: catalogue.v3.EQ154 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ155 | 심판 갑옷 | 실행 연결: catalogue.v3.EQ155 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ156 | 무한 갑옷 | 실행 연결: catalogue.v3.EQ156 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ157 | 잿빛 장갑 | 실행 연결: catalogue.v3.EQ157 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ158 | 황혼 장갑 | 실행 연결: catalogue.v3.EQ158 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ159 | 흑철 장갑 | 실행 연결: catalogue.v3.EQ159 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ160 | 바람무늬 장갑 | 실행 연결: catalogue.v3.EQ160 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ161 | 용린 장갑 | 실행 연결: catalogue.v3.EQ161 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ162 | 성좌 장갑 | 실행 연결: catalogue.v3.EQ162 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ163 | 마나 장갑 | 실행 연결: catalogue.v3.EQ163 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ164 | 수정 장갑 | 실행 연결: catalogue.v3.EQ164 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ165 | 정화 장갑 | 실행 연결: catalogue.v3.EQ165 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ166 | 잔혹 장갑 | 실행 연결: catalogue.v3.EQ166 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ167 | 태양 장갑 | 실행 연결: catalogue.v3.EQ167 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ168 | 월식 장갑 | 실행 연결: catalogue.v3.EQ168 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ169 | 은하 장갑 | 실행 연결: catalogue.v3.EQ169 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ170 | 파동 장갑 | 실행 연결: catalogue.v3.EQ170 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ171 | 군단 장갑 | 실행 연결: catalogue.v3.EQ171 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ172 | 신성 장갑 | 실행 연결: catalogue.v3.EQ172 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ173 | 공허 장갑 | 실행 연결: catalogue.v3.EQ173 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ174 | 혼돈 장갑 | 실행 연결: catalogue.v3.EQ174 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ175 | 영혼 장갑 | 실행 연결: catalogue.v3.EQ175 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ176 | 초월 장갑 | 실행 연결: catalogue.v3.EQ176 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ177 | 어둠 장갑 | 실행 연결: catalogue.v3.EQ177 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ178 | 시공 장갑 | 실행 연결: catalogue.v3.EQ178 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ179 | 영겁 장갑 | 실행 연결: catalogue.v3.EQ179 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ180 | 창세 장갑 | 실행 연결: catalogue.v3.EQ180 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ181 | 결계 장갑 | 실행 연결: catalogue.v3.EQ181 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ182 | 불멸 장갑 | 실행 연결: catalogue.v3.EQ182 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ183 | 심판 장갑 | 실행 연결: catalogue.v3.EQ183 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ184 | 잿빛 신발 | 실행 연결: catalogue.v3.EQ184 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ185 | 황혼 신발 | 실행 연결: catalogue.v3.EQ185 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ186 | 흑철 신발 | 실행 연결: catalogue.v3.EQ186 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ187 | 바람무늬 신발 | 실행 연결: catalogue.v3.EQ187 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ188 | 용린 신발 | 실행 연결: catalogue.v3.EQ188 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ189 | 성좌 신발 | 실행 연결: catalogue.v3.EQ189 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ190 | 마나 신발 | 실행 연결: catalogue.v3.EQ190 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ191 | 수정 신발 | 실행 연결: catalogue.v3.EQ191 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ192 | 정화 신발 | 실행 연결: catalogue.v3.EQ192 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ193 | 잔혹 신발 | 실행 연결: catalogue.v3.EQ193 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ194 | 태양 신발 | 실행 연결: catalogue.v3.EQ194 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ195 | 월식 신발 | 실행 연결: catalogue.v3.EQ195 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ196 | 은하 신발 | 실행 연결: catalogue.v3.EQ196 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ197 | 파동 신발 | 실행 연결: catalogue.v3.EQ197 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ198 | 군단 신발 | 실행 연결: catalogue.v3.EQ198 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ199 | 신성 신발 | 실행 연결: catalogue.v3.EQ199 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ200 | 공허 신발 | 실행 연결: catalogue.v3.EQ200 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ201 | 혼돈 신발 | 실행 연결: catalogue.v3.EQ201 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ202 | 영혼 신발 | 실행 연결: catalogue.v3.EQ202 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ203 | 초월 신발 | 실행 연결: catalogue.v3.EQ203 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ204 | 어둠 신발 | 실행 연결: catalogue.v3.EQ204 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ205 | 시공 신발 | 실행 연결: catalogue.v3.EQ205 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ206 | 영겁 신발 | 실행 연결: catalogue.v3.EQ206 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ207 | 창세 신발 | 실행 연결: catalogue.v3.EQ207 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ208 | 결계 신발 | 실행 연결: catalogue.v3.EQ208 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ209 | 불멸 신발 | 실행 연결: catalogue.v3.EQ209 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ210 | 심판 신발 | 실행 연결: catalogue.v3.EQ210 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ211 | 전투의 반지 | 실행 연결: catalogue.v3.EQ211 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ212 | 수호의 심층 반지 | 실행 연결: catalogue.v3.EQ212 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ213 | 용혈의 반지 | 실행 연결: catalogue.v3.EQ213 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ214 | 빙하의 반지 | 실행 연결: catalogue.v3.EQ214 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ215 | 화염의 반지 | 실행 연결: catalogue.v3.EQ215 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ216 | 황혼의 반지 | 실행 연결: catalogue.v3.EQ216 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ217 | 광휘의 반지 | 실행 연결: catalogue.v3.EQ217 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ218 | 망각의 반지 | 실행 연결: catalogue.v3.EQ218 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ219 | 대지의 반지 | 실행 연결: catalogue.v3.EQ219 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ220 | 바람의 반지 | 실행 연결: catalogue.v3.EQ220 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ221 | 균열의 반지 | 실행 연결: catalogue.v3.EQ221 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ222 | 심판의 반지 | 실행 연결: catalogue.v3.EQ222 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ223 | 정화의 반지 | 실행 연결: catalogue.v3.EQ223 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ224 | 월식의 반지 | 실행 연결: catalogue.v3.EQ224 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ225 | 태양의 반지 | 실행 연결: catalogue.v3.EQ225 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ226 | 은하의 반지 | 실행 연결: catalogue.v3.EQ226 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ227 | 강철의 반지 | 실행 연결: catalogue.v3.EQ227 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ228 | 유성의 반지 | 실행 연결: catalogue.v3.EQ228 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ229 | 폭풍의 반지 | 실행 연결: catalogue.v3.EQ229 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ230 | 영혼의 반지 | 실행 연결: catalogue.v3.EQ230 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ231 | 선지자의 반지 | 실행 연결: catalogue.v3.EQ231 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ232 | 결계의 반지 | 실행 연결: catalogue.v3.EQ232 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ233 | 회복의 반지 | 실행 연결: catalogue.v3.EQ233 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ234 | 학자의 반지 | 실행 연결: catalogue.v3.EQ234 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ235 | 천공의 반지 | 실행 연결: catalogue.v3.EQ235 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ236 | 바다의 반지 | 실행 연결: catalogue.v3.EQ236 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ237 | 망령의 반지 | 실행 연결: catalogue.v3.EQ237 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ238 | 초월의 반지 | 실행 연결: catalogue.v3.EQ238 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ239 | 영겁의 반지 | 실행 연결: catalogue.v3.EQ239 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ240 | 비밀의 반지 | 실행 연결: catalogue.v3.EQ240 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ241 | 전투의 목걸이 | 실행 연결: catalogue.v3.EQ241 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ242 | 수호의 심층 목걸이 | 실행 연결: catalogue.v3.EQ242 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ243 | 용혈의 목걸이 | 실행 연결: catalogue.v3.EQ243 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ244 | 빙하의 목걸이 | 실행 연결: catalogue.v3.EQ244 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ245 | 화염의 목걸이 | 실행 연결: catalogue.v3.EQ245 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ246 | 황혼의 목걸이 | 실행 연결: catalogue.v3.EQ246 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ247 | 광휘의 목걸이 | 실행 연결: catalogue.v3.EQ247 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ248 | 망각의 목걸이 | 실행 연결: catalogue.v3.EQ248 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ249 | 대지의 목걸이 | 실행 연결: catalogue.v3.EQ249 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ250 | 바람의 목걸이 | 실행 연결: catalogue.v3.EQ250 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ251 | 균열의 목걸이 | 실행 연결: catalogue.v3.EQ251 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ252 | 심판의 목걸이 | 실행 연결: catalogue.v3.EQ252 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ253 | 정화의 목걸이 | 실행 연결: catalogue.v3.EQ253 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ254 | 월식의 목걸이 | 실행 연결: catalogue.v3.EQ254 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ255 | 태양의 목걸이 | 실행 연결: catalogue.v3.EQ255 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ256 | 은하의 목걸이 | 실행 연결: catalogue.v3.EQ256 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ257 | 강철의 목걸이 | 실행 연결: catalogue.v3.EQ257 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ258 | 유성의 목걸이 | 실행 연결: catalogue.v3.EQ258 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ259 | 폭풍의 목걸이 | 실행 연결: catalogue.v3.EQ259 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ260 | 영혼의 목걸이 | 실행 연결: catalogue.v3.EQ260 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ261 | 선지자의 목걸이 | 실행 연결: catalogue.v3.EQ261 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ262 | 결계의 목걸이 | 실행 연결: catalogue.v3.EQ262 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ263 | 회복의 목걸이 | 실행 연결: catalogue.v3.EQ263 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ264 | 학자의 목걸이 | 실행 연결: catalogue.v3.EQ264 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ265 | 천공의 목걸이 | 실행 연결: catalogue.v3.EQ265 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ266 | 바다의 목걸이 | 실행 연결: catalogue.v3.EQ266 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ267 | 망령의 목걸이 | 실행 연결: catalogue.v3.EQ267 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ268 | 초월의 목걸이 | 실행 연결: catalogue.v3.EQ268 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ269 | 영겁의 목걸이 | 실행 연결: catalogue.v3.EQ269 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ270 | 비밀의 목걸이 | 실행 연결: catalogue.v3.EQ270 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ271 | 붉은의 대검 | 실행 연결: catalogue.v3.EQ271 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ272 | 흑요의 대검 | 실행 연결: catalogue.v3.EQ272 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ273 | 용암의 대검 | 실행 연결: catalogue.v3.EQ273 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ274 | 월식의 대검 | 실행 연결: catalogue.v3.EQ274 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ275 | 별의의 대검 | 실행 연결: catalogue.v3.EQ275 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ276 | 불굴의 대검 | 실행 연결: catalogue.v3.EQ276 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ277 | 파멸의 대검 | 실행 연결: catalogue.v3.EQ277 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ278 | 유성의 대검 | 실행 연결: catalogue.v3.EQ278 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ279 | 균열의 대검 | 실행 연결: catalogue.v3.EQ279 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ280 | 영겁의 대검 | 실행 연결: catalogue.v3.EQ280 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ281 | 폭풍의 도끼 | 실행 연결: catalogue.v3.EQ281 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ282 | 철갑의 도끼 | 실행 연결: catalogue.v3.EQ282 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ283 | 태양의 도끼 | 실행 연결: catalogue.v3.EQ283 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ284 | 혼돈의 도끼 | 실행 연결: catalogue.v3.EQ284 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ285 | 마력의 도끼 | 실행 연결: catalogue.v3.EQ285 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ286 | 수정의 도끼 | 실행 연결: catalogue.v3.EQ286 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ287 | 어둠의 도끼 | 실행 연결: catalogue.v3.EQ287 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ288 | 고대의 도끼 | 실행 연결: catalogue.v3.EQ288 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ289 | 용린의 도끼 | 실행 연결: catalogue.v3.EQ289 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ290 | 심판의 도끼 | 실행 연결: catalogue.v3.EQ290 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ291 | 참회의 철퇴 | 실행 연결: catalogue.v3.EQ291 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ292 | 성광의 철퇴 | 실행 연결: catalogue.v3.EQ292 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ293 | 암흑의 철퇴 | 실행 연결: catalogue.v3.EQ293 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ294 | 전격의 철퇴 | 실행 연결: catalogue.v3.EQ294 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ295 | 황혼의 철퇴 | 실행 연결: catalogue.v3.EQ295 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ296 | 운석의 철퇴 | 실행 연결: catalogue.v3.EQ296 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ297 | 폭렬의 철퇴 | 실행 연결: catalogue.v3.EQ297 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ298 | 불사의 철퇴 | 실행 연결: catalogue.v3.EQ298 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ299 | 심해의 철퇴 | 실행 연결: catalogue.v3.EQ299 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ300 | 성좌의 철퇴 | 실행 연결: catalogue.v3.EQ300 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ301 | 그림자의 단검 | 실행 연결: catalogue.v3.EQ301 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ302 | 침묵의 단검 | 실행 연결: catalogue.v3.EQ302 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ303 | 맹독의 단검 | 실행 연결: catalogue.v3.EQ303 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ304 | 암월의 단검 | 실행 연결: catalogue.v3.EQ304 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ305 | 눈보라의 단검 | 실행 연결: catalogue.v3.EQ305 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ306 | 붉은의 단검 | 실행 연결: catalogue.v3.EQ306 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ307 | 초월의 단검 | 실행 연결: catalogue.v3.EQ307 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ308 | 황금의 단검 | 실행 연결: catalogue.v3.EQ308 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ309 | 망령의 단검 | 실행 연결: catalogue.v3.EQ309 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ310 | 고요의 단검 | 실행 연결: catalogue.v3.EQ310 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ311 | 빛나는의 창 | 실행 연결: catalogue.v3.EQ311 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ312 | 태풍의 창 | 실행 연결: catalogue.v3.EQ312 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ313 | 은빛의 창 | 실행 연결: catalogue.v3.EQ313 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ314 | 지각의 창 | 실행 연결: catalogue.v3.EQ314 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ315 | 파도의 창 | 실행 연결: catalogue.v3.EQ315 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ316 | 유성의 창 | 실행 연결: catalogue.v3.EQ316 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ317 | 독니의 창 | 실행 연결: catalogue.v3.EQ317 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ318 | 영혼의 창 | 실행 연결: catalogue.v3.EQ318 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ319 | 전격의 창 | 실행 연결: catalogue.v3.EQ319 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ320 | 무한의 창 | 실행 연결: catalogue.v3.EQ320 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ321 | 달빛의 도검 | 실행 연결: catalogue.v3.EQ321 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ322 | 천공의 도검 | 실행 연결: catalogue.v3.EQ322 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ323 | 룬의 도검 | 실행 연결: catalogue.v3.EQ323 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ324 | 흑철의 도검 | 실행 연결: catalogue.v3.EQ324 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ325 | 혼돈의 도검 | 실행 연결: catalogue.v3.EQ325 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ326 | 환영의 도검 | 실행 연결: catalogue.v3.EQ326 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ327 | 백은의 도검 | 실행 연결: catalogue.v3.EQ327 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ328 | 단죄의 도검 | 실행 연결: catalogue.v3.EQ328 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ329 | 황혼의 도검 | 실행 연결: catalogue.v3.EQ329 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| EQ330 | 종언의 도검 | 실행 연결: catalogue.v3.EQ330 | 3 | 해금·생성·옵션·강화·경제 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |

## 장비 옵션 — 100개

| 원본 ID | 이름 | 현재 상태·연결 ID | 예정 단계 | 필수 연결·검수 | 최종 판정/증빙 |
|---|---|---|---|---|---|
| OPT001 | 힘 + | 1차 연결: catalogue.v3.OPT001 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT002 | 민첩 + | 1차 연결: catalogue.v3.OPT002 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT003 | 체력 + | 1차 연결: catalogue.v3.OPT003 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT004 | 지능 + | 1차 연결: catalogue.v3.OPT004 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT005 | 행운 + | 1차 연결: catalogue.v3.OPT005 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT006 | 공격력 + | 1차 연결: catalogue.v3.OPT006 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT007 | 방어력 + | 1차 연결: catalogue.v3.OPT007 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT008 | 최대 HP + | 1차 연결: catalogue.v3.OPT008 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT009 | 최대 MP + | 1차 연결: catalogue.v3.OPT009 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT010 | 치명타율 + | 1차 연결: catalogue.v3.OPT010 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT011 | 치명타 피해 + | 1차 연결: catalogue.v3.OPT011 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT012 | 회피율 + | 1차 연결: catalogue.v3.OPT012 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT013 | HP 재생 + | 1차 연결: catalogue.v3.OPT013 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT014 | MP 재생 + | 1차 연결: catalogue.v3.OPT014 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT015 | 처치 시 HP 회복 + | 1차 연결: catalogue.v3.OPT015 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT016 | 처치 시 MP 회복 + | 1차 연결: catalogue.v3.OPT016 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT017 | 흡혈 + | 1차 연결: catalogue.v3.OPT017 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT018 | 방어 무시 + | 1차 연결: catalogue.v3.OPT018 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT019 | 추가 피해 + | 1차 연결: catalogue.v3.OPT019 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT020 | 강공격 피해 + | 1차 연결: catalogue.v3.OPT020 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT021 | 일반 공격 피해 + | 1차 연결: catalogue.v3.OPT021 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT022 | 받는 피해 감소 + | 1차 연결: catalogue.v3.OPT022 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT023 | 치명타 저항 + | 1차 연결: catalogue.v3.OPT023 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT024 | 상태이상 저항 + | 1차 연결: catalogue.v3.OPT024 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT025 | 반격 확률 + | 1차 연결: catalogue.v3.OPT025 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT026 | 보호막 + | 1차 연결: catalogue.v3.OPT026 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT027 | 골드 획득 + | 1차 연결: catalogue.v3.OPT027 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT028 | 경험치 획득 + | 1차 연결: catalogue.v3.OPT028 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT029 | 장비 드롭률 + | 1차 연결: catalogue.v3.OPT029 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT030 | 희귀 등급 확률 + | 1차 연결: catalogue.v3.OPT030 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT031 | 화염 피해 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT032 | 냉기 피해 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT033 | 번개 피해 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT034 | 독 피해 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT035 | 암흑 피해 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT036 | 빛 피해 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT037 | 물리 관통 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT038 | 원소 추가타 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT039 | 원소 적중 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT040 | 원소 폭발 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT041 | 중독 확률 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT042 | 화상 확률 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT043 | 출혈 확률 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT044 | 감전 확률 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT045 | 빙결 확률 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT046 | 부식 확률 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT047 | 저주 확률 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT048 | 침묵 확률 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT049 | 둔화 확률 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT050 | 취약 확률 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT051 | 중독 저항 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT052 | 화상 저항 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT053 | 출혈 저항 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT054 | 기절 저항 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT055 | 빙결 저항 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT056 | 침묵 저항 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT057 | 혼란 저항 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT058 | 암흑 저항 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT059 | 부식 저항 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT060 | 저주 저항 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT061 | 공격 스킬 피해 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT062 | 방어 스킬 효율 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT063 | 회복 스킬 효율 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT064 | 버프 지속시간 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT065 | MP 소비 절감 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT066 | 스킬 치명타율 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT067 | 스킬 적중률 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT068 | 스킬 재사용 감소 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT069 | 연속타 확률 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT070 | 스킬 사용 후 방어 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT071 | 턴 시작 HP 회복 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT072 | 턴 시작 MP 회복 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT073 | 전투 승리 HP 회복 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT074 | 전투 승리 MP 회복 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT075 | 회복량 증가 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT076 | 포션 효율 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT077 | 최대HP 증가율 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT078 | 최대MP 증가율 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT079 | 전투 시작 보호막 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT080 | 사망 위험 피해감소 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT081 | 도주 성공률 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT082 | 회피 성공 보너스 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT083 | 반격 피해 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT084 | 받는 치명 피해 감소 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT085 | 첫 턴 피해 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT086 | 처치 시 공격력 증가 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT087 | 방어 행동 효율 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT088 | 연속 타격 피해 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT089 | 정예 상대 피해 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT090 | 보스 상대 피해 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT091 | 보물 이벤트 가중치 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT092 | 재료 획득량 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT093 | 보스 보상 골드 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT094 | 정예 경험치 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT095 | 소모품 드롭률 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT096 | 이벤트 골드 보상 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT097 | 거점 회복 할인 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT098 | 상점 구매 할인 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT099 | 장비 판매 가격 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |
| OPT100 | 강화 비용 할인 | 미연결 | 3 | 슬롯·중복·범위·실제 효과 | 미판정 |

## 소비품 — 50개

| 원본 ID | 이름 | 현재 상태·연결 ID | 예정 단계 | 필수 연결·검수 | 최종 판정/증빙 |
|---|---|---|---|---|---|
| CON001 | 소형 HP 물약 | 실행 연결: catalogue.v3.CON001 | 3 | 회복/효과·해금·가격·사용 상황 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| CON002 | 중형 HP 물약 | 실행 연결: catalogue.v3.CON002 | 3 | 회복/효과·해금·가격·사용 상황 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| CON003 | 대형 HP 물약 | 실행 연결: catalogue.v3.CON003 | 3 | 회복/효과·해금·가격·사용 상황 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| CON004 | 최상급 HP 물약 | 실행 연결: catalogue.v3.CON004 | 3 | 회복/효과·해금·가격·사용 상황 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| CON005 | 소형 MP 물약 | 실행 연결: catalogue.v3.CON005 | 3 | 회복/효과·해금·가격·사용 상황 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| CON006 | 중형 MP 물약 | 실행 연결: catalogue.v3.CON006 | 3 | 회복/효과·해금·가격·사용 상황 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| CON007 | 대형 MP 물약 | 실행 연결: catalogue.v3.CON007 | 3 | 회복/효과·해금·가격·사용 상황 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| CON008 | 최상급 MP 물약 | 실행 연결: catalogue.v3.CON008 | 3 | 회복/효과·해금·가격·사용 상황 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| CON009 | 힘의 물약 | 실행 연결: catalogue.v3.CON009 | 3 | 회복/효과·해금·가격·사용 상황 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| CON010 | 수호의 물약 | 실행 연결: catalogue.v3.CON010 | 3 | 회복/효과·해금·가격·사용 상황 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| CON011 | 치명타 물약 | 실행 연결: catalogue.v3.CON011 | 3 | 회복/효과·해금·가격·사용 상황 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| CON012 | 신속 물약 | 실행 연결: catalogue.v3.CON012 | 3 | 회복/효과·해금·가격·사용 상황 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| CON013 | 해독제 | 실행 연결: catalogue.v3.CON013 | 3 | 회복/효과·해금·가격·사용 상황 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| CON014 | 화상 치료제 | 실행 연결: catalogue.v3.CON014 | 3 | 회복/효과·해금·가격·사용 상황 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| CON015 | 해주 물약 | 실행 연결: catalogue.v3.CON015 | 3 | 회복/효과·해금·가격·사용 상황 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| CON016 | 만능 치료제 | 실행 연결: catalogue.v3.CON016 | 3 | 회복/효과·해금·가격·사용 상황 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| CON017 | 귀환 주문서 | 실행 연결: catalogue.v3.CON017 | 3 | 회복/효과·해금·가격·사용 상황 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| CON018 | 보물 탐지기 | 실행 연결: catalogue.v3.CON018 | 3 | 회복/효과·해금·가격·사용 상황 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| CON019 | 행운의 부적 | 실행 연결: catalogue.v3.CON019 | 3 | 회복/효과·해금·가격·사용 상황 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| CON020 | 보호 주문서 | 실행 연결: catalogue.v3.CON020 | 3 | 회복/효과·해금·가격·사용 상황 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| CON021 | 회복 비약 | 실행 연결: catalogue.v3.CON021 | 3 | 회복/효과·해금·가격·사용 상황 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| CON022 | 치유의 진액 | 실행 연결: catalogue.v3.CON022 | 3 | 회복/효과·해금·가격·사용 상황 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| CON023 | 생명의 영약 | 실행 연결: catalogue.v3.CON023 | 3 | 회복/효과·해금·가격·사용 상황 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| CON024 | 여명의 성수 | 실행 연결: catalogue.v3.CON024 | 3 | 회복/효과·해금·가격·사용 상황 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| CON025 | 불사의 물약 | 실행 연결: catalogue.v3.CON025 | 3 | 회복/효과·해금·가격·사용 상황 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| CON026 | 응급 보호막 | 미연결 | 3 | 회복/효과·해금·가격·사용 상황 | 미판정 |
| CON027 | 철갑 비약 | 미연결 | 3 | 회복/효과·해금·가격·사용 상황 | 미판정 |
| CON028 | 결계 스크롤 | 미연결 | 3 | 회복/효과·해금·가격·사용 상황 | 미판정 |
| CON029 | 피해 감소 영약 | 미연결 | 3 | 회복/효과·해금·가격·사용 상황 | 미판정 |
| CON030 | 최후의 보호 부적 | 미연결 | 3 | 회복/효과·해금·가격·사용 상황 | 미판정 |
| CON031 | 화염 저항제 | 미연결 | 3 | 회복/효과·해금·가격·사용 상황 | 미판정 |
| CON032 | 냉기 저항제 | 미연결 | 3 | 회복/효과·해금·가격·사용 상황 | 미판정 |
| CON033 | 번개 저항제 | 미연결 | 3 | 회복/효과·해금·가격·사용 상황 | 미판정 |
| CON034 | 독성 저항제 | 미연결 | 3 | 회복/효과·해금·가격·사용 상황 | 미판정 |
| CON035 | 암흑 저항제 | 미연결 | 3 | 회복/효과·해금·가격·사용 상황 | 미판정 |
| CON036 | 정신 정화제 | 실행 연결: catalogue.v3.CON036 | 3 | 회복/효과·해금·가격·사용 상황 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| CON037 | 감전 해제제 | 실행 연결: catalogue.v3.CON037 | 3 | 회복/효과·해금·가격·사용 상황 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| CON038 | 동상 치료제 | 실행 연결: catalogue.v3.CON038 | 3 | 회복/효과·해금·가격·사용 상황 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| CON039 | 부식 정화제 | 실행 연결: catalogue.v3.CON039 | 3 | 회복/효과·해금·가격·사용 상황 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| CON040 | 영혼 정화제 | 실행 연결: catalogue.v3.CON040 | 3 | 회복/효과·해금·가격·사용 상황 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| CON041 | 정예 탐지 주문서 | 미연결 | 3 | 회복/효과·해금·가격·사용 상황 | 미판정 |
| CON042 | 재료 탐색 지도 | 미연결 | 3 | 회복/효과·해금·가격·사용 상황 | 미판정 |
| CON043 | 경험치 비약 | 미연결 | 3 | 회복/효과·해금·가격·사용 상황 | 미판정 |
| CON044 | 골드 증폭 물약 | 미연결 | 3 | 회복/효과·해금·가격·사용 상황 | 미판정 |
| CON045 | 귀환 보호 부적 | 미연결 | 3 | 회복/효과·해금·가격·사용 상황 | 미판정 |
| CON046 | 화염 폭탄 | 미연결 | 3 | 회복/효과·해금·가격·사용 상황 | 미판정 |
| CON047 | 냉기 폭탄 | 미연결 | 3 | 회복/효과·해금·가격·사용 상황 | 미판정 |
| CON048 | 번개 구슬 | 미연결 | 3 | 회복/효과·해금·가격·사용 상황 | 미판정 |
| CON049 | 맹독 투척병 | 미연결 | 3 | 회복/효과·해금·가격·사용 상황 | 미판정 |
| CON050 | 광휘의 수류탄 | 미연결 | 3 | 회복/효과·해금·가격·사용 상황 | 미판정 |

## 재료 — 60개

| 원본 ID | 이름 | 현재 상태·연결 ID | 예정 단계 | 필수 연결·검수 | 최종 판정/증빙 |
|---|---|---|---|---|---|
| MAT001 | 철광석 | 실행 연결: catalogue.v3.MAT001 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT002 | 은광석 | 실행 연결: catalogue.v3.MAT002 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT003 | 금광석 | 실행 연결: catalogue.v3.MAT003 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT004 | 미스릴 | 실행 연결: catalogue.v3.MAT004 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT005 | 아다만티움 | 실행 연결: catalogue.v3.MAT005 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT006 | 뼈 조각 | 실행 연결: catalogue.v3.MAT006 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT007 | 짐승 가죽 | 실행 연결: catalogue.v3.MAT007 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT008 | 독샘 | 실행 연결: catalogue.v3.MAT008 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT009 | 악마의 뿔 | 실행 연결: catalogue.v3.MAT009 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT010 | 마력핵 | 실행 연결: catalogue.v3.MAT010 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT011 | 마석 | 실행 연결: catalogue.v3.MAT011 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT012 | 정령석 | 실행 연결: catalogue.v3.MAT012 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT013 | 룬 파편 | 실행 연결: catalogue.v3.MAT013 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT014 | 혼돈의 결정 | 실행 연결: catalogue.v3.MAT014 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT015 | 심연석 | 실행 연결: catalogue.v3.MAT015 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT016 | 강화석 | 실행 연결: catalogue.v3.MAT016 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT017 | 고급 강화석 | 실행 연결: catalogue.v3.MAT017 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT018 | 보스 결정 | 실행 연결: catalogue.v3.MAT018 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT019 | 고대 파편 | 실행 연결: catalogue.v3.MAT019 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT020 | 전설의 정수 | 실행 연결: catalogue.v3.MAT020 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT021 | 흑요철 | 실행 연결: catalogue.v3.MAT021 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT022 | 월은광 | 실행 연결: catalogue.v3.MAT022 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT023 | 용린석 | 실행 연결: catalogue.v3.MAT023 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT024 | 성철 | 실행 연결: catalogue.v3.MAT024 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT025 | 빛나는 철가루 | 실행 연결: catalogue.v3.MAT025 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT026 | 마력 합금 | 실행 연결: catalogue.v3.MAT026 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT027 | 유성철 | 실행 연결: catalogue.v3.MAT027 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT028 | 공허광 | 실행 연결: catalogue.v3.MAT028 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT029 | 수인 송곳니 | 실행 연결: catalogue.v3.MAT029 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT030 | 용족 비늘 | 실행 연결: catalogue.v3.MAT030 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT031 | 심해 촉수 | 실행 연결: catalogue.v3.MAT031 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT032 | 균사 핵 | 실행 연결: catalogue.v3.MAT032 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT033 | 와이번 발톱 | 실행 연결: catalogue.v3.MAT033 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT034 | 사막 뿔 | 실행 연결: catalogue.v3.MAT034 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT035 | 변이 갑각 | 실행 연결: catalogue.v3.MAT035 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT036 | 영혼 가죽 | 실행 연결: catalogue.v3.MAT036 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT037 | 별빛 가루 | 실행 연결: catalogue.v3.MAT037 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT038 | 시간 파편 | 실행 연결: catalogue.v3.MAT038 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT039 | 달의 정수 | 실행 연결: catalogue.v3.MAT039 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT040 | 태양 정수 | 실행 연결: catalogue.v3.MAT040 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT041 | 마력 꽃잎 | 실행 연결: catalogue.v3.MAT041 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT042 | 혼돈 구슬 | 실행 연결: catalogue.v3.MAT042 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT043 | 원소 결정 | 실행 연결: catalogue.v3.MAT043 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT044 | 영혼 잉크 | 실행 연결: catalogue.v3.MAT044 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT045 | 야수왕 문장 | 실행 연결: catalogue.v3.MAT045 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT046 | 교단의 가면 | 실행 연결: catalogue.v3.MAT046 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT047 | 기계 군단 핵 | 실행 연결: catalogue.v3.MAT047 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT048 | 심해왕 진주 | 실행 연결: catalogue.v3.MAT048 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT049 | 균사왕 포자 | 실행 연결: catalogue.v3.MAT049 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT050 | 성좌의 눈 | 실행 연결: catalogue.v3.MAT050 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT051 | 영혼 관 | 실행 연결: catalogue.v3.MAT051 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT052 | 공허 수정핵 | 실행 연결: catalogue.v3.MAT052 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT053 | 순수 강화석 | 실행 연결: catalogue.v3.MAT053 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT054 | 정교한 강화석 | 실행 연결: catalogue.v3.MAT054 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT055 | 고대 연마제 | 실행 연결: catalogue.v3.MAT055 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT056 | 룬 접합제 | 실행 연결: catalogue.v3.MAT056 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT057 | 별의 조각 | 실행 연결: catalogue.v3.MAT057 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT058 | 전설 각인석 | 실행 연결: catalogue.v3.MAT058 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT059 | 정화 촉매 | 실행 연결: catalogue.v3.MAT059 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| MAT060 | 심연 정제석 | 실행 연결: catalogue.v3.MAT060 | 3·4 | 획득·제작/정제/강화 소비처 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |

## 이벤트 — 200개

| 원본 ID | 이름 | 현재 상태·연결 ID | 예정 단계 | 필수 연결·검수 | 최종 판정/증빙 |
|---|---|---|---|---|---|
| EVT001 | 낡은 상자 | 2차 연결: phase2.event.EVT001 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT002 | 숨겨진 금고 | 2차 연결: phase2.event.EVT002 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT003 | 비밀 창고 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT004 | 보물 지도 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT005 | 봉인된 궤짝 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT006 | 가시 함정 | 2차 연결: phase2.event.EVT006 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT007 | 독가스 | 2차 연결: phase2.event.EVT007 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT008 | 낙석 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT009 | 화염 함정 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT010 | 무너지는 바닥 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT011 | 회복의 샘 | 2차 연결: phase2.event.EVT011 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT012 | 안전한 야영지 | 2차 연결: phase2.event.EVT012 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT013 | 치유의 제단 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT014 | 약초밭 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT015 | 정령의 축복 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT016 | 떠돌이 상인 | 2차 연결: phase2.event.EVT016 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT017 | 수상한 상인 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT018 | 암시장 상인 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT019 | 약초상 | 2차 연결: phase2.event.EVT019 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT020 | 유물상 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT021 | 고대 제단 | 2차 연결: phase2.event.EVT021 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT022 | 피의 제단 | 2차 연결: phase2.event.EVT022 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT023 | 행운의 신전 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT024 | 저주의 제단 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT025 | 잊힌 성소 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT026 | 갈림길 | 2차 연결: phase2.event.EVT026 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT027 | 수상한 문 | 2차 연결: phase2.event.EVT027 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT028 | 어두운 통로 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT029 | 폐쇄된 방 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT030 | 지하 미로 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT031 | 부상자 | 2차 연결: phase2.event.EVT031 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT032 | 길 잃은 상인 | 2차 연결: phase2.event.EVT032 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT033 | 수상한 기사 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT034 | 도망친 죄수 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT035 | 고대 학자 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT036 | 몬스터 매복 | 2차 연결: phase2.event.EVT036 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT037 | 정예 출현 | 2차 연결: phase2.event.EVT037 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT038 | 군집 공격 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT039 | 보물 수호자 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT040 | 복수자 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT041 | 고대 비석 | 2차 연결: phase2.event.EVT041 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT042 | 신비한 수정 | 2차 연결: phase2.event.EVT042 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT043 | 유물 조각 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT044 | 마법 서고 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT045 | 황금 제단 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT046 | 저주받은 계약 | 2차 연결: phase2.event.EVT046 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT047 | 운명의 주사위 | 2차 연결: phase2.event.EVT047 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT048 | 수상한 우물 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT049 | 영혼 거래 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT050 | 미지의 포탈 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT051 | 부서진 보석함 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT052 | 별무리 금고 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT053 | 깊은 균열의 상자 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT054 | 바다 유리 궤짝 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT055 | 고대 황실 창고 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT056 | 용의 은닉물 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT057 | 지하 철제 금고 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT058 | 잊힌 장부 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT059 | 금빛 지도의 끝 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT060 | 움직이는 보관함 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT061 | 빛의 보석함 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT062 | 검은 수정 상자 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT063 | 비밀 전리품 창고 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT064 | 마력 잠금 상자 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT065 | 봉인된 왕실 상자 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT066 | 사슬 낙하 함정 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT067 | 붕괴된 용암판 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT068 | 순간 빙결 장치 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT069 | 실명 가루 덫 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT070 | 바닥 전격 문양 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT071 | 영혼 흡수 진 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT072 | 독성 수정 기둥 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT073 | 자동 발사 석궁 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT074 | 역중력 마법진 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT075 | 혼돈의 미로 함정 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT076 | 부식성 웅덩이 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT077 | 돌아가는 칼날 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT078 | 파도 압력 함정 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT079 | 균사 감염 포자 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT080 | 용암 분출구 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT081 | 푸른 생명수 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT082 | 수호자의 안식처 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT083 | 빛의 호수 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT084 | 정령의 숨결 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT085 | 잃어버린 의무실 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT086 | 마력 재생 돌 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT087 | 해질녘 야영지 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT088 | 별빛 휴식당 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT089 | 용혈 온천 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT090 | 성좌의 축복 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT091 | 상처를 봉합하는 이끼 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT092 | 영혼의 안식터 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT093 | 마법사의 실험대 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT094 | 고대 의료기 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT095 | 거울 속 치유실 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT096 | 달빛 교역상 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT097 | 수인 교환상 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT098 | 유물 해체상 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT099 | 용린 무기상 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT100 | 마력 약제사 | 미연결 | 3 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT101 | 균사 수집가 | 미연결 | 5 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT102 | 유성철 대장장이 | 미연결 | 5 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT103 | 영혼 저당상 | 미연결 | 5 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT104 | 고대 기록상 | 미연결 | 5 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT105 | 비밀 주화상 | 미연결 | 5 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT106 | 성좌 점술사 | 미연결 | 5 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT107 | 마석 중개인 | 미연결 | 5 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT108 | 흑철 수리상 | 미연결 | 5 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT109 | 공허 떠돌이 | 미연결 | 5 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT110 | 위험물 상인 | 미연결 | 5 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT111 | 별자리 기도실 | 미연결 | 5 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT112 | 깨어진 의식진 | 미연결 | 5 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT113 | 수인 조상 제단 | 미연결 | 5 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT114 | 용혈 봉헌대 | 미연결 | 5 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT115 | 마력 폭주 신전 | 미연결 | 5 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT116 | 검은 달 제단 | 미연결 | 5 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT117 | 변이의 석상 | 미연결 | 5 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT118 | 타락한 성수대 | 미연결 | 5 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT119 | 천공의 오벨리스크 | 미연결 | 5 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT120 | 정화의 분수 | 미연결 | 5 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT121 | 균사 부활 제단 | 미연결 | 5 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT122 | 망령의 고백실 | 미연결 | 5 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT123 | 시간의 성소 | 미연결 | 5 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT124 | 잊힌 왕의 묘비 | 미연결 | 5 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT125 | 허공의 약속 | 미연결 | 5 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT126 | 세 갈래 관문 | 미연결 | 5 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT127 | 물에 잠긴 계단 | 미연결 | 5 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT128 | 빛을 잃은 도서관 | 미연결 | 5 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT129 | 움직이는 복도 | 미연결 | 5 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT130 | 고요한 관측대 | 미연결 | 5 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT131 | 잠긴 함정 통로 | 미연결 | 5 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT132 | 수정 다리 | 미연결 | 5 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT133 | 주술 봉인문 | 미연결 | 5 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT134 | 고대 승강기 | 미연결 | 5 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT135 | 거울 회랑 | 미연결 | 5 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT136 | 사라지는 열쇠 | 미연결 | 5 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT137 | 바람 속 낡은 길 | 미연결 | 5 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT138 | 용의 발자국 | 미연결 | 5 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT139 | 해독되지 않는 표지 | 미연결 | 5 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT140 | 흑철 문 | 미연결 | 5 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT141 | 도망친 수인 아이 | 미연결 | 5 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT142 | 몰락한 대장장이 | 미연결 | 5 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT143 | 자신을 잊은 학자 | 미연결 | 5 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT144 | 길 잃은 의무병 | 미연결 | 5 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT145 | 파산한 교역인 | 미연결 | 5 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT146 | 마력을 잃은 정령 | 미연결 | 5 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT147 | 늙은 기사 | 미연결 | 5 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT148 | 거짓말하는 정찰병 | 미연결 | 5 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT149 | 부상당한 해양인 | 미연결 | 5 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT150 | 포자를 뒤집어쓴 모험가 | 미연결 | 5 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT151 | 시간을 쫓는 기록관 | 미연결 | 7 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT152 | 마석을 구하는 연금술사 | 미연결 | 7 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT153 | 유품을 찾는 망령 | 미연결 | 7 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT154 | 침묵의 음유시인 | 미연결 | 7 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT155 | 공허에 갇힌 병사 | 미연결 | 7 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT156 | 깊은 매복 진형 | 미연결 | 7 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT157 | 광폭화 무리 | 미연결 | 7 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT158 | 전장 난입자 | 미연결 | 7 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT159 | 정예의 도전 | 미연결 | 7 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT160 | 불사의 수호대 | 미연결 | 7 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT161 | 생체 무기 실험 | 미연결 | 7 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT162 | 용족의 사냥 | 미연결 | 7 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT163 | 맹독의 축제 | 미연결 | 7 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT164 | 균사 폭발전 | 미연결 | 7 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT165 | 기계 순찰대 | 미연결 | 7 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT166 | 심해 습격 | 미연결 | 7 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT167 | 연속 결투 | 미연결 | 7 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT168 | 기억 수호자의 시련 | 미연결 | 7 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT169 | 상급 사냥꾼 | 미연결 | 7 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT170 | 혼돈의 불시전 | 미연결 | 7 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT171 | 고대 지도 조각 | 미연결 | 7 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT172 | 마석 비축실 | 미연결 | 7 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT173 | 전쟁 기록석 | 미연결 | 7 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT174 | 성좌의 서책 | 미연결 | 7 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT175 | 황실 군수물자 | 미연결 | 7 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT176 | 유성 보물함 | 미연결 | 7 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT177 | 수인 공훈장 | 미연결 | 7 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT178 | 마력 계량기 | 미연결 | 7 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT179 | 정령 씨앗 | 미연결 | 7 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT180 | 영혼 병 | 미연결 | 7 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT181 | 붉은 결정 파편 | 미연결 | 7 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT182 | 신탁의 잔해 | 미연결 | 7 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT183 | 고대 무기 도면 | 미연결 | 7 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT184 | 불멸의 흑서 | 미연결 | 7 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT185 | 심해 진주 조각 | 미연결 | 7 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT186 | 저주받은 동전 | 미연결 | 7 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT187 | 심연 속 도박사 | 미연결 | 7 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT188 | 부서진 운명판 | 미연결 | 7 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT189 | 붉은 운명의 문 | 미연결 | 7 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT190 | 영혼의 저울 | 미연결 | 7 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT191 | 달의 룰렛 | 미연결 | 7 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT192 | 낡은 욕망의 탁자 | 미연결 | 7 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT193 | 마력 추첨기 | 미연결 | 7 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT194 | 금빛 균열 | 미연결 | 7 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT195 | 예언의 세 주사위 | 미연결 | 7 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT196 | 공허와의 내기 | 미연결 | 7 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT197 | 황혼의 계약서 | 미연결 | 7 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT198 | 왕좌의 시험 | 미연결 | 7 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT199 | 죽음의 동전 던지기 | 미연결 | 7 | 조건·비용·성공/실패·결과 저장 | 미판정 |
| EVT200 | 별빛 맹세 | 미연결 | 7 | 조건·비용·성공/실패·결과 저장 | 미판정 |

## 환경 — 30개

| 원본 ID | 이름 | 현재 상태·연결 ID | 예정 단계 | 필수 연결·검수 | 최종 판정/증빙 |
|---|---|---|---|---|---|
| ENV001 | 버려진 지하실 | 실행 연결: catalogue.v3.ENV001 | 3 | 지역·가중치·보정·표시 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| ENV002 | 고블린 소굴 | 실행 연결: catalogue.v3.ENV002 | 3 | 지역·가중치·보정·표시 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| ENV003 | 지하 묘지 | 실행 연결: catalogue.v3.ENV003 | 3 | 지역·가중치·보정·표시 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| ENV004 | 맹독 늪지 | 실행 연결: catalogue.v3.ENV004 | 3 | 지역·가중치·보정·표시 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| ENV005 | 얼어붙은 동굴 | 실행 연결: catalogue.v3.ENV005 | 3 | 지역·가중치·보정·표시 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| ENV006 | 불타는 심연 | 실행 연결: catalogue.v3.ENV006 | 3 | 지역·가중치·보정·표시 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| ENV007 | 고대 신전 | 실행 연결: catalogue.v3.ENV007 | 3 | 지역·가중치·보정·표시 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| ENV008 | 잊힌 성채 | 실행 연결: catalogue.v3.ENV008 | 3 | 지역·가중치·보정·표시 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| ENV009 | 공허의 균열 | 실행 연결: catalogue.v3.ENV009 | 3 | 지역·가중치·보정·표시 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| ENV010 | 심연의 왕좌 | 실행 연결: catalogue.v3.ENV010 | 3 | 지역·가중치·보정·표시 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| ENV011 | 깊은 수인 분지 | 실행 연결: catalogue.v3.ENV011 | 3 | 지역·가중치·보정·표시 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| ENV012 | 늑대 달의 숲 | 실행 연결: catalogue.v3.ENV012 | 3 | 지역·가중치·보정·표시 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| ENV013 | 검은 예배당 | 실행 연결: catalogue.v3.ENV013 | 3 | 지역·가중치·보정·표시 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| ENV014 | 낙인의 회랑 | 실행 연결: catalogue.v3.ENV014 | 3 | 지역·가중치·보정·표시 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| ENV015 | 용의 무덤 | 실행 연결: catalogue.v3.ENV015 | 3 | 지역·가중치·보정·표시 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| ENV016 | 비룡 둥지 | 실행 연결: catalogue.v3.ENV016 | 3 | 지역·가중치·보정·표시 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| ENV017 | 증기 공장 | 실행 연결: catalogue.v3.ENV017 | 3 | 지역·가중치·보정·표시 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| ENV018 | 시계태엽 성 | 실행 연결: catalogue.v3.ENV018 | 3 | 지역·가중치·보정·표시 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| ENV019 | 가라앉은 수로 | 실행 연결: catalogue.v3.ENV019 | 3 | 지역·가중치·보정·표시 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| ENV020 | 해구의 제단 | 실행 연결: catalogue.v3.ENV020 | 3 | 지역·가중치·보정·표시 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| ENV021 | 포자 동굴 | 실행 연결: catalogue.v3.ENV021 | 3 | 지역·가중치·보정·표시 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| ENV022 | 균사 정원 | 실행 연결: catalogue.v3.ENV022 | 3 | 지역·가중치·보정·표시 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| ENV023 | 유리 사막 | 실행 연결: catalogue.v3.ENV023 | 3 | 지역·가중치·보정·표시 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| ENV024 | 태양의 유적 | 실행 연결: catalogue.v3.ENV024 | 3 | 지역·가중치·보정·표시 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| ENV025 | 수정 광맥 | 실행 연결: catalogue.v3.ENV025 | 3 | 지역·가중치·보정·표시 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| ENV026 | 마석 제련소 | 실행 연결: catalogue.v3.ENV026 | 3 | 지역·가중치·보정·표시 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| ENV027 | 별빛 관측소 | 실행 연결: catalogue.v3.ENV027 | 3 | 지역·가중치·보정·표시 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| ENV028 | 월식의 탑 | 실행 연결: catalogue.v3.ENV028 | 3 | 지역·가중치·보정·표시 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| ENV029 | 혼돈의 실험실 | 실행 연결: catalogue.v3.ENV029 | 3 | 지역·가중치·보정·표시 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |
| ENV030 | 영혼 왕실 회랑 | 실행 연결: catalogue.v3.ENV030 | 3 | 지역·가중치·보정·표시 | [고층 경로 연결·후속 전수 검수](HIGH_FLOORS.md) |

## 층 유형 — 5개

| 원본 ID | 이름 | 현재 상태·연결 ID | 예정 단계 | 필수 연결·검수 | 최종 판정/증빙 |
|---|---|---|---|---|---|
| FLR001 | 일반 층 | 1차 연결: catalogue.v3.FLR001 | 3 | 출현 확률·전투/보상 보정 | 미판정 |
| FLR002 | 정예 층 | 1차 연결: catalogue.v3.FLR002 | 3 | 출현 확률·전투/보상 보정 | 미판정 |
| FLR003 | 보물 층 | 1차 연결: catalogue.v3.FLR003 | 3 | 출현 확률·전투/보상 보정 | 미판정 |
| FLR004 | 위험 층 | 1차 연결: catalogue.v3.FLR004 | 3 | 출현 확률·전투/보상 보정 | 미판정 |
| FLR005 | 보스 층 | 1차 연결: catalogue.v3.FLR005 | 3 | 출현 확률·전투/보상 보정 | 미판정 |

## 스킬 — 70개

| 원본 ID | 이름 | 현재 상태·연결 ID | 예정 단계 | 필수 연결·검수 | 최종 판정/증빙 |
|---|---|---|---|---|---|
| SKL001 | 강타 | 별도 기존 구현: base.skill.strike; 통합 대조 필요 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL002 | 연속 베기 | 별도 기존 구현: base.skill.slash; 통합 대조 필요 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL003 | 관통 공격 | 2차 연결: phase2.skill.SKL003 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL004 | 처형 | 2차 연결: phase2.skill.SKL004 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL005 | 분쇄 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL006 | 철벽 방어 | 2차 연결: phase2.skill.SKL006 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL007 | 반격 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL008 | 피해 흡수 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL009 | 보호막 | 2차 연결: phase2.skill.SKL009 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL010 | 불굴 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL011 | 회복 | 별도 기존 구현: base.skill.heal; 통합 대조 필요 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL012 | 재생 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL013 | 응급 치료 | 2차 연결: phase2.skill.SKL013 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL014 | 정신 집중 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL015 | 생명 흡수 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL016 | 전투의 함성 | 2차 연결: phase2.skill.SKL016 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL017 | 광폭화 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL018 | 집중 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL019 | 신속 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL020 | 전투 준비 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL021 | 무기 숙련 | 별도 기존 구현: base.skill.weapon; 통합 대조 필요 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL022 | 철벽 | 별도 기존 구현: base.skill.wall; 통합 대조 필요 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL023 | 강인한 생명력 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL024 | 행운의 전사 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL025 | 치명적 일격 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL026 | 폭풍 베기 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL027 | 용의 일격 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL028 | 마력 절단 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL029 | 급습 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL030 | 지각 파쇄 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL031 | 독성 검술 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL032 | 혼돈 난격 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL033 | 빛의 처단 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL034 | 방어 진형 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL035 | 투사의 결의 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL036 | 정령 보호 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL037 | 응보의 자세 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL038 | 생명 물결 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL039 | 마나 순환 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL040 | 정화의 숨결 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL041 | 전장의 응급술 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL042 | 성좌의 함성 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL043 | 고속 연격 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL044 | 죽음 극복 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL045 | 운명의 편린 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL046 | 용기의 힘 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL047 | 굳센 의지 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL048 | 생명의 그릇 | 2차 연결: phase2.skill.SKL048 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL049 | 마력의 그릇 | 2차 연결: phase2.skill.SKL049 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL050 | 예리한 눈 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL051 | 민첩한 발 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL052 | 행운의 손 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL053 | 학습 열정 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL054 | 강철 피부 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL055 | 원소 수련 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL056 | 독 저항 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL057 | 화염 저항 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL058 | 빙결 저항 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL059 | 심연 적응 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL060 | 치명 숙련 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL061 | 재생 체질 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL062 | 마나 호흡 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL063 | 위기 대처 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL064 | 보스 사냥꾼 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL065 | 정예 추적자 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL066 | 전리품 감식 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL067 | 금화 탐지 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL068 | 긴급 회복 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL069 | 숙련 강화자 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |
| SKL070 | 불굴의 생명 | 미연결 | 5 | 학습·자동·대기·성장·통합 | 미판정 |

## 유물 — 24개

| 원본 ID | 이름 | 현재 상태·연결 ID | 예정 단계 | 필수 연결·검수 | 최종 판정/증빙 |
|---|---|---|---|---|---|
| REL001 | 전사의 문장 | 미연결 | 6 | 획득·가루·강화·장착·상한 | 미판정 |
| REL002 | 강철 심장 | 미연결 | 6 | 획득·가루·강화·장착·상한 | 미판정 |
| REL003 | 생명의 수정 | 미연결 | 6 | 획득·가루·강화·장착·상한 | 미판정 |
| REL004 | 마력의 핵 | 미연결 | 6 | 획득·가루·강화·장착·상한 | 미판정 |
| REL005 | 바람의 깃털 | 미연결 | 6 | 획득·가루·강화·장착·상한 | 미판정 |
| REL006 | 예리한 송곳니 | 미연결 | 6 | 획득·가루·강화·장착·상한 | 미판정 |
| REL007 | 흡혈의 송곳니 | 미연결 | 6 | 획득·가루·강화·장착·상한 | 미판정 |
| REL008 | 불사조의 재 | 미연결 | 6 | 획득·가루·강화·장착·상한 | 미판정 |
| REL009 | 수호자의 눈 | 미연결 | 6 | 획득·가루·강화·장착·상한 | 미판정 |
| REL010 | 생명의 나뭇잎 | 미연결 | 6 | 획득·가루·강화·장착·상한 | 미판정 |
| REL011 | 정화의 구슬 | 미연결 | 6 | 획득·가루·강화·장착·상한 | 미판정 |
| REL012 | 반격의 인장 | 미연결 | 6 | 획득·가루·강화·장착·상한 | 미판정 |
| REL013 | 황금 나침반 | 미연결 | 6 | 획득·가루·강화·장착·상한 | 미판정 |
| REL014 | 지혜의 서판 | 미연결 | 6 | 획득·가루·강화·장착·상한 | 미판정 |
| REL015 | 행운의 주사위 | 미연결 | 6 | 획득·가루·강화·장착·상한 | 미판정 |
| REL016 | 보물 탐지석 | 미연결 | 6 | 획득·가루·강화·장착·상한 | 미판정 |
| REL017 | 수집가의 주머니 | 미연결 | 6 | 획득·가루·강화·장착·상한 | 미판정 |
| REL018 | 강화의 룬 | 미연결 | 6 | 획득·가루·강화·장착·상한 | 미판정 |
| REL019 | 화염의 보주 | 미연결 | 6 | 획득·가루·강화·장착·상한 | 미판정 |
| REL020 | 독사의 눈 | 미연결 | 6 | 획득·가루·강화·장착·상한 | 미판정 |
| REL021 | 얼음의 결정 | 미연결 | 6 | 획득·가루·강화·장착·상한 | 미판정 |
| REL022 | 마법사의 고서 | 미연결 | 6 | 획득·가루·강화·장착·상한 | 미판정 |
| REL023 | 심연의 파편 | 미연결 | 6 | 획득·가루·강화·장착·상한 | 미판정 |
| REL024 | 영원의 시계 | 미연결 | 6 | 획득·가루·강화·장착·상한 | 미판정 |

## 현상금 — 24개

| 원본 ID | 이름 | 현재 상태·연결 ID | 예정 단계 | 필수 연결·검수 | 최종 판정/증빙 |
|---|---|---|---|---|---|
| BNT001 | 일반 몬스터 1단계 | 미연결 | 7 | 대상 고정·진척·보고·보상 | 미판정 |
| BNT002 | 일반 몬스터 2단계 | 미연결 | 7 | 대상 고정·진척·보고·보상 | 미판정 |
| BNT003 | 일반 몬스터 3단계 | 미연결 | 7 | 대상 고정·진척·보고·보상 | 미판정 |
| BNT004 | 일반 몬스터 4단계 | 미연결 | 7 | 대상 고정·진척·보고·보상 | 미판정 |
| BNT005 | 정예 몬스터 1단계 | 미연결 | 7 | 대상 고정·진척·보고·보상 | 미판정 |
| BNT006 | 정예 몬스터 2단계 | 미연결 | 7 | 대상 고정·진척·보고·보상 | 미판정 |
| BNT007 | 정예 몬스터 3단계 | 미연결 | 7 | 대상 고정·진척·보고·보상 | 미판정 |
| BNT008 | 정예 몬스터 4단계 | 미연결 | 7 | 대상 고정·진척·보고·보상 | 미판정 |
| BNT009 | 보스 사냥 1단계 | 미연결 | 7 | 대상 고정·진척·보고·보상 | 미판정 |
| BNT010 | 보스 사냥 2단계 | 미연결 | 7 | 대상 고정·진척·보고·보상 | 미판정 |
| BNT011 | 보스 사냥 3단계 | 미연결 | 7 | 대상 고정·진척·보고·보상 | 미판정 |
| BNT012 | 보스 사냥 4단계 | 미연결 | 7 | 대상 고정·진척·보고·보상 | 미판정 |
| BNT013 | 재료 수집 1단계 | 미연결 | 7 | 대상 고정·진척·보고·보상 | 미판정 |
| BNT014 | 재료 수집 2단계 | 미연결 | 7 | 대상 고정·진척·보고·보상 | 미판정 |
| BNT015 | 재료 수집 3단계 | 미연결 | 7 | 대상 고정·진척·보고·보상 | 미판정 |
| BNT016 | 재료 수집 4단계 | 미연결 | 7 | 대상 고정·진척·보고·보상 | 미판정 |
| BNT017 | 던전 탐험 1단계 | 미연결 | 7 | 대상 고정·진척·보고·보상 | 미판정 |
| BNT018 | 던전 탐험 2단계 | 미연결 | 7 | 대상 고정·진척·보고·보상 | 미판정 |
| BNT019 | 던전 탐험 3단계 | 미연결 | 7 | 대상 고정·진척·보고·보상 | 미판정 |
| BNT020 | 던전 탐험 4단계 | 미연결 | 7 | 대상 고정·진척·보고·보상 | 미판정 |
| BNT021 | 이벤트 조사 1단계 | 미연결 | 7 | 대상 고정·진척·보고·보상 | 미판정 |
| BNT022 | 이벤트 조사 2단계 | 미연결 | 7 | 대상 고정·진척·보고·보상 | 미판정 |
| BNT023 | 이벤트 조사 3단계 | 미연결 | 7 | 대상 고정·진척·보고·보상 | 미판정 |
| BNT024 | 이벤트 조사 4단계 | 미연결 | 7 | 대상 고정·진척·보고·보상 | 미판정 |

## 직업 트리 — 45개

| 원본 ID | 이름 | 현재 상태·연결 ID | 예정 단계 | 필수 연결·검수 | 최종 판정/증빙 |
|---|---|---|---|---|---|
| TRE001 | 일반 공격 강화 | 미연결 | 5 | 선행·비용·포인트·효과 | 미판정 |
| TRE002 | 강타 강화 | 미연결 | 5 | 선행·비용·포인트·효과 | 미판정 |
| TRE003 | 연속 공격 강화 | 미연결 | 5 | 선행·비용·포인트·효과 | 미판정 |
| TRE004 | 방어력 증진 | 미연결 | 5 | 선행·비용·포인트·효과 | 미판정 |
| TRE005 | 방어 숙련 | 미연결 | 5 | 선행·비용·포인트·효과 | 미판정 |
| TRE006 | 견고한 육체 | 미연결 | 5 | 선행·비용·포인트·효과 | 미판정 |
| TRE007 | 강공격 숙련 | 미연결 | 5 | 선행·비용·포인트·효과 | 미판정 |
| TRE008 | 피의 분노 | 미연결 | 5 | 선행·비용·포인트·효과 | 미판정 |
| TRE009 | 보스 학살 | 미연결 | 5 | 선행·비용·포인트·효과 | 미판정 |
| TRE010 | 급소 노리기 | 미연결 | 5 | 선행·비용·포인트·효과 | 미판정 |
| TRE011 | 치명적인 칼날 | 미연결 | 5 | 선행·비용·포인트·효과 | 미판정 |
| TRE012 | 후속 공격 | 미연결 | 5 | 선행·비용·포인트·효과 | 미판정 |
| TRE013 | 재빠른 발 | 미연결 | 5 | 선행·비용·포인트·효과 | 미판정 |
| TRE014 | 회피 집중 | 미연결 | 5 | 선행·비용·포인트·효과 | 미판정 |
| TRE015 | 빈틈 추격 | 미연결 | 5 | 선행·비용·포인트·효과 | 미판정 |
| TRE016 | 맹독 묻히기 | 미연결 | 5 | 선행·비용·포인트·효과 | 미판정 |
| TRE017 | 독성 강화 | 미연결 | 5 | 선행·비용·포인트·효과 | 미판정 |
| TRE018 | 독의 추격 | 미연결 | 5 | 선행·비용·포인트·효과 | 미판정 |
| TRE019 | 화염 친화 | 미연결 | 5 | 선행·비용·포인트·효과 | 미판정 |
| TRE020 | 작열 | 미연결 | 5 | 선행·비용·포인트·효과 | 미판정 |
| TRE021 | 폭염 추격 | 미연결 | 5 | 선행·비용·포인트·효과 | 미판정 |
| TRE022 | 서리 손길 | 미연결 | 5 | 선행·비용·포인트·효과 | 미판정 |
| TRE023 | 얼음 파쇄 | 미연결 | 5 | 선행·비용·포인트·효과 | 미판정 |
| TRE024 | 빙결 파열 | 미연결 | 5 | 선행·비용·포인트·효과 | 미판정 |
| TRE025 | 마력 저장 | 미연결 | 5 | 선행·비용·포인트·효과 | 미판정 |
| TRE026 | 절제된 마력 | 미연결 | 5 | 선행·비용·포인트·효과 | 미판정 |
| TRE027 | 대마법 | 미연결 | 5 | 선행·비용·포인트·효과 | 미판정 |
| TRE028 | 집중 사격 | 미연결 | 5 | 선행·비용·포인트·효과 | 미판정 |
| TRE029 | 약점 조준 | 미연결 | 5 | 선행·비용·포인트·효과 | 미판정 |
| TRE030 | 치명 조준 | 미연결 | 5 | 선행·비용·포인트·효과 | 미판정 |
| TRE031 | 연사 숙련 | 미연결 | 5 | 선행·비용·포인트·효과 | 미판정 |
| TRE032 | 연속 사격 | 미연결 | 5 | 선행·비용·포인트·효과 | 미판정 |
| TRE033 | 추가 발사 | 미연결 | 5 | 선행·비용·포인트·효과 | 미판정 |
| TRE034 | 정예 추적 | 미연결 | 5 | 선행·비용·포인트·효과 | 미판정 |
| TRE035 | 전리품 수집 | 미연결 | 5 | 선행·비용·포인트·효과 | 미판정 |
| TRE036 | 보스 현상금 | 미연결 | 5 | 선행·비용·포인트·효과 | 미판정 |
| TRE037 | 치유 숙련 | 미연결 | 5 | 선행·비용·포인트·효과 | 미판정 |
| TRE038 | 정신 수련 | 미연결 | 5 | 선행·비용·포인트·효과 | 미판정 |
| TRE039 | 회복의 기도 | 미연결 | 5 | 선행·비용·포인트·효과 | 미판정 |
| TRE040 | 신성 체력 | 미연결 | 5 | 선행·비용·포인트·효과 | 미판정 |
| TRE041 | 청정의 가호 | 미연결 | 5 | 선행·비용·포인트·효과 | 미판정 |
| TRE042 | 성역 | 미연결 | 5 | 선행·비용·포인트·효과 | 미판정 |
| TRE043 | 언데드 심판 | 미연결 | 5 | 선행·비용·포인트·효과 | 미판정 |
| TRE044 | 저주 차단 | 미연결 | 5 | 선행·비용·포인트·효과 | 미판정 |
| TRE045 | 정화의 결의 | 미연결 | 5 | 선행·비용·포인트·효과 | 미판정 |

## 직업 — 5개

| 원본 ID | 이름 | 현재 상태·연결 ID | 예정 단계 | 필수 연결·검수 | 최종 판정/증빙 |
|---|---|---|---|---|---|
| CLS001 | 전사 | 미연결 | 5 | 누적 해금·선택·보너스 | 미판정 |
| CLS002 | 도적 | 미연결 | 5 | 누적 해금·선택·보너스 | 미판정 |
| CLS003 | 마법사 | 미연결 | 5 | 누적 해금·선택·보너스 | 미판정 |
| CLS004 | 궁수 | 미연결 | 5 | 누적 해금·선택·보너스 | 미판정 |
| CLS005 | 성직자 | 미연결 | 5 | 누적 해금·선택·보너스 | 미판정 |

## 전직 — 10개

| 원본 ID | 이름 | 현재 상태·연결 ID | 예정 단계 | 필수 연결·검수 | 최종 판정/증빙 |
|---|---|---|---|---|---|
| ADV001 | 기사 | 미연결 | 5 | 회차 조건·1회 선택·보너스 | 미판정 |
| ADV002 | 광전사 | 미연결 | 5 | 회차 조건·1회 선택·보너스 | 미판정 |
| ADV003 | 암살자 | 미연결 | 5 | 회차 조건·1회 선택·보너스 | 미판정 |
| ADV004 | 그림자 | 미연결 | 5 | 회차 조건·1회 선택·보너스 | 미판정 |
| ADV005 | 화염술사 | 미연결 | 5 | 회차 조건·1회 선택·보너스 | 미판정 |
| ADV006 | 현자 | 미연결 | 5 | 회차 조건·1회 선택·보너스 | 미판정 |
| ADV007 | 저격수 | 미연결 | 5 | 회차 조건·1회 선택·보너스 | 미판정 |
| ADV008 | 사냥꾼 | 미연결 | 5 | 회차 조건·1회 선택·보너스 | 미판정 |
| ADV009 | 성기사 | 미연결 | 5 | 회차 조건·1회 선택·보너스 | 미판정 |
| ADV010 | 정화사 | 미연결 | 5 | 회차 조건·1회 선택·보너스 | 미판정 |

## 계승 — 10개

| 원본 ID | 이름 | 현재 상태·연결 ID | 예정 단계 | 필수 연결·검수 | 최종 판정/증빙 |
|---|---|---|---|---|---|
| PRG001 | 힘의 계승 | 미연결 | 8 | 회차·포인트·상한·영구 보존 | 미판정 |
| PRG002 | 강철의 계승 | 미연결 | 8 | 회차·포인트·상한·영구 보존 | 미판정 |
| PRG003 | 생명의 계승 | 미연결 | 8 | 회차·포인트·상한·영구 보존 | 미판정 |
| PRG004 | 마력의 계승 | 미연결 | 8 | 회차·포인트·상한·영구 보존 | 미판정 |
| PRG005 | 지식의 계승 | 미연결 | 8 | 회차·포인트·상한·영구 보존 | 미판정 |
| PRG006 | 황금의 계승 | 미연결 | 8 | 회차·포인트·상한·영구 보존 | 미판정 |
| PRG007 | 행운의 계승 | 미연결 | 8 | 회차·포인트·상한·영구 보존 | 미판정 |
| PRG008 | 수집의 계승 | 미연결 | 8 | 회차·포인트·상한·영구 보존 | 미판정 |
| PRG009 | 회복의 계승 | 미연결 | 8 | 회차·포인트·상한·영구 보존 | 미판정 |
| PRG010 | 유물의 계승 | 미연결 | 8 | 회차·포인트·상한·영구 보존 | 미판정 |

## 특수 던전 — 6개

| 원본 ID | 이름 | 현재 상태·연결 ID | 예정 단계 | 필수 연결·검수 | 최종 판정/증빙 |
|---|---|---|---|---|---|
| SDG001 | 황금 광산 | 미연결 | 7 | 입장·체크포인트·보상·귀환 | 미판정 |
| SDG002 | 강화석 광산 | 미연결 | 7 | 입장·체크포인트·보상·귀환 | 미판정 |
| SDG003 | 시련의 탑 | 미연결 | 7 | 입장·체크포인트·보상·귀환 | 미판정 |
| SDG004 | 저주받은 묘지 | 미연결 | 7 | 입장·체크포인트·보상·귀환 | 미판정 |
| SDG005 | 보물 미궁 | 미연결 | 7 | 입장·체크포인트·보상·귀환 | 미판정 |
| SDG006 | 심연의 균열 | 미연결 | 7 | 입장·체크포인트·보상·귀환 | 미판정 |

## 시설 — 6개

| 원본 ID | 이름 | 현재 상태·연결 ID | 예정 단계 | 필수 연결·검수 | 최종 판정/증빙 |
|---|---|---|---|---|---|
| FAC001 | 훈련장 | 미연결 | 7 | 비용·레벨·효과·영구 보존 | 미판정 |
| FAC002 | 대장간 | 미연결 | 7 | 비용·레벨·효과·영구 보존 | 미판정 |
| FAC003 | 연금 공방 | 미연결 | 7 | 비용·레벨·효과·영구 보존 | 미판정 |
| FAC004 | 보관소 | 미연결 | 7 | 비용·레벨·효과·영구 보존 | 미판정 |
| FAC005 | 모험가 길드 | 미연결 | 7 | 비용·레벨·효과·영구 보존 | 미판정 |
| FAC006 | 유물 연구소 | 미연결 | 7 | 비용·레벨·효과·영구 보존 | 미판정 |

## 칭호 — 20개

| 원본 ID | 이름 | 현재 상태·연결 ID | 예정 단계 | 필수 연결·검수 | 최종 판정/증빙 |
|---|---|---|---|---|---|
| TTL001 | 초심자 탐험가 | 미연결 | 7 | 해금·장착·효과·누적 보존 | 미판정 |
| TTL002 | 던전 개척자 | 미연결 | 7 | 해금·장착·효과·누적 보존 | 미판정 |
| TTL003 | 심연을 걷는 자 | 미연결 | 7 | 해금·장착·효과·누적 보존 | 미판정 |
| TTL004 | 끝없는 여행자 | 미연결 | 7 | 해금·장착·효과·누적 보존 | 미판정 |
| TTL005 | 몬스터 사냥꾼 | 미연결 | 7 | 해금·장착·효과·누적 보존 | 미판정 |
| TTL006 | 숙련된 학살자 | 미연결 | 7 | 해금·장착·효과·누적 보존 | 미판정 |
| TTL007 | 전장의 지배자 | 미연결 | 7 | 해금·장착·효과·누적 보존 | 미판정 |
| TTL008 | 보스 정복자 | 미연결 | 7 | 해금·장착·효과·누적 보존 | 미판정 |
| TTL009 | 첫 전설 | 미연결 | 7 | 해금·장착·효과·누적 보존 | 미판정 |
| TTL010 | 장비 수집가 | 미연결 | 7 | 해금·장착·효과·누적 보존 | 미판정 |
| TTL011 | 행운의 손 | 미연결 | 7 | 해금·장착·효과·누적 보존 | 미판정 |
| TTL012 | 황금의 주인 | 미연결 | 7 | 해금·장착·효과·누적 보존 | 미판정 |
| TTL013 | 의뢰 해결사 | 미연결 | 7 | 해금·장착·효과·누적 보존 | 미판정 |
| TTL014 | 길드의 신뢰 | 미연결 | 7 | 해금·장착·효과·누적 보존 | 미판정 |
| TTL015 | 전설의 해결사 | 미연결 | 7 | 해금·장착·효과·누적 보존 | 미판정 |
| TTL016 | 극한의 사냥꾼 | 미연결 | 7 | 해금·장착·효과·누적 보존 | 미판정 |
| TTL017 | 재시작한 자 | 미연결 | 7 | 해금·장착·효과·누적 보존 | 미판정 |
| TTL018 | 불굴의 영혼 | 미연결 | 7 | 해금·장착·효과·누적 보존 | 미판정 |
| TTL019 | 계승자 | 미연결 | 7 | 해금·장착·효과·누적 보존 | 미판정 |
| TTL020 | 영원한 모험가 | 미연결 | 7 | 해금·장착·효과·누적 보존 | 미판정 |

## 도전 — 30개

| 원본 ID | 이름 | 현재 상태·연결 ID | 예정 단계 | 필수 연결·검수 | 최종 판정/증빙 |
|---|---|---|---|---|---|
| CHL001 | 무약의 시련 1단계 | 미연결 | 7 | 규칙·스냅샷·복원·1회 보상 | 미판정 |
| CHL002 | 무약의 시련 2단계 | 미연결 | 7 | 규칙·스냅샷·복원·1회 보상 | 미판정 |
| CHL003 | 무약의 시련 3단계 | 미연결 | 7 | 규칙·스냅샷·복원·1회 보상 | 미판정 |
| CHL004 | 무약의 시련 4단계 | 미연결 | 7 | 규칙·스냅샷·복원·1회 보상 | 미판정 |
| CHL005 | 무약의 시련 5단계 | 미연결 | 7 | 규칙·스냅샷·복원·1회 보상 | 미판정 |
| CHL006 | 무마력의 시련 1단계 | 미연결 | 7 | 규칙·스냅샷·복원·1회 보상 | 미판정 |
| CHL007 | 무마력의 시련 2단계 | 미연결 | 7 | 규칙·스냅샷·복원·1회 보상 | 미판정 |
| CHL008 | 무마력의 시련 3단계 | 미연결 | 7 | 규칙·스냅샷·복원·1회 보상 | 미판정 |
| CHL009 | 무마력의 시련 4단계 | 미연결 | 7 | 규칙·스냅샷·복원·1회 보상 | 미판정 |
| CHL010 | 무마력의 시련 5단계 | 미연결 | 7 | 규칙·스냅샷·복원·1회 보상 | 미판정 |
| CHL011 | 무방어의 시련 1단계 | 미연결 | 7 | 규칙·스냅샷·복원·1회 보상 | 미판정 |
| CHL012 | 무방어의 시련 2단계 | 미연결 | 7 | 규칙·스냅샷·복원·1회 보상 | 미판정 |
| CHL013 | 무방어의 시련 3단계 | 미연결 | 7 | 규칙·스냅샷·복원·1회 보상 | 미판정 |
| CHL014 | 무방어의 시련 4단계 | 미연결 | 7 | 규칙·스냅샷·복원·1회 보상 | 미판정 |
| CHL015 | 무방어의 시련 5단계 | 미연결 | 7 | 규칙·스냅샷·복원·1회 보상 | 미판정 |
| CHL016 | 생존의 시련 1단계 | 미연결 | 7 | 규칙·스냅샷·복원·1회 보상 | 미판정 |
| CHL017 | 생존의 시련 2단계 | 미연결 | 7 | 규칙·스냅샷·복원·1회 보상 | 미판정 |
| CHL018 | 생존의 시련 3단계 | 미연결 | 7 | 규칙·스냅샷·복원·1회 보상 | 미판정 |
| CHL019 | 생존의 시련 4단계 | 미연결 | 7 | 규칙·스냅샷·복원·1회 보상 | 미판정 |
| CHL020 | 생존의 시련 5단계 | 미연결 | 7 | 규칙·스냅샷·복원·1회 보상 | 미판정 |
| CHL021 | 신속의 시련 1단계 | 미연결 | 7 | 규칙·스냅샷·복원·1회 보상 | 미판정 |
| CHL022 | 신속의 시련 2단계 | 미연결 | 7 | 규칙·스냅샷·복원·1회 보상 | 미판정 |
| CHL023 | 신속의 시련 3단계 | 미연결 | 7 | 규칙·스냅샷·복원·1회 보상 | 미판정 |
| CHL024 | 신속의 시련 4단계 | 미연결 | 7 | 규칙·스냅샷·복원·1회 보상 | 미판정 |
| CHL025 | 신속의 시련 5단계 | 미연결 | 7 | 규칙·스냅샷·복원·1회 보상 | 미판정 |
| CHL026 | 정예 사냥의 시련 1단계 | 미연결 | 7 | 규칙·스냅샷·복원·1회 보상 | 미판정 |
| CHL027 | 정예 사냥의 시련 2단계 | 미연결 | 7 | 규칙·스냅샷·복원·1회 보상 | 미판정 |
| CHL028 | 정예 사냥의 시련 3단계 | 미연결 | 7 | 규칙·스냅샷·복원·1회 보상 | 미판정 |
| CHL029 | 정예 사냥의 시련 4단계 | 미연결 | 7 | 규칙·스냅샷·복원·1회 보상 | 미판정 |
| CHL030 | 정예 사냥의 시련 5단계 | 미연결 | 7 | 규칙·스냅샷·복원·1회 보상 | 미판정 |

## 집계 외 기존 콘텐츠와 추가 개발 항목

- 기존 스킬 5개: 투자·효과·ID 보존 후 대응 원본과 통합 매핑. 중복 지급하지 않는다.
- 기존 이벤트 10개: 유지·회귀 검사. 원본 200개와 같은 이름이 있어도 별도 ID를 임의 삭제하지 않는다.
- 기존 업적 7개: 유지·보상 중복 방지·환생 누적/회차 조건 명시.
- 제작 조리법·분해·정제: 원본 정의 개수에 포함되지 않는 4단계 신규 설계 산출물.
- 자동 전투 정책·저장 이전·UI·패키징·문서: 콘텐츠 개수와 별개로 실행 체크리스트에서 관리.

## 검수 규칙

1. 연결 완료는 데이터 존재가 아니라 실제 획득/조우/사용과 저장·UI·테스트까지 갖춘 상태다.
2. 통합 시 원본 ID, 실행 ID, 기존 투자·보유 정보의 변환 규칙, 효과 차이와 증빙을 기록한다.
3. 제외 시 중복·규칙 충돌·게임 방향 등의 구체적 사유와 사용자 결정 기록을 남긴다. 개발 편의만으로 제외 완료 처리하지 않는다.
4. 후속 단계로 이동할 때는 이 표와 상세 기획·작업 체크리스트를 함께 갱신한다.
5. 최종 배포 전 미판정/미검토 항목이 0개인지 검사한다.

2026-10-18 03-02: 기존 260개 활성 ID를 명시적 목록으로 전환했다. 콘텐츠 연결 개수·판정은 그대로이며 지역 선택과 미지원 항목 차단을 검증했다. [검증 기록](EXPLICIT_SELECTION.md).

2026-10-18 03-03: 공통 효과 처리 경로와 EF016~040의 실행 계약을 확정했다. 활성/연결 개수는 그대로이며 신규 효과 구현 완료를 뜻하지 않는다. 다음은 EF016~025 구현이다. [효과 시점 계약](EFFECT_TIMING.md).

2026-10-18 03-04/05: 공통 효과 40개 실행/저장 연결, 총 출처 연결 313개. 신규 공급 콘텐츠의 자연 획득·조우 완성은 별도 판정이며 해당 효과의 엔진 구현과 구분한다. [구현 기록](PHASE3_EFFECTS.md).

2026-10-18 03-06~09: 카탈로그 735개와 phase2 28개, 총 763개 출처를 연결했다. 고층 조우·장비·보스·물약·환경·재료 판매 경로는 [고층 명세](HIGH_FLOORS.md)를 따른다. 신규 장비는 현재 지원 옵션만 사용하며 재료 제작·정제는 후속 단계다. 활성 개수 증가를 03-10~23의 전수 검수 완료로 간주하지 않는다.
