"""data_layer/live_data/market/regime_state -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `regime_state.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `regime_state.py`.
"""
from data_layer.live_data.market.regime_state.regime_state import (
    dataclass,
    RegimeState,
)

__all__ = [
    "dataclass",
    "RegimeState",
]
