# IMPLEMENTATION.md — context_layer/trend/market_regime

## `market_regime.py`

Public surface:

- `dataclass`
- `Enum`
- `Optional`
- `Sequence`
- `TYPE_CHECKING`
- `Candle`
- `StructurePoint`
- `most_recent_bias`
- `WyckoffEvent`
- `WyckoffPhase`
- `classify_session`
- `compute_session_volatility`
- `HTFBias`
- `MarketRegime`
- `RegimeDirection`
- `MarketRegimeResult`
- `WYCKOFF_REGIME_CONFIDENCE`
- `TRENDING_CONFIRMED_CONFIDENCE`
- `TRENDING_UNCONFIRMED_CONFIDENCE`
- `VOLATILITY_CONFIDENCE`
- `RANGE_CONFIDENCE`
- `UNKNOWN_CONFIDENCE`
- `HIGH_VOLATILITY_RATIO_THRESHOLD`
- `LOW_VOLATILITY_RATIO_THRESHOLD`
- `compute_market_regime`

## Design Notes

Converted from a flat `market_regime.py` to a canonical package under GEL-001 (Strict) with zero behavioural change; public import path preserved by the package `__init__`.
---
*Generated 2026-08-04 under GoldBot Engineering Law GEL-001 (Strict Canonical Module Rule). Flat `market_regime.py` converted to package form; implementation moved intact, public import path preserved via `__init__` re-export.*
