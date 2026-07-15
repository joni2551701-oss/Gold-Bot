# analytics/

## Purpose
Phase 59 Preparation foundation (TASK 3: Trading Performance Schema).
**Trading** performance — did a signal make money, in how many R, in
which strategy/session/market phase — never to be confused with
`performance/` (Phase A19), which measures **system** performance
(pipeline stage duration, API latency) and has no notion of a trade
outcome at all. See `signal_performance.py`'s own module docstring for
the full three-way distinction against `performance/` (A19) and
`monitoring/performance.py`'s pre-existing `PerformanceTracker`
(database-driven, strategy-only win/loss/win-rate — a real, narrower,
already-working calculator this package does not replace or import).

## Modules

### `signal_performance.py`
`SignalPerformance` (`performance_id`, `signal_id`, `strategy_id`,
`context_id`, `result`, `profit_loss`, `r_multiple`, `duration`,
`session`, `market_phase`, `created_at`) plus
`compute_signal_performance(signal, paper_trade=None, session=None,
market_phase=None)` — a standardization adapter, like
`signals/schema.py`/`context/snapshot.py` before it: relays
already-known values (`strategy_id` = `SignalSchema.strategy_name`,
`context_id` = `SignalSchema.context_id`, both real since AC-03) and
computes only `r_multiple` (a pure, disclosed arithmetic derivation —
see `compute_r_multiple()`) and `duration` (from
`PaperTrade.opened_at`/`closed_at`). `profit_loss` is always `None` —
an honest hook; no PnL/lot-value computation exists anywhere in this
codebase today (would need sizing/currency logic, out of this task's
scope — `risk/risk_manager.py` is untouched).

### `strategy_report.py`
`StrategyPerformanceReport` plus `build_strategy_report(performances)`
— groups `SignalPerformance` records by `strategy_id`, computing
`win_count`/`loss_count`/`breakeven_count`/`expired_count`/
`cancelled_count` (the latter two added Phase 59.4, TASK 3)/`win_rate`/
`average_r_multiple`. `win_rate` deliberately reuses
`monitoring/performance.py`'s own `WIN / (WIN + LOSS)` formula and
zero-division guard — the same convention, not a competing one.
`compute_win_rate()` (renamed from a private `_win_rate()` in Phase
59.4 once `context_report.py` became a second real caller — no
behavior change).

### `context_report.py` (Phase 59.4, TASK 4)
`ContextPerformanceReport` plus `build_context_report(performances,
include_market_phase=False)` — the same counting/`win_rate` logic as
`strategy_report.py` (a small, disclosed duplication, not a shared
abstraction forced onto two callers), grouped by `(session,
strategy_id)` by default, or `(session, strategy_id, market_phase)`
when `include_market_phase=True`. Matches this task's own worked
example ("London + Liquidity Sweep → Winrate 71%"); the brief's own
illustrative third dimension ("+FVG") is deliberately substituted with
`market_phase` — the real third dimension `SignalPerformance` actually
carries, not a fabricated field.

### `execution_report.py` (Phase 60.3: Execution Simulator Foundation, TASK 8)
`ExecutionAnalyticsRecord`/`ExecutionAnalyticsSummary` plus
`build_execution_record(result)`/`summarize_execution_records(records)`/
`format_execution_record(record)` — packages an
`execution.simulator.models.ExecutionSimulationResult` (requested
price, fill price, slippage, spread, latency, rejection reason) for
later comparison against real MT5 fills, per the Director's own
brief. No new execution/slippage/spread/latency logic — reads an
already-computed result only, same "adapter, not calculator" posture
`signal_performance.py` already established for `SignalSchema`/`PaperTrade`.

## What this package does NOT do
- Does not read or write the database — no new table, no migration,
  no dependency on `database/`.
- Does not call `SignalRepository` or `monitoring/performance.py` —
  its input is an in-memory `List[SignalPerformance]`, built by the
  caller from already-computed `SignalSchema`/`PaperTrade` objects.
- Does not change `risk/risk_manager.py`, `decision/decision_engine.py`,
  or any strategy — `r_multiple` is a pure post-hoc arithmetic
  derivation from already-approved price levels, never a sizing
  decision.
- Is not wired into `core/pipeline.py` — a standalone foundation, same
  posture as `lifecycle/` and `data/market_data_snapshot.py` (this
  phase's other two tasks).

## Dependencies
`signal_performance.py` imports `lifecycle.trade_state.TradeState`
(Phase 59.4, TASK 1 — a real runtime import, needed to detect a
`CANCELLED` `PaperTrade`) plus, `TYPE_CHECKING`-only,
`lifecycle.paper_trade.PaperTrade` and `signals.schema.SignalSchema`.
`strategy_report.py` imports `analytics.signal_performance` (same
package) only. Neither imports `context/`, `strategies/`, `ai/`,
`decision/`, `risk/`, `execution/`, `database/`, or `telegram/`.
`execution_report.py` imports `execution.simulator.models.ExecutionSimulationResult`
(`TYPE_CHECKING`-only) — the one exception to the "no `execution/`
dependency" rule above, read-only and scoped to this single new file.

## Future Roadmap
Persistence (a `signal_performance` table), `core/pipeline.py` wiring,
a `profit_loss` computation once account-currency/lot-value sizing
exists, and a live consumer for `docs/PHASE59_VALIDATION.md`'s 7-day
report all remain unimplemented — separate, explicitly-approvable
future steps.
