"""
TASK-CORE-006 gap-fill — dedicated unit tests for context/market_structure.py.

Exercises the EXISTING frozen detectors read-only (no logic change):
detect_swing_points (swing high/low), classify_structure (HH/HL/LH/LL),
and most_recent_bias (trend/bias). Also covers empty and invalid input.
"""

from datetime import datetime, timedelta, timezone

from data.twelve_data_client import Candle

from context.market_structure import (
    SwingPoint,
    SwingType,
    StructurePoint,
    StructureType,
    classify_structure,
    detect_swing_points,
    most_recent_bias,
)

BASE = datetime(2026, 1, 1, tzinfo=timezone.utc)


def _c(i, high, low, open_=None, close=None):
    return Candle(
        timestamp=BASE + timedelta(minutes=15 * i),
        open=open_ if open_ is not None else (high + low) / 2,
        high=high, low=low,
        close=close if close is not None else (high + low) / 2,
    )


def _swing(index, price, stype):
    return SwingPoint(index=index, price=price, timestamp=BASE + timedelta(minutes=15 * index), type=stype)


# ---- detect_swing_points -------------------------------------------------

def test_detect_swing_points_finds_high_and_low():
    # left=right=1: swing high at idx 1 (15), swing low at idx 3 (2).
    candles = [
        _c(0, high=10, low=5),
        _c(1, high=15, low=8),
        _c(2, high=9, low=6),
        _c(3, high=8, low=2),
        _c(4, high=7, low=4),
    ]
    swings = detect_swing_points(candles, 1, 1)
    assert [(s.index, s.type) for s in swings] == [(1, SwingType.HIGH), (3, SwingType.LOW)]
    assert swings[0].price == 15
    assert swings[1].price == 2


def test_detect_swing_points_too_few_candles_is_empty():
    assert detect_swing_points([_c(0, 10, 5), _c(1, 11, 6)], 2, 2) == []


def test_detect_swing_points_invalid_strength_is_empty():
    candles = [_c(i, 10 + i, 5) for i in range(5)]
    assert detect_swing_points(candles, 0, 1) == []
    assert detect_swing_points(candles, 1, -1) == []


# ---- classify_structure --------------------------------------------------

def test_classify_structure_hh_hl_lh_ll():
    swings = [
        _swing(0, 10, SwingType.HIGH),   # first HIGH  -> UNKNOWN
        _swing(1, 5, SwingType.LOW),     # first LOW   -> UNKNOWN
        _swing(2, 12, SwingType.HIGH),   # 12 > 10     -> HH
        _swing(3, 6, SwingType.LOW),     # 6 > 5       -> HL
        _swing(4, 11, SwingType.HIGH),   # 11 < 12     -> LH
        _swing(5, 4, SwingType.LOW),     # 4 < 6       -> LL
    ]
    classified = classify_structure(swings)
    assert [p.structure for p in classified] == [
        StructureType.UNKNOWN, StructureType.UNKNOWN,
        StructureType.HIGHER_HIGH, StructureType.HIGHER_LOW,
        StructureType.LOWER_HIGH, StructureType.LOWER_LOW,
    ]


def test_classify_structure_empty_is_empty():
    assert classify_structure([]) == []


# ---- most_recent_bias (trend / bias) ------------------------------------

def test_most_recent_bias_bullish_from_hh_hl():
    structure = classify_structure([_swing(0, 10, SwingType.HIGH), _swing(1, 12, SwingType.HIGH)])
    assert most_recent_bias(structure) == "BULLISH"


def test_most_recent_bias_bearish_from_ll():
    structure = classify_structure([
        _swing(0, 10, SwingType.HIGH), _swing(1, 5, SwingType.LOW),
        _swing(2, 12, SwingType.HIGH), _swing(3, 4, SwingType.LOW),  # last -> LL
    ])
    assert most_recent_bias(structure) == "BEARISH"


def test_most_recent_bias_none_when_all_unknown():
    # Single high + single low: both first-of-type -> UNKNOWN -> no bias.
    structure = classify_structure([_swing(0, 10, SwingType.HIGH), _swing(1, 5, SwingType.LOW)])
    assert most_recent_bias(structure) is None
    assert most_recent_bias([]) is None


def test_structure_point_is_immutable():
    p = StructurePoint(_swing(0, 10, SwingType.HIGH), StructureType.HIGHER_HIGH)
    try:
        p.structure = StructureType.LOWER_LOW  # type: ignore[misc]
    except Exception as exc:
        assert "frozen" in type(exc).__name__.lower() or "cannot assign" in str(exc).lower()
    else:
        raise AssertionError("StructurePoint must be immutable")
