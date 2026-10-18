"""Damage categories for the shared HP commit point.

This is the existing combat contract, not an EF016+ activation registry.
Events and HP costs are outside combat damage processing.
"""
from enum import Enum


class DamageKind(str, Enum):
    DIRECT = 'direct'
    COUNTER = 'counter'
    PERIODIC = 'periodic'
    REFLECTED = 'reflected'


SHIELDED_DAMAGE = frozenset((DamageKind.DIRECT, DamageKind.COUNTER))
