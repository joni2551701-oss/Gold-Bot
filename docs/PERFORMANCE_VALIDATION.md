# Performance Validation Foundation (Phase 60.4)

**Not wired into the live bot.** Same "real function, not live-wired"
posture as every phase before it. Nothing in `core/pipeline.py` or any
Telegram routing surface constructs or reads anything in
`analytics/performance_metrics.py`/`equity_curve.py`/`benchmark.py`/
`platform_layer/telegram/owner/performance_commands.py` this phase.

## Where this sits

```
Historical Data -> Replay Engine (60.1) -> Backtesting Engine (60.2)
      -> Strategy -> Decision -> Risk -> Paper Trade
      -> Execution Simulator (60.3)
      -> analytics.signal_performance.SignalPerformance (Phase 59)
              |
              v
      analytics.performance_metrics   -- TASK 2, this phase
      analytics.equity_curve          -- TASK 3, this phase
      analytics.benchmark             -- TASK 4, this phase
              |
              v
      platform_layer.telegram.owner.performance_commands  -- TASK 7, this phase
```

Every module in this phase consumes an already-built
`Sequence[SignalPerformance]` (and, for `benchmark.py`, an
already-built equity curve plus two caller-supplied prices) — none of
them read the database, call a repository, or fetch candles. This
matches `analytics/README.md`'s own "What this package does NOT do"
section, unchanged by this phase.

## TASK 1: Reuse audit

Read `core_layer/health_monitor/performance.py` (`PerformanceTracker`: database-driven
win/loss/win_rate off the persisted `signals` table via
`SignalRepository`) and `analytics/validation_report.py`
(`ValidationReport`: per-strategy breakdown + best session/market
phase). Neither computes expectancy, profit factor, drawdown, recovery
factor, or a risk-adjusted return — confirmed no overlap with TASK 2's
scope. Both are read-only inputs to this audit, not extended or
imported by any new module in this phase.

## TASK 2: `analytics/performance_metrics.py`

`PerformanceMetrics` (frozen) + `compute_performance_metrics(performances,
equity_curve=None)` + `format_performance_metrics(metrics)`. Portfolio-wide
(ungrouped) — a caller wanting per-strategy metrics groups with
`strategy_report.filter_performances()` first, the same composition
pattern `strategy_report.py`/`context_report.py` already use.

All R-based, not dollar-based (no PnL/lot-value model exists anywhere
in this codebase — see `signal_performance.py`'s own docstring):

- **Expectancy** = `(win_rate * average_win_r) - (loss_rate *
  average_loss_r)` — the Director's own formula, `average_win_r`/
  `average_loss_r` both magnitudes in R.
- **Profit Factor** = gross winning R / gross losing R (magnitudes).
  `None` when there are no losing trades (undefined, not infinite).
- **Risk-Adjusted Return** = expectancy / population-stdev of every
  decided trade's signed R-multiple — a Sharpe-like ratio that never
  needs a dollar amount. `None` with fewer than 2 decided trades or a
  zero stdev.
- **Max Drawdown / Recovery Factor** are the one exception: both stay
  `None` unless the caller supplies an already-built equity curve
  (TASK 3) — a drawdown "fraction of peak" needs a peak, which needs a
  dollar-shaped curve, which this module does not build itself.
  Recovery Factor = net profit / (max\_drawdown\_fraction \*
  starting\_balance), reusing the *same* `starting_balance` reference
  the supplied curve was already built against — no new dollar
  assumption invented here.

`compute_win_rate()` is imported from `analytics.strategy_report`
directly, not reimplemented — the same WIN/(WIN+LOSS) convention this
codebase has used since Phase 59.

## TASK 3: `analytics/equity_curve.py`

`EquityCurveConfig` (`starting_balance=1000.0`, `unit_risk_amount=100.0`)
+ `EquityPoint` (`timestamp`, `balance`, `drawdown`) +
`build_equity_curve(performances, config=None)` + `max_drawdown(points)`
+ `format_equity_curve_summary(points)`.

**The one disclosed assumption in this phase**: no PnL/dollar
computation exists anywhere in this codebase
(`SignalPerformance.profit_loss` is always `None`), but the Director's
own worked example (`1000$ -> +30 -> 1030$`) is expressed in dollars.
`EquityCurveConfig.unit_risk_amount` bridges that gap — a configurable
dollar value representing "1R" that converts each trade's already-real
`r_multiple` into a dollar delta. This is **visualization-only**, not a
sizing or PnL computation; `risk_layer/risk_engine/risk_manager.py` is untouched. Same
disclosed-assumption posture `backtest_engine.py`'s own HTF-neutral
fallback used in Phase 60.2.

Records are ordered by `SignalPerformance.created_at` (its only
timestamp — not a close time, since none exists on that model either).
Records with `r_multiple is None` are skipped. Never raises: an empty
or all-unresolved list produces a single starting point.

## TASK 4: `analytics/benchmark.py`

`BenchmarkComparison` (`strategy_return_pct`, `benchmark_return_pct`,
`alpha_pct`) + `compute_benchmark_comparison(equity_curve,
benchmark_start_price, benchmark_end_price)` +
`format_benchmark_comparison(comparison)` — matches the Director's own
worked example exactly: `Gold +5%, Strategy +18% -> Alpha: +13%`.

Deliberately does not read candles itself — the caller (a future
`backtest_commands.py`/`performance_commands.py` consumer) already has
both endpoint prices from the backtested range; this module only does
the subtraction. `alpha_pct` is a plain return-difference, not a
risk-adjusted (beta-weighted) alpha — no claim beyond the brief's own
worked example. `None` when the equity curve has fewer than 2 points
(nothing to compare) or `benchmark_start_price <= 0` (undefined
percentage base).

## TASK 5: Validation Report duplicate — reconfirmed, not touched

`docs/PHASE60_ARCHITECTURE_AUDIT.md` already found and the Director
already decided (finding 1, Director decision 1):
`platform_layer/telegram/owner/validation_commands.py`'s `get_validation_report()` is
deprecated in favor of `platform_layer/telegram/owner/report_commands.py`'s
`get_validation_summary()`. That same document is explicit that **none
of the six Phase 60.0 decisions are implemented yet** — each is "a
target shape for a future, separately-approved wiring/consolidation
phase, not an instruction to refactor `platform_layer/telegram/owner/` in this pass."

This phase's TASK 5 re-read both functions and confirmed the finding
still holds exactly as documented (both still exist, same signature,
same target command name, genuinely different output shape). No code
in either file was touched — doing so now would contradict the
Director's own explicit deferral. The deprecation itself remains a
future, separately-approved step.

## TASK 6: Database decision — foundation-only, no new table

No `performance_snapshots` table (or any new table) was added.
`database/` gained nothing this phase. This matches every other
analytics module built so far (`signal_performance`, `strategy_report`,
`context_report`, `execution_report`, and now `equity_curve`,
`performance_metrics`, `benchmark`) — all in-memory-only, computed on
demand from an already-built `Sequence[SignalPerformance]`, never
persisted. `analytics/README.md`'s own "Future Roadmap" already names
persistence as a separate, explicitly-approvable future step; this
phase does not change that.

## TASK 7: `platform_layer/telegram/owner/performance_commands.py`

Three thin wrappers, same "compute from supplied data, don't fetch"
posture as `validation_commands.py`:

- `get_performance_report(performances)` — the future `/performance`
  command. Wraps `compute_performance_metrics()`/
  `format_performance_metrics()` unmodified. No equity curve is built
  here, so `max_drawdown`/`recovery_factor` report "N/A".
- `get_equity_curve_report(performances, starting_balance=None,
  unit_risk_amount=None)` — the future `/equity_curve` command. Wraps
  `build_equity_curve()`/`format_equity_curve_summary()` unmodified;
  the two optional overrides feed `EquityCurveConfig` when supplied.
- `get_backtest_performance_report(performances,
  benchmark_start_price=None, benchmark_end_price=None)` — the future
  `/backtest_report` command. Combines the performance-metrics section
  with a benchmark-comparison section when both prices are supplied,
  falling back to metrics-only otherwise.

Not registered into `platform_layer/telegram/commands.py`, not called from
`platform_layer/telegram/command_router.py` or `platform_layer/telegram/handlers.py` — same
foundation posture as `backtest_commands.py`/`execution_commands.py`.

## Dependencies

`performance_metrics.py` imports `analytics.signal_performance` and
`analytics.strategy_report.compute_win_rate` (reused, not
reimplemented); imports `analytics.equity_curve.max_drawdown` locally
inside `compute_performance_metrics()` only when an equity curve is
supplied, avoiding an unconditional import-time dependency between the
two sibling modules. `equity_curve.py` imports `analytics.signal_performance`
(`TYPE_CHECKING`-only). `benchmark.py` imports `analytics.equity_curve`
(`TYPE_CHECKING`-only). `performance_commands.py` imports all three
plus `platform_layer.telegram.owner.provider_commands.ProviderCommandResult`, the same
envelope every other module in `platform_layer/telegram/owner/` already uses. None of
the four modules import `database/`, `risk/`, `decision/`, `ai/`,
`strategies/`, or `signals/`.

## Known gaps (disclosed, not hidden)

- `profit_loss`/real dollar PnL still does not exist anywhere in this
  codebase — every dollar figure in `equity_curve.py`/`benchmark.py`
  is derived from the disclosed `unit_risk_amount` assumption, never a
  real sizing computation.
- Nothing persists a `SignalPerformance` list yet, so none of this
  phase's owner commands have a real data source to call today — same
  gap `validation_commands.py`/`report_commands.py` already carry.
- The `get_validation_report()`/`get_validation_summary()` duplicate
  remains unresolved by design (TASK 5) — a future, separately-approved
  step.

## Future Roadmap

Phase 60.5 — Fundamental Intelligence, per the Director's own roadmap
note: "the last big foundation before the v0.4 AI layer."
