"""
CoreGateway facade (v1.1 Phase 1, module 10) -- the single entry point.

Composes registry + router + auth + authorization + rate limiting + health
+ metrics + version behind one object. Platforms (Telegram, Web, Mobile,
AI, Chart, Media) hold a CoreGateway and reach every Core service through
`dispatch()` -- never by importing a service directly.

Lifecycle (amendment 1): services register in REGISTERED; `start()`
validates the dependency graph (amendment 3), then brings each service up
in dependency order REGISTERED -> STARTING -> READY. Only READY services
receive requests.

Hard boundary (Director's rule): the Gateway knows nothing of Strategy,
Decision, Signal or Trading logic. It offers no trade/execution route and
can never become a shortcut around `RiskManager.evaluate()`. It is a
foundation module -- not wired into `core/pipeline.py`, and it never imports
`strategies/`, `signals/`, `decision/`, `risk/`, `execution/`, `ai/`,
`telegram/`, `database/`, or `data/`.

Foundation Reuse Audit (Constitution Art. 11): a composed facade over new
sibling components; no existing module is a Core service gateway. New.
"""

from __future__ import annotations

from datetime import datetime
from typing import Callable, Dict, List, Optional

from core.gateway.service_manifest import ServiceManifest, ServiceKind
from core.gateway.service import RegisteredService, ServiceHandler
from core.gateway.service_state import ServiceState
from core.gateway.service_registry import ServiceRegistry
from core.gateway.authentication import Authenticator
from core.gateway.authorization import Authorizer
from core.gateway.rate_limiter import RateLimiter
from core.gateway.metrics_service import GatewayMetrics
from core.gateway.health_service import HealthService, GatewayHealth
from core.gateway.version_service import VersionService
from core.gateway.router import GatewayRouter
from core.gateway.gateway_request import GatewayRequest, GatewayResponse
from core.gateway.gateway_events import (
    GatewayEvent, GatewayEventName, EventSink,
)
from core.gateway.gateway_context import utcnow


class CoreGateway:
    def __init__(self, authenticator: Optional[Authenticator] = None,
                 authorizer: Optional[Authorizer] = None,
                 rate_limiter: Optional[RateLimiter] = None,
                 clock: Optional[Callable[[], datetime]] = None,
                 event_sink: Optional[EventSink] = None):
        self._registry = ServiceRegistry()
        self._metrics = GatewayMetrics()
        self._health = HealthService()
        self._version = VersionService()
        self._clock = clock or utcnow
        self._sink = event_sink
        self._router = GatewayRouter(
            self._registry, authenticator=authenticator,
            authorizer=authorizer, rate_limiter=rate_limiter,
            metrics=self._metrics, core_version=self._version.core_version,
            api_version=self._version.api_version, clock=self._clock,
            event_sink=event_sink)

    # -- registration ---------------------------------------------------
    def register_service(self, manifest: ServiceManifest,
                         handler: ServiceHandler) -> RegisteredService:
        service = self._registry.register(manifest, handler)
        self._emit(GatewayEventName.SERVICE_REGISTERED, service.name)
        return service

    # -- lifecycle (amendments 1, 3) -----------------------------------
    def start(self) -> List[str]:
        """Validate dependencies, then bring every service up in order."""
        order = self._registry.startup_order()      # raises on cycle/missing
        for name in order:
            service = self._registry.get(name)
            if service is None:
                continue
            if service.state is ServiceState.REGISTERED:
                service.transition(ServiceState.STARTING)
            if service.state is ServiceState.STARTING:
                service.transition(ServiceState.READY)
        return order

    def mark_degraded(self, name: str) -> None:
        self._registry.discover(name).transition(ServiceState.DEGRADED)

    def mark_ready(self, name: str) -> None:
        self._registry.discover(name).transition(ServiceState.READY)

    def stop(self, name: str) -> None:
        service = self._registry.discover(name)
        if service.state in (ServiceState.READY, ServiceState.DEGRADED,
                             ServiceState.STARTING):
            service.transition(ServiceState.STOPPING)
        service.transition(ServiceState.STOPPED)

    # -- dispatch (single entry point) ---------------------------------
    def dispatch(self, request: GatewayRequest,
                 now: Optional[datetime] = None) -> GatewayResponse:
        return self._router.dispatch(request, now=now)

    # -- discovery (amendment 2) ---------------------------------------
    def discover(self, name: str) -> RegisteredService:
        return self._registry.discover(name)

    def find(self, capability: Optional[str] = None,
             kind: Optional[ServiceKind] = None) -> List[RegisteredService]:
        return self._registry.find(capability=capability, kind=kind)

    def services(self) -> List[RegisteredService]:
        return self._registry.all()

    # -- built-in service endpoints ------------------------------------
    @property
    def health(self) -> HealthService:
        return self._health

    def health_report(self) -> Dict:
        return self._health.report()

    def health_status(self) -> GatewayHealth:
        return self._health.status()

    def metrics_snapshot(self) -> Dict:
        return self._metrics.snapshot()

    def version_info(self) -> Dict[str, str]:
        return self._version.info()

    # -- events ---------------------------------------------------------
    def _emit(self, name: GatewayEventName, service: str) -> None:
        if self._sink is None:
            return
        self._sink(GatewayEvent(name=name, service=service,
                                timestamp=self._clock()))
