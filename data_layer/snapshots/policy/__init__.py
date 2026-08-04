"""data_layer/snapshots/policy -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `policy.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `policy.py`.
"""
from data_layer.snapshots.policy.policy import (
    annotations,
    dataclass,
    datetime,
    timedelta,
    List,
    Optional,
    Tuple,
    CatalogEntry,
    SnapshotPolicy,
)

__all__ = [
    "annotations",
    "dataclass",
    "datetime",
    "timedelta",
    "List",
    "Optional",
    "Tuple",
    "CatalogEntry",
    "SnapshotPolicy",
]
