"""core_layer/performance/timer -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `timer.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `timer.py`.
"""
from core_layer.performance.timer.timer import (
    functools,
    time,
    datetime,
    timezone,
    Any,
    Callable,
    Dict,
    Optional,
    GoldBotError,
    setup_logger,
    PerformanceCollector,
    PerformanceMetric,
    generate_metric_id,
    logger,
    PerformanceTimer,
    measure_performance,
)

__all__ = [
    "functools",
    "time",
    "datetime",
    "timezone",
    "Any",
    "Callable",
    "Dict",
    "Optional",
    "GoldBotError",
    "setup_logger",
    "PerformanceCollector",
    "PerformanceMetric",
    "generate_metric_id",
    "logger",
    "PerformanceTimer",
    "measure_performance",
]
