"""
core_layer.gateway -- GoldBot v1.1 Market Data Foundation: Core Gateway Layer
(Phase 1 module 10). The single entry point into Core: every external
client (Telegram, Web, Mobile, AI, Chart, Media) reaches Core services
through the Gateway, never by importing a service directly.

Provides: a service registry + capability/dependency-aware discovery, a
service lifecycle state machine, a per-service reliability circuit breaker,
authentication + authorization + rate limiting, a standard per-request
context, health/metrics/version endpoints, and a CoreGateway facade.

Transport-independent (in-process handlers now; HTTP/WS/gRPC/IPC later) and
trading-agnostic: the Gateway holds no Strategy/Decision/Signal/Risk logic,
offers no execution route, is not wired into core/pipeline.py, and imports
nothing from strategies/, signals/, decision/, risk/, execution/, ai/,
telegram/, database/, or data/.
"""

from core_layer.gateway.service_state import (
    ServiceState, ServiceStateError, can_transition, assert_transition,
)
from core_layer.gateway.service_breaker import BreakerState, ServiceCircuitBreaker
from core_layer.gateway.service_manifest import (
    ServiceManifest, ServiceKind, HealthPolicy,
)
from core_layer.gateway.service import RegisteredService, ServiceHandler
from core_layer.gateway.dependency_graph import (
    DependencyError, missing_dependencies, find_cycle, validate,
    resolution_order, build_graph,
)
from core_layer.gateway.service_registry import (
    ServiceRegistry, DuplicateServiceError, ServiceNotFoundError,
)
from core_layer.gateway.gateway_request import (
    GatewayRequest, GatewayResponse, GatewayStatus, Principal, ANONYMOUS,
)
from core_layer.gateway.gateway_context import GatewayContext, new_context, utcnow
from core_layer.gateway.authentication import (
    Authenticator, AllowAllAuthenticator, TokenAuthenticator,
)
from core_layer.gateway.authorization import (
    Authorizer, AllowAllAuthorizer, RoleAuthorizer,
)
from core_layer.gateway.rate_limiter import RateLimiter
from core_layer.gateway.metrics_service import GatewayMetrics
from core_layer.gateway.health_service import HealthService, GatewayHealth
from core_layer.gateway.version_service import (
    VersionService, CORE_VERSION, GATEWAY_API_VERSION,
)
from core_layer.gateway.gateway_events import (
    GatewayEvent, GatewayEventName, EventSink,
)
from core_layer.gateway.router import GatewayRouter
from core_layer.gateway.gateway import CoreGateway

__all__ = [
    "ServiceState", "ServiceStateError", "can_transition", "assert_transition",
    "BreakerState", "ServiceCircuitBreaker",
    "ServiceManifest", "ServiceKind", "HealthPolicy",
    "RegisteredService", "ServiceHandler",
    "DependencyError", "missing_dependencies", "find_cycle", "validate",
    "resolution_order", "build_graph",
    "ServiceRegistry", "DuplicateServiceError", "ServiceNotFoundError",
    "GatewayRequest", "GatewayResponse", "GatewayStatus", "Principal",
    "ANONYMOUS",
    "GatewayContext", "new_context", "utcnow",
    "Authenticator", "AllowAllAuthenticator", "TokenAuthenticator",
    "Authorizer", "AllowAllAuthorizer", "RoleAuthorizer",
    "RateLimiter",
    "GatewayMetrics",
    "HealthService", "GatewayHealth",
    "VersionService", "CORE_VERSION", "GATEWAY_API_VERSION",
    "GatewayEvent", "GatewayEventName", "EventSink",
    "GatewayRouter",
    "CoreGateway",
]
