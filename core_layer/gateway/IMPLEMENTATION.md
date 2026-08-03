# IMPLEMENTATION.md -- core_layer/gateway

## `authentication.py`

Gateway authentication (v1.1 Phase 1, module 10).

Classes: `Authenticator`, `AllowAllAuthenticator`, `TokenAuthenticator`

## `authorization.py`

Gateway authorization (v1.1 Phase 1, module 10).

Classes: `Authorizer`, `AllowAllAuthorizer`, `RoleAuthorizer`

## `dependency_graph.py`

Service dependency graph (v1.1 Phase 1, module 10; ORDER-064 amendment 3).

Classes: `DependencyError`

Top-level functions: `missing_dependencies()`, `find_cycle()`, `validate()`, `resolution_order()`, `build_graph()`

## `gateway.py`

CoreGateway facade (v1.1 Phase 1, module 10) -- the single entry point.

Classes: `CoreGateway`

## `gateway_context.py`

Gateway request context (v1.1 Phase 1, module 10; ORDER-064 amendment 4).

Classes: `GatewayContext`

Top-level functions: `utcnow()`, `new_context()`

## `gateway_events.py`

Gateway events (v1.1 Phase 1, module 10).

Classes: `GatewayEventName`, `GatewayEvent`

## `gateway_request.py`

Gateway request/response model (v1.1 Phase 1, module 10).

Classes: `GatewayStatus`, `Principal`, `GatewayRequest`, `GatewayResponse`

## `health_service.py`

Gateway health service (v1.1 Phase 1, module 10).

Classes: `GatewayHealth`, `HealthService`

## `metrics_service.py`

Gateway metrics (v1.1 Phase 1, module 10).

Classes: `GatewayMetrics`

## `rate_limiter.py`

Gateway rate limiter (v1.1 Phase 1, module 10).

Classes: `_Bucket`, `RateLimiter`

## `router.py`

Gateway router (v1.1 Phase 1, module 10) -- the single dispatch pipeline.

Classes: `GatewayRouter`

## `service.py`

RegisteredService (v1.1 Phase 1, module 10).

Classes: `RegisteredService`

## `service_breaker.py`

Service circuit breaker (v1.1 Phase 1, module 10; ORDER-064 amendment 5).

Classes: `BreakerState`, `ServiceCircuitBreaker`

## `service_manifest.py`

Service manifest (v1.1 Phase 1, module 10; ORDER-064 amendments 2, 3, 6).

Classes: `ServiceKind`, `HealthPolicy`, `ServiceManifest`

## `service_registry.py`

Service registry + discovery (v1.1 Phase 1, module 10; ORDER-064

Classes: `DuplicateServiceError`, `ServiceNotFoundError`, `ServiceRegistry`

## `service_state.py`

Service lifecycle state machine (v1.1 Phase 1, module 10; ORDER-064

Classes: `ServiceState`, `ServiceStateError`

Top-level functions: `can_transition()`, `assert_transition()`

## `version_service.py`

Gateway version service (v1.1 Phase 1, module 10).

Classes: `VersionService`

## Runtime / Algorithms / Pipeline / Event Flow / Sequence / Design Decisions / Performance Notes

Not authored at rollout time -- this section requires domain understanding beyond what can be mechanically derived from code, and is left for a future Development Phase to fill in (per Director Order No. 012/013, this rollout is documentation standardization only, not new authorship of technical narrative).

---
*Generated 2026-08-03 by GoldBot Engineering Standard v1.0 rollout (Director Order No. 012/013).*
