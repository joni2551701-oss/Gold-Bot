"""data_layer/live_data/market/liquidity_state -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `liquidity_state.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `liquidity_state.py`.
"""
from data_layer.live_data.market.liquidity_state.liquidity_state import (
    dataclass,
    Optional,
    LiquidityState,
)

__all__ = [
    "dataclass",
    "Optional",
    "LiquidityState",
]
