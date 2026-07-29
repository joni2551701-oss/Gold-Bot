"""
Market Layer — Candle read model (TASK-CORE-005).

A plain OHLCV container the market facade hands to consumers. It holds
NO logic (no indicator, no structure math) -- it is a view adapted from
an upstream candle/event. Adapters accept a stream.StreamEvent or a
data.providers.MarketCandle (the FROZEN provider shape) without
importing either module's internals -- only their public attributes.

This is deliberately a thin, separate view type (not a re-export) so a
consumer of market/ never has to reach back into stream/ or
data/providers/ to read a candle; the market layer is the single facade
(Director decision: market/ is the Facade Layer). It reuses upstream
values verbatim -- it never recomputes OHLCV.
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
    def from_stream_event(cls, event) -> "Candle":
        """Adapt a stream.StreamEvent (public attributes only) into a market Candle."""
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
