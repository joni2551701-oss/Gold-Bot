# strategy_layer / strategy_library

**Module**

## Purpose

strategies/ — setup-detection layer.

Two coexisting contracts:
  * Live SignalCandidate path (frozen): strategy_manager.StrategyManager
    runs LiquidityStrategy/FVGStrategy/AMDStrategy.analyze() into signals/.
  * Setup layer (TASK-CORE-007): SetupManager runs the eleven
    SetupStrategy classes, each returning a StrategyResult (setup yes/no,
    no signal). Not wired into core/pipeline.py.

Only the setup-layer public API is re-exported here; the live path is
imported directly by signal_layer/signal_engine/signal_engine.py and is left untouched.

## Files

- `__init__.py` -- strategies/ — setup-detection layer.
- `amd_strategy.py`
- `bos_strategy.py` -- Strategies — BOS / CHoCH setup strategy (TASK-CORE-007, setup layer).
- `breakout_strategy.py` -- Strategies — Breakout / failed-breakout setup strategy (TASK-CORE-007, setup layer).
- `fvg_strategy.py`
- `liquidity_strategy.py`
- `ob_strategy.py` -- Strategies — Order Block setup strategy (TASK-CORE-007, setup layer).
- `registry.py` -- Strategies — setup-layer registry (TASK-CORE-007).
- `reversal_strategy.py` -- Strategies — Reversal setup strategy (TASK-CORE-007, setup layer).
- `session_strategy.py` -- Strategies — Session setup strategy (TASK-CORE-007, setup layer).
- `snr_strategy.py` -- Strategies — Support / Resistance setup strategy (TASK-CORE-007, setup layer).
- `trend_strategy.py` -- Strategies — Trend continuation setup strategy (TASK-CORE-007, setup layer).
- `wyckoff_strategy.py` -- Strategies — Wyckoff setup strategy (TASK-CORE-007, setup layer).

## Responsibilities

See `CONTRACTS.md` and `MODULE_MAP.md` in this directory.

## Dependencies

See `CONTRACTS.md` in this directory for cross-layer dependencies (mechanically derived from actual imports).

## Public API

- `amd_strategy.py`: class `StrategyConfig`
- `amd_strategy.py`: class `AMDStrategy`
- `amd_strategy.py`: class `AMDSetupStrategy`
- `bos_strategy.py`: class `BOSStrategy`
- `breakout_strategy.py`: class `BreakoutStrategy`
- `fvg_strategy.py`: class `StrategyConfig`
- `fvg_strategy.py`: class `FVGStrategy`
- `fvg_strategy.py`: class `FVGSetupStrategy`
- `liquidity_strategy.py`: class `LiquidityStrategy`
- `liquidity_strategy.py`: class `LiquiditySetupStrategy`
- `ob_strategy.py`: class `OBStrategy`
- `registry.py`: class `DuplicateStrategyNameError`
- `registry.py`: class `SetupRegistry`
- `registry.py`: function `build_setup_registry()`
- `reversal_strategy.py`: class `ReversalStrategy`
- `session_strategy.py`: class `SessionStrategy`
- `snr_strategy.py`: class `SNRStrategy`
- `trend_strategy.py`: class `TrendStrategy`
- `wyckoff_strategy.py`: class `WyckoffStrategy`

---
*Generated 2026-08-03 by GoldBot Engineering Standard v1.0 rollout (Director Order No. 012/013). Documentation standardization only -- content mechanically derived from existing code, not authored from scratch.*
