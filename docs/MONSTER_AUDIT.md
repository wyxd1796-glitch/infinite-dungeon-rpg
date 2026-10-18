# 03-10 몬스터 150종 전수 검수

2026-10-18. 원본 150종과 실행 출현·패턴·효과·보상을 전수 대조했다. 역할은 원본에 없어 별도 monster_roles.json에 명시했다. 기존 전투 스냅샷과 수치는 바꾸지 않는다.

역할 집계: 강화형 35종, 공격형 22종, 방어형 41종, 일반형 11종, 제어형 37종, 지속피해형 4종.

방어 행동이 있는 경우 방어형을 주 역할로 표시한다. 나머지는 실제 지속 피해/제어/자기 강화 효과, 특수공격 유무에 따라 분류했다. 표의 효과 열로 복합 역할을 확인할 수 있다. 이름·설명 문자열을 실행해 역할 효과를 추정하지 않는다.

## 구현과 수정

- 종족·출현층·양수 가중치·효과/재료의 종류·0~100% 확률·선언된 패턴 길이를 로딩 시 검증한다. 전투 화면에 종족·역할·기본 재료 확률을 줄바꿈 표시한다.
- MON001~040은 special_proc_pct가 원본에 없다. 401층 이후 재등장 시 이를 0%로 처리하던 오류를 수정하여 효과 자체의 기본 확률을 사용한다. 수치가 있는 MON041~150은 해당 확률을 사용한다. 보스와 진행 중 기존 전투의 기본 확률 경로는 유지한다.
- 적에게 걸린 EF031/040 골드 강화는 처치 골드에 반영한다. 플레이어의 같은 계열 효과와 최댓값 하나만 적용하고 기존 골드 보너스 상한을 유지한다. 처치 확정 경로에서 한 번만 지급한다.
- EF035 MP 흡수는 현재 150종의 effect_id에 없다. 이번 몬스터 검수에서 새 MP 소비 규칙을 만들지 않는다. 원소와 마력 체계의 추가 설계는 별도 과제다.
- 개별 재료 드롭과 추가 재료 추첨, 골드/경험치, 장비 보상은 공통 처치 경로를 따른다. 모든 재료의 현행 사용처는 판매 또는 기존 강화 대체이고 제작은 후속이다.
- 원본 element/reward_tier는 출처 메타데이터다. 현재 원소 상성이나 등급별 보상 계수로 실행하지 않는다. 원소 시스템을 이번 완료 범위로 주장하지 않는다.
- 도감은 6단계다. 이번 화면은 현재 전투의 적 정보이며 미보유 소지품/미학습 스킬을 사용 목록에 노출하지 않는다.

## 전수 연결표

층 범위는 400층 원형 순환 안의 실제 유효 범위다. 효과 확률은 상태 저항 차감 전이며 디버프는 유효 피해 이후, 버프는 자신에게 적용한다. 특수 행동이 있는 패턴에서는 해당 순서에만 발동한다. 재료 확률은 1~100층 20%, 고층은 명시값 또는 20%다.

| ID | 이름 | 종족 | 역할 | 원형 층 | 가중치 | 실행 패턴 | 효과/확률 | 재료/고층 확률 |
|---|---|---|---|---|---:|---|---|---|
| MON001 | 슬라임 | 야수·점액 | 일반형 | 1~30 | 50 | attack | 없음 | MAT011 20% |
| MON002 | 늑대 | 야수·점액 | 공격형 | 1~30 | 42 | attack → attack → special | 없음 | MAT012 20% |
| MON003 | 박쥐 | 야수·점액 | 방어형 | 1~30 | 34 | attack → defend | 없음 | MAT013 20% |
| MON004 | 거대쥐 | 야수·점액 | 일반형 | 1~30 | 26 | attack | 없음 | MAT014 20% |
| MON005 | 그림자 표범 | 야수·점액 | 공격형 | 1~30 | 18 | attack → attack → special | 없음 | MAT015 20% |
| MON006 | 고블린 | 고블린·오크 | 일반형 | 11~40 | 50 | attack | 없음 | MAT012 20% |
| MON007 | 고블린 궁수 | 고블린·오크 | 공격형 | 11~40 | 42 | attack → attack → special | 없음 | MAT013 20% |
| MON008 | 오크 | 고블린·오크 | 방어형 | 11~40 | 34 | attack → defend | 없음 | MAT014 20% |
| MON009 | 오크 전사 | 고블린·오크 | 일반형 | 11~40 | 26 | attack | 없음 | MAT015 20% |
| MON010 | 트롤 | 고블린·오크 | 공격형 | 11~40 | 18 | attack → attack → special | 없음 | MAT016 20% |
| MON011 | 해골 병사 | 언데드 | 일반형 | 21~50 | 50 | attack | 없음 | MAT013 20% |
| MON012 | 좀비 | 언데드 | 제어형 | 21~50 | 42 | attack → attack → special | EF007 15% | MAT014 20% |
| MON013 | 망령 | 언데드 | 방어형 | 21~50 | 34 | attack → defend | 없음 | MAT015 20% |
| MON014 | 구울 | 언데드 | 제어형 | 21~50 | 26 | attack | EF007 15% | MAT016 20% |
| MON015 | 리치의 하수인 | 언데드 | 공격형 | 21~50 | 18 | attack → attack → special | 없음 | MAT017 20% |
| MON016 | 거대 거미 | 곤충·식물 | 일반형 | 31~60 | 50 | attack | 없음 | MAT014 20% |
| MON017 | 독전갈 | 곤충·식물 | 지속피해형 | 31~60 | 42 | attack → attack → special | EF001 15% | MAT015 20% |
| MON018 | 식인꽃 | 곤충·식물 | 방어형 | 31~60 | 34 | attack → defend | 없음 | MAT016 20% |
| MON019 | 가시 덩굴 | 곤충·식물 | 지속피해형 | 31~60 | 26 | attack | EF001 15% | MAT017 20% |
| MON020 | 맹독 벌레 | 곤충·식물 | 공격형 | 31~60 | 18 | attack → attack → special | 없음 | MAT018 20% |
| MON021 | 화염 정령 | 정령 | 일반형 | 41~70 | 50 | attack | 없음 | MAT015 20% |
| MON022 | 물 정령 | 정령 | 지속피해형 | 41~70 | 42 | attack → attack → special | EF002 15% | MAT016 20% |
| MON023 | 얼음 정령 | 정령 | 방어형 | 41~70 | 34 | attack → defend | 없음 | MAT017 20% |
| MON024 | 바람 정령 | 정령 | 지속피해형 | 41~70 | 26 | attack | EF002 15% | MAT018 20% |
| MON025 | 대지 정령 | 정령 | 공격형 | 41~70 | 18 | attack → attack → special | 없음 | MAT019 20% |
| MON026 | 돌 골렘 | 골렘·인형 | 일반형 | 61~90 | 50 | attack | 없음 | MAT016 20% |
| MON027 | 철 골렘 | 골렘·인형 | 공격형 | 61~90 | 42 | attack → attack → special | 없음 | MAT017 20% |
| MON028 | 마력 인형 | 골렘·인형 | 방어형 | 61~90 | 34 | attack → defend | 없음 | MAT018 20% |
| MON029 | 고대 파수병 | 골렘·인형 | 일반형 | 61~90 | 26 | attack | 없음 | MAT019 20% |
| MON030 | 수정 골렘 | 골렘·인형 | 공격형 | 61~90 | 18 | attack → attack → special | 없음 | MAT020 20% |
| MON031 | 임프 | 악마 | 일반형 | 51~80 | 50 | attack | 없음 | MAT017 20% |
| MON032 | 하급 악마 | 악마 | 강화형 | 51~80 | 42 | attack → attack → special | EF013 100% | MAT018 20% |
| MON033 | 마족 전사 | 악마 | 방어형 | 51~80 | 34 | attack → defend | 없음 | MAT019 20% |
| MON034 | 서큐버스 | 악마 | 강화형 | 51~80 | 26 | attack | EF013 100% | MAT020 20% |
| MON035 | 지옥 사냥개 | 악마 | 공격형 | 51~80 | 18 | attack → attack → special | 없음 | MAT011 20% |
| MON036 | 심연 촉수 | 심연 생물 | 일반형 | 81~110 | 50 | attack | 없음 | MAT018 20% |
| MON037 | 공허 추적자 | 심연 생물 | 제어형 | 81~110 | 42 | attack → attack → special | EF009 15% | MAT019 20% |
| MON038 | 타락한 기사 | 심연 생물 | 방어형 | 81~110 | 34 | attack → defend | 없음 | MAT020 20% |
| MON039 | 혼돈의 눈 | 심연 생물 | 제어형 | 81~110 | 26 | attack | EF009 15% | MAT011 20% |
| MON040 | 심연 포식자 | 심연 생물 | 공격형 | 81~110 | 18 | attack → attack → special | 없음 | MAT012 20% |
| MON041 | 늑대인간 정찰병 | 수인 부족 | 공격형 | 101~230 | 42 | attack → attack → special | 없음 | MAT021 18% |
| MON042 | 곰전사 | 수인 부족 | 방어형 | 101~230 | 39 | attack → defend → special | EF016 16% | MAT022 22% |
| MON043 | 호랑이 주술사 | 수인 부족 | 제어형 | 101~230 | 36 | attack → special → attack | EF020 20% | MAT023 26% |
| MON044 | 여우 암살자 | 수인 부족 | 제어형 | 101~230 | 33 | attack → attack → special | EF021 24% | MAT024 30% |
| MON045 | 멧돼지 투사 | 수인 부족 | 방어형 | 101~230 | 30 | attack → defend → special | EF023 12% | MAT025 18% |
| MON046 | 표범 추격자 | 수인 부족 | 제어형 | 108~237 | 27 | attack → special → attack | EF026 16% | MAT026 22% |
| MON047 | 매눈 궁수 | 수인 부족 | 강화형 | 108~237 | 24 | attack → attack → special | EF029 20% | MAT027 26% |
| MON048 | 사자 수호병 | 수인 부족 | 방어형 | 108~237 | 21 | attack → defend → special | EF031 24% | MAT028 30% |
| MON049 | 하이에나 약탈자 | 수인 부족 | 강화형 | 108~237 | 18 | attack → special → attack | EF033 12% | MAT029 18% |
| MON050 | 수인 대전사 | 수인 부족 | 강화형 | 108~237 | 15 | attack → attack → special | EF040 16% | MAT030 22% |
| MON051 | 검은 신도 | 이단 교단 | 공격형 | 118~247 | 42 | attack → attack → special | 없음 | MAT031 22% |
| MON052 | 가면 제사장 | 이단 교단 | 방어형 | 118~247 | 39 | attack → defend → special | EF016 20% | MAT032 26% |
| MON053 | 이단 사냥꾼 | 이단 교단 | 제어형 | 118~247 | 36 | attack → special → attack | EF020 24% | MAT033 30% |
| MON054 | 금기술사 | 이단 교단 | 제어형 | 118~247 | 33 | attack → attack → special | EF021 12% | MAT034 18% |
| MON055 | 광신도 전사 | 이단 교단 | 방어형 | 118~247 | 30 | attack → defend → special | EF023 16% | MAT035 22% |
| MON056 | 기도하는 광인 | 이단 교단 | 제어형 | 125~254 | 27 | attack → special → attack | EF026 20% | MAT036 26% |
| MON057 | 피의 집행자 | 이단 교단 | 강화형 | 125~254 | 24 | attack → attack → special | EF029 24% | MAT037 30% |
| MON058 | 봉인 해제자 | 이단 교단 | 방어형 | 125~254 | 21 | attack → defend → special | EF031 12% | MAT038 18% |
| MON059 | 부패한 사제 | 이단 교단 | 강화형 | 125~254 | 18 | attack → special → attack | EF033 16% | MAT039 22% |
| MON060 | 심판의 전도자 | 이단 교단 | 강화형 | 125~254 | 15 | attack → attack → special | EF040 20% | MAT040 26% |
| MON061 | 새끼 와이번 | 용족 | 공격형 | 135~264 | 42 | attack → attack → special | 없음 | MAT041 26% |
| MON062 | 비늘 파수꾼 | 용족 | 방어형 | 135~264 | 39 | attack → defend → special | EF016 24% | MAT042 30% |
| MON063 | 화염 드레이크 | 용족 | 제어형 | 135~264 | 36 | attack → special → attack | EF020 12% | MAT043 18% |
| MON064 | 서리 드레이크 | 용족 | 제어형 | 135~264 | 33 | attack → attack → special | EF021 16% | MAT044 22% |
| MON065 | 폭풍 비룡 | 용족 | 방어형 | 135~264 | 30 | attack → defend → special | EF023 20% | MAT045 26% |
| MON066 | 흑비늘 사냥꾼 | 용족 | 제어형 | 142~271 | 27 | attack → special → attack | EF026 24% | MAT046 30% |
| MON067 | 용혈 광전사 | 용족 | 강화형 | 142~271 | 24 | attack → attack → special | EF029 12% | MAT047 18% |
| MON068 | 고대 도마뱀 | 용족 | 방어형 | 142~271 | 21 | attack → defend → special | EF031 16% | MAT048 22% |
| MON069 | 수정 와이번 | 용족 | 강화형 | 142~271 | 18 | attack → special → attack | EF033 20% | MAT049 26% |
| MON070 | 황혼 용기사 | 용족 | 강화형 | 142~271 | 15 | attack → attack → special | EF040 24% | MAT050 30% |
| MON071 | 고철 파수기 | 기계 군단 | 공격형 | 152~281 | 42 | attack → attack → special | 없음 | MAT051 30% |
| MON072 | 증기 보병 | 기계 군단 | 방어형 | 152~281 | 39 | attack → defend → special | EF016 12% | MAT052 18% |
| MON073 | 톱날 인형 | 기계 군단 | 제어형 | 152~281 | 36 | attack → special → attack | EF020 16% | MAT053 22% |
| MON074 | 강철 수색기 | 기계 군단 | 제어형 | 152~281 | 33 | attack → attack → special | EF021 20% | MAT054 26% |
| MON075 | 전격 포탑 | 기계 군단 | 방어형 | 152~281 | 30 | attack → defend → special | EF023 24% | MAT055 30% |
| MON076 | 자동 수리기 | 기계 군단 | 제어형 | 159~288 | 27 | attack → special → attack | EF026 12% | MAT056 18% |
| MON077 | 마도 장갑병 | 기계 군단 | 강화형 | 159~288 | 24 | attack → attack → special | EF029 16% | MAT057 22% |
| MON078 | 분쇄 기갑 | 기계 군단 | 방어형 | 159~288 | 21 | attack → defend → special | EF031 20% | MAT058 26% |
| MON079 | 시계태엽 처형자 | 기계 군단 | 강화형 | 159~288 | 18 | attack → special → attack | EF033 24% | MAT059 30% |
| MON080 | 제어핵 수호병 | 기계 군단 | 강화형 | 159~288 | 15 | attack → attack → special | EF040 12% | MAT060 18% |
| MON081 | 깊은 물 해파리 | 심해 생물 | 공격형 | 169~298 | 42 | attack → attack → special | 없음 | MAT021 18% |
| MON082 | 산호 전사 | 심해 생물 | 방어형 | 169~298 | 39 | attack → defend → special | EF016 16% | MAT022 22% |
| MON083 | 아귀 사냥꾼 | 심해 생물 | 제어형 | 169~298 | 36 | attack → special → attack | EF020 20% | MAT023 26% |
| MON084 | 거대 갯지렁이 | 심해 생물 | 제어형 | 169~298 | 33 | attack → attack → special | EF021 24% | MAT024 30% |
| MON085 | 심해 문어 | 심해 생물 | 방어형 | 169~298 | 30 | attack → defend → special | EF023 12% | MAT025 18% |
| MON086 | 해골 어인 | 심해 생물 | 제어형 | 176~305 | 27 | attack → special → attack | EF026 16% | MAT026 22% |
| MON087 | 심연 해마 | 심해 생물 | 강화형 | 176~305 | 24 | attack → attack → special | EF029 20% | MAT027 26% |
| MON088 | 조개 포식자 | 심해 생물 | 방어형 | 176~305 | 21 | attack → defend → special | EF031 24% | MAT028 30% |
| MON089 | 파도 정령수 | 심해 생물 | 강화형 | 176~305 | 18 | attack → special → attack | EF033 12% | MAT029 18% |
| MON090 | 바다 무덤지기 | 심해 생물 | 강화형 | 176~305 | 15 | attack → attack → special | EF040 16% | MAT030 22% |
| MON091 | 포자 벌레 | 균사 군락 | 공격형 | 186~315 | 42 | attack → attack → special | 없음 | MAT031 22% |
| MON092 | 버섯 투사 | 균사 군락 | 방어형 | 186~315 | 39 | attack → defend → special | EF016 20% | MAT032 26% |
| MON093 | 균사 추적자 | 균사 군락 | 제어형 | 186~315 | 36 | attack → special → attack | EF020 24% | MAT033 30% |
| MON094 | 부패 이끼수 | 균사 군락 | 제어형 | 186~315 | 33 | attack → attack → special | EF021 12% | MAT034 18% |
| MON095 | 포자 투척자 | 균사 군락 | 방어형 | 186~315 | 30 | attack → defend → special | EF023 16% | MAT035 22% |
| MON096 | 감염된 곰 | 균사 군락 | 제어형 | 193~322 | 27 | attack → special → attack | EF026 20% | MAT036 26% |
| MON097 | 독버섯 기사 | 균사 군락 | 강화형 | 193~322 | 24 | attack → attack → special | EF029 24% | MAT037 30% |
| MON098 | 균핵 수호자 | 균사 군락 | 방어형 | 193~322 | 21 | attack → defend → special | EF031 12% | MAT038 18% |
| MON099 | 잠복 포식균 | 균사 군락 | 강화형 | 193~322 | 18 | attack → special → attack | EF033 16% | MAT039 22% |
| MON100 | 군락 지배체 | 균사 군락 | 강화형 | 193~322 | 15 | attack → attack → special | EF040 20% | MAT040 26% |
| MON101 | 모래 도적 | 사막 망령 | 공격형 | 203~332 | 42 | attack → attack → special | 없음 | MAT041 26% |
| MON102 | 사막 맹독뱀 | 사막 망령 | 방어형 | 203~332 | 39 | attack → defend → special | EF016 24% | MAT042 30% |
| MON103 | 먼지 정령 | 사막 망령 | 제어형 | 203~332 | 36 | attack → special → attack | EF020 12% | MAT043 18% |
| MON104 | 유리 전갈 | 사막 망령 | 제어형 | 203~332 | 33 | attack → attack → special | EF021 16% | MAT044 22% |
| MON105 | 사구 방랑자 | 사막 망령 | 방어형 | 203~332 | 30 | attack → defend → special | EF023 20% | MAT045 26% |
| MON106 | 모래 미이라 | 사막 망령 | 제어형 | 210~339 | 27 | attack → special → attack | EF026 24% | MAT046 30% |
| MON107 | 바람 모래벌레 | 사막 망령 | 강화형 | 210~339 | 24 | attack → attack → special | EF029 12% | MAT047 18% |
| MON108 | 태양 이교도 | 사막 망령 | 방어형 | 210~339 | 21 | attack → defend → special | EF031 16% | MAT048 22% |
| MON109 | 메마른 기사 | 사막 망령 | 강화형 | 210~339 | 18 | attack → special → attack | EF033 20% | MAT049 26% |
| MON110 | 사막의 매복자 | 사막 망령 | 강화형 | 210~339 | 15 | attack → attack → special | EF040 24% | MAT050 30% |
| MON111 | 광석 구더기 | 깊은 광맥 | 공격형 | 220~349 | 42 | attack → attack → special | 없음 | MAT051 30% |
| MON112 | 수정 박쥐 | 깊은 광맥 | 방어형 | 220~349 | 39 | attack → defend → special | EF016 12% | MAT052 18% |
| MON113 | 철광 파먹이 | 깊은 광맥 | 제어형 | 220~349 | 36 | attack → special → attack | EF020 16% | MAT053 22% |
| MON114 | 보석 지네 | 깊은 광맥 | 제어형 | 220~349 | 33 | attack → attack → special | EF021 20% | MAT054 26% |
| MON115 | 마력 광부 | 깊은 광맥 | 방어형 | 220~349 | 30 | attack → defend → special | EF023 24% | MAT055 30% |
| MON116 | 암석 소환사 | 깊은 광맥 | 제어형 | 227~356 | 27 | attack → special → attack | EF026 12% | MAT056 18% |
| MON117 | 광맥 수호자 | 깊은 광맥 | 강화형 | 227~356 | 24 | attack → attack → special | EF029 16% | MAT057 22% |
| MON118 | 동굴 석화수 | 깊은 광맥 | 방어형 | 227~356 | 21 | attack → defend → special | EF031 20% | MAT058 26% |
| MON119 | 빛나는 수정인형 | 깊은 광맥 | 강화형 | 227~356 | 18 | attack → special → attack | EF033 24% | MAT059 30% |
| MON120 | 심층 파쇄자 | 깊은 광맥 | 강화형 | 227~356 | 15 | attack → attack → special | EF040 12% | MAT060 18% |
| MON121 | 별빛 망령 | 성좌 잔재 | 공격형 | 237~366 | 42 | attack → attack → special | 없음 | MAT021 18% |
| MON122 | 천문 파수병 | 성좌 잔재 | 방어형 | 237~366 | 39 | attack → defend → special | EF016 16% | MAT022 22% |
| MON123 | 유성 추적자 | 성좌 잔재 | 제어형 | 237~366 | 36 | attack → special → attack | EF020 20% | MAT023 26% |
| MON124 | 시간 사냥꾼 | 성좌 잔재 | 제어형 | 237~366 | 33 | attack → attack → special | EF021 24% | MAT024 30% |
| MON125 | 월식 기사 | 성좌 잔재 | 방어형 | 237~366 | 30 | attack → defend → special | EF023 12% | MAT025 18% |
| MON126 | 태양 잔영 | 성좌 잔재 | 제어형 | 244~373 | 27 | attack → special → attack | EF026 16% | MAT026 22% |
| MON127 | 별무리 정령 | 성좌 잔재 | 강화형 | 244~373 | 24 | attack → attack → special | EF029 20% | MAT027 26% |
| MON128 | 은하 맹수 | 성좌 잔재 | 방어형 | 244~373 | 21 | attack → defend → special | EF031 24% | MAT028 30% |
| MON129 | 궤도 감시자 | 성좌 잔재 | 강화형 | 244~373 | 18 | attack → special → attack | EF033 12% | MAT029 18% |
| MON130 | 공전 인형 | 성좌 잔재 | 강화형 | 244~373 | 15 | attack → attack → special | EF040 16% | MAT030 22% |
| MON131 | 일그러진 살점 | 혼돈 변이체 | 공격형 | 254~383 | 42 | attack → attack → special | 없음 | MAT031 22% |
| MON132 | 기억 포식자 | 혼돈 변이체 | 방어형 | 254~383 | 39 | attack → defend → special | EF016 20% | MAT032 26% |
| MON133 | 뒤틀린 뼈수 | 혼돈 변이체 | 제어형 | 254~383 | 36 | attack → special → attack | EF020 24% | MAT033 30% |
| MON134 | 혼돈 모사체 | 혼돈 변이체 | 제어형 | 254~383 | 33 | attack → attack → special | EF021 12% | MAT034 18% |
| MON135 | 허공 절단자 | 혼돈 변이체 | 방어형 | 254~383 | 30 | attack → defend → special | EF023 16% | MAT035 22% |
| MON136 | 불규칙 감시자 | 혼돈 변이체 | 제어형 | 261~390 | 27 | attack → special → attack | EF026 20% | MAT036 26% |
| MON137 | 타락한 원소수 | 혼돈 변이체 | 강화형 | 261~390 | 24 | attack → attack → special | EF029 24% | MAT037 30% |
| MON138 | 악몽 찌꺼기 | 혼돈 변이체 | 방어형 | 261~390 | 21 | attack → defend → special | EF031 12% | MAT038 18% |
| MON139 | 역행 포식자 | 혼돈 변이체 | 강화형 | 261~390 | 18 | attack → special → attack | EF033 16% | MAT039 22% |
| MON140 | 무형 변이체 | 혼돈 변이체 | 강화형 | 261~390 | 15 | attack → attack → special | EF040 20% | MAT040 26% |
| MON141 | 울부짖는 시종 | 영혼 궁정 | 공격형 | 271~400 | 42 | attack → attack → special | 없음 | MAT041 26% |
| MON142 | 고독한 감시자 | 영혼 궁정 | 방어형 | 271~400 | 39 | attack → defend → special | EF016 24% | MAT042 30% |
| MON143 | 혼령 재판관 | 영혼 궁정 | 제어형 | 271~400 | 36 | attack → special → attack | EF020 12% | MAT043 18% |
| MON144 | 유령 기병 | 영혼 궁정 | 제어형 | 271~400 | 33 | attack → attack → special | EF021 16% | MAT044 22% |
| MON145 | 전장 원혼 | 영혼 궁정 | 방어형 | 271~400 | 30 | attack → defend → special | EF023 20% | MAT045 26% |
| MON146 | 망각의 악사 | 영혼 궁정 | 제어형 | 278~400 | 27 | attack → special → attack | EF026 24% | MAT046 30% |
| MON147 | 빛바랜 귀부인 | 영혼 궁정 | 강화형 | 278~400 | 24 | attack → attack → special | EF029 12% | MAT047 18% |
| MON148 | 허무의 무희 | 영혼 궁정 | 방어형 | 278~400 | 21 | attack → defend → special | EF031 16% | MAT048 22% |
| MON149 | 영혼 구속자 | 영혼 궁정 | 강화형 | 278~400 | 18 | attack → special → attack | EF033 20% | MAT049 26% |
| MON150 | 망령 황실근위 | 영혼 궁정 | 강화형 | 278~400 | 15 | attack → attack → special | EF040 24% | MAT050 30% |

검증: test_monster_audit.py가 150종 각각의 출현·패턴 한 주기·효과 호출·골드/재료 지급·진행도·저장 유효성을 검사한다. 별도 순환 재등장 확률 회귀, 잘못된 데이터 거절, 기존 적 스냅샷 보존 검사를 포함한다. 기존 03-06~09 대량 측정은 당시 결과로 보존하며 이번 수정으로 그 원자료를 새로 측정한 것으로 표시하지 않는다.

최종 전체 검사: `QT_QPA_PLATFORM=offscreen`에서 `python -m unittest discover -s tests -p test_*.py`, 199개 통과(53.749초). 신규 엔진 검사 5개와 좁은 창 UI 검사 1개를 기존 193개에 추가했다. 1~100층 추첨 상태·난수 해시와 기존 48행동 전투 해시도 유지했다. 268×861/250×400의 역할·재료 안내 줄바꿈, 조회의 상태/난수 불변성을 확인했다.

재생성: `python -m tests.report_monsters`. 다음 작업은 03-11 접두어 50종이다. 보스 개별 대응/경제/자연 고층 진행은 기존 후속 단계에서 검증한다.
