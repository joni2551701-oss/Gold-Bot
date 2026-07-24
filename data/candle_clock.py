"""
CandleClock -- pure, deterministic timeframe-boundary math (v1.1 Phase 1,
Candle Builder companion).

Given a timeframe and an arbitrary instant, computes the candle window
that instant belongs to, and the next boundary. Stateless and pure:
never reads the system clock (DD-044) -- every answer is a function of
its arguments only, so it is fully deterministic and replay-safe.

Reuse (Constitution Art. 11): generalizes the window logic already in
`data.data_cache.SmartDataCache._get_next_candle_time` (which covers
M5/M15/H1/H4 with a provider-latency buffer) to all six Phase 1
timeframes (M1..D1) and without the latency buffer -- boundary math for
in-memory candle building is exact, not fetch-scheduling. The original
remains the fetch scheduler; this is the builder's clock.

Timeframes are minute-aligned from the UTC epoch day boundary. D1 aligns
to 00:00 UTC. This module never imports from any layer above data/.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone


# Canonical timeframe -> minutes-per-candle (all six ON, DD-026).
TIMEFRAME_MINUTES = {
    "M1": 1,
    "M5": 5,
    "M15": 15,
    "H1": 60,
    "H4": 240,
    "D1": 1440,
}

# Strict processing order when one event touches several timeframes
# (DD-045): smallest -> largest.
TIMEFRAME_ORDER = ["M1", "M5", "M15", "H1", "H4", "D1"]


def _require_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        raise ValueError("timestamp must be timezone-aware (UTC)")
    return dt.astimezone(timezone.utc)


class CandleClock:
    """Pure timeframe-boundary calculator (no system-clock access)."""

    _EPOCH = datetime(1970, 1, 1, tzinfo=timezone.utc)

    def minutes(self, timeframe: str) -> int:
        try:
            return TIMEFRAME_MINUTES[timeframe]
        except KeyError:
            raise KeyError(
                f"unknown timeframe {timeframe!r}; "
                f"known: {list(TIMEFRAME_MINUTES)}")

    def window_start(self, timeframe: str, dt: datetime) -> datetime:
        """
        The open time of the candle that `dt` belongs to: `dt` floored to
        the timeframe's minute grid, anchored at the UTC epoch (so D1 ->
        00:00 UTC, H4 -> 00/04/08/12/16/20:00, etc.).
        """
        dt = _require_utc(dt)
        step = self.minutes(timeframe)
        total_min = int((dt - self._EPOCH).total_seconds() // 60)
        floored = (total_min // step) * step
        return self._EPOCH + timedelta(minutes=floored)

    def next_boundary(self, timeframe: str, dt: datetime) -> datetime:
        """The open time of the NEXT candle after `dt`'s window."""
        return self.window_start(timeframe, dt) + timedelta(
            minutes=self.minutes(timeframe))

    def is_boundary(self, timeframe: str, dt: datetime) -> bool:
        """True if `dt` is exactly a candle open time for the timeframe."""
        return _require_utc(dt) == self.window_start(timeframe, dt)

    def same_window(self, timeframe: str, a: datetime, b: datetime) -> bool:
        """True if instants `a` and `b` fall in the same candle window."""
        return self.window_start(timeframe, a) == self.window_start(
            timeframe, b)
