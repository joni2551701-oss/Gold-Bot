"""core_layer/gateway/dependency_graph -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `dependency_graph.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `dependency_graph.py`.
"""
from core_layer.gateway.dependency_graph.dependency_graph import (
    annotations,
    Dict,
    Iterable,
    List,
    Tuple,
    DependencyError,
    missing_dependencies,
    find_cycle,
    validate,
    resolution_order,
    build_graph,
)

__all__ = [
    "annotations",
    "Dict",
    "Iterable",
    "List",
    "Tuple",
    "DependencyError",
    "missing_dependencies",
    "find_cycle",
    "validate",
    "resolution_order",
    "build_graph",
]
