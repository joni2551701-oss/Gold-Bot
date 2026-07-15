# Pipeline Guard

Phase 60.8: Safe Integration Layer (the Director's "Official" TASK 2-5
Worker Brief). `core/guards/pipeline_guard.py`'s `PipelineGuard` is the
first real, wired connection between two foundation-only managers
built in earlier phases —
`configuration.runtime_feature_manager.RuntimeFeatureManager`
(Phase 59.7) and `core.emergency.emergency_manager.EmergencyManager`
(Phase 59.9) — and the live `core/pipeline.py`. Both managers had zero
real callers before this phase (confirmed in `docs/PHASE60_8_INTEGRATION_AUDIT.md`,
TASK 1's own reuse audit).

This is deliberately a **controlled wiring** phase, not a new-feature
phase: no business logic in `decision/`, `risk/`, `strategies/`,
`signals/`, `context/`, `ai/`, or `execution/` changed. `PipelineGuard`
only ever answers "should this stage run right now" — it never decides
BUY/SELL, never computes a confidence score, never touches SL/TP/Lot.

## Stage diagram

```
Market Data
    |
Data Quality
    |
HTF Bias
    |
Context
    |
Market Phase
    |                                    <- no guard hook here (see Disclosed Findings #1)
PipelineGuard.before_signal() ----------> [skip -> signal_candidates = []] -> cascades to
    |                                       every downstream list (quality/explainability/
Signal                                      features/ai/decision/risk/signal_history) staying
    |                                       empty, same shape as any ordinary zero-candidate cycle
Signal Quality
    |
Explainability
    |
Features
    |
PipelineGuard.before_ai() --------------> [skip -> _neutral_ai_result() substituted per
    |                                       candidate -- Decision Engine still runs normally]
AI
    |
Decision
    |
Risk
    |
Signal History (context_snapshot built here)
    |
Telegram Format
    |
PipelineGuard.before_execution() -------> [skip -> Notifier.send_messages() not called;
    |                                       telegram_messages/formatting still happens]
Telegram Delivery
    |
PipelineGuard.before_database() --------> [skip -> SignalRepository.save_signal_record()
    |                                       not called]
Database
```

`EmergencyState.KILLED` aborts at whichever of the four hooks is
checked first (`before_signal()`, the earliest) — `run()` returns
immediately via `TradingPipeline._aborted_result()`, a dict with the
exact same key set as a normal return (empty lists / `None`
`context_snapshot` for everything the abort short-circuits).

## Runtime mapping

`configuration/feature_registry.py` (Phase 60.8 additions):

| Registry name | Gates | Default | Real? |
|---|---|---|---|
| `ENABLE_SIGNALS` | `before_signal()` -> `signal` stage | `True` | Yes, `config.Config`-backed |
| `ENABLE_AI` | `before_ai()` -> `ai` stage | `True` | Yes, `config.Config`-backed |
| `ENABLE_EXECUTION` | `before_execution()` -> `telegram_delivery` stage | n/a | **No** — see Disclosed Findings |
| `ENABLE_DATABASE` | `before_database()` -> `database` stage | `True` | Yes, `config.Config`-backed |

All real gates default `True` so a process with no explicit override
reproduces exactly the pre-Phase-60.8 pipeline behavior.

## Emergency mapping

`core.emergency.emergency_state.EmergencyState` (five real values):

| State | `before_signal()` | `before_ai()` | `before_execution()` | `before_database()` |
|---|---|---|---|---|
| `NORMAL` | proceed | proceed | proceed | proceed |
| `WARNING` | proceed + `logger.warning()` | proceed + warning | proceed + warning | proceed + warning |
| `PAUSED` | proceed | proceed | **skip** | proceed |
| `MAINTENANCE` | skip | skip | skip | skip |
| `KILLED` | **abort** | abort | abort | abort |

## Guard lifecycle

One `PipelineGuard` per `TradingPipeline` instance, constructed eagerly
in `__init__` (same convention as every other pipeline dependency).
Both `RuntimeFeatureManager`/`EmergencyManager` are injectable — a test
supplies stub managers (`tests/core/guards/test_pipeline_guard.py`,
`tests/integration/test_pipeline_guard_wiring.py`) instead of touching
the real database. `TradingPipeline.__init__` also accepts an optional
`pipeline_guard=` override for the same reason — a new, backward-
compatible keyword argument, not a signature-breaking change.

Each `before_X()` call re-reads `EmergencyManager.get_status()` fresh
(a database read) — no in-process caching within a single `run()`.
Since `main.py`'s `GoldBot` runs exactly one pipeline cycle per process
invocation (confirmed in TASK 1's audit — there is no live scheduler
loop in this codebase), this is not a meaningful cost, and it means a
toggle an owner makes between two scheduled runs is always picked up
by the very next one.

## Design rationale

- **Cascading skip, not per-stage rewiring**: `before_signal()`'s skip
  produces an empty `signal_candidates` list; every downstream stage
  (`signal_quality`, `explainability`, `features`, `decision`, `risk`,
  `signal_history`) is already a list comprehension *over*
  `signal_candidates` — so skipping the one upstream list empties
  everything below it with zero additional code in any of those
  stages. This is how `MAINTENANCE` ends up skipping Signal/Decision/
  Risk without a single line of new code touching `decision/` or
  `risk/`.
- **AI skip substitutes a neutral value, not an empty list**: unlike
  `before_signal()`, `before_ai()`'s skip must NOT cascade — the
  Director's own acceptance test is "ENABLE_AI OFF -> AI skipped,
  Decision continues." `_neutral_ai_result()` (`core/pipeline.py`)
  returns `AIAnalysisResult(approved=True, confidence=0.5,
  risk_score=0.5, ...)` per candidate — the exact midpoint, matching
  this codebase's own "AI optional" architecture: AI's absence must
  never itself force a reject, and must never be worse than AI's own
  current heuristic-stub verdict (`ai/ai_analyzer.py`'s `analyze()`
  today always returns `approved=False` — a fact this phase does not
  change, only avoids making worse when AI is explicitly disabled).
- **`before_execution()` gates only delivery, not formatting**: a
  skipped execution stage still lets `telegram_format` run, so
  `result["telegram_messages"]` shows what *would* have been sent —
  useful for a future dashboard/audit view, and it costs nothing (pure
  string formatting, no side effect).

## Disclosed Findings

1. **No `before_market_data()` hook.** The Director's brief names
   exactly four methods. `market_data`, `data_quality`, `htf_bias`,
   `context`, and `market_phase` all run regardless of Emergency
   state, including under `MAINTENANCE`/`KILLED`. All five are pure,
   read-only computations with no trade/Telegram/database side effect,
   so this does not violate either state's safety intent, but it does
   mean `MAINTENANCE`'s own "Faqat Market Data ... ishga ruxsat" is not
   literally true — several read-only context stages also still run.
2. **`before_execution()` maps to `telegram_delivery`, not
   `execution/execution_engine.py`.** The pipeline has no real
   "execution" stage today (`ExecutionEngine.dispatch()` has zero real
   callers anywhere, confirmed in TASK 1's audit) — Telegram delivery
   is the only point where an actual outward effect happens, so it is
   the practical stand-in for "execution" in a bot with no live broker
   connection.
3. **Blocking, discovered during implementation — `ENABLE_EXECUTION`
   could not be promoted to a real registry entry.** This was
   attempted exactly as the brief named it, then reverted. Root cause:
   `configuration/feature_dependency_validator.py`'s `DEPENDENCY_RULES`
   already declares `"ENABLE_EXECUTION": ("ENABLE_RISK",
   "ENABLE_DECISION")` (Phase 59.6) — both of which are still
   declared-only (`implemented=False`, always `enabled=False`).
   `validate_feature_dependencies()` checks that rule against the
   *entire* registry snapshot on *every* `RuntimeFeatureManager`
   toggle attempt to *any* feature, not just to `ENABLE_EXECUTION`
   itself. With `ENABLE_EXECUTION` promoted to real and `enabled=True`,
   26 tests failed — all 18 in
   `tests/configuration/test_runtime_feature_manager.py`,
   `test_default_registry_has_no_violations`, and three
   `telegram/owner/` tests — because toggling even an unrelated
   feature like `ENABLE_NEWS` was rejected: the dry-run's hypothetical
   snapshot still carried `ENABLE_EXECUTION=True` forward against its
   permanently-unmet dependencies. The alternative (`ENABLE_EXECUTION`
   defaulting `False` instead) was rejected too — that would silently
   disable live Telegram delivery by default, a severe undisclosed
   behavior change this phase's own Acceptance Criteria explicitly
   forbid ("python main.py logi funksional jihatdan o'zgarmagan").
   **Resolution applied**: `ENABLE_EXECUTION` stays declared-only
   (unchanged from before this phase); `before_execution()` reads
   `EmergencyManager` only (`PAUSED`/`MAINTENANCE`/`KILLED` all still
   work correctly) and does not consult any runtime feature flag. The
   owner-toggleable-at-runtime half of TASK 2's brief for this one gate
   is blocked pending the Director's choice between: (a) renaming this
   gate to a name that doesn't collide with `DEPENDENCY_RULES`, (b)
   also promoting `ENABLE_RISK`/`ENABLE_DECISION` to real flags (out of
   this phase's scope), or (c) amending `DEPENDENCY_RULES` itself (also
   out of scope, and a `configuration/` semantic change, not a minimal
   diff).
4. **Constructing `PipelineGuard()` changes `main.py`'s log output
   shape.** `TradingPipeline.__init__` now always constructs a real
   `RuntimeFeatureManager` + `EmergencyManager`, each of which touches
   the database (schema init for `runtime_features`/`audit_log`/
   `config_snapshots`/`emergency_states`) on every `TradingPipeline`
   instantiation — previously this only happened when
   `persist_signals=True` constructed a `SignalRepository`. This adds
   3-4 new `DatabaseModels`-logger INFO lines (schema-init
   confirmations) compared to the pre-Phase-60.8 baseline. The 13
   `TradingPipeline`-logger `stage=X` lines themselves (what
   `tests/performance/test_pipeline_execution_time.py::test_pipeline_stage_timing_is_logged`
   actually asserts) are unchanged in count, order, and content — only
   these new, harmless, one-time-per-process schema lines are new.
5. **Learning is still not connected to live trading.** See
   `docs/LEARNING_LOOP.md`'s Phase 60.8 section — `bridge_closed_trade()`
   is now wired into `backtesting/backtest_engine.py` only, since that
   remains the one real `CLOSED`-`PaperTrade` producer in this
   codebase (`core/pipeline.py` still never constructs a `PaperTrade`).

## What this phase does NOT do

- Does not change any `decision/`, `risk/`, `strategies/`, `signals/`,
  `context/`, or `ai/` logic, threshold, or formula.
- Does not wire `execution/execution_engine.py` — it stays untouched
  and inert.
- Does not register any Telegram command (`/dashboard`, `/pause`,
  etc.) — no `telegram/command_router.py`/`telegram/handlers.py`
  change.
- Does not add owner-toggle capability for the `before_execution()`
  gate (see Disclosed Finding 3) — Emergency-state gating for that hook
  works today; runtime-feature gating for it does not yet.
