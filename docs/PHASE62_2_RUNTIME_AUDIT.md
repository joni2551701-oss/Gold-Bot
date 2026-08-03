# Phase 62.2 — AI Runtime Integration Completion & Production Wiring: Audit

**TASK 0/1 combined** (Constitution Compliance Audit + AI Runtime
Integration Audit). Read before any code change, per this phase's own
mandatory rule and `docs/constitution/CONSTITUTION.md`'s own mandatory
reading order.

## Constitution compliance check

| Rule | Status | Evidence |
|---|---|---|
| Dependency Law (Article 2) | Holds | `ai/runtime/`, `ai/providers/` import only `ai/*`/`core/*`; no upward import introduced by this audit's planned changes |
| Import Rules (Article 3) | Holds | `grep -rn "^from decision\|^from risk\|^from execution" ai/` → zero results (re-verified this phase, see Final Audit below) |
| Reuse Principle (Article 7) | Directly shapes this plan | See "What already exists" below — every TASK in the brief is checked against real code before any new file/function is proposed |
| AI Isolation Rule | Holds | `ai/runtime/ai_service.py`'s own docstring already states this; unchanged this phase |
| Trading Core Independence | Holds | No planned change touches `decision/`, `risk/`, `execution/`, `strategies/` |

## What already exists (Phase 61.6/61.7) — do not rebuild

The brief's TASK 2/3/4/6 describe a target flow that **Phase 61.7
already built and shipped**, real and tested (`ai/runtime/ai_service.py`,
2166 passing tests, `docs/PHASE61_7_FREEZE.md`). Re-reading the brief
against the real file line by line:

- **Canonical flow** (TASK 2) — `AIService._execute()` already runs:
  Runtime health → Access → Capability → prompt resolution → circuit
  sync → **loop**(route → cache lookup → circuit breaker gate →
  provider call → validation → audit(`response_log`) → cache save) →
  response. This is the brief's own listed sequence, in a functionally
  equivalent order (Runtime State is checked first rather than after
  Permission/Capability — a deliberate fail-fast ordering, not a gap;
  changing it would be a cosmetic reorder with no behavior difference,
  which `CLAUDE.md`'s "no unnecessary refactor" rule argues against).
  **No rebuild needed.**
- **Runtime Lifecycle Connection** (TASK 3) — `_execute()`'s first
  line already is `if not self._runtime_manager.is_healthy(): return
  RuntimeResponse(accepted=False, ...)`, and `ask()`'s wrapper already
  publishes `EventType.REQUEST_FAILED` for any rejected response,
  including this one. **Real gap found**: this early-rejection path
  never calls `self._request_log.record()`/`self._response_log.record()`
  — every other rejection/success path in `_execute()` does. A
  request rejected because the runtime is `FAILED` today leaves **no
  audit trail** at all. This is the one concrete, addressable gap in
  TASK 3.
- **Circuit Breaker** (TASK 4) — `_sync_circuit_breakers()`,
  `allow_request()`/`record_success()`/`record_failure()` around the
  real provider call, writing only into the shared
  `ProviderHealthTracker` (no second state store) — all real,
  unchanged, already exactly what TASK 4 asks for. **No new code
  needed**, only verification (done — see Final Audit).
- **Runtime Events** (TASK 6) — `EventType` already has 15 members
  including `REQUEST_STARTED`/`REQUEST_COMPLETED`/`REQUEST_FAILED`
  (the brief's `AI_REQUEST_STARTED/COMPLETED/FAILED`, renamed to this
  enum's existing un-prefixed convention — see `event_bus.py`'s own
  docstring) and `PROVIDER_RECOVERED`. **Real gap found**: no event
  distinguishes a timeout specifically from any other provider
  failure — `PROVIDER_FAILED`'s payload carries `reason` as free text
  (e.g. `"request timed out"`) but no structured `error_type`. The
  brief's `PROVIDER_TIMEOUT` is addressed the same way this codebase
  already resolved the identical question for `ProviderDown` (see
  `circuit_breaker.py`'s own docstring): reuse `PROVIDER_FAILED`,
  add a distinguishing payload key (`error_type`), not a new
  `EventType` member — consistent with Rule 5 (extend in place) and
  avoids a fourth near-duplicate "provider went wrong" signal.

## Real gaps this phase actually closes

1. **TASK 3** — audit-log the runtime-unhealthy rejection path
   specifically (the one path with zero audit trail today). Scope: only
   this path — the pre-existing access-denied/capability-disabled/
   no-prompt rejections are a separate, already-existing design and
   out of this phase's asked-for scope.
2. **TASK 5** — no backoff wait exists between same-request retry
   attempts today (`_execute()`'s loop fails over to the next provider
   immediately, no delay). Add an injectable exponential backoff
   (`2 ** attempt` seconds, matching `data_layer/providers/twelve_data_client.py`'s
   own already-established formula — Reuse Principle: reuse the
   existing formula, do not invent a new one), gated by
   `RuntimeProfile.max_retries` (already the attempt-count knob, no
   new field). Sleep function itself is injectable (defaults to
   `time.sleep`) so tests never actually block.
3. **TASK 6** — add `error_type` to `PROVIDER_FAILED`'s payload
   (`"TIMEOUT"`/`"RATE_LIMIT"`/`"INVALID_RESPONSE"`/`"UNAVAILABLE"`),
   derived from the already-existing `_ERROR_HEALTH_STATUS` mapping in
   `ai/providers/runtime_errors.py` — no new event type.
4. **TASK 7** — `/runtime_restart` and `/runtime_provider` do not
   exist. Genuinely new, added to the existing
   `platform_layer/telegram/owner/runtime_commands.py` (extend in place, not a new
   file — Article 7).
5. **TASK 8** — no daily token/cost limit exists anywhere.
   `ai/access/usage_limits.py`'s `UsageLimiter` tracks per-role daily
   **call count** only; `ai/audit/provider_stats.py` computes cost
   from history but nothing reads it back to gate anything (documented
   as "observability only" in that file's own docstring — this phase
   is the first to actually consume it for a decision). Genuinely new:
   a small cost-threshold check that, on breach, calls
   `RuntimeManager.transition(RuntimeState.DEGRADED, ...)` and queues
   an Owner alert via the existing `RuntimeNotifier` pattern.

## Duplicate logic / unused foundation / circular import risk — none found

- No duplicate logic identified — every genuine gap above extends an
  existing file in place.
- No unused foundation piece found beyond what `docs/PHASE61_7_FREEZE.md`
  already honestly listed (`RuntimeProfile.timeout_seconds` still not
  wired — real provider still has no injectable per-call timeout seam;
  out of this phase's scope, unchanged).
- No circular import risk introduced — all five real gaps above extend
  existing `ai/runtime/`, `ai/providers/`, `platform_layer/telegram/owner/` files
  using imports those files (or their siblings) already have.

## Plan for this phase (scope discipline)

Only the five real gaps above are implemented. TASK 2/4's "canonical
flow"/"circuit breaker real integration" are **verified, not
rewritten** — Constitution Article 7 and `CLAUDE.md`'s "no unnecessary
refactor" rule both argue against re-deriving working, tested code to
match brief prose that already describes it.
