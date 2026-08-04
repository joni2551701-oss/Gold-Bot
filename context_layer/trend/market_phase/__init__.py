"""context_layer/trend/market_phase -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `market_phase.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `market_phase.py`.
"""
from context_layer.trend.market_phase.market_phase import (
    dataclass,
    Enum,
    TYPE_CHECKING,
    AmdEventType,
    MarketRegime,
    RegimeDirection,
    WyckoffPhase,
    MarketPhase,
    MarketPhaseResult,
    compute_market_phase,
)

__all__ = [
    "dataclass",
    "Enum",
    "TYPE_CHECKING",
    "AmdEventType",
    "MarketRegime",
    "RegimeDirection",
    "WyckoffPhase",
    "MarketPhase",
    "MarketPhaseResult",
    "compute_market_phase",
]
