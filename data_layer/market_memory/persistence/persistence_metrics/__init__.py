"""data_layer/market_memory/persistence/persistence_metrics -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `persistence_metrics.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `persistence_metrics.py`.
"""
from data_layer.market_memory.persistence.persistence_metrics.persistence_metrics import (
    annotations,
    dataclass,
    PersistenceMetrics,
)

__all__ = [
    "annotations",
    "dataclass",
    "PersistenceMetrics",
]
