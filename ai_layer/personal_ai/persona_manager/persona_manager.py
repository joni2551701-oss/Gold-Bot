"""
AI Layer — Persona Manager (Phase 63.0: Senior Trading AI Foundation,
TASK 1).

Read-only lookup over `persona_registry.py`'s static catalog. Never
builds a prompt, never calls `AIService`, never touches
`ai/prompts/`/`ai/runtime/` -- identity only (Rule 5).
"""

from typing import Dict, List, Optional

from ai_layer.personal_ai.persona_manager.persona import Persona
from ai_layer.personal_ai.persona_manager.persona_registry import SENIOR_TRADING_AI, build_persona_registry


class PersonaManager:
    """Every dependency is injectable, same convention as every other Phase 61.x/62.x manager -- a caller/test never needs the real static registry to exercise this class."""

    def __init__(self, personas: Optional[List[Persona]] = None) -> None:
        registry = personas if personas is not None else build_persona_registry()
        self._by_name: Dict[str, Persona] = {p.name: p for p in registry}

    def get(self, name: str) -> Optional[Persona]:
        """Never raises: an unknown name returns None rather than a fabricated persona."""
        return self._by_name.get(name)

    def get_active_persona(self) -> Persona:
        """The one persona this phase actually uses -- Senior Trading AI. Always succeeds: falls back to the module-level constant if it was somehow excluded from an injected registry, never raises."""
        return self._by_name.get(SENIOR_TRADING_AI.name, SENIOR_TRADING_AI)

    def all(self) -> List[Persona]:
        return list(self._by_name.values())
