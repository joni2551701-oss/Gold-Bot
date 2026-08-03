# Core Gateway Layer — Architecture (v1.1 Phase 1, Module 10)

Status: implemented (MA-010 pending Director Final Review). Package:
`core_layer/gateway/`.

## 1. Purpose

The Gateway is the **single entry point** into Core. After Module 10, no
external client (Telegram, Web, Mobile, AI, Chart, Media) calls a Core
service directly — every call is `Client → Gateway → Core Service`. The
Gateway **connects and governs** services; it holds **no** Strategy /
Decision / Signal / Trading logic and offers **no** execution route.

```
 Telegram   Web   Mobile   AI/Chart   Media
     └────────┬──────┴────────┬──────────┘
              ▼
      ┌───────────────────────────┐
      │       CORE GATEWAY        │   authenticate → discover →
      │   (single entry point)    │   authorize → ready? → rate-limit →
      └───────────┬───────────────┘   circuit-breaker → dispatch
                  ▼   (ServiceContract handlers only — no imports)
  MarketMemory · MemoryReader · Replay · Snapshot · Health · Metrics · Version …
```

## 2. Position in the layer model

`core_layer/gateway/` is a subpackage of the existing `core/` package (Director
Decision 1). It sits at orchestration altitude, like `core/pipeline.py`,
but is deliberately **decoupled downward**: it imports **nothing** from
`data/`, `strategies/`, `signals/`, `decision/`, `risk/`, `execution/`,
`ai/`, `telegram/`, or `database/`. Where it needs infrastructure that
lives above it (the Event Bus in `data_layer/event_system`, the health source in
`monitoring/`), it takes that dependency by **injection**, never by import
— keeping the dependency arrow pointing the right way.

## 3. Dispatch pipeline

Every request runs one ordered gate sequence, then the service handler:

| Stage | Gate | Failure status |
|---|---|---|
| context | build `GatewayContext` (amendment 4) | — |
| authenticate | who is calling? | `UNAUTHENTICATED` |
| discover | by name or capability (amendment 2) | `NOT_FOUND` |
| authorize | may they? | `FORBIDDEN` |
| readiness | service `READY`? (amendment 1) | `UNAVAILABLE` |
| rate limit | token bucket | `RATE_LIMITED` |
| circuit breaker | reliability (amendment 5) | `UNAVAILABLE` (circuit open) |
| dispatch | run handler | `OK` / `ERROR` |

Each stage emits a `GatewayEvent` to an injected sink.

## 4. Components (`core_layer/gateway/`)

| File | Responsibility |
|---|---|
| `service_state.py` | `ServiceState` lifecycle machine (amendment 1) |
| `service_breaker.py` | `ServiceCircuitBreaker` OPEN/HALF_OPEN/CLOSED (amendment 5) |
| `service_manifest.py` | `ServiceManifest` — capabilities, dependencies, health policy, owner (amendments 2/3/6) |
| `service.py` | `RegisteredService` — manifest + handler + state + breaker |
| `dependency_graph.py` | missing-dep + cycle detection, topological startup order (amendment 3) |
| `service_registry.py` | register / discover / find-by-capability / dependency validation |
| `gateway_request.py` | `GatewayRequest` / `GatewayResponse` / `GatewayStatus` / `Principal` |
| `gateway_context.py` | `GatewayContext` per-request standard context (amendment 4) |
| `authentication.py` | `Authenticator` + allow-all / token backends |
| `authorization.py` | `Authorizer` + allow-all / role-based backends |
| `rate_limiter.py` | clock-injected token bucket |
| `metrics_service.py` | request counts by status / service |
| `health_service.py` | injected checks → OK/DEGRADED/DOWN |
| `version_service.py` | Core version + Gateway API version |
| `gateway_events.py` | `GatewayEvent` + injected `EventSink` |
| `router.py` | `GatewayRouter` — the pipeline above |
| `gateway.py` | `CoreGateway` facade (register / start / dispatch / find / health / metrics / version) |

## 5. Director amendments (ORDER-064)

1. **Service Lifecycle** — REGISTERED/STARTING/READY/DEGRADED/STOPPING/STOPPED/FAILED; only `READY` is routable.
2. **Capability Discovery** — services declare capabilities; `gateway.find(capability="Replay")`.
3. **Dependency Graph** — services declare dependencies; `start()` validates (missing + cycle) and brings services up in dependency order.
4. **Gateway Context** — request_id, correlation_id, principal, timestamp, versions, metadata on every request.
5. **Circuit Breaker** — per-service OPEN/HALF_OPEN/CLOSED reliability breaker, clock-injected.
6. **Service Manifest** — name, version, capabilities, dependencies, health policy, owner, description at registration.

## 6. Decisions

- **Placement** (Decision 1): `core_layer/gateway/` subpackage, not a new top-level package (Constitution Art. 11).
- **Transport** (Decision 2): in-process handlers now; HTTP / WebSocket / gRPC / IPC / remote are later, separately-authorized bindings. The Gateway is transport-independent — a `GatewayRequest` is a plain value.
- **Events**: the Gateway emits `GatewayEvent`s to an injected sink. The canonical `GATEWAY.*` `EventType`s are reserved in `data_layer/event_system/event_model.py`; a future data-layer bridge forwards `GatewayEvent → EventType.GATEWAY_*` onto the bus. This mirrors the transport deferral and preserves the layer boundary.

## 7. Hard boundary (Trading Safety)

The Gateway knows nothing of Strategy, Decision, Signal or Trading logic.
It exposes no trade/execution path and can never become a shortcut around
`RiskManager.evaluate()`. It is a **foundation module** — not wired into
`core/pipeline.py`. Any trading-capable service stays behind the existing
pipeline; that is out of Module 10's scope.

## 8. Reuse audit (Constitution Art. 11)

| Concern | Finding | Outcome |
|---|---|---|
| Circuit breaker | `core_layer/emergency/circuit_breaker.py` is a *trading* breaker (stateless ALLOW/BLOCK) | **New** service-reliability breaker (documented) |
| Health grading | `core_layer/health_monitor/health_monitor.py` grades OK/WARNING/CRITICAL | **Reused by injection** (no upward import) |
| Registry shape | `assets/asset_registry.py`, `platform_layer/platform_service/platform_registry.py` | **Pattern reused**, new service instance |
| Event vocabulary | `data_layer/event_system` EventBus | `GATEWAY.*` reserved additively; bridge deferred |
| Platform side | `platforms/*` | Client side — Gateway is the Core side; no overlap |
