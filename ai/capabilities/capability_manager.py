"""
AI Layer — Capability Manager (Phase 61.0: AI Infrastructure
Foundation, TASK 2).

Turns `capability_registry.py`'s static defaults into a live,
independently-toggleable state per `Capability` -- each capability can
be enabled/disabled on its own, matching the brief's own requirement
("har biri mustaqil yoqiladi/o'chiriladi"). In-memory only, like
`configuration/runtime_state.py`'s `RuntimeStateCache` in *shape*, but
a separate instance/namespace -- see
`docs/PHASE61_AI_FOUNDATION_AUDIT.md` for why this is not built on top
of `configuration/`'s Infrastructure-only registry.

Not wired into `core/pipeline.py`, any Telegram handler, or
`telegram/command_router.py` -- foundation only, constructed and
called directly (e.g. from a test, or a future owner command).
"""

from typing import Dict, List, Optional

from ai.capabilities.capability import Capability
from ai.capabilities.capability_registry import CapabilityDescriptor, build_capability_registry
from core_layer.logger.logger import setup_logger

logger = setup_logger("CapabilityManager")


class CapabilityManager:
    """
    Holds one enabled/disabled bool per `Capability`, seeded from
    `build_capability_registry()`'s defaults on construction.
    """

    def __init__(self) -> None:
        self._state: Dict[Capability, bool] = {
            descriptor.capability: descriptor.enabled
            for descriptor in build_capability_registry()
        }

    def is_enabled(self, capability: Capability) -> bool:
        """Returns the current state; an unknown Capability is impossible (enum-typed), so this never raises."""
        return self._state.get(capability, False)

    def enable(self, capability: Capability) -> None:
        self._state[capability] = True
        logger.info(f"Capability enabled: {capability.value}")

    def disable(self, capability: Capability) -> None:
        self._state[capability] = False
        logger.info(f"Capability disabled: {capability.value}")

    def status(self) -> List[CapabilityDescriptor]:
        """Current live state for every capability, same descriptor shape the static registry uses -- a caller does not need to know this manager exists separately from the registry."""
        return [
            CapabilityDescriptor(capability=capability, enabled=enabled)
            for capability, enabled in self._state.items()
        ]

    def enabled_capabilities(self) -> List[Capability]:
        return [capability for capability, enabled in self._state.items() if enabled]


_default_manager: Optional[CapabilityManager] = None


def get_capability_manager() -> CapabilityManager:
    """
    Process-wide default instance, lazily constructed -- matches the
    convenience convention other foundation singletons in this
    codebase use (e.g. a single shared cache) without forcing every
    caller to construct and pass one explicitly. A test or future
    caller needing an isolated instance constructs `CapabilityManager()`
    directly instead of calling this.
    """
    global _default_manager
    if _default_manager is None:
        _default_manager = CapabilityManager()
    return _default_manager
