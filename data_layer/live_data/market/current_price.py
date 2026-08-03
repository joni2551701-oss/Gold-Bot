"""
Market Layer — Current Price read point (TASK-CORE-005; canonicalized
TASK-ARCH-101 PART-03).

The market projection's fast "what is the latest price?" accessor. It
does NOT keep history and does NOT compute a signal.

Canonical source (Owner ruling, Option 3A): the latest price is read
from the Data Layer's `data_layer.market_memory.MemoryReader` (MA-002) — the
canonical read surface over `MarketMemory` — NOT from the now-DEPRECATED
`stream/`. `market/` (the Application-Services-tier Market Projection)
consumes Data Layer output via `MemoryReader` and Core output via
`ContextSnapshotSchema`; it introduces no other dependency. This module
provides the market-facing value object (`MarketPrice`) and a fail-safe
helper that READS the freshest last candle from a `MemoryReader`. No
secret is read or logged here.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class MarketPrice:
    """The market projection's latest-price value. The projection's own
    read type (Application-Services tier)."""
    symbol: str
    price: float
    timestamp: Optional[datetime] = None
    provider: Optional[str] = None

    @classmethod
    def from_price_point(cls, point) -> Optional["MarketPrice"]:
        """Adapt any point-like value with public `symbol`/`price`
        (+ optional `timestamp`/`provider`) attributes into a
        MarketPrice. None-safe: returns None for a None point."""
        if point is None:
            return None
        return cls(symbol=point.symbol, price=point.price,
                   timestamp=getattr(point, "timestamp", None),
                   provider=getattr(point, "provider", None))

    @classmethod
    def from_candle_record(cls, symbol: str, record) -> Optional["MarketPrice"]:
        """Adapt a `data_layer.market_memory` CandleRecord (the shape `MemoryReader`
        returns) into a MarketPrice: `close` is the latest price,
        `last_update_time`/`timestamp` its time. None-safe."""
        if record is None:
            return None
        ts = getattr(record, "last_update_time", None) or getattr(record, "timestamp", None)
        return cls(symbol=symbol, price=record.close, timestamp=ts, provider=None)


def read_current_price(memory_reader, symbol: str,
                       timeframe: Optional[str] = None) -> Optional[MarketPrice]:
    """
    Read `symbol`'s latest price from a `data_layer.market_memory.MemoryReader` and
    return it as a MarketPrice, or None if unknown. Reads the freshest
    `get_last_candle` (forming if present, else last closed) across the
    asset's timeframes — or just `timeframe` when given. Pure read:
    never writes, never computes, never raises for a missing symbol/
    unregistered asset (fail-safe → None), matching the projection's
    "missing data → None/UNKNOWN" posture.
    """
    if memory_reader is None:
        return None
    try:
        timeframes = [timeframe] if timeframe else memory_reader.timeframes(symbol)
        best = None  # freshest CandleRecord
        for tf in timeframes:
            rec = memory_reader.get_last_candle(symbol, tf)
            if rec is None:
                continue
            if best is None or rec.timestamp > best.timestamp:
                best = rec
        return MarketPrice.from_candle_record(symbol, best)
    except Exception:  # noqa: BLE001 -- fail-safe read (unknown asset, etc.)
        return None
