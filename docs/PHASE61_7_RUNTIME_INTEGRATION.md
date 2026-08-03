# Phase 61.7 — AI Platform Stabilization & Integration

Not a new capability phase. Phase 61.0–61.6 built the AI Core's
individual foundation pieces — access control, providers, router,
cache, audit, memory, knowledge, runtime lifecycle, a circuit breaker,
runtime metrics, an event bus, configuration profiles — each real and
tested in isolation, several deliberately left **unwired** into
`ai/runtime/ai_service.py`'s own control flow so no existing test
could regress. Phase 61.7 closes that gap: `AIService.ask()` becomes
the single orchestration point that actually uses all of them
together. Full reuse audit: `docs/PHASE61_7_INTEGRATION_AUDIT.md`.

## What changed

`ai/runtime/ai_service.py`:

- **`RuntimeManager` integration** — `ask()`'s first action is a
  runtime-health gate (`is_healthy()`); an unhealthy runtime rejects
  before touching access control, capability checks, or any provider.
- **`ProviderCircuitBreaker` integration** — every real provider call
  is gated by `allow_request()` and followed by `record_success()`/
  `record_failure()`. A per-request "tick" (`_sync_circuit_breakers()`)
  gives a tripped breaker a chance to move `OPEN → HALF_OPEN` once its
  recovery timeout elapses, before routing — without it, a provider
  `AIRouter.route()` stops offering would never be reconsidered.
- **`RuntimeProfile` integration** — `validate_response()`'s existing
  `schema` parameter and `ResponseCache`'s existing `policy` parameter
  are both driven by an injected profile's `validation_schema`/
  `to_cache_policy()`; the per-request attempt budget is capped by
  `profile.max_retries`. `None` (no profile) reproduces exactly Phase
  61.6's behavior.
- **`EventBus` integration** — `ask()` publishes `RequestStarted`/
  `RequestCompleted`/`RequestFailed` bracketing its own body, plus
  `RetryStarted`/`RetryCompleted` around every attempt after the
  first. The four Phase 61.6 events (`CacheHit`/`CacheMiss`/
  `ProviderFailed`/`ValidationFailed`) are unchanged.
- **A discovered, intentional behavior change** — `record_provider_failure()`
  (Phase 61.2's immediate single-failure health write) now fires only
  for `ProviderRateLimitError`/`ProviderInvalidResponseError`, not for
  `ProviderTimeoutError`/`ProviderUnavailableError`. Both of the
  latter already map to `HealthStatus.OFFLINE` — writing that on the
  very first failure would make the provider invisible to
  `AIRouter.route()` before the breaker could ever accumulate a
  second failure, so its 5-strikes threshold could never be reached
  through real, repeated usage. This was found by writing an
  integration test that drives five separate `ask()` calls and
  asserting the breaker (not a single failure) trips the circuit —
  see `tests/ai/runtime/test_ai_service.py`'s own updated tests for
  the before/after.
- **A second discovered fix, same root cause** — once a single
  failure no longer marks a provider unavailable, `AIRouter.route()`
  (unmodified) would keep re-offering the same just-failed provider
  as "best" for the rest of that same request, since nothing in the
  tracker changed. `_AttemptScopedHealthTracker` (a small, local,
  read-only view — introduces no new provider-state store, Rule 4)
  additionally treats provider names already attempted *this call* as
  unavailable, used only for retry attempts within one `ask()` call.
  `AIRouter.route()`'s own selection logic is completely untouched —
  this only changes which health signal one specific retry call reads.

`ai/runtime/event_bus.py` — five new `EventType` members:
`RequestFailed`, `RuntimeStateChanged`, `RetryStarted`,
`RetryCompleted` (this phase), plus `RequestStarted`/`RequestCompleted`
(also this phase, TASK 5). `RuntimeManager.transition()` now
additionally publishes `RuntimeStateChanged` unconditionally on every
valid transition, alongside its existing specific
`RuntimeStarted`/`RuntimeStopped`/`RuntimeFailed` publishes.

`ai/runtime/self_check.py` (new) — `run_self_check()`, seven
independently-wrapped checks (Provider/Runtime/Validation/Cache/
Audit/EventBus/CircuitBreaker), each `PASS`/`WARNING`/`FAILED`, never
raises.

`platform_layer/telegram/owner/runtime_commands.py` — two new functions:
`runtime_full_status()` (`/runtime_status`, one combined panel over
state/profile/providers/circuit/validation/cache/failover/events) and
`runtime_check()` (`/runtime_check`, formats a `RuntimeSelfCheckReport`).

## Acceptance Criteria — self-check

- ✅ Trading Pipeline untouched — `git diff --stat` against
  `core/pipeline.py`/`decision/`/`execution/`/`risk/`/`strategies/`/
  `signals/` is empty.
- ✅ Decision Engine untouched — no new `ai/` → `decision/` import
  anywhere (grep confirms zero, this phase or any prior one).
- ✅ `AIRouter.route()`'s own selection logic unchanged — `router.py`
  has zero diff this phase; `_route()`'s retry path only changes
  which `health_tracker` a freshly-constructed `AIRouter` instance
  reads, never `route()`'s own code.
- ✅ `RuntimeManager` used by `AIService` — the health gate at the top
  of every `ask()` call.
- ✅ `ProviderCircuitBreaker` used by `AIService` — gate + record calls
  around every real provider attempt.
- ✅ `RuntimeProfile` used by `AIService` — validation schema, cache
  policy, and max-retries all driven by an injected profile when one
  is supplied; proven by dedicated tests for all three named profiles.
- ✅ `EventBus` really used — nine event types published from real
  control-flow points across `ai_service.py`/`runtime_manager.py`/
  `circuit_breaker.py`.
- ✅ Owner Runtime Dashboard works — `/runtime_status` reads only
  already-existing services (`RuntimeManager`/`RuntimeProfile`/
  `RuntimeMetricsCollector`/`EventBus`/`ProviderCircuitBreaker`/
  `ProviderManager`/`ProviderHealthTracker`), never constructs a live
  `AIService`.
- ✅ Runtime Self Check works — `/runtime_check`, seven checks, never
  raises.
- ✅ 2166 tests green (target: 2100+).
- ✅ Working tree clean at commit time (Commit Protocol, below).

## Final Audit (per the Director's own five-point checklist)

1. **`ai/` → `decision/`/`risk/`/`execution/`/`strategies/`/`signals/`
   dependency count == 0** for `decision/`/`risk/`/`execution/`/
   `strategies/` (confirmed by grep, zero results). `signals/` has
   seven pre-existing, unchanged-this-phase, type-import-only sites
   (`SignalCandidate`/`SignalType`/`SignalExplanation`/`SignalSchema`)
   already documented since Phase 61.0's own audit — none import
   `decision/`/`risk/`/`execution/`.
2. **Router → Provider → Validator → Audit → Cache → Events sequence**
   — documented in full in `docs/AI_RUNTIME_FLOW.md`.
3. **Circuit Breaker / ProviderHealth / RuntimeState responsibilities**
   — `ai/providers/circuit_breaker.py`'s own docstring states it
   plainly: breaker-internal bookkeeping (failure counts, `opened_at`)
   decides a transition; `ProviderHealthTracker` is the one place that
   transition's *result* is recorded (`OPEN→OFFLINE`,
   `HALF_OPEN→DEGRADED`, `CLOSED→ONLINE`); `RuntimeState`
   (`ai/runtime/runtime_state.py`) is a third, unrelated concern
   entirely — the AI *runtime process's own* lifecycle
   (INITIALIZING/READY/BUSY/DEGRADED/FAILED/SHUTDOWN), not a
   per-provider concept at all. No naming collision, no logic reuse
   between the three, confirmed distinct in `docs/PHASE61_6_RUNTIME_OPERATIONS_AUDIT.md`
   and re-confirmed here.
4. **Provider API key sourcing** — `grep -rn "os.getenv\|os.environ" ai/`
   returns zero results; every secret read goes through
   `core/secrets.py`'s own `Secrets.get()`/`get_optional()`.
5. **RuntimeProfile real-usage proof** — three dedicated tests
   (`test_development_profile_is_actually_used_...`,
   `test_testing_profile_is_actually_used_...`,
   `test_production_profile_is_actually_used_...` in
   `tests/ai/runtime/test_ai_service_integration.py`) each construct a
   real `AIService` with a named profile and assert the profile's own
   effect (cache TTL, disabled caching, strict validation) actually
   happened, not merely that the profile object exists.
