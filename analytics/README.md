# analytics/

## Purpose
Phase 59 Preparation foundation (TASK 3: Trading Performance Schema).
**Trading** performance — did a signal make money, in how many R, in
which strategy/session/market phase — never to be confused with
`performance/` (Phase A19), which measures **system** performance
(pipeline stage duration, API latency) and has no notion of a trade
outcome at all. See `signal_performance.py`'s own module docstring for
the full three-way distinction against `performance/` (A19) and
`core_layer/health_monitor/performance.py`'s pre-existing `PerformanceTracker`
(database-driven, strategy-only win/loss/win-rate — a real, narrower,
already-working calculator this package does not replace or import).

## Modules

### `signal_performance.py`
`SignalPerformance` (`performance_id`, `signal_id`, `strategy_id`,
`context_id`, `result`, `profit_loss`, `r_multiple`, `duration`,
`session`, `market_phase`, `created_at`) plus
`compute_signal_performance(signal, paper_trade=None, session=None,
market_phase=None)` — a standardization adapter, like
`signal_layer/signal_builder/schema.py`/`context_layer/context_engine/snapshot.py` before it: relays
already-known values (`strategy_id` = `SignalSchema.strategy_name`,
`context_id` = `SignalSchema.context_id`, both real since AC-03) and
computes only `r_multiple` (a pure, disclosed arithmetic derivation —
see `compute_r_multiple()`) and `duration` (from
`PaperTrade.opened_at`/`closed_at`). `profit_loss` is always `None` —
an honest hook; no PnL/lot-value computation exists anywhere in this
codebase today (would need sizing/currency logic, out of this task's
scope — `risk_layer/risk_engine/risk_manager.py` is untouched).

### `strategy_report.py`
`StrategyPerformanceReport` plus `build_strategy_report(performances)`
— groups `SignalPerformance` records by `strategy_id`, computing
`win_count`/`loss_count`/`breakeven_count`/`expired_count`/
`cancelled_count` (the latter two added Phase 59.4, TASK 3)/`win_rate`/
`average_r_multiple`. `win_rate` deliberately reuses
`core_layer/health_monitor/performance.py`'s own `WIN / (WIN + LOSS)` formula and
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
`execution_layer.execution_engine.simulator.models.ExecutionSimulationResult` (requested
price, fill price, slippage, spread, latency, rejection reason) for
later comparison against real MT5 fills, per the Director's own
brief. No new execution/slippage/spread/latency logic — reads an
already-computed result only, same "adapter, not calculator" posture
`signal_performance.py` already established for `SignalSchema`/`PaperTrade`.

### `performance_metrics.py` (Phase 60.4: Performance Validation Foundation, TASK 2)
`PerformanceMetrics` plus `compute_performance_metrics(performances,
equity_curve=None)`/`format_performance_metrics(metrics)` — portfolio-
wide (ungrouped) expectancy, profit factor, and a risk-adjusted return,
all R-based (no PnL model exists — see `signal_performance.py`'s own
docstring). Reuses `strategy_report.compute_win_rate()` directly, not
reimplemented. Max Drawdown/Recovery Factor stay `None` unless the
caller supplies an `equity_curve.py`-built curve. See
`docs/PERFORMANCE_VALIDATION.md`.

### `equity_curve.py` (Phase 60.4: Performance Validation Foundation, TASK 3)
`EquityCurveConfig`/`EquityPoint` plus `build_equity_curve(performances,
config=None)`/`max_drawdown(points)`/`format_equity_curve_summary(points)`
— walks a chronologically-sorted, resolved-only (`r_multiple is not
None`) sequence of `SignalPerformance` into a running balance/drawdown
curve. Makes one disclosed, visualization-only assumption
(`EquityCurveConfig.unit_risk_amount`, a configurable dollar-per-1R) to
bridge the same "no PnL model exists" gap `performance_metrics.py`
also discloses — `risk_layer/risk_engine/risk_manager.py` is untouched. See
`docs/PERFORMANCE_VALIDATION.md`.

### `benchmark.py` (Phase 60.4: Performance Validation Foundation, TASK 4)
`BenchmarkComparison` plus `compute_benchmark_comparison(equity_curve,
benchmark_start_price, benchmark_end_price)`/`format_benchmark_comparison(comparison)`
— strategy return vs. buy-and-hold XAUUSD over the same period,
matching the Director's own worked example ("Gold +5%, Strategy +18%
-> Alpha: +13%"). Does not read candles itself — the caller supplies
both benchmark prices. See `docs/PERFORMANCE_VALIDATION.md`.

### `learning_report.py` (Phase 60.6: Learning Loop Foundation, TASK 6)
`LearningReport` plus `build_learning_report(records,
min_occurrences=3)`/`format_learning_report(report)` — reuses
`learning.pattern_detector.detect_patterns()` directly, picking the
highest-/lowest-win-rate `PatternInsight` as `best_condition`/
`worst_condition`. Matches the Director's own "Last 100 trades / Best
condition / Worst condition" worked example shape. See
`docs/LEARNING_LOOP.md`.

## What this package does NOT do
- Does not read or write the database — no new table, no migration,
  no dependency on `database/`.
- Does not call `SignalRepository` or `core_layer/health_monitor/performance.py` —
  its input is an in-memory `List[SignalPerformance]`, built by the
  caller from already-computed `SignalSchema`/`PaperTrade` objects.
- Does not change `risk_layer/risk_engine/risk_manager.py`, `decision_layer/decision_engine/decision_engine.py`,
  or any strategy — `r_multiple` is a pure post-hoc arithmetic
  derivation from already-approved price levels, never a sizing
  decision.
- Is not wired into `core/pipeline.py` — a standalone foundation, same
  posture as `lifecycle/` and `data_layer/live_data/market_data_snapshot.py` (this
  phase's other two tasks).

## Dependencies
`signal_performance.py` imports `trade_monitoring_layer.paper_trading.trade_state.TradeState`
(Phase 59.4, TASK 1 — a real runtime import, needed to detect a
`CANCELLED` `PaperTrade`) plus, `TYPE_CHECKING`-only,
`trade_monitoring_layer.paper_trading.paper_trade.PaperTrade` and `signal_layer.signal_builder.schema.SignalSchema`.
`strategy_report.py` imports `analytics.signal_performance` (same
package) only. Neither imports `context/`, `strategies/`, `ai/`,
`decision/`, `risk/`, `execution/`, `database/`, or `telegram/`.
`execution_report.py` imports `execution_layer.execution_engine.simulator.models.ExecutionSimulationResult`
(`TYPE_CHECKING`-only) — the one exception to the "no `execution/`
dependency" rule above, read-only and scoped to this single new file.
`performance_metrics.py` imports `analytics.signal_performance` and
`analytics.strategy_report.compute_win_rate` at module level, plus
`analytics.equity_curve.max_drawdown` locally (inside
`compute_performance_metrics()`, only when a curve is supplied).
`equity_curve.py` imports `analytics.signal_performance`
(`TYPE_CHECKING`-only). `benchmark.py` imports `analytics.equity_curve`
(`TYPE_CHECKING`-only). `learning_report.py` imports
`learning.models`/`learning.pattern_detector` (real, runtime imports
-- both read-only, no trading-decision logic). None of the four import
`database/`, `risk/`, `decision/`, `ai/`, `strategies/`, `signals/`,
or `execution/`.

## Future Roadmap
Persistence (a `signal_performance` table), `core/pipeline.py` wiring,
a `profit_loss` computation once account-currency/lot-value sizing
exists, and a live consumer for `docs/PHASE59_VALIDATION.md`'s 7-day
report all remain unimplemented — separate, explicitly-approvable
future steps.
