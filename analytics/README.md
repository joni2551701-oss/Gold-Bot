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
`win_count`/`loss_count`/`breakeven_count`/`win_rate`/
`average_r_multiple`. `win_rate` deliberately reuses
`monitoring/performance.py`'s own `WIN / (WIN + LOSS)` formula and
zero-division guard — the same convention, not a competing one.

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
`signal_performance.py` imports only the standard library at runtime,
plus `lifecycle.paper_trade.PaperTrade` and `signals.schema.SignalSchema`
(`TYPE_CHECKING`-only). `strategy_report.py` imports
`analytics.signal_performance` (same package) only. Neither imports
`context/`, `strategies/`, `ai/`, `decision/`, `risk/`, `execution/`,
`database/`, or `telegram/`.

## Future Roadmap
Persistence (a `signal_performance` table), `core/pipeline.py` wiring,
a `profit_loss` computation once account-currency/lot-value sizing
exists, and a live consumer for `docs/PHASE59_VALIDATION.md`'s 7-day
report all remain unimplemented — separate, explicitly-approvable
future steps.
