import copy
import json
import tempfile
import unittest

from core.game_engine import GameEngine
from core.save_manager import SaveManager
from release_fixtures import ROOT, fixtures


class ReleaseSaveTests(unittest.TestCase):
    def test_historical_fixture_roundtrip_and_backups(self):
        for name, original in fixtures():
            with self.subTest(fixture=name), tempfile.TemporaryDirectory() as folder:
                store = SaveManager(folder)
                raw = json.dumps(original, ensure_ascii=False).encode('utf-8')
                store.path(1).write_bytes(raw)
                migrated = store.load(1)
                engine = GameEngine(ROOT / 'content', migrated)
                self.assertEqual(store.path(1).read_bytes(), raw)
                for field in ('player', 'inventory', 'equipped', 'bag', 'skills'):
                    if field == 'skills':
                        for key, value in original[field].items():
                            self.assertEqual(engine.s[field][key], value)
                    else:
                        self.assertEqual(engine.s[field], original[field])
                for field in ('event', 'enemy', 'event_result', 'shop_stock'):
                    if field in original:
                        self.assertEqual(engine.s[field], original[field])
                if original['save_schema_version'] < 3:
                    self.assertEqual(store.path(1).with_suffix('.json.pre-v3.bak').read_bytes(), raw)
                if original['save_schema_version'] == 1:
                    self.assertEqual(store.path(1).with_suffix('.json.pre-v2.bak').read_bytes(), raw)
                if name.endswith('overflow'):
                    self.assertEqual(sum(row['quantity'] for row in engine.s['pending_loot']), 4)
                snapshot = copy.deepcopy(engine.s)
                store.save(1, engine.s)
                reloaded = GameEngine(ROOT / 'content', store.load(1))
                for field in ('player', 'skills', 'pending_loot', 'skill_auto', 'event_result'):
                    self.assertEqual(reloaded.s[field], snapshot[field])


if __name__ == '__main__':
    unittest.main()
