# IMPLEMENTATION.md — core_layer/errors/exceptions

## `exceptions.py`

Public surface:

- `GoldBotError`
- `ConfigurationError`
- `ValidationError`
- `DataError`
- `ExternalAPIError`
- `DatabaseError`
- `PermissionError`
- `StrategyError`
- `DecisionError`
- `ExecutionError`

## Design Notes

Converted from a flat `exceptions.py` to a canonical package under GEL-001 (Strict) with zero behavioural change; public import path preserved by the package `__init__`.
---
*Generated 2026-08-04 under GoldBot Engineering Law GEL-001 (Strict Canonical Module Rule). Flat `exceptions.py` converted to package form; implementation moved intact, public import path preserved via `__init__` re-export.*
