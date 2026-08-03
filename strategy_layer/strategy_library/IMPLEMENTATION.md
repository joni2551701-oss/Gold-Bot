# strategies/

## Purpose
Independent SMC (Smart Money Concepts) signal-candidate generation.
Each strategy is a stateless, read-only class that inspects an
already-built `ContextSnapshot` and produces zero or more
`SignalCandidate`s. As of Phase A11, `strategies/lifecycle/` adds a
separate metadata layer describing these strategies (status, version,
supported assets/styles/timeframes) for future AI/Analytics/
Validation consumers — it does not generate signals itself.

## Flow
```
Context Engine
      |
      v
StrategyManager (strategy_manager.py)
      |     runs every registered strategy, aggregates candidates
      |
      |-- LiquidityStrategy (liquidity_strategy.py)
      |-- FVGStrategy (fvg_strategy.py)
      |-- AMDStrategy (amd_strategy.py)
      v
Signal Engine (signals/)
```

## Responsibilities
- `strategy_manager.py` — `StrategyManager.run_all_strategies()`,
  the single place every strategy is instantiated and run.
- `liquidity_strategy.py` — Liquidity Sweep + BOS + Order Block
  confluence.
- `fvg_strategy.py` — Fair Value Gap + structural break confluence.
- `amd_strategy.py` — AMD Distribution + structural break + OB/FVG
  footprint confluence.
- `lifecycle/` (Phase A11) — `StrategyDefinition`/`StrategyRegistry`
  metadata layer, see "Strategy Lifecycle" below.

## Input
`ContextSnapshot` (from `context/`).

## Output
`List[SignalCandidate]` (from `signal_layer/signal_builder/models.py`) per strategy;
`StrategyManager` aggregates all strategies' candidates into one list.

## Dependencies
`context/` and `signals/` (for `SignalCandidate`/`SignalType`) only.
Never imports `ai/`, `decision/`, `risk/`, `database/`, or
`telegram/`.

---

## Strategy Lifecycle (Phase A11)

`strategies/lifecycle/` is a **metadata layer, not a strategy**. It
does not generate a signal, does not run a strategy, and does not
write to the database — see `docs/STRATEGY_LIFECYCLE.md` for the full
contract.

### Why it exists
Phase 59 Validation, Quant Research, a future AI Assistant, and
Analytics all eventually need to answer "what strategies exist, what
state are they in, what do they support" without re-reading
`strategy_manager.py`'s source or re-deriving the answer themselves.
`StrategyRegistry` is the single, standard place that question is
answered.

### Components
- `strategy_status.py` — `StrategyStatus` (`TESTING`/`ACTIVE`/
  `DISABLED`/`DEPRECATED`), metadata only — does not control whether
  `StrategyManager` actually runs a strategy.
- `strategy_model.py` — `StrategyDefinition`, immutable metadata
  (`id`, `name`, `version`, `status`, `supported_assets`,
  `supported_styles`, `supported_timeframes`, plus the `performance`/
  `win_rate`/`last_validation` hooks below). No trading logic.
- `strategy_registry.py` — `StrategyRegistry` (`register()`/`get()`/
  `list()`/`active()`) and `build_default_registry()`, which registers
  the three strategies above under their real, already-in-production
  `SignalCandidate.strategy_name` values
  (`LIQUIDITY_SWEEP_STRATEGY`/`FVG_STRATEGY`/`AMD_STRATEGY`) — no new
  strategy is introduced.

### Future hooks — never fabricated
`StrategyDefinition.performance`, `.win_rate`, and `.last_validation`
are always `None` in this phase. This codebase does not compute
per-strategy performance or win rate anywhere yet
(`monitoring/performance.py` aggregates by `strategy_name` from the
database, a different, already-existing concern `lifecycle/` does not
duplicate or read from). Wiring a real value into these fields is a
future, separately-approved phase (Phase 59 Validation/Analytics) —
never a placeholder number.

### What Strategy Lifecycle does NOT do
- Does not generate a `BUY`/`SELL` signal.
- Does not instantiate or call `LiquidityStrategy`/`FVGStrategy`/
  `AMDStrategy` — `strategy_manager.py` is untouched, and
  `StrategyManager`'s own strategy list is the only thing that
  actually runs a strategy.
- Does not compute performance or win rate.
- Does not write to the database.
- Does not change `decision/`, `ai/`, `risk/`, or `telegram/` — none
  import from `strategies/lifecycle/` in this phase.

### Dependencies
`strategies/lifecycle/` imports nothing outside itself — no
dependency on `context/`, `signals/`, `ai/`, `decision/`, `risk/`,
`database/`, or `telegram/`, and no dependency on
`strategy_manager.py` or any `strategies/*.py` strategy class.

### Future Roadmap
See `docs/STRATEGY_LIFECYCLE.md`'s "Future usage" section — Phase 59
Validation populating `performance`/`win_rate`/`last_validation`,
Analytics reading `StrategyRegistry.list()`, and a future AI Assistant
querying `StrategyRegistry.active()` are all named, explicit future
steps, none implemented in this phase.
