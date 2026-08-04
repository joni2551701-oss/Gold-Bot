"""
Stream Layer — Stream Mode (TASK-CORE-004).

StreamMode is the runtime posture of the real-time stream. Weekends
and closed markets must pause the stream WITHOUT crashing the system
("stream'ni to'xtatadi, lekin tizimni buzmaydi") -- a paused stream is
a normal, expected state, not an error.

Modes:
    ACTIVE        -- market open, stream flowing
    PAUSED        -- generic pause (operator or upstream backpressure)
    WEEKEND_WAIT  -- Sat/Sun: waiting for the week to open
    MARKET_CLOSED -- weekday but outside market hours
    MANUAL_HOLD   -- an operator explicitly held the stream

resolve_mode() decides the mode from the clock (and an optional manual
hold). It is deliberately simple and self-contained: XAUUSD/forex is a
24x5 market -- open from Sunday 22:00 UTC through Friday 22:00 UTC,
closed over the weekend. This is a coarse, documented default, not an
exchange-holiday calendar (that would be a later, separately-approved
addition). No secret is read here; no .env access; no business logic
beyond the open/closed clock decision.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Optional


class StreamMode(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    WEEKEND_WAIT = "weekend_wait"
    MARKET_CLOSED = "market_closed"
    MANUAL_HOLD = "manual_hold"

    def is_flowing(self) -> bool:
        """True only for ACTIVE -- the one mode where data events are routed to subscribers."""
        return self is StreamMode.ACTIVE

    def is_waiting(self) -> bool:
        """True for every non-ACTIVE mode -- the stream is intact but holding."""
        return self is not StreamMode.ACTIVE


# Forex/XAUUSD weekly session in UTC: opens Sunday 22:00, closes Friday
# 22:00. Saturday (5) is always closed; Sunday (6) before 22:00 and
# Friday (4) after 22:00 are closed.
_SUNDAY = 6
_FRIDAY = 4
_SATURDAY = 5
_WEEK_OPEN_HOUR = 22
_WEEK_CLOSE_HOUR = 22


def is_weekend(now: Optional[datetime] = None) -> bool:
    """
    Whether `now` (UTC; defaults to current UTC time) falls in the
    forex weekend close: all of Saturday, Sunday before 22:00, and
    Friday from 22:00 on. Never raises.
    """
    now = now or datetime.now(timezone.utc)
    weekday = now.weekday()  # Mon=0 .. Sun=6
    if weekday == _SATURDAY:
        return True
    if weekday == _SUNDAY and now.hour < _WEEK_OPEN_HOUR:
        return True
    if weekday == _FRIDAY and now.hour >= _WEEK_CLOSE_HOUR:
        return True
    return False


def is_market_open(now: Optional[datetime] = None) -> bool:
    """True when the forex market is open (i.e. not in the weekend close). Never raises."""
    return not is_weekend(now)


def resolve_mode(
    now: Optional[datetime] = None,
    manual_hold: bool = False,
    paused: bool = False,
) -> StreamMode:
    """
    Decide the current StreamMode. Precedence: an explicit manual hold
    wins, then a generic pause, then the weekend/closed clock, else
    ACTIVE. Pure and side-effect-free -- callers (price_stream.py) use
    it to gate routing; it never itself stops anything or raises.
    """
    if manual_hold:
        return StreamMode.MANUAL_HOLD
    if paused:
        return StreamMode.PAUSED
    if is_weekend(now):
        return StreamMode.WEEKEND_WAIT
    return StreamMode.ACTIVE
