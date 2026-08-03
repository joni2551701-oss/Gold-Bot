# Execution Simulator Foundation (Phase 60.3)

**Not wired into the live bot, and never touches live execution.**
Same "real function, not live-wired" posture as every phase before
it. `execution_layer/execution_engine/execution_engine.py`'s `ExecutionEngine.dispatch()` and
`execution_layer/execution_monitor/signal_lifecycle.py`'s `SignalLifecycle.transition()` are
both completely untouched by this phase — still deliberately inert,
still requiring a separate, explicit approval to wire up per
`CLAUDE.md`'s Trading Safety rules.

## Why `execution_layer/execution_engine/simulator/`, not `simulation/`

Per the Director's own instruction and the Module Reuse Principle
(`CLAUDE.md`): before creating any new module, check whether an
existing one can be extended. TASK 1's reuse audit read
`execution_layer/execution_engine/execution_engine.py` and `execution_layer/execution_monitor/signal_lifecycle.py`
directly — both are deliberately inert stubs ("Currently
unimplemented"/"Currently a placeholder") with nothing to reuse, and
extending either would blur the "intentionally inert, needs separate
approval" line `CLAUDE.md` draws around live execution. The correct,
minimal-cost choice was a new subpackage inside the *existing*
`execution/` top-level package — not a new `simulation/` package, and
not a modification to either existing file.

## The chain

```
Decision APPROVE
      |
Risk Approved
      |
      v
lifecycle.paper_trade.create_paper_trade()/open_paper_trade()   -- unmodified (Phase 59 Preparation)
      |  (an OPEN PaperTrade + its RiskResult)
      v
execution_layer.execution_engine.simulator.simulator_engine.ExecutionSimulator.simulate()   -- Phase 60.3
      |
      +-- execution_layer.execution_engine.simulator.spread.get_spread()/is_spread_too_wide()   -- TASK 4
      +-- execution_layer.execution_engine.simulator.slippage.compute_slippage()/apply_slippage()  -- TASK 3
      +-- execution_layer.execution_engine.simulator.latency.compute_latency()/apply_latency()     -- TASK 5
      |
      v
ExecutionSimulationResult (filled=True + SimulatedFill, or filled=False + rejection_reason)
      |
      v
analytics.execution_report.build_execution_record()   -- TASK 8
      |
      v
ExecutionAnalyticsRecord (requested price, fill price, slippage, latency, rejection reason)
```

`ExecutionSimulator.simulate()` never mutates the `PaperTrade` it
reads — `PaperTrade.entry`/`stop_loss`/`take_profit` stay exactly what
`create_paper_trade()` set them to (copied from an already-APPROVEd
`SignalSchema`, per `lifecycle/paper_trade.py`'s own "What this module
does NOT do" list, itself untouched by this phase). The simulator
produces a separate result describing what a *fill* would look like,
alongside the trade, not instead of it.

## Fill price formula

```
fill_price = apply_slippage(requested_price, direction, slippage_points + spread_points)
```

Spread and slippage are both adverse-to-the-trader costs, folded into
one offset via `slippage.py`'s own `apply_slippage()` (worse/higher
for a BUY, worse/lower for a SELL) rather than a second near-identical
function — the Director's own worked example (BUY 2350.00 requested →
2350.15 filled) is reproduced exactly when `spread_points=0`.

Both slippage and spread are **deterministic**, not a random/stochastic
draw: the same `SlippageConfig`/`SpreadConfig` always produces the
same offset for a given signal, which keeps a `backtesting/` run
reproducible and directly comparable across repeated runs. A future
phase could layer a stochastic distribution on top without changing
`apply_slippage()`'s own contract.

## Reject condition

A spread at or above `SpreadConfig.max_points` rejects the order
before any fill price is computed — `ExecutionSimulationResult.filled=False`,
`fill=None`, `rejection_reason` set. This models a real broker's own
max-spread guard (e.g. during a news spike) without inventing new risk
logic — `risk_layer/risk_engine/risk_manager.py` is completely untouched; this reject
happens entirely inside the simulator, after Risk has already
approved the trade.

## Worked examples (from the Director's own brief)

- **Slippage**: BUY requested at `2350.00`, `SlippageConfig(points=0.15)` → filled at `2350.15`.
- **Spread**: London session → `0.15` points; NY news session → `0.80` points (`SpreadConfig.session_spreads`).
- **Latency**: signal at `10:00:00`, `LatencyConfig(execution_latency_ms=2000)` → order reaches the market at `10:00:02`.

## API reference

### `execution_layer/execution_engine/simulator/models.py`
- `SimulatedOrder(order_id, trade_id, symbol, direction, requested_price, lot_size, requested_at)` — frozen.
- `SimulatedFill(fill_price, spread_points, slippage_points, latency_ms, filled_at)` — frozen.
- `ExecutionSimulationResult(filled, order, fill=None, rejection_reason=None)` — frozen. Deliberately **not** named `ExecutionResult` — `execution_engine.py` already owns that name for its own, unrelated, still-inert dispatch stub.

### `execution_layer/execution_engine/simulator/slippage.py`
- `SlippageConfig(points=0.10, max_points=0.50)`.
- `compute_slippage(config=None) -> float`.
- `apply_slippage(requested_price, direction, slippage_points) -> float`.

### `execution_layer/execution_engine/simulator/spread.py`
- `SpreadConfig(default_points=0.20, max_points=1.00, session_spreads={"LONDON": 0.15, "NY_NEWS": 0.80})`.
- `get_spread(session, config=None) -> float`.
- `is_spread_too_wide(spread_points, config=None) -> bool`.

### `execution_layer/execution_engine/simulator/latency.py`
- `LatencyConfig(execution_latency_ms=2000)`.
- `compute_latency(config=None) -> int`.
- `apply_latency(signal_time, latency_ms) -> datetime`.

### `execution_layer/execution_engine/simulator/simulator_engine.py`
- `ExecutionSimulator(slippage_config=None, spread_config=None, latency_config=None)`.
- `.simulate(paper_trade, risk_result, session=None, signal_time=None) -> ExecutionSimulationResult`.

### `analytics/execution_report.py`
- `ExecutionAnalyticsRecord(order_id, trade_id, symbol, direction, requested_price, filled, fill_price=None, slippage_points=None, spread_points=None, latency_ms=None, rejection_reason=None, created_at=None)` — frozen.
- `ExecutionAnalyticsSummary(total_orders, filled_count, rejected_count, average_slippage_points=None, average_latency_ms=None)` — frozen; `.fill_rate` derived property.
- `build_execution_record(result) -> ExecutionAnalyticsRecord`.
- `summarize_execution_records(records) -> ExecutionAnalyticsSummary`.
- `format_execution_record(record) -> str`.

### `telegram/owner/execution_commands.py`
- `execution_status() -> ProviderCommandResult` — current simulator config + selected mode.
- `slippage_status() -> ProviderCommandResult`.
- `set_simulation_mode(mode) -> ProviderCommandResult` — selects a named session preset (`DEFAULT`/`LONDON`/`NY_NEWS`) for a future `simulate()` call's own `session` argument; in-memory only, does not survive a restart.

## What this phase does NOT do

- Does not call `execution_layer/execution_engine/execution_engine.py`'s `ExecutionEngine` or
  `execution_layer/execution_monitor/signal_lifecycle.py`'s `SignalLifecycle` — both remain
  exactly as inert as before this phase.
- Does not touch `decision_layer/decision_engine/decision_engine.py` or `risk_layer/risk_engine/risk_manager.py`
  — every eligibility decision (APPROVE/REJECT, risk-approved) is made
  entirely upstream, unchanged; the simulator only decides fill-vs-reject
  on its own spread condition.
- Does not mutate `lifecycle.paper_trade.PaperTrade` — the simulator
  reads a trade's `entry`/`direction`, never writes back to it.
- Does not model a real bid/ask order book, partial fills, or
  requotes — spread + slippage are both single scalar offsets.
- Does not persist `ExecutionAnalyticsRecord` to a database table.
- Does not register `/execution_status`/`/slippage_status`/
  `/set_simulation_mode` into `telegram/commands.py`/
  `command_router.py`/`handlers.py`.

## Future wiring plan

```
docs/EXECUTION_SIMULATOR.md (Phase 60.3 -- foundation, this document)
        |
        v
execution_layer/execution_engine/simulator/*.py, analytics/execution_report.py,
telegram/owner/execution_commands.py (Phase 60.3 -- real logic, not wired)
        |
        v
A future, separately-approved phase (60.4 Performance Validation per
the current roadmap):
  - Wire ExecutionSimulator.simulate() into backtesting/backtest_engine.py's
    own loop, alongside create_paper_trade()/open_paper_trade(), so a
    backtest produces both a PaperTrade result AND an
    ExecutionAnalyticsRecord per trade
  - Compare simulated fills against real MT5 fills once execution/
    itself is wired up (a separate, explicit approval)
  - Persist ExecutionAnalyticsRecord for a resumable, comparable-across-runs report
  - telegram/commands.py/command_router.py registration
```
