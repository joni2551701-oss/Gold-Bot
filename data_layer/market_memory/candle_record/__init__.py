"""data_layer/market_memory/candle_record -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `candle_record.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `candle_record.py`.
"""
from data_layer.market_memory.candle_record.candle_record import (
    annotations,
    dataclass,
    field,
    datetime,
    date,
    timezone,
    Enum,
    Optional,
    Dict,
    Any,
    Candle,
    CandleStatus,
    CandleSource,
    MemoryMode,
    CandleRecord,
)

__all__ = [
    "annotations",
    "dataclass",
    "field",
    "datetime",
    "date",
    "timezone",
    "Enum",
    "Optional",
    "Dict",
    "Any",
    "Candle",
    "CandleStatus",
    "CandleSource",
    "MemoryMode",
    "CandleRecord",
]
