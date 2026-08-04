"""core_layer/features/feature_engine -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `feature_engine.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `feature_engine.py`.
"""
from core_layer.features.feature_engine.feature_engine import (
    Optional,
    TYPE_CHECKING,
    MarketRegime,
    MarketFeatures,
    compute_market_features,
)

__all__ = [
    "Optional",
    "TYPE_CHECKING",
    "MarketRegime",
    "MarketFeatures",
    "compute_market_features",
]
