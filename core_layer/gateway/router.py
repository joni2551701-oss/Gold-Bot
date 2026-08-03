"""
Gateway router (v1.1 Phase 1, module 10) -- the single dispatch pipeline.

Every request runs the same ordered gate sequence, then the service
handler:

    build context (amendment 4)
      -> authenticate       (who?            -> UNAUTHENTICATED)
      -> discover service   (what?           -> NOT_FOUND)         [name|capability]
      -> authorize          (allowed?        -> FORBIDDEN)
      -> readiness check    (READY only,     -> UNAVAILABLE)        (amendment 1)
      -> rate limit         (throttle,       -> RATE_LIMITED)
      -> circuit breaker    (reliability,    -> UNAVAILABLE)        (amendment 5)
      -> dispatch handler   (OK | ERROR, records success/failure)

Each stage emits a GatewayEvent to the injected sink. The router imports no
trading layer and no transport; it holds no Strategy/Decision/Signal/Risk
logic (Director's hard rule).

Imports only sibling gateway modules.
"""

from __future__ import annotations

from datetime import datetime
from typing import Callable, Optional

from core_layer.gateway.gateway_request import (
    GatewayRequest, GatewayResponse, GatewayStatus, Principal,
)
from core_layer.gateway.gateway_context import new_context, utcnow
from core_layer.gateway.service_registry import ServiceRegistry, ServiceNotFoundError
from core_layer.gateway.service import RegisteredService
from core_layer.gateway.authentication import Authenticator, AllowAllAuthenticator
from core_layer.gateway.authorization import Authorizer, AllowAllAuthorizer
from core_layer.gateway.rate_limiter import RateLimiter
from core_layer.gateway.metrics_service import GatewayMetrics
from core_layer.gateway.gateway_events import (
    GatewayEvent, GatewayEventName, EventSink,
)


class GatewayRouter:
    def __init__(self, registry: ServiceRegistry,
                 authenticator: Optional[Authenticator] = None,
                 authorizer: Optional[Authorizer] = None,
                 rate_limiter: Optional[RateLimiter] = None,
                 metrics: Optional[GatewayMetrics] = None,
                 core_version: str = "", api_version: str = "",
                 clock: Optional[Callable[[], datetime]] = None,
                 event_sink: Optional[EventSink] = None):
        self._registry = registry
        self._auth = authenticator or AllowAllAuthenticator()
        self._authz = authorizer or AllowAllAuthorizer()
        self._rate = rate_limiter
        self._metrics = metrics or GatewayMetrics()
        self._core_version = core_version
        self._api_version = api_version
        self._clock = clock or utcnow
        self._sink = event_sink

    @property
    def metrics(self) -> GatewayMetrics:
        return self._metrics

    def dispatch(self, request: GatewayRequest,
                 now: Optional[datetime] = None) -> GatewayResponse:
        now = now or self._clock()
        principal = self._auth.authenticate(request)
        ctx_principal = principal or Principal()
        ctx = new_context(
            service=request.service, principal=ctx_principal, now=now,
            correlation_id=request.correlation_id,
            core_version=self._core_version, api_version=self._api_version,
            metadata=request.metadata)
        rid, cid = ctx.request_id, ctx.correlation_id
        self._emit(GatewayEventName.REQUEST_RECEIVED, rid, cid,
                   request.service, now)

        # -- authenticate --------------------------------------------
        if principal is None:
            return self._done(GatewayStatus.UNAUTHENTICATED, request, rid, cid,
                              now, error="unauthenticated",
                              event=GatewayEventName.REJECTED)
        self._emit(GatewayEventName.AUTHENTICATED, rid, cid, request.service,
                   now)

        # -- discover ------------------------------------------------
        try:
            service = self._resolve(request)
        except ServiceNotFoundError:
            return self._done(GatewayStatus.NOT_FOUND, request, rid, cid, now,
                              error="service not found",
                              event=GatewayEventName.SERVICE_UNAVAILABLE)

        # -- authorize -----------------------------------------------
        if not self._authz.authorize(principal, service.name,
                                     request.capability):
            return self._done(GatewayStatus.FORBIDDEN, request, rid, cid, now,
                              service=service.name, error="forbidden",
                              event=GatewayEventName.REJECTED)

        # -- readiness (amendment 1) ---------------------------------
        if not service.ready:
            return self._done(GatewayStatus.UNAVAILABLE, request, rid, cid, now,
                              service=service.name,
                              error=f"service not ready ({service.state.value})",
                              event=GatewayEventName.SERVICE_UNAVAILABLE)

        # -- rate limit ----------------------------------------------
        if self._rate is not None:
            key = f"{principal.id}:{service.name}"
            if not self._rate.allow(key, now):
                return self._done(GatewayStatus.RATE_LIMITED, request, rid, cid,
                                  now, service=service.name,
                                  error="rate limited",
                                  event=GatewayEventName.RATE_LIMITED)

        # -- circuit breaker (amendment 5) ---------------------------
        if not service.breaker.allow(now):
            return self._done(GatewayStatus.UNAVAILABLE, request, rid, cid, now,
                              service=service.name, error="circuit open",
                              event=GatewayEventName.CIRCUIT_OPENED)

        # -- dispatch ------------------------------------------------
        self._emit(GatewayEventName.DISPATCHED, rid, cid, service.name, now)
        try:
            result = service.handler(ctx, request.payload)
        except Exception as exc:                # handler failure is contained
            service.breaker.record_failure(now)
            return self._done(GatewayStatus.ERROR, request, rid, cid, now,
                              service=service.name, error=str(exc),
                              event=GatewayEventName.COMPLETED)
        service.breaker.record_success()
        return self._done(GatewayStatus.OK, request, rid, cid, now,
                          service=service.name, payload=result,
                          event=GatewayEventName.COMPLETED)

    # -- helpers --------------------------------------------------------
    def _resolve(self, request: GatewayRequest) -> RegisteredService:
        if request.service:
            return self._registry.discover(request.service)
        if request.capability:
            matches = self._registry.find(capability=request.capability)
            if matches:
                return matches[0]
        raise ServiceNotFoundError(request.service or request.capability or "")

    def _done(self, status: GatewayStatus, request: GatewayRequest,
              rid: str, cid: str, now: datetime, service: str = "",
              payload=None, error: str = "",
              event: Optional[GatewayEventName] = None) -> GatewayResponse:
        response = GatewayResponse(
            status=status, payload=payload, error=error,
            service=service or request.service, request_id=rid,
            correlation_id=cid)
        self._metrics.record(response)
        if event is not None:
            self._emit(event, rid, cid, response.service, now,
                       status=status.value)
        return response

    def _emit(self, name: GatewayEventName, rid: str, cid: str, service: str,
              now: datetime, status: str = "") -> None:
        if self._sink is None:
            return
        self._sink(GatewayEvent(
            name=name, request_id=rid, correlation_id=cid, service=service,
            status=status, timestamp=now))
