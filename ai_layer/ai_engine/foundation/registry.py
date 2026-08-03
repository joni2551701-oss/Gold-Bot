"""
AI Foundation — AI Registry (TASK-AI-001: AI Foundation Activation).

Holds the live `AIComponent` instances the Foundation manages, keyed
by `component.name`. The single, unified registry the TASK-AI-000 audit
found missing (there were 6 per-subsystem registries in two
incompatible shapes). Depends only on the `AIComponent` *interface*
(Dependency Inversion) -- never on any concrete component.

Depends only on stdlib and `ai_layer.ai_engine.foundation.interfaces`.
"""

from typing import Dict, List, Optional, Sequence

from ai_layer.ai_engine.foundation.interfaces import AIComponent


class FoundationRegistry:
    """Register/unregister/get/list over `AIComponent`s. Duplicate names raise; unknown lookups return None/False."""

    def __init__(self) -> None:
        self._components: Dict[str, AIComponent] = {}

    def register(self, component: AIComponent) -> None:
        name = component.name
        if name in self._components:
            raise ValueError(f"component already registered: {name}")
        self._components[name] = component

    def unregister(self, name: str) -> bool:
        return self._components.pop(name, None) is not None

    def get(self, name: str) -> Optional[AIComponent]:
        return self._components.get(name)

    def list(self) -> List[str]:
        """Registered component names."""
        return list(self._components.keys())

    def components(self) -> Sequence[AIComponent]:
        """The live component instances, for lifecycle fan-out (init/start/stop/shutdown/health)."""
        return list(self._components.values())

    def clear(self) -> None:
        self._components.clear()
