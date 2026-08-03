# strategy_layer / strategy_manager / lifecycle

**Module**

## Purpose

No module-level docstring was present in `__init__.py` at the time this file was generated (2026-08-03) by the Engineering Standard v1.0 rollout (Director Order No. 012/013). This is a placeholder pending a real description from a future Development Phase -- content below is limited to what could be verified mechanically from the code.

## Files

- `__init__.py`
- `strategy_model.py` -- Strategy Lifecycle — data model (Phase A11).
- `strategy_registry.py` -- Strategy Lifecycle — registry (Phase A11).
- `strategy_status.py` -- Strategy Lifecycle — status enum (Phase A11).

## Responsibilities

See `CONTRACTS.md` and `MODULE_MAP.md` in this directory.

## Dependencies

See `CONTRACTS.md` in this directory for cross-layer dependencies (mechanically derived from actual imports).

## Public API

- `strategy_model.py`: class `StrategyDefinition`
- `strategy_registry.py`: class `DuplicateStrategyIdError`
- `strategy_registry.py`: class `StrategyRegistry`
- `strategy_registry.py`: function `build_default_registry()`
- `strategy_status.py`: class `StrategyStatus`

---
*Generated 2026-08-03 by GoldBot Engineering Standard v1.0 rollout (Director Order No. 012/013). Documentation standardization only -- content mechanically derived from existing code, not authored from scratch.*
