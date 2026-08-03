# Phase 60.8 — Safe Integration Layer: TASK 1 Reuse Audit

No code was written for this document — per the Director's own TASK 1
instruction ("Hech qanday kod yozilmaydi"), this is read-only analysis
of `core/pipeline.py`, `decision/`, `risk/`, `execution/`, `telegram/`,
`configuration/runtime_feature_manager.py`,
`core_layer/emergency/emergency_manager.py`,
`database/learning_repository.py` (+ `learning/trade_event_bridge.py`),
and `backtesting/replay_engine.py` (+ `backtesting/data_feed.py`).

## Method

Every module below was read in full, plus a full-codebase grep for its
own real call sites (not just its own definition), to separate "this
class exists" from "this class is actually constructed/called
somewhere live."

## Per-module findings

### `core/pipeline.py`

**Current Hook Points**: none. `TradingPipeline.run()` is one linear,
synchronous method with 13 named stages (`market_data`, `data_quality`,
`htf_bias`, `context`, `market_phase`, `signal`, `signal_quality`,
`explainability`, `features`, `ai`, `decision`, `risk`,
`signal_history`, `telegram_format`, `telegram_delivery`, `database`),
each already bounded by a `t0 = time.perf_counter()` / `self._log_stage(...)`
pair (Phase 53). No `RuntimeFeatureManager`, `EmergencyManager`, or any
`configuration/`/`core_layer/emergency/` import exists in this file today —
confirmed by grep, and by both managers' own docstrings ("nothing in
`core/pipeline.py` ... reads this module").

**Safe Extension Points**: the existing per-stage boundaries
(`t0 = ...` / `self._log_stage(...)` pairs) are already a clean seam —
a guard check inserted immediately before a stage's own code, deciding
only "run" vs "skip," fits this shape without touching what any stage
computes.

**Unsafe Points**: the body of any stage — `DecisionEngine.evaluate()`'s
weighted-confidence formula, `RiskManager.evaluate()`'s geometry/sizing
checks, `SignalEngine.generate_signals()`'s strategy dispatch — must
never be reached by a guard's own logic. A guard may only wrap a stage
call, never rewrite one.

**Recommended Integration Points**: a new, thin `PipelineGuard`
(TASK 2/3) constructed once in `TradingPipeline.__init__` and called at
stage boundaries, mirroring `_log_stage()`'s own "one line before, one
line after, no side effect on the stage itself" shape.

---

### `decision_layer/decision_engine/decision_engine.py`, `risk_layer/risk_engine/risk_manager.py`

Both are pure, stateless, dependency-free calculation classes (no
`database/`, `configuration/`, `core_layer/emergency/`, or `telegram/`
import in either file). `RiskManager.evaluate()` remains the single
hard safety gate every `TradeDecision` passes through before
Telegram/persistence eligibility.

**Current Hook Points / Safe Extension Points**: none, and none are
being proposed — TASK 2/3's own brief correctly never touches this
directory, which this audit confirms is the right call: there is no
seam here a runtime toggle or emergency state should touch without
becoming a second, competing decision authority.

**Unsafe Points**: `DecisionConfig`/`DecisionWeights`'s threshold and
weight constants, `RiskConfig`'s sizing constants, `validate_geometry()`,
`calculate_position_size()` — all out of scope, matching CLAUDE.md's
Trading Safety rules verbatim.

---

### `execution_layer/execution_engine/execution_engine.py`

`ExecutionEngine.dispatch()` always returns
`ExecutionResult(dispatched=False, reason="Not implemented")` and has
**zero real call sites** anywhere in the live codebase (grep across
non-doc `*.py` files: only its own definition and
`execution/simulator/models.py`, an unrelated dataclass, match).

**Current Hook Points**: none exist because nothing calls this class.

**Recommended Integration Points**: none for Phase 60.8. Wiring
`ExecutionEngine` up is explicitly its own, separately-approvable
change per CLAUDE.md ("execution/ is intentionally inert ... wiring it
up is itself a change requiring explicit approval, not a routine
addition") — out of scope for this phase's "Safe Integration," not an
oversight.

---

### `telegram/`

`telegram/owner/*.py` (18 modules) are uniformly "real function, not
live-wired": every one composes already-tested logic and returns a
`ProviderCommandResult`, and none is imported by
`telegram/command_router.py`, `telegram/handlers.py`, or
`telegram/commands.py` (confirmed by the same posture disclosed in
each module's own docstring, e.g. `emergency_commands.py`: "NOT
registered into telegram/commands.py, NOT called from
telegram/command_router.py or telegram/handlers.py").

`telegram/owner/dashboard.py`'s `get_dashboard()` today composes
exactly three sections: `status_commands.get_system_status()`,
`control_commands.get_feature_states()`,
`provider_commands.list_providers()`. It does not yet surface
Emergency state, Replay session state, Learning stats, or Performance
metrics.

**Safe Extension Points**: `dashboard.py` itself — adding more
`sections.append(...)` calls that compose
`emergency_commands.get_emergency_status()`,
`replay_commands.*`, `learning_commands.*`, `performance_commands.*`
(TASK 6) stays entirely inside `telegram/owner/`, the same pattern
already used for its three existing sections. No `handlers.py`/
`command_router.py` touch needed or proposed.

**Unsafe Points**: registering any of this into
`telegram/command_router.py`/`telegram/handlers.py` — out of scope,
not requested by TASK 6 ("Telegram handlerga ulanmaydi").

---

### `configuration/runtime_feature_manager.py`

Fully built (Phase 59.7): `status()`/`get_feature_state()` are
read-only cache reads; `enable()`/`disable()`/`toggle()` are the only
mutating methods. **Zero callers outside its own tests,
`telegram/owner/control_commands.py`/`feature_commands.py`, and
`configuration/runtime_api.py`** — confirmed by grep for
`RuntimeFeatureManager()`. `core/pipeline.py` and `main.py` never
construct one.

**Safe Extension Points**: `PipelineGuard` constructing one instance
and calling only `status(name)`/`get_feature_state(name)` (read-only,
non-mutating) per stage.

**Gap found, not assumed away**: `configuration/feature_registry.py`'s
current registry has no name that maps 1:1 onto "should stage X run" —
the closest is `enable_ai` (`FeatureFlags.enable_ai`, currently
documented as "Reserved ... `ai/ai_analyzer.py` stays a heuristic stub
regardless"). None of `before_signal`/`before_ai`/`before_execution`/
`before_database` (TASK 2's own named hook points) has an existing,
real registry entry it would naturally read. This needs an explicit
mapping decision before TASK 2 can be implemented — see "Open
Questions" below.

---

### `core_layer/emergency/emergency_manager.py`

Fully built (Phase 59.9): `get_status()` is read-only.
**Zero callers outside its own tests and
`telegram/owner/emergency_commands.py`** — confirmed by grep for
`EmergencyManager()`. Not read by `core/pipeline.py`, `decision/`,
`risk/`, or `execution/` today (confirmed by its own docstring).

**Safe Extension Points**: `PipelineGuard` calling
`EmergencyManager().get_status()` (read-only) per cycle or per stage.

**Gap found, not assumed away**: `EmergencyState` has **five** values
(`NORMAL`, `WARNING`, `PAUSED`, `KILLED`, `MAINTENANCE`), but the
Director's TASK 3 brief maps only three
(`NORMAL`→continue, `PAUSED`→skip execution, `KILLED`→abort pipeline).
`WARNING` (a circuit-breaker advisory state, no action taken yet per
its own docstring) and `MAINTENANCE` (an owner-initiated planned
window) have no assigned behavior in the brief. Guessing either
mapping silently risks exactly the kind of unapproved trading-safety
judgment call this phase is designed to avoid — flagged for the
Director's explicit decision.

---

### `database/learning_repository.py` / `learning/trade_event_bridge.py`

`LearningRepository.record()` has **exactly one caller in the entire
codebase**: `trade_event_bridge.bridge_closed_trade()` (Phase 60.7,
TASK 2). `bridge_closed_trade()` itself has **zero callers anywhere** —
built and tested in isolation as pure foundation, exactly as Phase
60.7's own docstring discloses.

**The deeper finding**: `core/pipeline.py` never constructs a
`PaperTrade` at all (re-confirmed this audit, same result as Phase
60.7 TASK 1). There is **no live monitor loop** anywhere in this
codebase — `lifecycle/README.md`'s own "Future Roadmap" already
disclosed this as unbuilt. The **only** place a `PaperTrade` ever
actually reaches `TradeState.CLOSED` today is
`backtesting/backtest_engine.py`'s `_process_candidate()`, via
`check_paper_trade_against_candles()`.

**Safe Extension Points**: `BacktestEngine._process_candidate()`,
immediately after `paper_trade` is reassigned from
`check_paper_trade_against_candles(...).trade` — gated on
`paper_trade.status == TradeState.CLOSED` — call
`trade_event_bridge.bridge_closed_trade(paper_trade, ..., learning_repository=...)`.
This confines TASK 4 entirely to `backtesting/` (already a
foundation-only package) — **no `core/pipeline.py` touch is needed or
proposed for TASK 4**, because there is no live `PaperTrade` producer
for it to hook into yet.

**Gap found, not assumed away**: TASK 4's brief phrasing ("PaperTrade:
CLOSED bo'lsa LearningRepository.record() chaqiriladi") reads as if a
live monitor loop already exists to hook into. It doesn't. Implementing
TASK 4 against the real codebase means wiring it into
`BacktestEngine` only — Learning will start accumulating real records
from every future backtest run, but will still record **nothing** from
live trading until a separate, future, explicitly-approved live
monitor-loop phase exists. This must be stated plainly in the TASK 4
report, not silently reinterpreted as "wired into production."

---

### `backtesting/replay_engine.py` / `backtesting/data_feed.py`

`ReplayDataFeed(IDataFeed)` is real and is the only feed
`BacktestEngine` uses (`self.data_feed = ReplayDataFeed(self.replay_engine.feed)`).

`LiveDataFeed(IDataFeed)` is fully implemented (wraps
`MarketDataNormalizer.get_candles()` — "no new fetch logic," per its
own docstring) but has **zero real call sites** anywhere except its
own test file (`tests/backtesting/test_data_feed.py`). `core/pipeline.py`'s
live `market_data` stage still calls
`self.data_normalizer.get_candles(self.symbol, self.interval, self.outputsize)`
directly — it does not go through `IDataFeed` at all.

A full-codebase grep for `if.*replay`/`if.*backtest` (case-insensitive)
found **no leftover `if replay: ... else: ...` branching** anywhere —
that half of TASK 5 is already clean; there is nothing to remove.

**Current Hook Points**: `TradingPipeline.__init__` (where
`self.data_normalizer = MarketDataNormalizer()` is constructed) and the
one call site in `run()` (`market_data` stage).

**Gap found, not assumed away**: making TASK 5's "both use `IDataFeed`"
claim literally true requires changing that one `core/pipeline.py` call
site to go through a `LiveDataFeed` instance instead of calling
`MarketDataNormalizer.get_candles()` directly. This is small and
mechanical (one field added to `__init__`, one call site swapped, same
return type, same signature-visible behavior) but it **is** a real
`core/pipeline.py` edit, which CLAUDE.md's Trading Safety section
requires explicit, separate approval for. The conservative alternative
— leave `core/pipeline.py`'s direct call as-is, and read TASK 5 as
"confirm `LiveDataFeed` is a correct, available abstraction" rather
than "force live traffic through it this phase" — avoids that
`pipeline.py` touch entirely. Flagged for the Director's choice, not
assumed.

---

## Summary table

| Module | Real callers today | Safe to hook in Phase 60.8? |
|---|---|---|
| `core/pipeline.py` | `main.py` (`GoldBot.run()`) | Yes — stage-boundary guard only |
| `decision/`, `risk/` | `core/pipeline.py`, `backtesting/backtest_engine.py` | No — out of scope, none proposed |
| `execution_layer/execution_engine/execution_engine.py` | none | No — stays inert, separate approval required |
| `telegram/owner/*.py` | tests only (not wired to handlers) | Yes — `dashboard.py` composition only |
| `RuntimeFeatureManager` | tests, `telegram/owner/*`, `runtime_api.py` | Yes, but needs a feature-name mapping decision |
| `EmergencyManager` | tests, `telegram/owner/emergency_commands.py` | Yes, but needs a 5-state mapping decision |
| `LearningRepository.record()` | `trade_event_bridge.bridge_closed_trade()` only | Yes, but only inside `BacktestEngine` — no live producer exists |
| `IDataFeed` (`ReplayDataFeed`) | `BacktestEngine` | Already correct |
| `IDataFeed` (`LiveDataFeed`) | its own test only | Needs a `core/pipeline.py` call-site swap, or a scope decision |

## Open Questions for the Director (blocking TASK 2/3/4/5 until answered)

1. **TASK 2 feature-name mapping**: which real `RuntimeFeatureManager`
   feature name (existing or new) should gate each of
   `before_signal`/`before_ai`/`before_execution`/`before_database`?
   None of the four currently has a 1:1 real registry entry.
2. **TASK 3 five-state mapping**: what should `PipelineGuard` do on
   `EmergencyState.WARNING` and `EmergencyState.MAINTENANCE`, not just
   `NORMAL`/`PAUSED`/`KILLED`?
3. **TASK 4 scope confirmation**: proceed with wiring
   `trade_event_bridge.bridge_closed_trade()` into
   `BacktestEngine._process_candidate()` only (the one real `CLOSED`
   producer), explicitly disclosing that live trading still records
   nothing to Learning this phase?
4. **TASK 5 scope choice**: swap `core/pipeline.py`'s one
   `get_candles()` call site to go through `LiveDataFeed` (a real,
   minimal `pipeline.py` edit), or keep TASK 5 to "confirm the
   abstraction is correct and available" without touching
   `core/pipeline.py`?

No code was written to answer any of these — per TASK 1's own
instruction, this document is audit only.
