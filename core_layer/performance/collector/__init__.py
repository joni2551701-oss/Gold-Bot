"""core_layer/performance/collector -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `collector.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `collector.py`.
"""
from core_layer.performance.collector.collector import (
    List,
    PerformanceMetric,
    PerformanceCollector,
)

__all__ = [
    "List",
    "PerformanceMetric",
    "PerformanceCollector",
]
