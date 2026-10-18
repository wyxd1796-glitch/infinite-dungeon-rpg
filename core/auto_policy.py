"""Read-only automatic action selection shared by execution and preview."""
import math


class AutoPolicyMixin:
    def next_auto_action(self):
        def choice(action, key=None, reason=''):
            return dict(action=action, key=key, reason=reason)
        if self.s['mode'] != 'combat' or self.s.get('event_result'):
            return choice('stop', reason='진행 중인 전투 없음')
        settings = self.s['settings']
        fraction = self.p['hp'] / self.derived()['hp']
        if settings['stop_danger'] and fraction <= settings['danger']:
            return choice('stop', reason='위험 HP · 자동 전투 중단')
        if any(st.get('effect_number') in (4,5) for st in self.s['statuses']):
            return choice('attack', reason='행동불가 · 이번 행동은 소모되고 자원은 사용하지 않음')
        skills = sorted((r for r in self.content['skills'] if r['kind'] == 'active'),
                        key=lambda r: (self.s['skill_auto'][r['id']]['priority'], r['id']))
        usable = [r for r in skills if settings['auto_skill'] and
                  self.s['skill_auto'][r['id']]['enabled'] and self.auto_skill_allowed(r)]
        def healing(row):
            return any(effect['type'] == 'heal_hp' for effect in row['effects'])
        def amount(row, level=1):
            value = 0
            for effect in row['effects']:
                if effect['type'] != 'heal_hp': continue
                heal = effect['value'] + effect.get('growth', 0) * (level - 1)
                value += math.floor(heal * self.derived()['hp'] if effect.get('fraction') else heal)
            return min(max(0, self.derived()['hp'] - self.p['hp']), value)
        heals = [r for r in usable if healing(r)]
        potions = [r for r in self.available_items('소비품')
                   if settings['auto_potion'] and fraction <= settings['potion_threshold']
                   and self.s['items'].get(r['id'], 0) > 0
                   and 'combat' in r.get('contexts', ['combat']) and healing(r)]
        policy = settings['recovery_policy']
        potion = self.automatic_potion() if potions else None
        if policy == 'potion_first':
            # Compatibility: keep the old skill-priority order after potions.
            if potion: return choice('potion', potion, '물약 우선 · HP 기준 도달')
        elif policy == 'skill_first':
            if heals: return choice('skill', heals[0]['id'], '회복 스킬 우선')
            if potion: return choice('potion', potion, '사용 가능한 회복 스킬 없음 · 물약')
        else:
            cleanse = [r for r in heals if any(x['type'] == 'cleanse' for x in r['effects'])]
            if self.has_treatable_status() and cleanse:
                return choice('skill', cleanse[0]['id'], '제거 가능한 상태이상 · 정화 우선')
            candidates = [(amount(r, self.s['skills'][r['id']]), 1, -i, 'skill', r['id'])
                          for i, r in enumerate(heals)]
            candidates += [(amount(r), 0, -i, 'potion', r['id'])
                           for i, r in enumerate(sorted(potions, key=lambda r: r['id']))]
            candidates = [r for r in candidates if r[0] > 0]
            if candidates:
                best = max(candidates)
                return choice(best[3], best[4], f'효율 우선 · 유효 HP 회복 {best[0]}')
        reserved = False
        for skill in usable:
            attacks = any(x['type'] in ('damage', 'tactical_damage') for x in skill['effects'])
            if attacks and self.p['mp'] - skill['mp'] < settings['mp_reserve']:
                reserved = True
                continue
            return choice('skill', skill['id'], '자동 스킬 우선순위')
        return choice('attack', reason='예약 MP 유지 · 일반 공격' if reserved else '사용 조건을 만족하는 자동 스킬 없음 · 일반 공격')

    def auto_battle(self):
        self.require(self.s['mode'] == 'combat', '현재 전투가 없습니다.')
        for _ in range(self.content.balance['auto_turn_limit']):
            if self.s['mode'] != 'combat': break
            decision = self.next_auto_action()
            if decision['action'] == 'stop':
                self.log(decision['reason']); break
            self.battle(decision['action'], decision['key'])
        else: self.log('500턴 안전 한도 · 자동 전투 중단')

    def _execute(self, action, **args):
        if action == 'setting' and args.get('key') in ('recovery_policy', 'mp_reserve'):
            key, value = args['key'], args.get('value')
            valid = value in ('potion_first', 'skill_first', 'efficient') if key == 'recovery_policy' else type(value) is int and 0 <= value <= 999
            self.require(valid, '자동 전투 설정값이 유효하지 않습니다.')
            self.s['settings'][key] = value
            return
        return super()._execute(action, **args)
