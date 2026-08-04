# IMPLEMENTATION.md — core_layer/gateway/service

## `service.py`

Public surface:

- `annotations`
- `Any`
- `Callable`
- `ServiceManifest`
- `ServiceState`
- `assert_transition`
- `ServiceCircuitBreaker`
- `GatewayContext`
- `ServiceHandler`
- `RegisteredService`

## Design Notes

Converted from a flat `service.py` to a canonical package under GEL-001 (Strict) with zero behavioural change; public import path preserved by the package `__init__`.
---
*Generated 2026-08-04 under GoldBot Engineering Law GEL-001 (Strict Canonical Module Rule). Flat `service.py` converted to package form; implementation moved intact, public import path preserved via `__init__` re-export.*
