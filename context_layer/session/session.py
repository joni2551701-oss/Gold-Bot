"""
Context Layer — Session Intelligence foundation (Phase A6).

Classifies which trading session a candle falls into (Asia, London,
New York, the London/New York overlap, or off-hours), and derives two
real, data-backed statistics from that classification: average range
(volatility proxy) and liquidity-sweep activity, both per session. It
does NOT generate a signal and is NOT a strategy -- see
docs/SESSION_INTELLIGENCE.md for the full contract.

Distinct from data_layer/live_data/session_filter.py's is_trading_time(): that
function answers "is it trading time right now" (wall-clock,
Tashkent-time, binary) for gating when the pipeline should run at
all. This module answers "which session was THIS candle in" (any
candle's own UTC timestamp, five-way classification) for describing
market context after the fact -- a different question, not a
duplicate of session_filter.py's logic. Session boundaries used here
are standard, widely-cited UTC hour ranges, not derived from
session_filter.py's Tashkent-time convention.

Reuses existing detection output rather than duplicating it:
- context.liquidity.LiquiditySweepEvent (unchanged) supplies the
  sweep timestamps compute_session_liquidity_activity() groups by
  session -- no new sweep detection.
"""

from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Sequence

from data_layer.providers.twelve_data_client import Candle
from context_layer.liquidity.liquidity import LiquiditySweepEvent


class Session(Enum):
    """
    Five-way classification by UTC hour. Boundaries are standard,
    widely-cited approximate session hours, not official
    broker/exchange cutoffs -- real session activity ramps up/down
    gradually, not at a hard clock instant. Deliberately simplified to
    non-overlapping hour blocks for this foundation phase, with the
    one exception being the named London/New York overlap, since real
    trading convention treats that specific window as its own
    higher-liquidity regime.

        00:00-08:00 UTC  ASIA
        08:00-13:00 UTC  LONDON
        13:00-16:00 UTC  LONDON_NEW_YORK_OVERLAP
        16:00-21:00 UTC  NEW_YORK
        21:00-24:00 UTC  OFF_HOURS
    """
    ASIA = "ASIA"
    LONDON = "LONDON"
    LONDON_NEW_YORK_OVERLAP = "LONDON_NEW_YORK_OVERLAP"
    NEW_YORK = "NEW_YORK"
    OFF_HOURS = "OFF_HOURS"


@dataclass(frozen=True)
class SessionEvent:
    """A session transition -- emitted only when the classified session changes from the previous candle's (including the first candle)."""
    index: int
    timestamp: datetime
    session: Session


def classify_session(timestamp: datetime) -> Session:
    """
    Classifies a single timestamp by UTC hour. Naive (no tzinfo)
    datetimes are assumed already UTC, matching every other module in
    this codebase (data_layer.providers.twelve_data_client.Candle.timestamp is always
    UTC per its own docstring) -- never raises.
    """
    hour = timestamp.astimezone(timezone.utc).hour if timestamp.tzinfo else timestamp.hour

    if 13 <= hour < 16:
        return Session.LONDON_NEW_YORK_OVERLAP
    if 8 <= hour < 13:
        return Session.LONDON
    if 16 <= hour < 21:
        return Session.NEW_YORK
    if 0 <= hour < 8:
        return Session.ASIA
    return Session.OFF_HOURS


def detect_session_events(candles: Sequence[Candle]) -> List[SessionEvent]:
    """
    Walks the candle series and emits one SessionEvent per transition
    (including the first candle, which is always a transition from
    "no session yet"). Sparse by design -- matches the other
    ContextSnapshot event-list fields' convention (BosEvent, ChochEvent,
    etc. also only fire on a meaningful change, not on every candle).
    """
    events: List[SessionEvent] = []
    previous_session = None

    for index, candle in enumerate(candles):
        session = classify_session(candle.timestamp)
        if session != previous_session:
            events.append(SessionEvent(index=index, timestamp=candle.timestamp, session=session))
            previous_session = session

    return events


def compute_session_volatility(candles: Sequence[Candle]) -> Dict[Session, float]:
    """
    Average (high - low) range per session, computed directly from
    real OHLC data already available in the provided candle window --
    not a fabricated statistic. A session with zero candles in the
    window is simply absent from the result (no 0.0 placeholder), so
    a caller can distinguish "no data for this session in this
    window" from "measured zero volatility."
    """
    total_range: Dict[Session, float] = defaultdict(float)
    candle_count: Dict[Session, int] = defaultdict(int)

    for candle in candles:
        session = classify_session(candle.timestamp)
        total_range[session] += candle.high - candle.low
        candle_count[session] += 1

    return {
        session: round(total_range[session] / candle_count[session], 5)
        for session in total_range
    }


def compute_session_liquidity_activity(liquidity_sweeps: Sequence[LiquiditySweepEvent]) -> Dict[Session, int]:
    """
    Count of already-detected liquidity sweeps per session -- a real,
    data-backed answer to "which session tends to sweep liquidity in
    this window," reusing context.liquidity.LiquiditySweepEvent
    directly rather than re-detecting sweeps. A session with zero
    sweeps in the window is absent from the result, same convention
    as compute_session_volatility().
    """
    activity: Dict[Session, int] = defaultdict(int)
    for sweep in liquidity_sweeps:
        activity[classify_session(sweep.timestamp)] += 1
    return dict(activity)
