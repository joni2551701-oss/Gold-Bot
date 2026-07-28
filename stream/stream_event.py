"""
Stream Layer — Stream Event model (TASK-CORE-004).

StreamEvent is the single, standard shape every real-time market
update takes once it enters the stream layer. Raw provider output
(data/providers/base_provider.py's MarketCandle) is adapted into a
StreamEvent BEFORE anything downstream (validator, state, router,
subscribers) touches it -- a consumer never sees a raw provider
response, only this uniform event.

Relationship to data/providers/ (FROZEN): StreamEvent does NOT
replace MarketCandle. MarketCandle is the provider layer's output
shape; StreamEvent is the stream layer's transport shape and adds two
stream-only fields the provider layer has no concept of:

    source   -- the stream channel/origin this event arrived through
                (e.g. "provider", "poll", "replay") -- lets a future
                WebSocket/live transport and today's poll path be told
                apart without changing the provider contract.
    (provider is carried through unchanged from MarketCandle.provider)

from_candle() is the one adapter; a future WebSocket frame parser
would build a StreamEvent the same way. This module holds NO signal,
strategy, decision, risk, or rendering logic -- it is a plain data
model (CLAUDE.md: stream/ is "faqat data oqimi").
"""

from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class StreamEvent:
    """
    One standardized real-time market event. Mirrors MarketCandle's
    OHLC shape and adds `source` (stream origin) alongside `provider`
    (upstream provider name), exactly the fields TASK-CORE-004 names:
    symbol, timeframe, timestamp, open, high, low, close, volume,
    source, provider.

    volume stays Optional and is never fabricated (same posture as
    MarketCandle -- TwelveData does not return volume for XAU/USD).
    """
    symbol: str
    timeframe: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: Optional[float] = None
    source: str = "provider"
    provider: Optional[str] = None

    def to_dict(self) -> dict:
        data = asdict(self)
        data["timestamp"] = self.timestamp.isoformat() if self.timestamp else None
        return data

    @classmethod
    def from_candle(cls, candle, source: str = "provider") -> "StreamEvent":
        """
        Adapt one data.providers.base_provider.MarketCandle into a
        StreamEvent. Reads only the candle's public attributes (never
        mutates it, never imports the provider package's internals), so
        the FROZEN provider contract is untouched. `source` labels how
        this event entered the stream (defaults to "provider").
        """
        return cls(
            symbol=candle.symbol,
            timeframe=candle.timeframe,
            timestamp=candle.timestamp,
            open=candle.open,
            high=candle.high,
            low=candle.low,
            close=candle.close,
            volume=getattr(candle, "volume", None),
            source=source,
            provider=getattr(candle, "provider", None),
        )
