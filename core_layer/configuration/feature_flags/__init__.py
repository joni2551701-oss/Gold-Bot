"""core_layer/configuration/feature_flags -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `feature_flags.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `feature_flags.py`.
"""
from core_layer.configuration.feature_flags.feature_flags import (
    dataclass,
    FeatureFlags,
    DEFAULT_FLAGS,
)

__all__ = [
    "dataclass",
    "FeatureFlags",
    "DEFAULT_FLAGS",
]
