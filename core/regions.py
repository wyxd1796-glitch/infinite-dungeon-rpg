"""Validated cyclic region routing; selection never consumes random numbers."""
import math


class Regions:
    def __init__(self, definition, chosen):
        self.cycle = definition['cycle_floors']
        self.interval = definition['boss_interval']
        self.family_weight = definition['primary_family_weight']
        self.environment_ids=definition.get('environment_ids')
        self.environment_cycle=definition.get('environment_cycle',self.cycle)
        if type(self.cycle) is not int or not 1 <= self.cycle <= 10000:
            raise ValueError('잘못된 지역 반복 층수')
        if type(self.interval) is not int or self.interval < 1 or self.cycle % self.interval:
            raise ValueError('잘못된 보스 간격')
        if type(self.family_weight) not in (int, float) or not math.isfinite(self.family_weight) or self.family_weight <= 0:
            raise ValueError('잘못된 지역 계열 가중치')
        groups = {k: {r['id']: r for r in rows} for k, rows in chosen.items()}
        if self.environment_ids is not None:
            if type(self.environment_cycle) is not int or self.environment_cycle!=len(self.environment_ids)*self.interval or len(set(self.environment_ids))!=len(self.environment_ids) or any(k not in groups['environments'] for k in self.environment_ids):
                raise ValueError('잘못된 환경 순환 연결')
        self.by_floor = {}
        ids = set()
        for region in definition['regions']:
            key = region['id']
            if not isinstance(key, str) or not key or key in ids:
                raise ValueError('지역 ID 누락 또는 중복')
            ids.add(key)
            lo, hi = region['min_floor'], region['max_floor']
            if type(lo) is not int or type(hi) is not int or not 1 <= lo <= hi <= self.cycle:
                raise ValueError('잘못된 지역 층 범위')
            for field, group in (('environment_id', 'environments'), ('boss_id', 'bosses')):
                if region[field] not in groups[group]:
                    raise ValueError('지역의 비활성 참조: ' + field)
            pool = region['monster_ids']
            if not isinstance(pool, list) or not all(isinstance(k, str) for k in pool) or len(pool) != len(set(pool)):
                raise ValueError('잘못된 지역 몬스터 목록')
            if any(k not in groups['monsters'] for k in pool):
                raise ValueError('지역의 비활성 몬스터 참조')
            for floor in range(lo, hi + 1):
                if floor in self.by_floor:
                    raise ValueError('지역 층 범위 중복')
                if not any(groups['monsters'][k]['min_floor'] <= floor <= groups['monsters'][k]['max_floor'] and groups['monsters'][k]['weight'] > 0 for k in pool):
                    raise ValueError(f'{floor}층 출현 풀 없음')
                self.by_floor[floor] = region
        if set(self.by_floor) != set(range(1, self.cycle + 1)):
            raise ValueError('지역 층 범위 누락')

    def zone(self, floor):
        return (floor - 1) % self.cycle + 1

    def at(self, floor):
        region=self.by_floor[self.zone(floor)]
        if self.environment_ids is None: return region
        return dict(region,environment_id=self.environment_ids[((floor-1)%self.environment_cycle)//self.interval])

    def boss_id(self, floor):
        # Retain the previous public API behavior even on a non-boss floor.
        if floor<=100: return self.by_floor[(floor//self.interval*self.interval-1)%100+1]['boss_id']
        return self.at(floor // self.interval * self.interval)['boss_id']

    def monsters(self, content, floor):
        zone = self.zone(floor)
        rows = [content.by_id['catalogue.v3.' + key] for key in self.at(floor)['monster_ids']]
        return [r for r in rows if r['min_floor'] <= zone <= r['max_floor']]
