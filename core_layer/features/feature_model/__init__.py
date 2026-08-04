"""core_layer/features/feature_model -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `feature_model.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `feature_model.py`.
"""
from core_layer.features.feature_model.feature_model import (
    dataclass,
    Optional,
    MarketFeatures,
)

__all__ = [
    "dataclass",
    "Optional",
    "MarketFeatures",
]
