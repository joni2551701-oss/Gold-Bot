"""
AI Foundation — AI Factory (TASK-AI-001: AI Foundation Activation).

Constructs (`create`) and tears down (`destroy`) `AIComponent`s from
registered builder callables. This formalizes, as a named component,
the `build_x_registry()`-style construction pattern that existed
informally across `ai/` (per the TASK-AI-000 audit). Depends only on
the `AIComponent` interface (Dependency Inversion) -- a builder returns
*an* `AIComponent`, the factory neither knows nor cares which.

Depends only on stdlib and `ai_layer.ai_engine.foundation.interfaces`.
"""

from typing import Callable, Dict, List

from ai_layer.ai_engine.foundation.interfaces import AIComponent

ComponentBuilder = Callable[[], AIComponent]


class FoundationFactory:
    """Builder-backed construction. Unknown names raise; `destroy` shuts a component down."""

    def __init__(self) -> None:
        self._builders: Dict[str, ComponentBuilder] = {}

    def register_builder(self, name: str, builder: ComponentBuilder) -> None:
        if name in self._builders:
            raise ValueError(f"builder already registered: {name}")
        self._builders[name] = builder

    def unregister_builder(self, name: str) -> bool:
        return self._builders.pop(name, None) is not None

    def create(self, name: str) -> AIComponent:
        builder = self._builders.get(name)
        if builder is None:
            raise KeyError(f"no builder registered for: {name}")
        return builder()

    def destroy(self, component: AIComponent) -> None:
        """Tear a component down via its own lifecycle. Never raises: a shutdown error is swallowed (best-effort teardown)."""
        try:
            component.shutdown()
        except Exception:
            pass

    def list_builders(self) -> List[str]:
        return list(self._builders.keys())
