"""
GapRecovery -- detect and fill missing candle windows in memory
(v1.1 Phase 1, module 5; architecture §3/§15).

Uses candle_clock (module 3) to enumerate the windows expected between
the last present closed candle and `now`; any missing window is a gap.
Gaps are filled by a windowed `fetch_range` (never a full rebuild) and
merged into memory as source=RECOVERY (existing candles untouched). No
fabrication: only real provider candles fill gaps.

This module never imports from any layer above data/.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional

from core.logger import setup_logger
from data.candle_clock import CandleClock
from data.memory.market_memory import MarketMemory
from data.memory.candle_record import CandleSource
from data.bootstrap.historical_provider import HistoricalProvider

logger = setup_logger("GapRecovery")


class GapRecovery:
    """Windowed gap detection + fill for one asset's memory."""

    def __init__(self, memory: MarketMemory, provider: HistoricalProvider,
                 clock: Optional[CandleClock] = None):
        self._memory = memory
        self._provider = provider
        self._clock = clock or CandleClock()

    def has_gap(self, timeframe: str, now: datetime) -> bool:
        last = self._memory.timeframe(timeframe).get_last_closed()
        if last is None:
            return False   # nothing to gap-fill; cold load handles empty
        expected_prev = self._clock.window_start(timeframe, now) - timedelta(
            minutes=self._clock.minutes(timeframe))
        return last.timestamp < expected_prev

    def recover(self, timeframe: str, now: datetime) -> int:
        """
        Fill any gap between the last present closed candle and `now`.
        Returns the number of candles inserted.
        """
        tfm = self._memory.timeframe(timeframe)
        last = tfm.get_last_closed()
        if last is None:
            return 0
        step = timedelta(minutes=self._clock.minutes(timeframe))
        start = last.timestamp + step
        end = self._clock.window_start(timeframe, now)   # exclusive of forming window
        if start >= end:
            return 0
        candles = self._provider.fetch_range(
            self._memory.asset, timeframe, start, end)
        if not candles:
            return 0
        inserted = tfm.merge_closed(candles, source=CandleSource.RECOVERY)
        if inserted:
            logger.info("GapRecovery[%s|%s] filled %d candle(s)",
                        self._memory.asset, timeframe, inserted)
        return inserted
