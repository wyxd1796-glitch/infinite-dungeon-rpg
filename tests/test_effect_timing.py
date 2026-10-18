import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from core.effect_timing import DamageKind
from core.game_engine import GameEngine, RuleError
from core.save_manager import SaveManager

ROOT = Path(__file__).resolve().parents[1]


def combat_digest():
    rows = []
    for seed in (7, 713, 20261018):
        for floor in (1, 10, 30, 100, 101, 200):
            e = GameEngine(ROOT / 'content', seed=seed)
            e.execute('enter'); e.s['floor'] = floor
            e.start_combat('boss' if floor % 10 == 0 else 'normal')
            e.apply_status(14, 'player', 'player', 1)
            e.apply_status(2, 'enemy', 'player', 1)
            for i in range(20):
                if e.s['mode'] != 'combat': break
                e.execute(('attack', 'heavy', 'defend')[i % 3])
                state = copy.deepcopy(e.s)
                # Additive battle version metadata does not change old combat outcomes.
                for key in ('started_at', 'saved_at', 'battle_rules_version', 'effect_combat_state', 'catalogue_version', 'active_content_packs'): state.pop(key, None)
                rows.append(state)
    return len(rows), hashlib.sha256(json.dumps(rows, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


class EffectTimingTests(unittest.TestCase):
    def combat(self):
        e = GameEngine(ROOT / 'content', seed=713)
        e.execute('enter'); e.start_combat()
        e.s['enemy'].update(hp=10000, max_hp=10000, atk=10, defense=0,
                           evasion=0, accuracy=2, pattern=['defend'],
                           on_hit_effects=[], effect_id=None)
        return e

    def test_existing_combat_snapshot(self):
        # 03-06..09 intentionally replaces the 101/200-floor encounters in this fixture.
        # The pre-change 1..100 selection/state/RNG digest remains fixed in test_selection.
        self.assertEqual(combat_digest(), (48, 'c4f920bdca83e670c99270cda33bc0757937eeb829c6e4cf8052d16c1bea8b08'))

    def test_action_phase_order(self):
        e = self.combat(); seen = []; original = e.actor_phase
        def record(side, phase):
            seen.append((side, phase)); return original(side, phase)
        with patch.object(e, 'actor_phase', side_effect=record): e.execute('attack')
        self.assertEqual(seen, [('player', 'turn_start'), ('player', 'turn_end'),
                                ('enemy', 'turn_start'), ('enemy', 'turn_end')])

    def test_damage_categories_shield_and_overkill(self):
        e = self.combat()
        for kind in DamageKind:
            with self.subTest(kind=kind):
                e.p.update(hp=10, shield=8)
                self.assertEqual(e.damage_hp('player', 12, kind), 4 if kind in (DamageKind.DIRECT, DamageKind.COUNTER) else 10)
                self.assertEqual(e.p['shield'], 0 if kind in (DamageKind.DIRECT, DamageKind.COUNTER) else 8)
        for args in (('other', 1, 'direct'), ('player', -1, 'direct'), ('player', 1, 'unknown')):
            with self.assertRaises(ValueError): e.damage_hp(*args)

    def test_full_absorption_prevents_on_damage_chains(self):
        e = self.combat(); e.p['hp'] = 50; e.s['enemy']['shield'] = 10000
        enemy = dict(e.enemy_stats(), counter=1, reflect=1)
        player = dict(e.derived(), leech=1)
        with patch.object(e, 'stats_for', side_effect=lambda side: player if side == 'player' else enemy), patch.object(e.rng, 'random', return_value=.5):
            self.assertEqual(e.direct_hit('player'), 0)
        self.assertEqual(e.p['hp'], 50); self.assertEqual(e.s['enemy']['hp'], 10000)

    def test_counter_never_recurses_or_leeches(self):
        e = self.combat(); e.p['hp'] = 500; e.s['enemy']['hp'] = 200
        common = dict(e.derived(), hp=500, defense=0, evasion=0, crit=0,
                      counter=1, reflect=.2, leech=.5)
        stats = {'player': dict(common, atk=100), 'enemy': dict(common, atk=20)}
        with patch.object(e, 'stats_for', side_effect=stats.__getitem__), patch.object(e.rng, 'random', return_value=.1), patch.object(e.rng, 'uniform', return_value=1), patch.object(e, 'direct_hit', wraps=e.direct_hit) as hit:
            e.direct_hit('player')
            self.assertEqual(hit.call_count, 2)
        self.assertEqual(e.p['hp'], 460); self.assertEqual(e.s['enemy']['hp'], 100)

    def test_leech_before_reflection_and_double_death_loses(self):
        e = self.combat(); e.p['hp'] = 1; e.s['enemy']['hp'] = 10
        stats = {'player': dict(e.derived(), atk=100, crit=0, leech=.25),
                 'enemy': dict(e.enemy_stats(), reflect=1, counter=0)}
        with patch.object(e, 'stats_for', side_effect=stats.__getitem__), patch.object(e.rng, 'random', return_value=.5), patch.object(e.rng, 'uniform', return_value=1):
            self.assertEqual(e.direct_hit('player'), 10)
        self.assertEqual((e.p['hp'], e.s['enemy']['hp']), (0, 0))
        e.resolve_deaths(); e.resolve_deaths()
        self.assertEqual(e.s['stats']['deaths'], 1); self.assertEqual(e.s['stats']['wins'], 0)

    def test_periodic_death_prevents_enemy_action(self):
        e = self.combat(); e.p['hp'] = 1; e.apply_status(1, 'player', 'enemy', 1)
        with patch.object(e, 'counter', wraps=e.counter) as counter:
            e.execute('defend'); counter.assert_not_called()
        self.assertEqual(e.s['mode'], 'base')

    def test_kill_settles_before_player_periodic_damage(self):
        e = self.combat(); e.p['hp'] = 1; e.s['enemy']['hp'] = 1
        e.apply_status(1, 'player', 'enemy', 1)
        with patch.object(e.rng, 'random', return_value=.5): e.execute('attack')
        self.assertEqual(e.s['stats']['wins'], 1); self.assertEqual(e.s['stats']['deaths'], 0)
        before = copy.deepcopy(e.s); e.resolve_deaths(); self.assertEqual(e.s, before)

    def test_rejected_action_does_not_regenerate_or_tick(self):
        e = self.combat(); e.p['mp'] = 0; e.apply_status(14, 'player', 'player', 1)
        before = copy.deepcopy(e.s); rng = e.rng.getstate()
        with self.assertRaises(RuleError): e.execute('skill', key='base.skill.strike')
        self.assertEqual(e.s, before); self.assertEqual(e.rng.getstate(), rng)

    def test_failure_after_damage_rolls_back_entire_action(self):
        e = self.combat(); before = copy.deepcopy(e.s); rng = e.rng.getstate(); original = e.actor_phase
        def fail(side, phase):
            original(side, phase)
            if phase == 'turn_end': raise RuntimeError('injected failure')
        with patch.object(e, 'actor_phase', side_effect=fail), self.assertRaises(RuntimeError): e.execute('attack')
        self.assertEqual(e.s, before); self.assertEqual(e.rng.getstate(), rng)

    def test_save_resume_matches_uninterrupted_turns(self):
        e = self.combat(); e.p.update(level=30, mp=30)
        key = 'phase2.skill.SKL016'; e.s['skills'][key] = 1
        e.apply_status(1, 'player', 'enemy', 1); e.execute('skill', key=key)
        with tempfile.TemporaryDirectory() as directory:
            manager = SaveManager(directory)
            for action in ('defend', 'attack', 'heavy', 'defend'):
                manager.save(1, e.s)
                restored = GameEngine(ROOT / 'content', state=manager.load(1))
                e.execute(action); restored.execute(action)
                self.assertEqual(json.dumps(e.s, sort_keys=True), json.dumps(restored.s, sort_keys=True))
                self.assertEqual(e.rng.getstate(), restored.rng.getstate())

    def test_stun_ticks_cooldown_without_mp_or_pattern_consumption(self):
        e = self.combat(); key = 'phase2.skill.SKL003'
        e.s['skill_cooldowns'][key] = 2
        e.apply_status(4, 'player', 'enemy', 1); e.apply_status(4, 'enemy', 'player', 1)
        mp = e.p['mp']; e.execute('defend')
        self.assertEqual(e.p['mp'], mp); self.assertEqual(e.s['skill_cooldowns'][key], 1)
        self.assertEqual(e.s['enemy']['pattern_index'], 0)
