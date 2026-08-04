"""core_layer/configuration/runtime_state -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `runtime_state.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `runtime_state.py`.
"""
from core_layer.configuration.runtime_state.runtime_state import (
    dataclass,
    datetime,
    timezone,
    Dict,
    List,
    Optional,
    FeatureRuntimeState,
    create_feature_runtime_state,
    RuntimeStateCache,
)

__all__ = [
    "dataclass",
    "datetime",
    "timezone",
    "Dict",
    "List",
    "Optional",
    "FeatureRuntimeState",
    "create_feature_runtime_state",
    "RuntimeStateCache",
]
