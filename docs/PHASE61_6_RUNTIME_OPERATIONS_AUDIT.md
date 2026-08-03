# Phase 61.6 — AI Operations & Reliability Foundation: Reuse Audit (TASK 1)

Per the Director's explicit brief structure and Strict Rules. This
phase does not touch the Trading Pipeline at all (Rule 1); it makes
the existing AI Core (Phase 61.0-61.5) observable, self-aware, and
resilient. Every design decision below traces back to Rule 3 (extend,
never a parallel manager) and Rule 4 (no duplicate provider state).

## `ai/runtime/`

Current contents: `ai_service.py` (`AIService.ask()`, the one real
orchestration), `runtime_request.py`/`runtime_response.py` (I/O
shapes). No lifecycle concept exists — `AIService` has no notion of
"am I ready, busy, degraded, failed, or shut down." No event
mechanism exists — every step inside `ask()` (cache hit/miss,
validation rejection, provider failure) currently only logs to
`ai/audit/request_log.py`/`response_log.py` or a plain `logger.info`
call; nothing is published anywhere a second listener could observe.

- **Missing**: a state machine for the runtime's own lifecycle; a
  decoupled event mechanism.
- **Reuse**: `ai_service.py`'s existing `ask()` control flow — the
  cache-hit branch, the `ProviderRuntimeError`/`NotImplementedError`
  except blocks, and the `validation.accepted` check are the exact,
  already-existing points where TASK 5's events naturally occur. No
  new orchestration logic is written; `ask()` gains **event
  publication calls at points that already exist**.
- **Create**: `runtime_state.py` (`RuntimeState` enum +
  `RuntimeStateRecord`), `runtime_manager.py` (`RuntimeManager`, a
  transition-validating state machine, same shape as
  `core_layer/emergency/emergency_manager.py`'s `EmergencyManager`),
  `runtime_events.py` (`RuntimeLifecycleEvent`, the record
  `RuntimeManager` appends to its own history on each transition —
  distinct from TASK 5's cross-cutting `event_bus.py`), `event_bus.py`
  (`EventBus`, `EventType`, `RuntimeEvent` — genuinely new, no
  existing pub/sub exists anywhere in `ai/`; Module Reuse Principle
  step 1/2 both "no").

## `ai/router/`

Current: `router.py` (`AIRouter.route()`, `provider_metrics()`),
`routing_rules.py`, `routing_result.py`, `provider_score.py` (Phase
61.5, analytics-only). `router.py`'s own docstring already documents
the "never influenced by metrics" invariant this phase must keep
intact.

- **Missing**: nothing new here. Circuit Breaker (TASK 3) is
  explicitly **not** a router concern per the Director's own framing
  ("Router faqat healthy provider ishlatadi" — the router already
  does this today via `ProviderHealthTracker.is_available()`; a
  breaker that also writes into `ProviderHealthTracker` needs **zero**
  change to `router.py` itself for the router to automatically respect
  it).
- **Reuse**: `router.py` is **not modified this phase** — the breaker
  writes into the same `ProviderHealthTracker` the router already
  reads, so "only healthy providers are used" falls out for free.
- **Create**: nothing in `ai/router/`.

## `ai/providers/`

Current: `provider_manager.py` (owner-intent PREFERRED/FALLBACK/
DISABLED), `provider_health.py` (`ProviderHealthTracker`, observed
ONLINE/DEGRADED/RATE_LIMITED/OFFLINE/DISABLED), `provider_status.py`
(the `HealthStatus` enum + `AVAILABLE_STATUSES`), `provider_failover.py`
(`select_available()`, a pure "first healthy candidate" walk),
`runtime_errors.py` (`ProviderRuntimeError` hierarchy +
`record_provider_failure()`), four real providers + one placeholder.

**Rule 4 is decisive here**: "Provider holati faqat ProviderManager /
ProviderHealth" — a circuit breaker must not become a third
provider-state store. `circuit_breaker.py`'s `CLOSED`/`OPEN`/
`HALF_OPEN` states are **breaker-internal bookkeeping** (failure
counts, the timestamp a circuit opened) — the moment a transition
happens, the breaker calls `ProviderHealthTracker.record()`, the
existing single source of truth: `OPEN` → `HealthStatus.OFFLINE`,
`HALF_OPEN` (the one-probe-request window) → `HealthStatus.DEGRADED`
(already in `AVAILABLE_STATUSES`, so exactly one request is allowed
through), `CLOSED` (recovered) → `HealthStatus.ONLINE`. No new
"is this provider available" boolean is ever asked anywhere except
`ProviderHealthTracker.is_available()`, unchanged.

- **Missing**: automatic OPEN→HALF_OPEN→CLOSED recovery on a
  timeout; a failure-count threshold before a provider is taken out of
  rotation (today `ProviderHealthTracker.record()` is a single
  caller-supplied status with no threshold/counting logic of its own —
  correctly so, since counting is a *policy*, and `ProviderHealthTracker`
  is deliberately just a *record*, per its own docstring).
- **Reuse**: `ProviderHealthTracker`/`HealthStatus`/
  `AVAILABLE_STATUSES` entirely unmodified; `runtime_errors.py`'s
  existing `record_provider_failure()` flow (`ProviderRuntimeError` →
  `ProviderHealthTracker`) is extended so the same call site also
  drives the breaker's failure count.
- **Create**: `circuit_breaker.py`
  (`CircuitState`/`CircuitBreakerConfig`/`ProviderCircuitBreaker`).

## `ai/audit/`

Current: `request_log.py`/`response_log.py` (in-memory attempt/outcome
logs), `provider_stats.py` (`ProviderStats`,
`compute_provider_stats()`, `rank_providers()` — Phase 61.3 TASK 9),
`trace.py` (`RequestLog`+`ResponseLog` join), `usage_accounting.py`
(per-user aggregation, Phase 61.4).

The Director's TASK 4 is explicit: "Yangi emas. Mavjud provider_stats.py
kengayadi." (Not new. The existing provider_stats.py is extended.)

- **Missing**: a requests/min rate (today's log entries have
  `created_at` but nothing computes a rolling rate from it); cache
  hit/miss counts (never recorded anywhere — a cache hit in
  `ai_service.py` returns immediately without touching
  `request_log.py`/`response_log.py` at all today); validator-failure/
  retry/failover counts (retries and failover are implicit in
  `ai_service.py`'s attempt loop, never counted).
- **Reuse**: `ProviderStats`'s existing fields (`total_calls`,
  `success_rate`, `avg_latency_ms`, `total_cost`, `failure_count`)
  cover the provider-level half of "runtime metrics" already —
  nothing there is recomputed. `AIRequestLogEntry.created_at` is
  reused directly for the requests/min calculation (a pure function
  over already-recorded timestamps, same "reuse the already-computed
  record" convention every prior `provider_stats.py`/`usage_accounting.py`
  function follows).
- **Create**: inside the **same file** (`provider_stats.py`, not a new
  module): `compute_requests_per_minute()` (pure, over
  `RequestLog.all()`), `RuntimeMetrics` dataclass, and
  `RuntimeMetricsCollector` — a small `EventBus` subscriber that
  accumulates cache-hit/miss/validation-failure/retry/failover counts
  from the four events `ai_service.py` newly publishes (TASK 5).
  Deliberately still in-memory-only, same posture as every counter in
  this package.

## `ai/cache/`

Current: `response_cache.py` (`ResponseCache`), `cache_policy.py`
(`CacheKey`/`CachePolicy`). Both already real and already used by
`ai_service.py`. No change needed to either — `ai_service.py`'s
existing `self._response_cache.get(cache_key)` call is simply the
point a `CacheHit`/`CacheMiss` event is published from, not a reason
to touch `response_cache.py` itself.

- **Missing**: nothing to build here.
- **Reuse**: both files, unmodified.
- **Create**: nothing in `ai/cache/`.

## `ai/session/`

Current: `session_manager.py` (`SessionManager`), `conversation_state.py`,
`context_window.py`. Entirely orthogonal to this phase — sessions are
a per-conversation concern (Phase 61.0 TASK 7), runtime lifecycle is a
process-wide concern. No overlap, no reuse opportunity, no change.

## `telegram/owner/`

Current relevant modules: `ai_commands.py` (Phase 61.4/61.5 — six
functions, `ai_runtime_online()`/`current_provider_for()` helpers
added Phase 61.5 Addendum), `dashboard.py` (Phase 59.8/61.5 Addendum —
`get_dashboard()`/`get_owner_summary()`/`get_doctor_report()`).

- **Missing**: `/runtime`, `/runtime_events`, `/runtime_metrics`
  commands; an Owner-facing runtime notification layer.
- **Reuse**: the exact "standalone function returning a
  `ProviderCommandResult`/`AICommandResult`, every dependency
  injectable, never raises" convention every function in both files
  already uses. `owner_handler()`/`doctor_handler()` (Phase 61.5
  Addendum) are the direct precedent for how a new `runtime_handler()`
  gets wired: `telegram/commands.py`'s `OWNER_COMMANDS` +
  `telegram/handlers.py`'s `{command}_handler`, no change to
  `command_router.py` itself (registry-driven dispatch, reconfirmed).
- **Create**: three new functions inside `dashboard.py` (or a new,
  narrowly-scoped `runtime_commands.py` if `dashboard.py` would grow
  unreasonably large — decided per Module Reuse Principle at
  implementation time) for TASK 6; a new `runtime_notifications.py`
  for TASK 7 (a genuinely different concern — proactive Telegram sends
  on an event, not a pull-based command reply, so it does not belong
  in `dashboard.py`).

## Isolation boundary (Rule 1, Rule 2)

Every module this phase touches is inside `ai/` (runtime/router/
providers/audit/cache) or `telegram/owner/` (a pure consumer of `ai/`
state, same relationship every prior phase's owner commands already
have). Confirmed via `git diff --stat` against
`core/pipeline.py`/`decision/`/`execution/`/`risk/`/`strategies/`/
`signals/` at the end of this phase (TASK 10): **zero lines changed**.
AI still never approves/rejects a trade, calls `risk.risk_manager.
RiskManager`, or triggers execution — every module added this phase
is explain/summarize/educate/analyze-shaped or pure operations
tooling (health, metrics, notifications), never a new capability that
touches a trade decision.

## Broadcast (Director's own addendum)

No `ai/content/`/`ai/broadcast_output.py` change this phase — the
Director's own instruction is explicit that Broadcast stays a
capability/interface-only concern until AI Runtime reaches production
maturity, and this phase is exactly that maturity work, not a
broadcast feature. Nothing under `ai/content/` is touched.
