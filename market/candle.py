"""
Market Layer — Candle read model (TASK-CORE-005).

A plain OHLCV container the market projection hands to consumers. It
holds NO logic (no indicator, no structure math) -- it is a view
adapted from an upstream candle. Adapters accept a `data.memory`
CandleRecord (from `MemoryReader`, the canonical read surface) or a
`data.providers.MarketCandle` (the FROZEN provider shape) without
importing either module's internals -- only their public attributes.

This is deliberately a thin, separate view type (not a re-export) so a
consumer of market/ never has to reach back into `data/` to read a
candle; the market projection is the single facade. It reuses upstream
values verbatim -- it never recomputes OHLCV. (TASK-ARCH-101 PART-03:
re-pointed off the now-DEPRECATED `stream/`; a generic public-attribute
adapter remains for any candle-shaped object.)
"""

from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class Candle:
    """One OHLCV bar as the market layer exposes it. volume stays Optional and is never fabricated (matches the provider/stream posture)."""
    symbol: str
    timeframe: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: Optional[float] = None
    provider: Optional[str] = None

    def to_dict(self) -> dict:
        data = asdict(self)
        data["timestamp"] = self.timestamp.isoformat() if self.timestamp else None
        return data

    @classmethod
    def from_candle_record(cls, symbol: str, record) -> "Candle":
        """Adapt a `data.memory` CandleRecord (from `MemoryReader`; public
        attributes only) into a market Candle. The record carries its own
        `timeframe`; `symbol` is supplied by the caller (CandleRecord is
        keyed per-asset by the memory, not on the record itself)."""
        return cls(
            symbol=symbol, timeframe=record.timeframe, timestamp=record.timestamp,
            open=record.open, high=record.high, low=record.low, close=record.close,
            volume=getattr(record, "volume", None), provider=None,
        )

    @classmethod
    def from_stream_event(cls, event) -> "Candle":
        """Adapt any candle-shaped object exposing public
        `symbol`/`timeframe`/`timestamp`/OHLC attributes into a market
        Candle. Generic and duck-typed -- it imports nothing from
        `stream/` (kept as a backward-compatible adapter name)."""
        return cls(
            symbol=event.symbol, timeframe=event.timeframe, timestamp=event.timestamp,
            open=event.open, high=event.high, low=event.low, close=event.close,
            volume=getattr(event, "volume", None), provider=getattr(event, "provider", None),
        )

    @classmethod
    def from_provider_candle(cls, candle) -> "Candle":
        """Adapt a data.providers.MarketCandle (FROZEN, public attributes only) into a market Candle."""
        return cls(
            symbol=candle.symbol, timeframe=candle.timeframe, timestamp=candle.timestamp,
            open=candle.open, high=candle.high, low=candle.low, close=candle.close,
            volume=getattr(candle, "volume", None), provider=getattr(candle, "provider", None),
        )
