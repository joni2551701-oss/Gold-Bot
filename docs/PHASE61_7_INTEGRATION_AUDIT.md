# Phase 61.7 — AI Platform Stabilization & Integration: Reuse Audit (TASK 1)

Phase 61.6 built five real, tested, but **standalone** foundation
pieces — `RuntimeManager`, `ProviderCircuitBreaker`, `EventBus`,
`RuntimeMetricsCollector`, `RuntimeProfile` — each deliberately not
wired into `ai/runtime/ai_service.py`'s own control flow, so no
existing test could regress. Phase 61.7's entire purpose is closing
that gap: making `AIService.ask()` — the one real orchestration this
whole `ai/` arc has — actually use them. No new capability, no new
top-level module beyond one small self-check utility (TASK 8).

## `ai/runtime/`

- **`RuntimeManager`** — exists (`runtime_manager.py`), defaults to
  `RuntimeState.READY`, `is_healthy()` already returns the correct
  READY/BUSY/DEGRADED-servable / FAILED/SHUTDOWN/INITIALIZING-not
  distinction. **Not used**: `AIService` has no `RuntimeManager`
  instance at all — nothing ever checks runtime health before
  processing a request.
  - **Reuse**: `is_healthy()` unchanged, called as-is.
  - **Create**: nothing new in `runtime_state.py`/`runtime_manager.py`
    itself. `ai_service.py` gains a `runtime_manager` constructor
    param (Optional, defaults to a fresh `RuntimeManager(event_bus=self._event_bus)`
    — same convention as every other Phase 61.x dependency) and one
    gate at the top of `ask()`.
  - **Interpretation note**: the Director's own flow diagram labels
    the gate "Runtime READY?" — implemented as `is_healthy()`, not a
    literal `current_state() == READY` check. A literal equality
    would reject requests while `DEGRADED`, contradicting
    `is_healthy()`'s own already-tested, already-frozen Phase 61.6
    docstring ("READY/BUSY/DEGRADED can all still serve requests").
    Reusing the existing method is the Module Reuse Principle's own
    answer here — not inventing a stricter, competing check.

- **`EventBus`** — exists, 9 event types, already published by
  `ai_service.py` (`ProviderChanged`/`CacheHit`/`CacheMiss`/
  `ProviderFailed`/`ValidationFailed`) and by `runtime_manager.py`/
  `circuit_breaker.py`. **Not used**: no event marks a request's own
  start/end — only sub-steps inside one are observable today; a
  listener cannot currently measure "how many requests total" or
  "how long did this whole request take," only cache/provider/
  validation sub-events.
  - **Reuse**: the existing four events unchanged.
  - **Create**: two new `EventType` members, `REQUEST_STARTED`/
    `REQUEST_COMPLETED` (the Director's own `AI_REQUEST_STARTED`/
    `AI_REQUEST_COMPLETED`, renamed to match this enum's existing
    un-prefixed convention — every member is domain-scoped by name
    alone, e.g. `RUNTIME_STARTED` not `AI_RUNTIME_STARTED`; no
    behavioral difference, purely a naming-convention match).

- **`RuntimeProfile`** — exists (`runtime_profiles.py`), three named
  profiles, `to_cache_policy()` already produces a real `CachePolicy`.
  **Not used**: `AIService` has no `runtime_profile` parameter at all.
  - **Reuse**: `validation_schema` plugs directly into
    `ai.validation.response_validator.validate_response(result,
    schema=...)`'s existing optional parameter — zero change to that
    function. `to_cache_policy()` plugs directly into
    `ai.cache.response_cache.ResponseCache(policy=...)`'s existing
    constructor parameter — zero change to that class.
  - **Honest gap, still not wired this phase**: `timeout_seconds` has
    no injectable seam anywhere in this codebase — every real
    provider's HTTP timeout (`gemini_provider.py`'s
    `_REQUEST_TIMEOUT_SECONDS`, and the equivalent constants in
    `openai_provider.py`/`claude_provider.py`/`grok_provider.py`) is a
    module-level constant, not a constructor/call parameter. Wiring
    it would mean changing four already-tested provider files' HTTP
    call signatures — a materially larger, riskier change than "wire
    an existing profile into `AIService`," and not required to
    satisfy this task's own Acceptance Criteria ("RuntimeProfile
    AIService bilan ishlaydi" is satisfied by validation+cache+retry
    wiring below). Documented here rather than fabricated as live.
    `max_retries` **is** wired — see below.

## `ai/providers/`

- **`ProviderCircuitBreaker`** — exists, real, tested against a real
  `AIRouter` (Phase 61.6). **Not used**: `AIService` never constructs
  or calls one — every real provider call still goes through the
  Phase 61.2 path (`record_provider_failure()` writes an immediate,
  single-failure-based `HealthStatus` with no recovery timer at all).
  A provider marked `OFFLINE` today via that path **never recovers**
  — nothing ever re-checks it.
  - **Reuse**: `ProviderHealthTracker` — the breaker writes into the
    exact same tracker instance `AIService` already owns, so
    `AIRouter.route()` (still unmodified) automatically respects
    every breaker transition, exactly as Phase 61.6 already proved.
  - **Create**: a `circuit_breaker` constructor param on `AIService`
    (Optional, defaults to a fresh `ProviderCircuitBreaker(health_tracker=self._health_tracker,
    event_bus=self._event_bus)`), and three call sites inside `ask()`:
    1. **A per-request "tick"** — before routing, call
       `allow_request(name)` for every registered provider name. This
       is the one non-obvious piece: `AIRouter.route()` only offers
       candidates `ProviderHealthTracker` already reports available,
       and `allow_request()` is the *only* code path that ever
       transitions `OPEN → HALF_OPEN` once the recovery timeout has
       elapsed. Without this tick, a tripped provider's `OFFLINE`
       status would never be re-evaluated — the router would never
       offer it as a candidate again, so `ask()` would never get a
       chance to call `allow_request()` on it, and it would stay
       `OFFLINE` forever. The tick breaks that deadlock.
    2. **A gate right before the real provider call** (after the
       cache-hit check, so a cache hit — which never touches the live
       provider — is never blocked by circuit state): `allow_request(provider_name)`;
       `False` skips straight to the next candidate.
    3. **Result recording**: `record_success()` on a validated,
       accepted response; `record_failure()` always, on any
       `ProviderRuntimeError`. The pre-existing (Phase 61.2)
       `record_provider_failure()` call now fires **only** for
       `ProviderRateLimitError`/`ProviderInvalidResponseError` — not
       for `ProviderTimeoutError`/`ProviderUnavailableError`, both of
       which already map to `HealthStatus.OFFLINE`, exactly what the
       breaker itself writes once it trips. **This is a discovered,
       intentional behavior change from the first implementation
       pass**: writing `OFFLINE` on the very first timeout (as the
       original Phase 61.2 path did, and as this task's own first
       draft kept doing unconditionally) makes the provider invisible
       to `AIRouter.route()` before the breaker can ever accumulate a
       second failure — its 5-strikes threshold could never be
       reached through real, repeated attempts, directly contradicting
       this phase's own worked example ("Gemini times out 5 times ->
       circuit opens"). Confirmed by a real integration test driving
       5 separate `AIService.ask()` calls against a provider that
       always times out and asserting the breaker (not a single
       failure) is what trips to `OPEN`.
  - **`ai/router/router.py` is not modified** — reconfirmed, same as
    Phase 61.6.

## `ai/audit/`

- **`RuntimeMetricsCollector`** — exists, subscribes to `EventBus`,
  already correctly counts cache hits/misses/validation failures/
  retries/failover **once attached to the same bus `AIService`
  publishes onto**. No code change needed in `provider_stats.py`
  itself — TASK 7's dashboard (below) is the first real caller that
  attaches one to a live `AIService`'s own event bus.

## `ai/cache/`, `ai/validation/`

Both already real, already used by `AIService`. No change to either
file — `RuntimeProfile.validation_schema`/`to_cache_policy()` are
consumed through each module's own pre-existing optional parameter.

## `ai/session/`

Unchanged, orthogonal to this phase (same finding as Phase 61.6's own
audit).

## `platform_layer/telegram/owner/`

- **`runtime_notifications.RuntimeNotifier`** — exists, subscribes to
  `PROVIDER_FAILED` (circuit-driven)/`PROVIDER_RECOVERED`/
  `RUNTIME_FAILED`. **Already correctly event-bus-driven** — no code
  change needed for TASK 6; the only reason its alerts were never
  triggered by a *real* request before now is that nothing called
  `circuit_breaker.record_failure()`/`record_success()` from a real
  `ask()` call. Once `AIService` does (TASK 3), `RuntimeNotifier`
  attached to the same bus starts receiving real alerts with zero
  changes to `runtime_notifications.py` itself — confirmed by a new
  integration test (TASK 9) that drives a real `AIService` to a
  tripped circuit and asserts a queued alert, not a fake `EventBus.publish()` call.
- **`runtime_commands.py`** — `runtime_status()`/`runtime_events()`/
  `runtime_metrics()` exist, each accepts an injected
  `RuntimeManager`/`EventBus`/`RuntimeMetricsCollector`. **Missing**:
  a single combined `/runtime_status` panel (TASK 7) showing Runtime
  State/Profile/Requests/Active Provider/Circuit/Validation/Cache/
  Failover/Events together — today's three commands are separate,
  narrower views. **Create**: one new function, `runtime_full_status()`,
  inside `runtime_commands.py` (extending the existing file, not a
  new one — it already owns this exact "compose Runtime* objects into
  an Owner panel" responsibility).
- **`ai/runtime/self_check.py`** — genuinely new (TASK 8): nothing in
  this codebase today runs a single "is everything actually
  reachable" sweep across Provider/Runtime/Validation/Cache/Audit/
  EventBus/CircuitBreaker. `platform_layer/telegram/owner/dashboard.py`'s
  `get_doctor_report()` (Phase 61.5 Addendum) is the closest
  precedent (nine independently-wrapped subsystem checks) but is a
  whole-bot check (Database/Telegram/Market Data/...), not AI-runtime-
  specific — this is a narrower, AI-only version of that same idea,
  reusing its "each check independently wrapped, PASS/WARNING/FAILED
  never a raised exception" posture rather than inventing a new
  result shape.

## Isolation boundary (Rule 1, Rule 2, Rule 3)

Every change this phase touches is inside `ai/runtime/`,
`ai/providers/circuit_breaker.py` (already Phase 61.6's own file,
extended in place — no new file), and `platform_layer/telegram/owner/`. No new
top-level package. `core/pipeline.py`/`decision/`/`execution/`/
`risk/`/`strategies/`/`signals/`: zero diff, confirmed at TASK 10.
`AIRouter.route()`'s own routing logic: zero diff — every integration
above works by writing into the same `ProviderHealthTracker` the
router already reads, or by composing already-existing optional
parameters (`validate_response(schema=...)`,
`ResponseCache(policy=...)`), never by changing what the router
decides or how it decides it.
