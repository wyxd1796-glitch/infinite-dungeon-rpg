import copy
import json
import math
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from core.game_engine import GameEngine, RuleError
from core.phase3_effects import EFFECTS, validate_definition
from core.save_manager import SaveManager

ROOT = Path(__file__).resolve().parents[1]


class Phase3EffectTests(unittest.TestCase):
    def combat(self):
        e = GameEngine(ROOT / 'content', seed=713)
        e.execute('enter'); e.start_combat()
        e.s['enemy'].update(hp=10000, max_hp=10000, atk=100, defense=0,
                           accuracy=2, evasion=0, pattern=['defend'],
                           effect_id=None, on_hit_effects=[])
        return e

    def apply(self, e, n, target='player'):
        self.assertTrue(e.apply_status(n, target, 'enemy' if target == 'player' else 'player', 1))

    def hit(self, e, source='player', action='attack', random=.5, accuracy=.95):
        with patch.object(e.rng, 'random', return_value=random), patch.object(e.rng, 'uniform', return_value=1):
            return e.direct_hit(source, action=action, accuracy=accuracy)

    def test_definitions_and_source_contract(self):
        e = self.combat()
        for n in range(16,26):
            row = copy.deepcopy(e.content.by_id[f'catalogue.v3.EF{n:03}'])
            self.assertEqual(row['source_id'], f'EF{n:03}')
            self.assertEqual(row['polarity'], 'debuff')
            row['id'] = row['source_id']; validate_definition(row)
            for field, value in (('operator', 'eval'), ('trigger', 'unknown'), ('magnitude', -1), ('duration_turns', 0), ('stack_limit', 99), ('base_chance_pct', float('nan'))):
                broken = dict(row); broken[field] = value
                with self.assertRaises(ValueError): validate_definition(broken)

    def test_all_effects_on_both_actors_and_expiry(self):
        for n in range(16,26):
            for side in ('player', 'enemy'):
                with self.subTest(n=n, side=side):
                    e = self.combat(); self.apply(e, n, side)
                    self.assertIn(e.content.by_id[f'catalogue.v3.EF{n:03}']['name'], e.status_label(side))
                    for _ in range(EFFECTS[n][3]):
                        e.s['turn'] += 1; e.tick_end(side)
                    self.assertFalse(e.actor_statuses(side))

    def test_dot_values_shield_bypass_and_snapshots(self):
        for n, amount in ((16, 6), (17, 1), (18, 2), (19, 4)):
            with self.subTest(n=n):
                e = self.combat(); e.p['shield'] = 1000; self.apply(e, n)
                e.s['enemy']['atk'] = 200; e.s['turn'] += 1; e.tick_end('player')
                self.assertEqual(e.p['hp'], 100 - amount); self.assertEqual(e.p['shield'], 1000)
        e = self.combat(); self.apply(e, 16); e.s['enemy']['atk'] = 200
        self.apply(e, 16); e.s['turn'] += 1; e.tick_end('player')
        self.assertEqual(e.p['hp'], 88)

    def test_stack_refresh_does_not_skip_recipient_turn(self):
        e = self.combat(); self.apply(e, 17, 'enemy'); self.apply(e, 17, 'enemy'); self.apply(e, 17, 'enemy')
        st = e.s['enemy']['statuses'][0]; self.assertEqual(st['stacks'], 2)
        e.tick_end('enemy'); self.assertEqual((e.s['enemy']['hp'], st['turns']), (9700, 3))
        self.apply(e, 17, 'enemy'); e.tick_end('enemy')
        self.assertEqual((e.s['enemy']['hp'], st['turns']), (9400, 3))
        e = self.combat(); self.apply(e, 19); e.tick_end('player')
        self.assertEqual(e.p['hp'], 100)
        e.s['turn'] += 1; e.tick_end('player'); self.assertEqual(e.p['hp'], 96)

    def test_accuracy_reduction_and_floor(self):
        e = self.combat(); self.apply(e, 20)
        self.assertEqual(self.hit(e, random=.85), 0)
        self.assertGreater(self.hit(e, random=.79), 0)
        e.s['enemy']['evasion'] = 2
        self.assertGreater(self.hit(e, random=.04, accuracy=.1), 0)
        self.assertEqual(self.hit(e, random=.05, accuracy=.1), 0)

    def test_basic_damage_only_and_vulnerability(self):
        e = self.combat(); normal = self.hit(e); self.apply(e, 21)
        self.assertEqual(self.hit(e), math.floor(e.derived()['atk'] * .7 - .6 * e.enemy_stats()['defense']))
        self.assertEqual(self.hit(e, action='skill'), normal)
        self.apply(e, 24, 'enemy')
        self.assertEqual(self.hit(e, action='skill'), math.floor(normal * 1.15))
        self.assertEqual(e.damage_hp('enemy', 10, 'periodic'), 10)
        self.assertEqual(e.damage_hp('enemy', 10, 'reflected'), 10)

    def test_evasion_combined_before_cap(self):
        e = self.combat(); e.s['enemy']['evasion'] = .8
        self.apply(e, 23, 'enemy'); self.apply(e, 25, 'enemy')
        self.assertEqual(e.enemy_stats()['evasion'], .45)
        e.s['enemy']['evasion'] = .3
        self.assertAlmostEqual(e.enemy_stats()['evasion'], .1)
        e.s['enemy']['evasion'] = .1; self.assertEqual(e.enemy_stats()['evasion'], 0)

    def test_confusion_actual_skill_and_potion_consumption(self):
        for action, key in (('skill', 'phase2.skill.SKL003'), ('use', 'catalogue.v3.CON001')):
            e = self.combat(); e.p['level'] = 30; e.s['skills']['phase2.skill.SKL003'] = 1
            self.apply(e, 22); before = copy.deepcopy(e.s)
            with patch.object(e.rng, 'random', return_value=.1): e.execute(action, key=key)
            self.assertEqual(e.p['mp'], before['player']['mp']); self.assertEqual(e.s['items'], before['items'])
            self.assertEqual(e.s['skill_usage'], {}); self.assertEqual(e.s['skill_cooldowns'], {})
            self.assertEqual(e.s['turn'], before['turn'] + 1)
        e = self.combat(); self.apply(e, 22, 'enemy')
        with patch.object(e.rng, 'random', return_value=.1): e.execute('defend')
        self.assertEqual(e.s['enemy']['pattern_index'], 0)

    def test_confusion_success_stun_precedence_and_no_preview_rng(self):
        e = self.combat(); self.apply(e, 22)
        rng = e.rng.getstate(); e.next_auto_action(); e.status_label(); e.action_blocked('player')
        self.assertEqual(e.rng.getstate(), rng)
        e.apply_status(4, 'player', 'enemy', 1)
        with patch.object(e.rng, 'random', side_effect=AssertionError('stun must not roll confusion')):
            e.execute('defend')
        e = self.combat(); self.apply(e, 22)
        with patch.object(e.rng, 'random', return_value=.25): e.execute('defend')
        self.assertTrue(e.p['guard'])

    def test_resistance_and_cc_immunity_independent(self):
        e = self.combat(); e.p['cc_until'] = 999
        stats = dict(e.derived(), status_resist=.75)
        with patch.object(e, 'stats_for', return_value=stats), patch.object(e.rng, 'random', return_value=.5):
            self.assertFalse(e.apply_status(16, 'player', chance=1))
        self.apply(e, 16)

    def test_cures_preserve_old_positive_effects_and_emergency_scope(self):
        e = self.combat()
        for n in range(16,26): self.apply(e, n)
        e.apply_status(10, 'player', 'player', 1)
        e.s['items']['catalogue.v3.CON013'] = 1; e.consume('catalogue.v3.CON013')
        self.assertNotIn(19, [st['effect_number'] for st in e.s['statuses']])
        self.assertFalse(e.has_treatable_status())
        e.s['items']['catalogue.v3.CON016'] = 1; e.consume('catalogue.v3.CON016')
        self.assertEqual([st['effect_number'] for st in e.s['statuses']], [10])

    def test_end_cleanup_and_victory_once(self):
        for end in ('victory', 'death', 'flee'):
            with self.subTest(end=end):
                e = self.combat(); self.apply(e, 20)
                if end == 'victory': e.s['enemy']['hp'] = 0; e.resolve_deaths()
                elif end == 'death': e.p['hp'] = 0; e.resolve_deaths()
                else:
                    with patch.object(e.rng, 'random', return_value=.1): e.execute('flee')
                self.assertFalse(any(st.get('effect_number') in EFFECTS for st in e.s['statuses']))
                SaveManager.validate(e.s)

    def test_save_all_effects_resume_rng_and_periods(self):
        e = self.combat()
        for n in range(16,26): self.apply(e, n); self.apply(e, n, 'enemy')
        e.execute('defend')
        with tempfile.TemporaryDirectory() as directory:
            store = SaveManager(directory); store.save(1, e.s)
            restored = GameEngine(ROOT / 'content', state=store.load(1))
            for _ in range(3):
                e.execute('defend'); restored.execute('defend')
                self.assertEqual(json.dumps(e.s, sort_keys=True), json.dumps(restored.s, sort_keys=True))

    def test_old_battle_gate_and_corrupt_new_state(self):
        e = self.combat(); old = copy.deepcopy(e.s); old.pop('battle_rules_version')
        restored = GameEngine(ROOT / 'content', state=old)
        rng = restored.rng.getstate(); before = copy.deepcopy(restored.s)
        self.assertFalse(restored.apply_status(16, 'player'))
        self.assertEqual(restored.s, before); self.assertEqual(restored.rng.getstate(), rng)
        restored.start_combat(); self.apply(restored, 16)
        for field, value in (('source_atk', float('nan')), ('source_side', 'other'), ('stacks', 3), ('turns', 99), ('eligible_turn', 9999), ('runtime_version', 9), ('effect_id', 'catalogue.v3.EF026')):
            state = copy.deepcopy(restored.s); state['statuses'][0][field] = value
            with self.assertRaises(ValueError): SaveManager.validate(state)
        state = copy.deepcopy(restored.s); state.pop('battle_rules_version')
        with self.assertRaises(ValueError): SaveManager.validate(state)

    def test_enemy_effect_routes_to_player(self):
        e = self.combat(); e.s['enemy'].update(pattern=['special'], effect_id='EF020')
        with patch.object(e.rng, 'random', return_value=.01): e.execute('defend')
        self.assertTrue(any(st.get('effect_number') == 20 for st in e.s['statuses']))
        self.assertFalse(e.s['enemy']['statuses'])

    def test_rejected_action_does_not_roll_confusion(self):
        e = self.combat(); self.apply(e, 22); e.p['mp'] = 0
        state = copy.deepcopy(e.s); rng = e.rng.getstate()
        with self.assertRaises(RuleError): e.execute('skill', key='base.skill.strike')
        self.assertEqual(e.s, state); self.assertEqual(e.rng.getstate(), rng)
