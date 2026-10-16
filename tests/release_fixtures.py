"""Synthetic release saves. Never reads or writes the player's saves directory."""
import copy
import json
from pathlib import Path

from core.legacy_engine import GameEngine as LegacyEngine
from core.expansion_engine import GameEngine as ExpansionEngine
from core.game_engine import GameEngine
from core.save_manager import SaveManager

ROOT = Path(__file__).resolve().parents[1]


def fixtures():
    for schema, engine_type in ((1, LegacyEngine), (2, ExpansionEngine), (3, GameEngine)):
        modes = ('base', 'combat', 'event', 'overflow')
        if schema >= 2:
            modes += ('result',)
        for mode in modes:
            engine = engine_type(ROOT / 'content', seed=20261017)
            engine.p.update(gold=10000, level=10, skill_points=2)
            # The current loader includes phase 2; historical fixtures must not.
            if schema < 3:
                for key in list(engine.s['skills']):
                    if key.startswith('phase2.'):
                        engine.s['skills'].pop(key)
                        engine.s['skill_auto'].pop(key, None)
            skill = next(iter(engine.s['skills']))
            engine.s['skills'][skill] = 2
            if schema >= 2:
                engine.execute('buy', key='catalogue.v3.EQ001')
            if mode == 'combat':
                engine.execute('enter')
                engine.start_combat()
            elif mode in ('event', 'result'):
                event = next(row for row in engine.content['events'] if not row.get('phase2'))
                engine.s.update(mode='event', event=copy.deepcopy(event))
                if mode == 'result':
                    engine.execute('event', index=1)
            elif mode == 'overflow':
                key = 'base.item.hp' if schema == 1 else 'catalogue.v3.CON001'
                engine.s['items'][key] = 103 if schema == 1 else 99
                if schema >= 2:
                    engine.grant_item(key, 4)
            state = copy.deepcopy(engine.s)
            state['save_schema_version'] = schema
            SaveManager.validate(state)
            yield f'v{schema}_{mode}', state


def export(directory):
    directory.mkdir(parents=True, exist_ok=True)
    names = []
    for name, state in fixtures():
        (directory / f'{name}.json').write_text(
            json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')
        names.append(name)
    return names


if __name__ == '__main__':
    print(json.dumps(export(ROOT / 'artifacts/release_1_2/fixtures'), ensure_ascii=False))
