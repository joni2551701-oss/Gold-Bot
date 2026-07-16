"""
AI Layer — AI Router (Phase 61.0: AI Infrastructure Foundation,
TASK 4).

Capability -> Provider -> Return, exactly as the brief's own worked
example states ("Explanation -> Gemini", "Image -> OpenAI"). Composes
`routing_rules.py`'s static table with `ai.providers.provider_manager.ProviderManager`'s
live status, and optionally `ai.capabilities.capability_manager.CapabilityManager`'s
live enabled/disabled state -- reimplements neither. Not wired into
`core/pipeline.py` or any live caller this phase.
"""

from typing import Optional

from ai.capabilities.capability import Capability
from ai.capabilities.capability_manager import CapabilityManager
from ai.providers.provider_manager import ProviderManager, ProviderStatus
from ai.router.routing_result import RoutingResult
from ai.router.routing_rules import get_candidate_providers


class AIRouter:
    """
    `capability_manager` is optional -- a router constructed without
    one skips the capability-enabled check entirely (useful for a test
    exercising provider selection in isolation), matching
    `ai.context.context_builder`'s own optional-input convention
    elsewhere in this phase's foundation.
    """

    def __init__(self, provider_manager: ProviderManager, capability_manager: Optional[CapabilityManager] = None) -> None:
        self._provider_manager = provider_manager
        self._capability_manager = capability_manager

    def route(self, capability: Capability) -> RoutingResult:
        """Never raises: every branch below returns a RoutingResult, including the "nothing available" case."""
        if self._capability_manager is not None and not self._capability_manager.is_enabled(capability):
            return RoutingResult(
                capability=capability, provider_name=None,
                reason=f"capability {capability.value} is disabled",
            )

        candidates = get_candidate_providers(capability)
        if not candidates:
            return RoutingResult(
                capability=capability, provider_name=None,
                reason=f"no routing rule declared for {capability.value}",
            )

        for name in candidates:
            status = self._provider_manager.status_of(name)
            if status is not None and status != ProviderStatus.DISABLED:
                return RoutingResult(
                    capability=capability, provider_name=name,
                    reason=f"matched routing rule for {capability.value}",
                )

        return RoutingResult(
            capability=capability, provider_name=None,
            reason=f"no available (non-disabled, registered) provider for {capability.value}",
        )
