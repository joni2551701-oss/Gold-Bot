"""
ForexMarketCalendar -- canonical Forex 24x5 market calendar for the
Live Data stream (TASK-ARCH-101, migrated from the legacy
`data_layer/live_data/stream/stream_mode.py`'s clock, TASK-CORE-004).

Reuse-First (Constitution Article 7): `data_layer.live_data.price_stream` already
defines the `MarketCalendar` Protocol (`is_open(now)` / `next_open(now)`)
and an `AlwaysOpenCalendar` (24/7 crypto). This module adds the missing
CONCRETE Forex implementation of that SAME protocol -- it is not a new
abstraction. A `PriceStream` constructed with
`calendar=ForexMarketCalendar()` gets the legacy `StreamMode`'s
weekend/market-closed behavior for free through `PriceStream`'s existing
waiting-mode machinery (DD-047): when the market is closed the stream
disconnects, makes no provider calls, idles, and auto-resumes on reopen
-- exactly what the legacy `resolve_mode()` + `WEEKEND_WAIT` gated,
now expressed via the canonical lifecycle state machine rather than a
parallel mode enum.

The Forex/XAUUSD weekly session in UTC: opens Sunday 22:00, closes
Friday 22:00. Saturday is always closed; Sunday before 22:00 and Friday
from 22:00 on are closed. This is a coarse, documented default, not an
exchange-holiday calendar (a later, separately-approved addition), same
scope as the legacy clock it replaces.

The module-level `is_weekend()` / `is_market_open()` helpers are kept
(same names/semantics as the legacy `data_layer/live_data/stream/stream_mode.py`) so the
capability is fully present in the canonical layer for any caller that
wants the boolean clock without a full calendar instance.

This module never imports from any layer above data/.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional

# Forex/XAUUSD weekly session in UTC (same constants as the legacy clock).
_MONDAY = 0
_FRIDAY = 4
_SATURDAY = 5
_SUNDAY = 6
_WEEK_OPEN_HOUR = 22    # Sunday 22:00 UTC
_WEEK_CLOSE_HOUR = 22   # Friday 22:00 UTC


def _utc(now: Optional[datetime]) -> datetime:
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)
    return now.astimezone(timezone.utc)


def is_weekend(now: Optional[datetime] = None) -> bool:
    """Whether `now` (UTC; defaults to now) falls in the forex weekend
    close: all of Saturday, Sunday before 22:00, and Friday from 22:00
    on. Never raises."""
    now = _utc(now)
    weekday = now.weekday()  # Mon=0 .. Sun=6
    if weekday == _SATURDAY:
        return True
    if weekday == _SUNDAY and now.hour < _WEEK_OPEN_HOUR:
        return True
    if weekday == _FRIDAY and now.hour >= _WEEK_CLOSE_HOUR:
        return True
    return False


def is_market_open(now: Optional[datetime] = None) -> bool:
    """True when the forex market is open (not in the weekend close).
    Never raises."""
    return not is_weekend(now)


class ForexMarketCalendar:
    """Concrete `data_layer.live_data.price_stream.MarketCalendar` for Forex/XAUUSD
    (24x5). Satisfies the protocol's `is_open(now)` / `next_open(now)`."""

    def is_open(self, now: datetime) -> bool:
        return is_market_open(now)

    def next_open(self, now: datetime) -> datetime:
        """The next Sunday 22:00 UTC market open at/after `now`. If the
        market is currently open, returns `now` (already open)."""
        now = _utc(now)
        if is_market_open(now):
            return now
        # Advance to the next Sunday 22:00 UTC.
        candidate = now
        # If it's Sunday before open, the open is today at 22:00.
        if candidate.weekday() == _SUNDAY and candidate.hour < _WEEK_OPEN_HOUR:
            return candidate.replace(hour=_WEEK_OPEN_HOUR, minute=0,
                                     second=0, microsecond=0)
        # Otherwise step forward day-by-day to the next Sunday, then 22:00.
        for _ in range(8):
            candidate = candidate + timedelta(days=1)
            if candidate.weekday() == _SUNDAY:
                return candidate.replace(hour=_WEEK_OPEN_HOUR, minute=0,
                                         second=0, microsecond=0)
        # Unreachable in practice (a Sunday always occurs within 7 days).
        return now
