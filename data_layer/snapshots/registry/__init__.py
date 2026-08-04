"""data_layer/snapshots/registry -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `registry.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `registry.py`.
"""
from data_layer.snapshots.registry.registry import (
    annotations,
    datetime,
    List,
    Optional,
    SnapshotCatalog,
    CatalogEntry,
    SnapshotRegistry,
)

__all__ = [
    "annotations",
    "datetime",
    "List",
    "Optional",
    "SnapshotCatalog",
    "CatalogEntry",
    "SnapshotRegistry",
]
