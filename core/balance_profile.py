"""Versioned active caps/defaults; other sections document unchanged sources."""
import json
from pathlib import Path

PROFILE = json.loads((Path(__file__).resolve().parents[1] / 'content/balance_profiles/1.2.0-policy1.json').read_text(encoding='utf-8'))
