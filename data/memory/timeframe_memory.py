"""
TimeframeMemory -- one timeframe's independent, thread-safe candle store
(DD-029 revision versioning; DD-013-style single-writer discipline).

Holds a bounded ring buffer of CLOSED candles plus at most one FORMING
candle. Each timeframe is managed independently (its own lock, depth,
revision, and sequence counter) -- matching the architecture's "har
timeframe mustaqil boshqariladi."

Concurrency model (architecture §13):
- One RLock guards all state.
- Writes (open/update/close/hydrate) are the CandleBuilder / bootstrap /
  recovery path; a given TimeframeMemory has a single logical writer.
- Reads return COPIES (copy-on-read) so a reader never holds a reference
  to mutable internal state.
- `revision` increments on every mutation, giving readers an O(1)
  change signal (DD-029) without scanning contents.

This module never imports from any layer above data/.
"""

from __future__ import annotations

import threading
from collections import deque
from datetime import datetime, date
from typing import Optional, List, Dict, Any

from data.twelve_data_client import Candle
from data.memory.candle_record import (
    CandleRecord,
    CandleStatus,
    CandleSource,
)


class TimeframeMemory:
    """Thread-safe store for a single (asset, timeframe)."""

    def __init__(self, asset: str, timeframe: str, capacity: int):
        if capacity <= 0:
            raise ValueError(f"capacity must be > 0, got {capacity}")
        self._asset = asset
        self._timeframe = timeframe
        self._capacity = capacity
        self._lock = threading.RLock()
        self._closed: "deque[CandleRecord]" = deque(maxlen=capacity)
        self._forming: Optional[CandleRecord] = None
        self._revision = 0
        self._seq = 0  # monotonic sequence number per (asset, timeframe)

    # -- identity -------------------------------------------------------
    @property
    def asset(self) -> str:
        return self._asset

    @property
    def timeframe(self) -> str:
        return self._timeframe

    @property
    def capacity(self) -> int:
        return self._capacity

    # -- internal (call under lock) ------------------------------------
    def _next_seq(self) -> int:
        self._seq += 1
        return self._seq

    def _new_record(
        self,
        timestamp: datetime,
        o: float, h: float, low: float, c: float,
        status: CandleStatus,
        source: CandleSource,
        volume: Optional[float],
        session: Optional[str],
        trading_day: Optional[date],
    ) -> CandleRecord:
        return CandleRecord(
            timestamp=timestamp,
            open=o, high=h, low=low, close=c,
            timeframe=self._timeframe,
            candle_id=CandleRecord.make_candle_id(
                self._asset, self._timeframe, timestamp),
            sequence_number=self._next_seq(),
            status=status,
            source=source,
            trading_day=trading_day or timestamp.date(),
            session=session,
            volume=volume,
        )

    # -- writes ---------------------------------------------------------
    def hydrate(self, candles: List[Candle],
                source: CandleSource = CandleSource.BOOTSTRAP,
                session: Optional[str] = None) -> int:
        """
        Load an ordered list of historical CLOSED candles (bootstrap /
        rebuild). Replaces existing closed history and clears any forming
        candle. Returns the number of candles retained (capped at
        capacity). One revision bump for the whole operation.
        """
        with self._lock:
            ordered = sorted(candles, key=lambda c: c.timestamp)
            self._closed.clear()
            self._forming = None
            for c in ordered:
                rec = self._new_record(
                    c.timestamp, c.open, c.high, c.low, c.close,
                    CandleStatus.CLOSED, source, None, session, None)
                self._closed.append(rec)
            self._revision += 1
            return len(self._closed)

    def open_candle(self, timestamp: datetime, price: float,
                    source: CandleSource = CandleSource.STREAM,
                    volume: Optional[float] = None,
                    session: Optional[str] = None,
                    trading_day: Optional[date] = None) -> CandleRecord:
        """
        Open a new FORMING candle at `timestamp` seeded with `price`
        (O=H=L=C=price). If a forming candle already exists it is closed
        first (it should have been closed by the caller on a boundary;
        this is a safety net). Returns a copy of the opened candle.
        """
        with self._lock:
            if self._forming is not None:
                self._forming.close_candle(timestamp)
                self._closed.append(self._forming)
                self._forming = None
            rec = self._new_record(
                timestamp, price, price, price, price,
                CandleStatus.FORMING, source, volume, session, trading_day)
            self._forming = rec
            self._revision += 1
            return rec.copy()

    def update_forming(self, price: float,
                       when: Optional[datetime] = None,
                       volume: Optional[float] = None) -> CandleRecord:
        """
        Fold a price into the current FORMING candle. Raises if there is
        no forming candle. Returns a copy of the updated candle.
        """
        with self._lock:
            if self._forming is None:
                raise ValueError(
                    f"{self._asset}:{self._timeframe} has no forming candle")
            self._forming.apply_price(price, when=when, volume=volume)
            self._revision += 1
            return self._forming.copy()

    def close_forming(self, when: Optional[datetime] = None
                      ) -> Optional[CandleRecord]:
        """
        Close the current FORMING candle and append it to closed history.
        Returns a copy of the closed candle, or None if none was forming.
        """
        with self._lock:
            if self._forming is None:
                return None
            self._forming.close_candle(when)
            closed = self._forming
            self._closed.append(closed)
            self._forming = None
            self._revision += 1
            return closed.copy()

    # -- reads (copy-on-read) ------------------------------------------
    def revision(self) -> int:
        with self._lock:
            return self._revision

    def get_forming(self) -> Optional[CandleRecord]:
        with self._lock:
            return self._forming.copy() if self._forming is not None else None

    def get_last_closed(self) -> Optional[CandleRecord]:
        with self._lock:
            return self._closed[-1].copy() if self._closed else None

    def get_last(self) -> Optional[CandleRecord]:
        """Forming candle if present, else the last closed candle."""
        with self._lock:
            if self._forming is not None:
                return self._forming.copy()
            return self._closed[-1].copy() if self._closed else None

    def get_series(self, n: Optional[int] = None,
                   include_forming: bool = False) -> List[CandleRecord]:
        """
        Return up to the last `n` candles (oldest -> newest) as copies.
        With `include_forming`, the forming candle is appended last.
        `n=None` returns the whole closed buffer.
        """
        with self._lock:
            items = list(self._closed)
            if include_forming and self._forming is not None:
                items.append(self._forming)
            if n is not None:
                items = items[-n:]
            return [rec.copy() for rec in items]

    def closed_count(self) -> int:
        with self._lock:
            return len(self._closed)

    def health(self) -> Dict[str, Any]:
        """A small status dict for the health monitor / snapshot."""
        with self._lock:
            last = self._closed[-1] if self._closed else None
            return {
                "asset": self._asset,
                "timeframe": self._timeframe,
                "capacity": self._capacity,
                "closed_count": len(self._closed),
                "has_forming": self._forming is not None,
                "revision": self._revision,
                "last_sequence": self._seq,
                "last_closed_time": last.timestamp.isoformat() if last else None,
            }
