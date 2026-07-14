"""
Phase A6 -- Session Intelligence foundation tests (context/session.py).

No mocking -- real Candle/LiquiditySweepEvent objects with hand-picked
UTC timestamps, same convention as tests/context/test_htf_bias.py and
tests/context/test_wyckoff.py.
"""

from datetime import datetime, timezone

from context.session import (
    Session,
    classify_session,
    detect_session_events,
    compute_session_volatility,
    compute_session_liquidity_activity,
)
from context.context_orchestrator import build_context_snapshot
from data.twelve_data_client import Candle
from context.liquidity import LiquidityZone, LiquiditySweepEvent, LiquidityType


def _ts(hour: int, minute: int = 0) -> datetime:
    return datetime(2024, 1, 2, hour, minute, tzinfo=timezone.utc)  # a Tuesday, arbitrary


def _candle(hour: int, high: float = 101.0, low: float = 99.0) -> Candle:
    return Candle(timestamp=_ts(hour), open=100.0, high=high, low=low, close=100.0)


def test_classify_session_boundaries():
    assert classify_session(_ts(0)) == Session.ASIA
    assert classify_session(_ts(7, 59)) == Session.ASIA
    assert classify_session(_ts(8)) == Session.LONDON
    assert classify_session(_ts(12, 59)) == Session.LONDON
    assert classify_session(_ts(13)) == Session.LONDON_NEW_YORK_OVERLAP
    assert classify_session(_ts(15, 59)) == Session.LONDON_NEW_YORK_OVERLAP
    assert classify_session(_ts(16)) == Session.NEW_YORK
    assert classify_session(_ts(20, 59)) == Session.NEW_YORK
    assert classify_session(_ts(21)) == Session.OFF_HOURS
    assert classify_session(_ts(23, 59)) == Session.OFF_HOURS


def test_classify_session_covers_full_24_hours_with_no_gaps():
    for hour in range(24):
        # Must resolve to exactly one of the 5 sessions -- never raise, never None.
        result = classify_session(_ts(hour))
        assert isinstance(result, Session)


def test_classify_session_assumes_utc_for_naive_datetime():
    naive = datetime(2024, 1, 2, 9, 0)  # no tzinfo
    assert classify_session(naive) == Session.LONDON


def test_detect_session_events_emits_only_on_transitions():
    candles = [
        _candle(1),  # ASIA (first candle -> transition)
        _candle(2),  # ASIA (no transition)
        _candle(9),  # LONDON (transition)
        _candle(10),  # LONDON (no transition)
        _candle(14),  # OVERLAP (transition)
    ]

    events = detect_session_events(candles)

    assert [e.session for e in events] == [Session.ASIA, Session.LONDON, Session.LONDON_NEW_YORK_OVERLAP]
    assert [e.index for e in events] == [0, 2, 4]


def test_detect_session_events_empty_input_returns_empty_list():
    assert detect_session_events([]) == []


def test_detect_session_events_single_session_emits_one_event():
    candles = [_candle(1), _candle(2), _candle(3)]
    events = detect_session_events(candles)
    assert len(events) == 1
    assert events[0].session == Session.ASIA
    assert events[0].index == 0


def test_compute_session_volatility_averages_real_ranges():
    candles = [
        _candle(1, high=105.0, low=100.0),  # ASIA, range 5.0
        _candle(2, high=103.0, low=100.0),  # ASIA, range 3.0
        _candle(9, high=110.0, low=100.0),  # LONDON, range 10.0
    ]

    volatility = compute_session_volatility(candles)

    assert volatility[Session.ASIA] == 4.0  # (5.0 + 3.0) / 2
    assert volatility[Session.LONDON] == 10.0
    assert Session.NEW_YORK not in volatility  # no candles in that session -- absent, not 0.0


def test_compute_session_volatility_empty_input_returns_empty_dict():
    assert compute_session_volatility([]) == {}


def test_compute_session_liquidity_activity_counts_real_sweeps():
    zone = LiquidityZone(price=100.0, type=LiquidityType.SSL, start_index=0, end_index=1, strength=2)
    sweeps = [
        LiquiditySweepEvent(index=1, timestamp=_ts(1), type=LiquidityType.SSL, sweep_price=99.0, zone=zone),
        LiquiditySweepEvent(index=2, timestamp=_ts(2), type=LiquidityType.SSL, sweep_price=99.0, zone=zone),
        LiquiditySweepEvent(index=3, timestamp=_ts(9), type=LiquidityType.BSL, sweep_price=101.0, zone=zone),
    ]

    activity = compute_session_liquidity_activity(sweeps)

    assert activity[Session.ASIA] == 2
    assert activity[Session.LONDON] == 1
    assert Session.NEW_YORK not in activity


def test_compute_session_liquidity_activity_empty_input_returns_empty_dict():
    assert compute_session_liquidity_activity([]) == {}


def test_session_events_is_wired_through_context_orchestrator():
    """Confirms ContextEngine.build()/build_context_snapshot() actually populates ContextSnapshot.session_events."""
    candles = [_candle(1), _candle(2), _candle(9)]

    snapshot = build_context_snapshot(candles)

    assert hasattr(snapshot, "session_events")
    assert isinstance(snapshot.session_events, list)
    assert len(snapshot.session_events) == 2  # ASIA -> LONDON transition
