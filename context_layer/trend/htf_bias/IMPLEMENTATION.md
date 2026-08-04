# IMPLEMENTATION.md — context_layer/trend/htf_bias

## `htf_bias.py`

Public surface:

- `dataclass`
- `Enum`
- `Dict`
- `Sequence`
- `Tuple`
- `MarketSnapshot`
- `Candle`
- `ContextConfig`
- `detect_swing_points`
- `classify_structure`
- `most_recent_bias`
- `setup_logger`
- `logger`
- `SUPPORTED_HTF_TIMEFRAMES`
- `HTFBias`
- `HTFBiasResult`
- `compute_htf_bias`

## Design Notes

Converted from a flat `htf_bias.py` to a canonical package under GEL-001 (Strict) with zero behavioural change; public import path preserved by the package `__init__`.
---
*Generated 2026-08-04 under GoldBot Engineering Law GEL-001 (Strict Canonical Module Rule). Flat `htf_bias.py` converted to package form; implementation moved intact, public import path preserved via `__init__` re-export.*
