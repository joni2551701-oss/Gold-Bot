"""
CandleBuilder -- aggregates a price stream into OHLC candles across all
timeframes and writes them into a MarketMemory (v1.1 Phase 1, module 3).

Design (docs/architecture/CANDLE_BUILDER.md, DD-039 + DD-042..DD-045):

- Single Writer (DD/§6): one CandleBuilder per asset is the sole writer of
  that asset's TimeframeMemories; it must be driven by a single thread.
  Readers (MemoryReader) stay consistent via the memories' own locks +
  copy-on-read.
- Clock Independence (DD-044): the builder NEVER reads the system clock.
  Every time value comes from a caller-supplied `timestamp`/`now`, so
  output is a pure function of the input event sequence -> deterministic
  and replay-safe (DD-042, DD-033).
- Event Ordering (DD-045): when one price touches several timeframe
  boundaries, timeframes are processed in the strict order M1 -> M5 ->
  M15 -> H1 -> H4 -> D1 (TIMEFRAME_ORDER), giving EventBus (module 7) and
  Snapshot (module 9) a predictable emission order.
- No business/signal logic: pure OHLC aggregation + candle lifecycle.

The builder emits lifecycle events through a CandleEventHook (default
no-op); module 7 (Event Bus) plugs the real bus in without changing this
module. This module never imports from any layer above data/.
"""

from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Optional, List, Any, Dict

from core_layer.logger.logger import setup_logger
from data.candle_clock import CandleClock, TIMEFRAME_ORDER
from data.memory.market_memory import MarketMemory
from data.memory.candle_record import CandleRecord, CandleSource

logger = setup_logger("CandleBuilder")


class CandleEventHook:
    """
    No-op lifecycle hook. Module 7 (Event Bus) subclasses / replaces this
    to fan candle transitions out to subscribers. Hook methods must not
    raise into the builder; the builder isolates exceptions regardless.
    """

    def on_new_candle(self, record: CandleRecord) -> None:      # pragma: no cover
        pass

    def on_candle_update(self, record: CandleRecord) -> None:   # pragma: no cover
        pass

    def on_candle_close(self, record: CandleRecord) -> None:    # pragma: no cover
        pass


class CandleBuilder:
    """Aggregates prices into OHLC candles for one asset (single writer)."""

    def __init__(self, asset: str, memory: MarketMemory,
                 clock: Optional[CandleClock] = None,
                 event_hook: Optional[CandleEventHook] = None,
                 timeframes: Optional[List[str]] = None):
        if memory is None:
            raise ValueError("memory must not be None")
        self._asset = asset
        self._memory = memory
        self._clock = clock or CandleClock()
        self._hook = event_hook or CandleEventHook()
        # Process timeframes the memory actually holds, in DD-045 order.
        held = set(memory.timeframes())
        ordered = [tf for tf in TIMEFRAME_ORDER if tf in held]
        # Any memory timeframe not in the canonical order is appended
        # deterministically (sorted) after the canonical six.
        extra = sorted(held - set(ordered))
        self._timeframes = (timeframes
                            if timeframes is not None else ordered + extra)
        self._stats: Dict[str, int] = {
            "processed": 0, "opened": 0, "updated": 0, "closed": 0,
            "dropped_out_of_order": 0, "rejected": 0, "gaps": 0,
            "hook_errors": 0,
        }

    @property
    def asset(self) -> str:
        return self._asset

    def timeframes(self) -> List[str]:
        return list(self._timeframes)

    def stats(self) -> Dict[str, int]:
        return dict(self._stats)

    # -- ingress --------------------------------------------------------
    def on_price(self, price: float, timestamp: datetime,
                 volume: Optional[float] = None,
                 source: CandleSource = CandleSource.STREAM) -> None:
        """
        Apply one price observation to every timeframe. `timestamp` must
        be timezone-aware UTC (DD-044: the builder never invents time).
        """
        if not self._valid_price(price) or not self._valid_time(timestamp):
            self._stats["rejected"] += 1
            return
        ts = timestamp.astimezone(timezone.utc)
        self._stats["processed"] += 1
        for tf in self._timeframes:
            self._apply_timeframe(tf, price, ts, volume, source)

    def on_event(self, event: Any) -> None:
        """
        Convenience for a duck-typed stream event (module 4's StreamEvent
        will satisfy this): needs `.price` and `.timestamp`; `.volume` and
        `.source` are optional.
        """
        self.on_price(
            price=event.price,
            timestamp=event.timestamp,
            volume=getattr(event, "volume", None),
            source=getattr(event, "source", CandleSource.STREAM),
        )

    def flush(self, now: datetime) -> None:
        """
        Close any timeframe whose current window has ended as of `now`
        with no new price to trigger it (quiet-period handling). Opens no
        new candle (there is no price). `now` is caller-supplied (DD-044).
        """
        if not self._valid_time(now):
            self._stats["rejected"] += 1
            return
        now = now.astimezone(timezone.utc)
        for tf in self._timeframes:
            tfm = self._memory.timeframe(tf)
            forming = tfm.get_forming()
            if forming is None:
                continue
            if now >= self._clock.next_boundary(tf, forming.timestamp):
                closed = tfm.close_forming(when=now)
                if closed is not None:
                    self._stats["closed"] += 1
                    self._emit_close(closed)

    # -- per-timeframe core --------------------------------------------
    def _apply_timeframe(self, tf: str, price: float, ts: datetime,
                         volume: Optional[float],
                         source: CandleSource) -> None:
        tfm = self._memory.timeframe(tf)
        win = self._clock.window_start(tf, ts)
        forming = tfm.get_forming()

        if forming is None:
            rec = tfm.open_candle(win, price, source=source,
                                  volume=volume, when=ts)
            self._stats["opened"] += 1
            self._emit_new(rec)
            return

        if win == forming.timestamp:
            rec = tfm.update_forming(price, when=ts, volume=volume)
            self._stats["updated"] += 1
            self._emit_update(rec)
        elif win > forming.timestamp:
            # boundary crossed -> close the old window, open the new one.
            # A multi-window jump is a gap: we do NOT fabricate the
            # skipped candles (gap-fill is recovery, module 5).
            if win > self._clock.next_boundary(tf, forming.timestamp):
                self._stats["gaps"] += 1
            closed = tfm.close_forming(when=ts)
            if closed is not None:
                self._stats["closed"] += 1
                self._emit_close(closed)
            rec = tfm.open_candle(win, price, source=source,
                                  volume=volume, when=ts)
            self._stats["opened"] += 1
            self._emit_new(rec)
        else:
            # win < forming.timestamp: an event older than the current
            # window. Never mutate a formed/closed window; drop it.
            self._stats["dropped_out_of_order"] += 1

    # -- validation -----------------------------------------------------
    @staticmethod
    def _valid_price(price: Any) -> bool:
        return isinstance(price, (int, float)) and math.isfinite(price)

    @staticmethod
    def _valid_time(ts: Any) -> bool:
        return isinstance(ts, datetime) and ts.tzinfo is not None

    # -- hook emission (exceptions isolated) ---------------------------
    def _emit_new(self, record: CandleRecord) -> None:
        self._safe_hook(self._hook.on_new_candle, record)

    def _emit_update(self, record: CandleRecord) -> None:
        self._safe_hook(self._hook.on_candle_update, record)

    def _emit_close(self, record: CandleRecord) -> None:
        self._safe_hook(self._hook.on_candle_close, record)

    def _safe_hook(self, fn, record: CandleRecord) -> None:
        try:
            fn(record)
        except Exception:  # a bad subscriber must never corrupt ingestion
            self._stats["hook_errors"] += 1
            logger.exception("CandleBuilder event hook raised; ignoring")
