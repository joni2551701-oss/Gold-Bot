"""core_layer/gateway/router -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `router.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `router.py`.
"""
from core_layer.gateway.router.router import (
    annotations,
    datetime,
    Callable,
    Optional,
    GatewayRequest,
    GatewayResponse,
    GatewayStatus,
    Principal,
    new_context,
    utcnow,
    ServiceRegistry,
    ServiceNotFoundError,
    RegisteredService,
    Authenticator,
    AllowAllAuthenticator,
    Authorizer,
    AllowAllAuthorizer,
    RateLimiter,
    GatewayMetrics,
    GatewayEvent,
    GatewayEventName,
    EventSink,
    GatewayRouter,
)

__all__ = [
    "annotations",
    "datetime",
    "Callable",
    "Optional",
    "GatewayRequest",
    "GatewayResponse",
    "GatewayStatus",
    "Principal",
    "new_context",
    "utcnow",
    "ServiceRegistry",
    "ServiceNotFoundError",
    "RegisteredService",
    "Authenticator",
    "AllowAllAuthenticator",
    "Authorizer",
    "AllowAllAuthorizer",
    "RateLimiter",
    "GatewayMetrics",
    "GatewayEvent",
    "GatewayEventName",
    "EventSink",
    "GatewayRouter",
]
