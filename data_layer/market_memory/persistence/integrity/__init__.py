"""data_layer/market_memory/persistence/integrity -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `integrity.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `integrity.py`.
"""
from data_layer.market_memory.persistence.integrity.integrity import (
    annotations,
    dataclass,
    field,
    timedelta,
    List,
    Dict,
    Candle,
    CandleClock,
    MarketMemory,
    IntegrityReport,
    check_series,
    check_integrity,
)

__all__ = [
    "annotations",
    "dataclass",
    "field",
    "timedelta",
    "List",
    "Dict",
    "Candle",
    "CandleClock",
    "MarketMemory",
    "IntegrityReport",
    "check_series",
    "check_integrity",
]
