"""data_layer/snapshots/catalog -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `catalog.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `catalog.py`.
"""
from data_layer.snapshots.catalog.catalog import (
    annotations,
    json,
    dataclass,
    asdict,
    datetime,
    timezone,
    Dict,
    List,
    Optional,
    Tuple,
    SnapshotState,
    VerifyState,
    CORE_VERSION,
    SnapshotManifest,
    CatalogEntry,
    SnapshotCatalog,
    utcnow,
)

__all__ = [
    "annotations",
    "json",
    "dataclass",
    "asdict",
    "datetime",
    "timezone",
    "Dict",
    "List",
    "Optional",
    "Tuple",
    "SnapshotState",
    "VerifyState",
    "CORE_VERSION",
    "SnapshotManifest",
    "CatalogEntry",
    "SnapshotCatalog",
    "utcnow",
]
