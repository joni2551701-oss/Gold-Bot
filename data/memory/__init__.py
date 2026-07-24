"""
data.memory -- GoldBot v1.1 Market Data Foundation: Multi-Timeframe
Memory Engine (MarketMemory Core, Phase 1 module 1).

The in-RAM, thread-safe store of market candles that every higher layer
reads through (Memory-First). This package holds ONLY the memory core:

- candle_record.py         -- CandleRecord model + status/source/mode enums
- timeframe_memory.py      -- per-timeframe thread-safe ring buffer + revision
- market_memory.py         -- per-asset multi-timeframe container (LIVE/REPLAY)
- market_memory_registry.py-- asset -> MarketMemory (no singleton, multi-asset)

Deliberately NOT here yet (later Phase 1 modules, per
docs/architecture/MARKET_DATA_FOUNDATION.md §25): the MemoryReader
facade, CandleBuilder, PriceStream, the event bus, snapshot serialization,
and the Central Data Manager.

Reuse (Constitution Art. 11): the OHLC+timestamp core reuses the existing
frozen `data.twelve_data_client.Candle` (via CandleRecord.to_candle()),
so the rest of `data/` keeps consuming `List[Candle]` unchanged.

This package never imports from telegram/, ai/, decision/, risk/,
strategies/, signals/, context/, or database/ -- it is the bottom of the
data layer.
"""

from data.memory.candle_record import (
    CandleRecord,
    CandleStatus,
    CandleSource,
    MemoryMode,
)
from data.memory.timeframe_memory import TimeframeMemory
from data.memory.market_memory import MarketMemory
from data.memory.memory_reader import MemoryReader
from data.memory.market_memory_registry import (
    MarketMemoryRegistry,
    DuplicateAssetError,
    UnknownAssetError,
    DEFAULT_TIMEFRAME_CAPACITY,
    build_default_registry,
)

__all__ = [
    "CandleRecord",
    "CandleStatus",
    "CandleSource",
    "MemoryMode",
    "TimeframeMemory",
    "MarketMemory",
    "MemoryReader",
    "MarketMemoryRegistry",
    "DuplicateAssetError",
    "UnknownAssetError",
    "DEFAULT_TIMEFRAME_CAPACITY",
    "build_default_registry",
]
