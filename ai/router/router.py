"""
AI Layer — AI Router (Phase 61.0: AI Infrastructure Foundation,
TASK 4; extended Phase 61.1: AI Provider Reliability Foundation,
TASK 4).

Capability -> Provider -> Return, exactly as the Phase 61.0 brief's own
worked example states ("Explanation -> Gemini", "Image -> OpenAI").
Composes `routing_rules.py`'s static table with
`ai.providers.provider_manager.ProviderManager`'s live status,
optionally `ai.capabilities.capability_manager.CapabilityManager`'s
live enabled/disabled state, and -- as of Phase 61.1 -- optionally
`ai.providers.provider_capabilities.supports()` and
`ai.providers.provider_health.ProviderHealthTracker`'s live health --
reimplements none of them. Not wired into `core/pipeline.py` or any
live caller this phase.

Selection order per candidate (Phase 61.1 TASK 4): capability-matrix
support first (a provider `routing_rules.py` lists but never declared
the capability for is not a real candidate at all), then
`ProviderManager` status (owner intent), then health (observed
reality) -- still "Hardcode YO'Q": every check is a lookup against a
declarative table/tracker, never a per-provider branch.

Phase 61.1 TASK 8 (Router Metrics Integration) adds `provider_metrics()`
-- a read-only view over `ai.audit.provider_stats.compute_provider_stats()`,
reusing that function exactly as TASK 8's brief requires ("Yangi
metrics moduli YO'Q. Reuse."). `route()` itself never calls or is
influenced by this method -- no automatic optimization, a caller
inspects metrics separately.
"""

from typing import Dict, Optional

from ai.audit.provider_stats import ProviderStats, compute_provider_stats
from ai.audit.response_log import ResponseLog
from ai.capabilities.capability import Capability
from ai.capabilities.capability_manager import CapabilityManager
from ai.providers.provider_capabilities import supports
from ai.providers.provider_health import ProviderHealthTracker
from ai.providers.provider_manager import ProviderManager, ProviderStatus
from ai.router.routing_result import RoutingResult
from ai.router.routing_rules import get_candidate_providers


class AIRouter:
    """
    `capability_manager`, `health_tracker`, and `response_log` are all
    optional -- a router constructed without any of them skips that
    concern entirely (useful for a test exercising one concern in
    isolation), matching `ai.context.context_builder`'s own
    optional-input convention elsewhere in this foundation. Omitting
    `health_tracker`/`response_log` reproduces Phase 61.0's exact
    selection behavior -- Phase 61.1 adds checks and a read-only view,
    it does not change what happens when nothing new is supplied.
    """

    def __init__(
        self, provider_manager: ProviderManager, capability_manager: Optional[CapabilityManager] = None,
        health_tracker: Optional[ProviderHealthTracker] = None, response_log: Optional[ResponseLog] = None,
    ) -> None:
        self._provider_manager = provider_manager
        self._capability_manager = capability_manager
        self._health_tracker = health_tracker
        self._response_log = response_log

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
            if not supports(name, capability):
                continue

            status = self._provider_manager.status_of(name)
            if status is None or status == ProviderStatus.DISABLED:
                continue

            if self._health_tracker is not None and not self._health_tracker.is_available(name):
                continue

            return RoutingResult(
                capability=capability, provider_name=name,
                reason=f"matched routing rule for {capability.value}",
            )

        return RoutingResult(
            capability=capability, provider_name=None,
            reason=f"no available (capability-supporting, non-disabled, healthy) provider for {capability.value}",
        )

    def provider_metrics(self) -> Dict[str, ProviderStats]:
        """Read-only: aggregates the response log this router was constructed with, via the existing ai/audit/provider_stats.py -- no metrics state of its own. Returns an empty dict if this router has no response_log."""
        if self._response_log is None:
            return {}
        return compute_provider_stats(self._response_log.all())
