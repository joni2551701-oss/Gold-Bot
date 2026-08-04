# IMPLEMENTATION.md — data_layer/event_system/producer_bridges

## `producer_bridges.py`

Public surface:

- `annotations`
- `itertools`
- `uuid`
- `datetime`
- `timezone`
- `Callable`
- `Optional`
- `CandleEventHook`
- `BootstrapEventHook`
- `BootstrapState`
- `EventBus`
- `Event`
- `EventType`
- `EventPriority`
- `CandleEventBridge`
- `BootstrapEventBridge`

## Design Notes

Converted from a flat `producer_bridges.py` to a canonical package under GEL-001 (Strict) with zero behavioural change; public import path preserved by the package `__init__`.
---
*Generated 2026-08-04 under GoldBot Engineering Law GEL-001 (Strict Canonical Module Rule). Flat `producer_bridges.py` converted to package form; implementation moved intact, public import path preserved via `__init__` re-export.*
