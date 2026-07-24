"""
Assistant Layer — Identity Manager (Phase 65.3: Personal AI Assistant
Foundation, TASK 1).

Read-only lookup over `identity_registry.py`'s static catalog. Mirrors
`ai/persona/persona_manager.py`'s `PersonaManager` shape exactly (same
Article 7 Reuse Principle) -- never builds a prompt, never calls an AI
provider, never mutates the registry it wraps.
"""

from typing import Dict, List, Optional

from assistant.identity import AssistantIdentity
from assistant.identity_registry import SENIOR_IDENTITY, build_identity_registry


class IdentityManager:
    """Every dependency is injectable, same convention as every other Phase 61.x-65.x manager -- a caller/test never needs the real static registry to exercise this class."""

    def __init__(self, identities: Optional[List[AssistantIdentity]] = None) -> None:
        registry = identities if identities is not None else build_identity_registry()
        self._by_name: Dict[str, AssistantIdentity] = {i.name: i for i in registry}

    def get(self, name: str) -> Optional[AssistantIdentity]:
        """Never raises: an unknown name returns None rather than a fabricated identity."""
        return self._by_name.get(name)

    def exists(self, name: str) -> bool:
        return name in self._by_name

    def default(self) -> AssistantIdentity:
        """Always succeeds: falls back to the module-level constant if it was somehow excluded from an injected registry, never raises."""
        return self._by_name.get(SENIOR_IDENTITY.name, SENIOR_IDENTITY)

    def all(self) -> List[AssistantIdentity]:
        return list(self._by_name.values())
