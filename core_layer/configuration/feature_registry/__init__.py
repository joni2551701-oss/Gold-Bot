"""core_layer/configuration/feature_registry -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `feature_registry.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `feature_registry.py`.
"""
from core_layer.configuration.feature_registry.feature_registry import (
    dataclass,
    List,
    Config,
    DEFAULT_FLAGS,
    FeatureDescriptor,
    build_feature_registry,
)

__all__ = [
    "dataclass",
    "List",
    "Config",
    "DEFAULT_FLAGS",
    "FeatureDescriptor",
    "build_feature_registry",
]
