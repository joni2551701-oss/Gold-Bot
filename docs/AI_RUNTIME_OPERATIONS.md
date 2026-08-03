# AI Runtime Operations (Phase 61.6: AI Operations & Reliability Foundation)

Phase 61.6 does not extend v0.4 AI Core's own capability surface
(that work — access, providers, router, cache, audit, memory,
knowledge, content — froze at the end of Phase 61.5). It makes the
existing AI Core **observable, self-aware, and resilient**: a runtime
lifecycle, a provider circuit breaker, richer metrics, a decoupled
event bus, an Owner dashboard over all of it, Owner-only alerts, and
named configuration profiles. Full reuse audit:
`docs/PHASE61_6_RUNTIME_OPERATIONS_AUDIT.md` (TASK 1).

**Strict Rules this phase operates under** (unchanged for the
lifetime of this phase, restated here for anyone reading this doc in
isolation):

1. Trading Pipeline is untouched — `core/pipeline.py`, `decision/`,
   `execution/`, `risk/`, `strategies/`, `signals/` have **zero diff**
   at the end of this phase.
2. AI still does not open trades — only explain/summarize/educate/
   analyze, exactly as `ai_layer/ai_service/interfaces.py`'s `AIAnalyzerInterface`
   already requires.
3. New code extends existing foundation (`ai/runtime/`,
   `ai/providers/`, `ai/audit/`, `platform_layer/telegram/owner/`) — no new parallel
   manager.
4. No duplicate state — provider state lives only in
   `ai_layer.ai_engine.providers.provider_manager.ProviderManager`/
   `ai_layer.ai_engine.providers.provider_health.ProviderHealthTracker`.
5. Every new function ships with tests.

## Runtime Lifecycle (TASK 2)

`ai/runtime/runtime_state.py` — `RuntimeState` enum
(`INITIALIZING`/`READY`/`BUSY`/`DEGRADED`/`FAILED`/`SHUTDOWN`) plus
`VALID_TRANSITIONS`, a transition-graph dict (`SHUTDOWN` is terminal —
`frozenset()`, no outgoing transitions). `ai/runtime/runtime_manager.py`
— `RuntimeManager`, a transition-validating state machine, same shape
`core_layer/emergency/emergency_manager.py`'s `EmergencyManager` already
established for a different domain: `transition(to_state, reason)`
rejects (returns `None`, logs a warning) rather than silently applying
an invalid transition. Defaults to `RuntimeState.READY` on
construction (not `INITIALIZING`) — a fresh `RuntimeManager()` (e.g.
inside an Owner `/runtime` command, which always constructs fresh —
see "No live shared state" below) reports a sensible default rather
than a permanently-stuck `INITIALIZING`.

## Provider Circuit Breaker (TASK 3)

`ai/providers/circuit_breaker.py` — `ProviderCircuitBreaker`,
`CircuitState` (`CLOSED`/`OPEN`/`HALF_OPEN`), `CircuitBreakerConfig`
(`failure_threshold=5`, `recovery_timeout_seconds=30`).

**Rule 4 is decisive**: the breaker introduces no third "is this
provider available" store. `CLOSED`/`OPEN`/`HALF_OPEN` are
breaker-internal bookkeeping (a failure count and the timestamp a
circuit opened, per provider name) used only to *decide* a
transition; the moment a transition happens, the breaker writes the
result into the existing `ProviderHealthTracker`:

    OPEN       -> HealthStatus.OFFLINE   (not in AVAILABLE_STATUSES -- no request reaches this provider)
    HALF_OPEN  -> HealthStatus.DEGRADED  (in AVAILABLE_STATUSES -- exactly the one probe request is allowed through)
    CLOSED     -> HealthStatus.ONLINE    (fully recovered)

**`ai/router/router.py` is not modified this phase.** "Router faqat
healthy provider ishlatadi" (the router only uses healthy providers)
already holds today, for free, because the breaker speaks the
router's existing language — proven directly in
`tests/ai/providers/test_provider_circuit_breaker.py::test_router_only_uses_healthy_providers_because_breaker_writes_into_the_same_tracker`
against a real `AIRouter`/`ProviderManager`, not a fake.

Worked example (the Director's own): Gemini times out 5 times →
`record_failure()` reaches `failure_threshold` → circuit opens →
`ProviderHealthTracker` reports OFFLINE → 30s elapse →
`allow_request()` transitions to HALF_OPEN, reports DEGRADED → the
next attempt is the one probe request → success calls
`record_success()` → CLOSED, ONLINE; failure calls `record_failure()`
→ back to OPEN, OFFLINE, and the 30s timer resets.

**Scoping decision (deliberate, not an oversight): `ai_service.py`
does not construct or call a `ProviderCircuitBreaker` internally this
phase.** `AIService.ask()`'s existing `record_provider_failure()` call
already writes an immediate, single-failure-based status into
`ProviderHealthTracker` (Phase 61.2 TASK 4); routing that through the
breaker's 5-strikes threshold instead would change already-tested,
frozen Phase 61.2 behavior — out of scope for a phase whose own Rule 3
is "extend, don't rewrite." `ProviderCircuitBreaker` is real, tested,
and integrates with Provider Health via shared state (Acceptance
Criteria: "Circuit Breaker is integrated with Provider Health" —
satisfied through `ProviderHealthTracker`, not through being called
from `ai_service.py`); a future, separately-approved phase can wire it
into `ai_service.py`'s own failure handling if the Director asks for
that specific change.

**Update (Phase 61.7):** that future phase arrived. `ProviderCircuitBreaker`
is now wired into `ai_service.py`'s real failure handling — see
`docs/PHASE61_7_RUNTIME_INTEGRATION.md`. The historical reasoning above
is kept for the record; it no longer describes current behavior.

## Runtime Metrics (TASK 4)

`ai/audit/provider_stats.py` extended in place — "Yangi emas. Mavjud
provider_stats.py kengayadi" (Not new. The existing provider_stats.py
is extended), per the Director's own instruction:

- `compute_requests_per_minute(requests, now=None)` — pure, over
  `ai_layer.ai_service.audit.request_log.AIRequestLogEntry.created_at`, same "reuse the
  already-recorded timestamp" convention `compute_provider_stats()`
  already uses for `response_log.py`.
- `RuntimeMetrics` dataclass — `requests_per_minute`, `cache_hits`,
  `cache_misses` (+ derived `cache_hit_rate`), `validation_failures`,
  `retries`, `failover_count`.
- `RuntimeMetricsCollector` — subscribes to the Event Bus (TASK 5,
  below) for `CACHE_HIT`/`CACHE_MISS`/`VALIDATION_FAILED`/
  `PROVIDER_FAILED` (counted as a retry)/`PROVIDER_CHANGED` (counted
  as a failover), accumulates in-memory counts. None of these five
  were recorded anywhere before this phase — a cache hit in
  `ai_service.py` returns before either log is ever touched.

## Runtime Event Bus (TASK 5)

`ai/runtime/event_bus.py` — genuinely new (no pub/sub mechanism
existed anywhere in `ai/`): `EventBus` (`subscribe()`/`publish()`/
`history()`), `RuntimeEvent` (`event_type`, `payload`, `occurred_at`),
`EventType`. `publish()` never raises even if a subscribed handler
does — one bad subscriber never breaks the publisher or any other
subscriber.

Nine event types (the Director's original eight, plus one addition
this same phase — see TASK 7):

    ProviderChanged, ProviderFailed, ProviderRecovered,
    CacheHit, CacheMiss, ValidationFailed,
    RuntimeStarted, RuntimeStopped, RuntimeFailed

**"Hech kim bir-birini to'g'ridan-to'g'ri chaqirmaydi"** (nobody calls
anybody directly) — publishers and subscribers never import each
other:

| Publisher | Event(s) | Where |
|---|---|---|
| `ai_service.py` | `ProviderChanged`, `CacheHit`, `CacheMiss`, `ProviderFailed` (no `circuit_state` key), `ValidationFailed` | at pre-existing control-flow points inside `ask()` — no new orchestration logic, `ask()`'s return value/timing is unchanged |
| `runtime_manager.py` | `RuntimeStarted`, `RuntimeStopped`, `RuntimeFailed` | `RuntimeManager.transition()`, one `if/elif` branch per target state |
| `circuit_breaker.py` | `ProviderFailed` (`circuit_state="OPEN"`), `ProviderRecovered` (`circuit_state="CLOSED"`) | `_open()` / `record_success()` |

| Subscriber | Listens for | Purpose |
|---|---|---|
| `RuntimeMetricsCollector` (`ai/audit/provider_stats.py`) | `CacheHit`/`CacheMiss`/`ValidationFailed`/`ProviderFailed`/`ProviderChanged` | accumulate runtime metrics |
| `RuntimeNotifier` (`platform_layer/telegram/owner/runtime_notifications.py`) | `ProviderFailed` (circuit-driven only)/`ProviderRecovered`/`RuntimeFailed` | queue Owner alerts |

`ai_service.py` never imports `provider_stats.py` or
`runtime_notifications.py`; neither of those imports `ai_service.py`.
Confirmed by `tests/ai/ -q` passing unchanged (466+ tests) after every
wiring change — the additive event-publish calls never altered
`ask()`'s existing behavior.

## Owner Runtime Dashboard (TASK 6)

`platform_layer/telegram/owner/runtime_commands.py` (new file — a genuinely distinct
concern from `dashboard.py`'s cross-cutting summary/diagnostic
functions and `ai_commands.py`'s capability/provider CRUD, matching
this codebase's established "one `*_commands.py` file per feature
area" convention):

- `/runtime` → `runtime_status()` — current `RuntimeState`, health,
  transition count.
- `/runtime_events` → `runtime_events()` — the N most recent published
  events, newest first.
- `/runtime_metrics` → `runtime_metrics()` — a `RuntimeMetrics`
  snapshot.

Wired via `platform_layer/telegram/commands.py`'s `OWNER_COMMANDS` (OWNER-only, not
dual-listed with `ADMIN_COMMANDS` — unlike the AI product-facing
commands, these expose internal runtime detail, matching `doctor`'s
own posture) and `platform_layer/telegram/handlers.py`'s `{command}_handler`
functions — no `command_router.py` change (registry-driven dispatch
via `getattr(handlers, f"{command}_handler")`, reconfirmed).

### No live shared state across Telegram commands

Every handler in this codebase constructs its service objects fresh
per call (no live shared state across Telegram commands — the same
posture `ai_cost_handler`'s own empty-dict default already
established). A `/runtime`/`/runtime_events`/`/runtime_metrics` call
with no injected `RuntimeManager`/`EventBus`/collector therefore
reports a fresh, default/empty state:

- `/runtime` — a fresh `RuntimeManager()` defaults to `READY`.
- `/runtime_events` — a fresh `EventBus()` has empty history.
- `/runtime_metrics` — a fresh `RuntimeMetricsCollector` has zero
  counts.

This is not a bug: these commands are the observability surface for
whichever `RuntimeManager`/`EventBus` a live, persistent `AIService`
instance was actually constructed with. Wiring a persistent,
process-wide `AIService` into the running bot process is out of scope
for this phase (Rule 1: no Trading Pipeline change; Rule 3: no new
orchestration) — a future phase can pass that same instance's objects
into these functions to make them reflect real, accumulated state.

## Runtime Notification Layer (TASK 7)

`platform_layer/telegram/owner/runtime_notifications.py` (new — a push-based concern,
genuinely different from every pull-based `*_commands.py` module):
`RuntimeNotifier` (an `EventBus` subscriber that queues `RuntimeAlert`s,
drained via `drain()`), `evaluate_high_cost()`/`evaluate_cache_disabled()`
(pure evaluator functions, no `EventBus`), `deliver_alerts()` (Owner-only
delivery via the existing `platform_layer.telegram.notifier.Notifier`).

Six alert conditions (the Director's own list), three sourcing
strategies:

- **Provider DOWN / Circuit OPEN** — one signal, not two. This
  codebase's circuit breaker is the thing that decides a provider is
  *truly* down (5 consecutive failures, not one attempt), so these
  collapse onto the breaker's `ProviderFailed` publish
  (`circuit_state="OPEN"`). A raw per-attempt `ai_service.py`
  `ProviderFailed` (no `circuit_state` key) is deliberately **not**
  alerted on — it fires on every failed attempt and would spam the
  Owner long before the breaker ever trips.
- **Provider RECOVERED** — the breaker's `ProviderRecovered` publish
  (`circuit_state="CLOSED"`) on `record_success()` closing from
  OPEN/HALF_OPEN.
- **Runtime FAILED** — `RuntimeManager.transition()`'s new
  `RuntimeFailed` publish (this task's one, in-place `EventType`
  addition) on any transition into `RuntimeState.FAILED`.
- **High Cost / Cache Disabled** — neither has a real, already-firing
  control-flow point anywhere in this codebase yet (no code path
  currently crosses a cost threshold or flips a cache on/off flag).
  Consistent with this codebase's "never fabricate" convention (see
  `ai_cost({})`'s honest $0.00, `doctor`'s honest "N/A" for
  Scheduler), these are pure evaluator functions instead —
  `evaluate_high_cost(provider_stats, threshold)`/
  `evaluate_cache_disabled(cache_enabled)` take real data a caller
  already has and return alerts if the condition holds, ready for a
  future phase's periodic caller.

`deliver_alerts()` resolves the Owner's chat id from
`core.secrets.Secrets().TELEGRAM_OWNER_ID` and **never falls back to
`TELEGRAM_CHAT_ID`** (the general broadcast chat) — an internal
reliability alert with no configured Owner id goes undelivered, not to
the public channel.

## Runtime Configuration Profiles (TASK 8)

`ai/runtime/runtime_profiles.py` (new file, in-place inside
`ai/runtime/` — Rule 3) — `RuntimeProfile` (pure data: `max_retries`,
`timeout_seconds`, `cache_ttl_seconds`, `validation_schema`,
`provider_priority`), three named constants
(`DEVELOPMENT_PROFILE`/`TESTING_PROFILE`/`PRODUCTION_PROFILE`),
`resolve_profile(name)`, `apply_provider_priority(candidates, priority)`.

Reuses existing types for each knob rather than inventing a parallel
representation: `cache_ttl_seconds` → `RuntimeProfile.to_cache_policy()`
returns a real `ai_layer.ai_engine.cache.cache_policy.CachePolicy`; `validation_schema`
is a real `ai_layer.confidence_ai.schemas.ResponseSchema` (already the
injectable "validation level" seam — `validate_response(result,
schema=...)`); `provider_priority` is a `Tuple[str, ...]` consumed by
`apply_provider_priority()`, which reorders whatever
`ai_layer.ai_coordinator.routing_rules.get_candidate_providers()` already returns —
never a second, competing source of candidate order.

`PRODUCTION_PROFILE` matches this codebase's own existing production
defaults exactly: `timeout_seconds=15` (the real
`gemini_provider.py`'s `_REQUEST_TIMEOUT_SECONDS`), `cache_ttl_seconds=300`
(the real `CachePolicy.default_ttl_seconds`), and requires a
`confidence` metadata key (strict validation). `TESTING_PROFILE` sets
`cache_ttl_seconds=0` — a cached response must never mask a test's own
assertion.

**`max_retries`/`timeout_seconds` have no existing injectable seam
yet** (`ai_service.py`'s own attempt count is derived from
`len(provider_manager.list_providers())`, and `gemini_provider.py`'s
timeout is a module-level constant) — carried here as plain data for a
future phase to actually thread through, not fabricated as
already-live behavior. **This phase does not wire `RuntimeProfile`
into `ai_service.py`** — the same scoping decision already made for
the circuit breaker: built real and tested, wiring deferred, so no
existing test's behavior can regress.

**Update (Phase 61.7):** `RuntimeProfile.validation_schema`,
`to_cache_policy()`, and `max_retries` are now wired into
`ai_service.py` — see `docs/PHASE61_7_RUNTIME_INTEGRATION.md`.
`timeout_seconds` alone remains unwired (still no real seam). The
historical reasoning above is kept for the record.

## Documentation (TASK 9)

This file. `docs/AI_RUNTIME_FOUNDATION.md` (Phase 61.2) and
`ai/README.md` gained pointers to this file rather than duplicating
its content — Phase 61.2's own doc describes the request lifecycle;
this doc describes the *operational* layer built on top of it this
phase.

## Acceptance Criteria (self-check against the Director's own list)

- Runtime Lifecycle works — `RuntimeManager`, 12 tests
  (`tests/ai/runtime/test_runtime_lifecycle.py`), including the new
  `RuntimeFailed` publish.
- Circuit Breaker is integrated with Provider Health — every
  transition writes into the shared `ProviderHealthTracker`; proven
  against a real `AIRouter` with zero `router.py` changes.
- No duplicate provider state — confirmed above (Rule 4).
- Runtime Metrics is built on top of existing `ProviderStats` — same
  file, same dataclass shape extended, not replaced.
- Event Bus is not connected to the Trading Pipeline — `EventBus`,
  `RuntimeEvent`, `EventType` have zero imports from `decision/`,
  `risk/`, `execution/`, `strategies/`, `signals/`, and nothing in
  those packages imports `ai/runtime/` either.
- Runtime Dashboard only reads existing services — `runtime_commands.py`
  composes `RuntimeManager`/`EventBus`/`RuntimeMetricsCollector`, never
  constructs a live `AIService` or reaches into pipeline state.
- Notification Layer is Owner-only — `deliver_alerts()` resolves
  `TELEGRAM_OWNER_ID` exclusively, never `TELEGRAM_CHAT_ID`.
- Configuration Profiles manage runtime parameters — three named
  profiles, each a real `RuntimeProfile`.
- AI is still independent of the Decision Engine — unchanged from
  every prior phase; this phase adds no new `ai/` → `decision/`
  import.
- Trading Pipeline has 0 diff — `core/pipeline.py`/`decision/`/
  `execution/`/`risk/`/`strategies/`/`signals/` untouched this phase
  (confirmed via `git diff --stat` at TASK 10).
- 2050+ tests green, GitHub Actions SUCCESS — see TASK 10's own commit
  report.

## Tests

`tests/ai/runtime/test_event_bus.py`,
`tests/ai/runtime/test_runtime_lifecycle.py`,
`tests/ai/runtime/test_runtime_profiles.py`,
`tests/ai/providers/test_provider_circuit_breaker.py`,
`tests/ai/audit/test_runtime_metrics.py`,
`tests/platform_layer/telegram/owner/test_runtime_commands.py`,
`tests/platform_layer/telegram/owner/test_runtime_notifications.py`.
