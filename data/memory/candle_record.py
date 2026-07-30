"""
CandleRecord -- the extended in-memory candle model (DD-027).

Memory stores more than OHLC. Per candle, per timeframe, a CandleRecord
carries: OHLC, timestamp, status, volume, candle_id, sequence_number,
source, last_update_time, session, trading_day, and open metadata --
everything replay (DD-033), chart diffing (DD-029) and AI context need.

Reuse (Constitution Art. 11): the OHLC+timestamp core is interoperable
with the existing frozen `data.twelve_data_client.Candle` via
`to_candle()` / `from_candle()`, so the rest of `data/` keeps working
with `List[Candle]` unchanged. CandleRecord itself is mutable, because a
FORMING candle's OHLC updates as prices arrive; a CLOSED candle is
immutable by convention (never mutated in place) and readers always
receive copies.

This module never imports from any layer above data/.
"""

from __future__ import annotations

import copy as _copy
from dataclasses import dataclass, field
from datetime import datetime, date, timezone
from enum import Enum
from typing import Optional, Dict, Any

from data.twelve_data_client import Candle


class CandleStatus(Enum):
    """Lifecycle status of a candle in memory."""
    FORMING = "forming"   # currently being built from incoming prices
    CLOSED = "closed"     # its timeframe window has ended; immutable


class CandleSource(Enum):
    """
    Where a candle's data originated.

    DD-043 (Source Traceability): STREAM, REPLAY and BOOTSTRAP are the
    canonical Phase 1 values. RECOVERY is an additional, non-canonical
    source used by the recovery/gap-fill path (module 5); further sources
    may be added later without disturbing the canonical three.
    """
    STREAM = "stream"         # live price stream (canonical)
    REPLAY = "replay"         # replay driver, module 8 (canonical)
    BOOTSTRAP = "bootstrap"   # one-time historical load (canonical)
    RECOVERY = "recovery"     # gap-fill / rebuild after a failure (additional)


class MemoryMode(Enum):
    """Operating mode of a MarketMemory (DD-033)."""
    LIVE = "live"       # fed by the live price stream
    REPLAY = "replay"   # fed from stored/snapshotted candles


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class CandleRecord:
    """
    One candle in memory, with full provenance and identity.

    OHLC + `timestamp` (the candle's open time, UTC) are the reusable
    core; the remaining fields are the DD-027 memory extension.
    """
    timestamp: datetime            # candle OPEN time (timezone-aware, UTC)
    open: float
    high: float
    low: float
    close: float
    timeframe: str                 # e.g. "M1", "H4"
    candle_id: str                 # stable unique id: "<asset>:<tf>:<epoch>"
    sequence_number: int           # monotonic per (asset, timeframe)
    status: CandleStatus = CandleStatus.FORMING
    source: CandleSource = CandleSource.STREAM
    trading_day: Optional[date] = None
    session: Optional[str] = None
    volume: Optional[float] = None
    last_update_time: datetime = field(default_factory=_utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def apply_price(self, price: float, when: Optional[datetime] = None,
                    volume: Optional[float] = None) -> None:
        """
        Fold a new price into a FORMING candle: close = price, high/low
        expand, open is preserved. No-op semantics are the caller's
        concern; this raises if the candle is already CLOSED (a closed
        candle is immutable).
        """
        if self.status is CandleStatus.CLOSED:
            raise ValueError(
                f"cannot apply price to a CLOSED candle {self.candle_id!r}"
            )
        self.close = price
        if price > self.high:
            self.high = price
        if price < self.low:
            self.low = price
        if volume is not None:
            self.volume = (self.volume or 0.0) + volume
        self.last_update_time = when or _utcnow()

    def close_candle(self, when: Optional[datetime] = None) -> None:
        """Mark this candle CLOSED (idempotent)."""
        self.status = CandleStatus.CLOSED
        self.last_update_time = when or _utcnow()

    def to_candle(self) -> Candle:
        """
        Return the reusable, frozen OHLC snapshot (the existing
        `data.twelve_data_client.Candle`) for interop with the rest of
        `data/`. Drops the memory-only fields by design.
        """
        return Candle(
            timestamp=self.timestamp,
            open=self.open,
            high=self.high,
            low=self.low,
            close=self.close,
        )

    def copy(self) -> "CandleRecord":
        """
        A deep-enough copy for safe copy-on-read: scalars are immutable,
        `metadata` is deep-copied so a reader can never mutate memory's
        internal dict.
        """
        return CandleRecord(
            timestamp=self.timestamp,
            open=self.open,
            high=self.high,
            low=self.low,
            close=self.close,
            timeframe=self.timeframe,
            candle_id=self.candle_id,
            sequence_number=self.sequence_number,
            status=self.status,
            source=self.source,
            trading_day=self.trading_day,
            session=self.session,
            volume=self.volume,
            last_update_time=self.last_update_time,
            metadata=_copy.deepcopy(self.metadata),
        )

    @staticmethod
    def make_candle_id(asset: str, timeframe: str, timestamp: datetime) -> str:
        """Stable id from asset + timeframe + open-time epoch seconds."""
        return f"{asset}:{timeframe}:{int(timestamp.timestamp())}"

    @classmethod
    def from_candle(
        cls,
        candle: Candle,
        *,
        asset: str,
        timeframe: str,
        sequence_number: int,
        status: CandleStatus = CandleStatus.CLOSED,
        source: CandleSource = CandleSource.BOOTSTRAP,
        trading_day: Optional[date] = None,
        session: Optional[str] = None,
        volume: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> "CandleRecord":
        """Build a CandleRecord from an existing frozen `Candle`."""
        return cls(
            timestamp=candle.timestamp,
            open=candle.open,
            high=candle.high,
            low=candle.low,
            close=candle.close,
            timeframe=timeframe,
            candle_id=cls.make_candle_id(asset, timeframe, candle.timestamp),
            sequence_number=sequence_number,
            status=status,
            source=source,
            trading_day=trading_day or candle.timestamp.date(),
            session=session,
            volume=volume,
            metadata=dict(metadata or {}),
        )
