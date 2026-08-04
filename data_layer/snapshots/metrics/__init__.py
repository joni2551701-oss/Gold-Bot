"""data_layer/snapshots/metrics -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `metrics.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `metrics.py`.
"""
from data_layer.snapshots.metrics.metrics import (
    annotations,
    datetime,
    Dict,
    List,
    Optional,
    CatalogEntry,
    SnapshotState,
    VerifyState,
    SnapshotMetrics,
)

__all__ = [
    "annotations",
    "datetime",
    "Dict",
    "List",
    "Optional",
    "CatalogEntry",
    "SnapshotState",
    "VerifyState",
    "SnapshotMetrics",
]
