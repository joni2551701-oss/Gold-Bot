# IMPLEMENTATION.md — core_layer/emergency/circuit_breaker

## `circuit_breaker.py`

Public surface:

- `dataclass`
- `Enum`
- `Optional`
- `DEFAULT_MAX_CONSECUTIVE_LOSSES`
- `DEFAULT_MAX_DAILY_DRAWDOWN`
- `CircuitDecision`
- `CircuitBreakerInput`
- `CircuitBreakerResult`
- `evaluate_circuit`

## Design Notes

Converted from a flat `circuit_breaker.py` to a canonical package under GEL-001 (Strict) with zero behavioural change; public import path preserved by the package `__init__`.
---
*Generated 2026-08-04 under GoldBot Engineering Law GEL-001 (Strict Canonical Module Rule). Flat `circuit_breaker.py` converted to package form; implementation moved intact, public import path preserved via `__init__` re-export.*
