"""data_layer/normalization/timeframe_mapper -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `timeframe_mapper.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `timeframe_mapper.py`.
"""
from data_layer.normalization.timeframe_mapper.timeframe_mapper import (
    Dict,
    to_provider_timeframe,
    from_provider_timeframe,
    is_known_timeframe,
)

__all__ = [
    "Dict",
    "to_provider_timeframe",
    "from_provider_timeframe",
    "is_known_timeframe",
]
