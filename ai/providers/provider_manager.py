"""
AI Layer — Provider Manager (Phase 61.0: AI Infrastructure Foundation,
TASK 3).

Owns Preferred -> Fallback -> Disabled selection over
`provider_registry.py`'s static catalog. `select_provider()` is the
one method a future caller (TASK 4's router, or a real integration
phase) needs: it never returns a disabled provider, prefers the
provider explicitly marked PREFERRED, and otherwise walks FALLBACK
providers in registry order. In-memory only, not wired into
`core/pipeline.py` or any live caller this phase.
"""

from enum import Enum
from typing import Dict, List, Optional

from ai.providers.base_provider import BaseAIProvider
from ai.providers.provider_registry import ProviderDescriptor, build_provider_registry
from core_layer.logger.logger import setup_logger

logger = setup_logger("ProviderManager")


class ProviderStatus(Enum):
    PREFERRED = "PREFERRED"
    FALLBACK = "FALLBACK"
    DISABLED = "DISABLED"


class ProviderManager:
    """
    Seeds every registered provider as FALLBACK by default (no
    provider is preferred or disabled until a caller says so) --
    `select_provider()` still works out of the box, walking registry
    order.
    """

    def __init__(self) -> None:
        self._descriptors: Dict[str, ProviderDescriptor] = {
            d.name: d for d in build_provider_registry()
        }
        self._status: Dict[str, ProviderStatus] = {
            name: ProviderStatus.FALLBACK for name in self._descriptors
        }
        self._order: List[str] = list(self._descriptors.keys())

    def set_status(self, name: str, status: ProviderStatus) -> None:
        """Unknown `name` is silently ignored -- same fail-safe posture as RuntimeFeatureManager's own toggle rejection, but there is no dependency graph to violate here, so nothing to reject beyond an unknown name."""
        if name not in self._descriptors:
            logger.warning(f"set_status called for unregistered provider: {name}")
            return
        self._status[name] = status
        logger.info(f"Provider {name} status set to {status.value}")

    def get_provider(self, name: str) -> Optional[BaseAIProvider]:
        descriptor = self._descriptors.get(name)
        return descriptor.provider if descriptor else None

    def list_providers(self) -> List[str]:
        return list(self._order)

    def status_of(self, name: str) -> Optional[ProviderStatus]:
        return self._status.get(name)

    def select_provider(self) -> Optional[BaseAIProvider]:
        """
        Preferred first (registry order among any providers marked
        PREFERRED), then the first FALLBACK in registry order, else
        None if every provider is DISABLED. Never raises.
        """
        preferred = [
            name for name in self._order
            if self._status.get(name) == ProviderStatus.PREFERRED
        ]
        if preferred:
            return self._descriptors[preferred[0]].provider

        for name in self._order:
            if self._status.get(name) == ProviderStatus.FALLBACK:
                return self._descriptors[name].provider

        return None
