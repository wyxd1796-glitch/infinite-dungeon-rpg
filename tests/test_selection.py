import copy
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from core.catalogue import activate, option_slots
from core.game_engine import GameEngine

ROOT = Path(__file__).resolve().parents[1]


def selection_digest():
    rows = []
    for seed in (7, 713, 20261018):
        engine = GameEngine(ROOT / 'content', seed=seed)
        for floor in range(1, 101):
            engine.s['floor'] = floor
            for kind in ('normal', 'elite', 'boss'):
                engine.start_combat(kind)
                rows.append([engine.environment(), engine.s['enemy'], engine.generate_equipment(), repr(engine.rng.getstate())])
    return hashlib.sha256(json.dumps(rows, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


class SelectionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'content'
        shutil.copytree(ROOT / 'content', self.root)
        self.engine = GameEngine(self.root, seed=713)

    def change(self, file, fn):
        path = self.root / file
        data = json.loads(path.read_text(encoding='utf-8'))
        fn(data)
        path.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')

    def test_seeded_results_unchanged(self):
        # Captured before 03-06..09: 3 seeds x 100 floors x 3 encounter kinds.
        self.assertEqual(selection_digest(), '8ba574a9606d4a205a9bd16417e0ab5239d97d050b6ae6ed4014eecba80d9719')

    def test_source_row_order_independent(self):
        before = copy.deepcopy(self.engine.content.by_id)
        self.change('source/catalogue_v4.json', lambda d: [r.reverse() for r in d['base_catalogue_v3']['content'].values() if isinstance(r, list)])
        digest = hashlib.sha256((self.root / 'source/catalogue_v4.json').read_bytes()).hexdigest()
        self.change('catalogue/selection.json', lambda d: d.update(source_sha256=digest))
        activate(self.engine.content)
        self.assertEqual(before, self.engine.content.by_id)
        for floor in range(1, 101):
            self.engine.s['floor'] = floor
            region = self.engine.content.regions
            expected = [r for r in self.engine.content['monsters'] if r['min_floor'] <= region.zone(floor) <= r['max_floor']]
            self.assertEqual(region.monsters(self.engine.content, floor), expected)

    def test_invalid_active_ids(self):
        original = (self.root / 'catalogue/selection.json').read_text(encoding='utf-8')
        for group, key in (('effects', 'EF041'), ('options', 'OPT031'), ('monsters', 'MON999'), ('monsters', 'EF001'), ('monsters', 'MON001')):
            with self.subTest(group=group, key=key):
                (self.root / 'catalogue/selection.json').write_text(original, encoding='utf-8')
                self.change('catalogue/selection.json', lambda d: d['active_ids'][group].append(key))
                with self.assertRaises(ValueError): activate(self.engine.content)

    def test_region_validation(self):
        original = (self.root / 'catalogue/regions.json').read_text(encoding='utf-8')
        changes = [lambda d: d['regions'][0].update(environment_id='ENV031'),
                   lambda d: d['regions'][0].update(boss_id='MON001'),
                   lambda d: d['regions'][0].update(monster_ids=[]),
                   lambda d: d['regions'][0].update(min_floor=2),
                   lambda d: d['regions'][1].update(min_floor=10),
                   lambda d: d['regions'][0].update(monster_ids=['MON041']),
                   lambda d: d.update(primary_family_weight=float('nan'))]
        for index, change in enumerate(changes):
            with self.subTest(index=index):
                (self.root / 'catalogue/regions.json').write_text(original, encoding='utf-8')
                self.change('catalogue/regions.json', change)
                with self.assertRaises(ValueError): activate(self.engine.content)

    def test_slots_normalized_and_unknown_rejected(self):
        self.assertEqual(option_slots('방어구, 목걸이'), option_slots('방어구·목걸이'))
        self.assertEqual(option_slots('무기, 반지'), ['무기', '반지'])
        for value in ('무기, 날개', '', None):
            with self.assertRaises(ValueError): option_slots(value)

    def test_unsupported_runtime_fields_rejected_during_load(self):
        path = self.root / 'source/catalogue_v4.json'
        original = json.loads(path.read_text(encoding='utf-8'))
        for group, field, value in (('monsters', 'attack_pattern', '알 수 없는 패턴'),
                                    ('bosses', 'pattern', ['summon']),
                                    ('options', 'slot_restriction', '날개')):
            with self.subTest(group=group):
                data = copy.deepcopy(original)
                data['base_catalogue_v3']['content'][group][0][field] = value
                path.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
                self.change('catalogue/selection.json', lambda d: d.update(source_sha256=digest))
                with self.assertRaises(ValueError): activate(self.engine.content)

    def test_save_preserves_inflight_objects(self):
        e = self.engine
        e.start_combat('elite')
        e.s['pending_loot'] = [e.generate_equipment()]
        before = copy.deepcopy(e.s)
        restored = GameEngine(self.root, state=before)
        for key in ('enemy', 'inventory', 'pending_loot', 'skills', 'items', 'player', 'settings', 'event', 'event_result'):
            self.assertEqual(restored.s.get(key), before.get(key), key)

    def test_active_order_is_explicit(self):
        self.change('catalogue/selection.json', lambda d: d['active_ids']['equipment'].reverse())
        activate(self.engine.content)
        self.assertEqual(self.engine.content['equipment'][0]['source_id'], 'EQ330')
        self.assertEqual(self.engine.content['equipment'][-1]['source_id'], 'EQ001')
