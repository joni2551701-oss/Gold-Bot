"""core_layer/configuration/runtime_api -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `runtime_api.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `runtime_api.py`.
"""
from core_layer.configuration.runtime_api.runtime_api import (
    dataclass,
    field,
    Any,
    Dict,
    List,
    Optional,
    RuntimeFeatureManager,
    setup_logger,
    logger,
    RuntimeApiResult,
    enable_feature,
    disable_feature,
    feature_status,
    list_runtime_features,
)

__all__ = [
    "dataclass",
    "field",
    "Any",
    "Dict",
    "List",
    "Optional",
    "RuntimeFeatureManager",
    "setup_logger",
    "logger",
    "RuntimeApiResult",
    "enable_feature",
    "disable_feature",
    "feature_status",
    "list_runtime_features",
]
