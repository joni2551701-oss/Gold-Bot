# AI Runtime Flow (Phase 61.7)

The complete, real `AIService.ask()` request flow, as actually
implemented in `ai/runtime/ai_service.py`, after Phase 61.7's
integration work. Every step below is a real code path, not aspirational.

```
Request
  │
  ▼
Runtime State  ────────────── RuntimeManager.is_healthy() ── unhealthy → RuntimeUnavailable
  │ healthy
  ▼
Permission ─────────────────── AccessControl.is_allowed() ── denied → Rejected
  │ allowed
  ▼
Capability ─────────────────── CapabilityManager.is_enabled() ── disabled → Rejected
  │ enabled + has a runtime method mapping + a prompt is resolvable
  ▼
┌─── per attempt, up to max_attempts (bounded by provider count, ─┐
│    further capped by RuntimeProfile.max_retries if one is set)  │
│                                                                   │
│  Router ──────────────── AIRouter.route() (or, for a retry,      │
│                           a scoped view excluding already-        │
│                           attempted names this call only)         │
│    │ provider selected                                            │
│    ▼                                                              │
│  Cache (read) ────────── ResponseCache.get() ── hit → Response    │
│                                                   (bypasses        │
│                                                    Circuit Breaker │
│                                                    entirely --     │
│                                                    no live call)   │
│    │ miss                                                         │
│    ▼                                                              │
│  Circuit Breaker ──────── ProviderCircuitBreaker.allow_request()  │
│    │ allowed                          │ denied (OPEN, still       │
│    ▼                                  │ within recovery window)   │
│  Provider (real call) ◄───────────────┘ skip to next attempt      │
│    │                                                               │
│    ├── ProviderRuntimeError → record_failure() [+ record_provider_│
│    │   failure() for RateLimit/InvalidResponse only] → next       │
│    │   attempt                                                    │
│    ├── NotImplementedError → next attempt (not a real failure)    │
│    ▼                                                               │
│  Validator ────────────── validate_response(schema=RuntimeProfile.│
│                            validation_schema if a profile is set) │
│    │ rejected → Rejected (returns here, does not retry)           │
│    ▼ accepted                                                      │
│  Cache (write) ─────────── ResponseCache.put()                     │
│    │                                                                │
│  Audit ───────────────────  ResponseLog.record(status=SUCCESS)     │
│    │                                                                │
│  Circuit Breaker ─────────  record_success()                       │
│    │                                                                │
└────┼────────────────────────────────────────────────────────────┘
     ▼
Events ───────────────────── EventBus.publish(RequestCompleted)
     │                       (+ RequestFailed if not accepted)
     ▼
Response
```

## Event publication points (not a separate pass — inline at the points above)

| Point in the flow | Event(s) |
|---|---|
| `ask()` entry, before `_execute()` | `RequestStarted` |
| Router selects a different provider than the previous attempt | `ProviderChanged` |
| A retry attempt begins (2nd+ provider tried this call) | `RetryStarted` |
| Cache hit | `CacheHit` |
| Cache miss | `CacheMiss` |
| `ProviderRuntimeError` caught | `ProviderFailed`; `RetryCompleted` (`success=False`) if this was a retry |
| Validation rejects the response | `ValidationFailed`; `RetryCompleted` (`success=False`) if this was a retry |
| Validated response accepted | `RetryCompleted` (`success=True`) if this was a retry |
| `ask()` returns, after `_execute()` | `RequestCompleted`; `RequestFailed` too if `not accepted` |
| `ProviderCircuitBreaker` opens (5th consecutive failure) | `ProviderFailed` (`circuit_state="OPEN"`) |
| `ProviderCircuitBreaker` closes (recovery probe succeeds) | `ProviderRecovered` (`circuit_state="CLOSED"`) |
| `RuntimeManager.transition()`, any valid transition | `RuntimeStateChanged` (always) + one of `RuntimeStarted`/`RuntimeStopped`/`RuntimeFailed` (target-state-specific) |

Nobody calls anybody directly — every row above is a `EventBus.publish()`
call; a subscriber (`RuntimeMetricsCollector`, `RuntimeNotifier`) never
appears anywhere in `ai_service.py`, `runtime_manager.py`, or
`circuit_breaker.py`'s own imports.

## Where Router/Provider/Validator/Audit/Cache/Events responsibilities live

| Concern | Module | Owns |
|---|---|---|
| Router | `ai/router/router.py` | Which provider is best for a capability, given declared candidate order + capability-matrix support + `ProviderManager` status + `ProviderHealthTracker` availability. **Unmodified this phase.** |
| Provider | `ai/providers/*_provider.py` | The real HTTP call to one AI vendor. Only ever invoked via `ProviderManager.get_provider()`, only ever called from `ai_service.py` — confirmed by `grep -rn "\.get_provider(" --include="*.py"` outside `tests/`, one result. |
| Circuit Breaker | `ai/providers/circuit_breaker.py` | Per-provider CLOSED/OPEN/HALF_OPEN bookkeeping; writes transitions into `ProviderHealthTracker`, never a second state store. |
| Validator | `ai/validation/response_validator.py` | Structural + safety checks on a `ProviderResult`, against an optional `ResponseSchema` (a `RuntimeProfile`'s `validation_schema` when one is set). |
| Audit | `ai/audit/request_log.py` / `response_log.py` | Every attempt, success or failure, logged with no API key ever present. |
| Cache | `ai/cache/response_cache.py` / `cache_policy.py` | Snapshot-scoped, role-scoped, TTL-bounded response reuse. |
| Events | `ai/runtime/event_bus.py` | Decoupled pub/sub — publishers and subscribers never import each other. |
| Runtime Lifecycle | `ai/runtime/runtime_manager.py` / `runtime_state.py` | The AI runtime *process's own* health (INITIALIZING/READY/BUSY/DEGRADED/FAILED/SHUTDOWN) — unrelated to any single provider's health. |
