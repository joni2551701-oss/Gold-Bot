"""data_layer/live_data/market/session_state -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `session_state.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `session_state.py`.
"""
from data_layer.live_data.market.session_state.session_state import (
    dataclass,
    datetime,
    Optional,
    is_weekend,
    SessionState,
)

__all__ = [
    "dataclass",
    "datetime",
    "Optional",
    "is_weekend",
    "SessionState",
]
