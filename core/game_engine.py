from .expansion_engine import GameEngine as ExpansionEngine, RuleError, SLOTS, STAT_NAMES
from .phase2 import Phase2Mixin
from .migrations import migrate_v1_to_v2, migrate_v2_to_v3


class GameEngine(Phase2Mixin, ExpansionEngine):
    def __init__(self,root,state=None,seed=None):
        if state and state.get('save_schema_version')==1: state=migrate_v1_to_v2(state)
        if state and state.get('save_schema_version')==2: state=migrate_v2_to_v3(state)
        super().__init__(root,state,seed)
        self.s.update(save_schema_version=3,game_version='1.2.0')
        for key,value in dict(skill_cooldowns={},skill_buffs={},skill_usage={},phase2_legacy_combat=False).items(): self.s.setdefault(key,value)
