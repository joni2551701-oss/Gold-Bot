# data_layer / normalization

**Module**

## Purpose

No module-level docstring was present in `__init__.py` at the time this file was generated (2026-08-03) by the Engineering Standard v1.0 rollout (Director Order No. 012/013). This is a placeholder pending a real description from a future Development Phase -- content below is limited to what could be verified mechanically from the code.

## Files

- `__init__.py`
- `candle_normalizer.py` -- Data Layer — Candle Normalizer (Phase 59.3, TASK 1: Provider
- `symbol_mapper.py` -- Data Layer — Symbol Mapper (Phase 59.3, TASK 1: Provider Normalization).
- `timeframe_mapper.py` -- Data Layer — Timeframe Mapper (Phase 59.3, TASK 1: Provider

## Responsibilities

See `CONTRACTS.md` and `MODULE_MAP.md` in this directory.

## Dependencies

See `CONTRACTS.md` in this directory for cross-layer dependencies (mechanically derived from actual imports).

## Public API

- `candle_normalizer.py`: function `stamp_provider()`
- `candle_normalizer.py`: function `normalize_candle_list()`
- `symbol_mapper.py`: function `to_provider_symbol()`
- `symbol_mapper.py`: function `from_provider_symbol()`
- `symbol_mapper.py`: function `is_known_symbol()`
- `timeframe_mapper.py`: function `to_provider_timeframe()`
- `timeframe_mapper.py`: function `from_provider_timeframe()`
- `timeframe_mapper.py`: function `is_known_timeframe()`

---
*Generated 2026-08-03 by GoldBot Engineering Standard v1.0 rollout (Director Order No. 012/013). Documentation standardization only -- content mechanically derived from existing code, not authored from scratch.*
