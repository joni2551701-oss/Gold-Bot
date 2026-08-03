# execution_layer / execution_engine / simulator

**Module**

## Purpose

No module-level docstring was present in `__init__.py` at the time this file was generated (2026-08-03) by the Engineering Standard v1.0 rollout (Director Order No. 012/013). This is a placeholder pending a real description from a future Development Phase -- content below is limited to what could be verified mechanically from the code.

## Files

- `__init__.py`
- `latency.py` -- Execution Layer — Execution Delay (Phase 60.3: Execution Simulator
- `models.py` -- Execution Layer — Simulator Models (Phase 60.3: Execution Simulator
- `simulator_engine.py` -- Execution Layer — Simulator Engine (Phase 60.3: Execution Simulator
- `slippage.py` -- Execution Layer — Slippage Engine (Phase 60.3: Execution Simulator
- `spread.py` -- Execution Layer — Spread Simulation (Phase 60.3: Execution Simulator

## Responsibilities

See `CONTRACTS.md` and `MODULE_MAP.md` in this directory.

## Dependencies

See `CONTRACTS.md` in this directory for cross-layer dependencies (mechanically derived from actual imports).

## Public API

- `latency.py`: class `LatencyConfig`
- `latency.py`: function `compute_latency()`
- `latency.py`: function `apply_latency()`
- `models.py`: class `SimulatedOrder`
- `models.py`: class `SimulatedFill`
- `models.py`: class `ExecutionSimulationResult`
- `simulator_engine.py`: class `ExecutionSimulator`
- `slippage.py`: class `SlippageConfig`
- `slippage.py`: function `compute_slippage()`
- `slippage.py`: function `apply_slippage()`
- `spread.py`: class `SpreadConfig`
- `spread.py`: function `get_spread()`
- `spread.py`: function `is_spread_too_wide()`

---
*Generated 2026-08-03 by GoldBot Engineering Standard v1.0 rollout (Director Order No. 012/013). Documentation standardization only -- content mechanically derived from existing code, not authored from scratch.*
