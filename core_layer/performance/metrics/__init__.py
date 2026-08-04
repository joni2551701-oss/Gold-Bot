"""core_layer/performance/metrics -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `metrics.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `metrics.py`.
"""
from core_layer.performance.metrics.metrics import (
    json,
    uuid,
    dataclass,
    field,
    datetime,
    timezone,
    Any,
    Dict,
    List,
    Optional,
    ALLOWED_STATUSES,
    METRIC_PIPELINE_TOTAL_TIME,
    METRIC_MARKET_DATA_FETCH_TIME,
    METRIC_CONTEXT_BUILD_TIME,
    METRIC_STRATEGY_EXECUTION_TIME,
    METRIC_AI_ANALYSIS_TIME,
    METRIC_DECISION_TIME,
    METRIC_DATABASE_QUERY_TIME,
    generate_metric_id,
    PerformanceMetric,
    ValidationResult,
    validate_metric,
)

__all__ = [
    "json",
    "uuid",
    "dataclass",
    "field",
    "datetime",
    "timezone",
    "Any",
    "Dict",
    "List",
    "Optional",
    "ALLOWED_STATUSES",
    "METRIC_PIPELINE_TOTAL_TIME",
    "METRIC_MARKET_DATA_FETCH_TIME",
    "METRIC_CONTEXT_BUILD_TIME",
    "METRIC_STRATEGY_EXECUTION_TIME",
    "METRIC_AI_ANALYSIS_TIME",
    "METRIC_DECISION_TIME",
    "METRIC_DATABASE_QUERY_TIME",
    "generate_metric_id",
    "PerformanceMetric",
    "ValidationResult",
    "validate_metric",
]
