# IMPLEMENTATION.md — core_layer/gateway/dependency_graph

## `dependency_graph.py`

Public surface:

- `annotations`
- `Dict`
- `Iterable`
- `List`
- `Tuple`
- `DependencyError`
- `missing_dependencies`
- `find_cycle`
- `validate`
- `resolution_order`
- `build_graph`

## Design Notes

Converted from a flat `dependency_graph.py` to a canonical package under GEL-001 (Strict) with zero behavioural change; public import path preserved by the package `__init__`.
---
*Generated 2026-08-04 under GoldBot Engineering Law GEL-001 (Strict Canonical Module Rule). Flat `dependency_graph.py` converted to package form; implementation moved intact, public import path preserved via `__init__` re-export.*
