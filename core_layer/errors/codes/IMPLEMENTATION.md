# IMPLEMENTATION.md — core_layer/errors/codes

## `codes.py`

Public surface:

- `re`
- `Dict`
- `CODE_PATTERN`
- `CONFIG_001`
- `CONFIG_002`
- `DATA_001`
- `DATA_002`
- `API_001`
- `API_002`
- `API_003`
- `API_004`
- `DB_001`
- `DB_002`
- `VALIDATION_001`
- `VALIDATION_002`
- `PERMISSION_001`
- `STRATEGY_001`
- `DECISION_001`
- `EXECUTION_001`
- `CODE_REGISTRY`
- `is_valid_code_format`
- `is_known_code`

## Design Notes

Converted from a flat `codes.py` to a canonical package under GEL-001 (Strict) with zero behavioural change; public import path preserved by the package `__init__`.
---
*Generated 2026-08-04 under GoldBot Engineering Law GEL-001 (Strict Canonical Module Rule). Flat `codes.py` converted to package form; implementation moved intact, public import path preserved via `__init__` re-export.*
