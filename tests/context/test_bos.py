"""
TASK-CORE-006 gap-fill — dedicated unit tests for context/bos.py.

Read-only exercise of the existing frozen detect_bos(): a bullish BOS is
a close above a HIGHER_HIGH pivot; a bearish BOS is a close below a
LOWER_LOW pivot.
"""

from datetime import datetime, timedelta, timezone

from data.twelve_data_client import Candle

from context.bos import detect_bos, BosDirection
from context.market_structure import SwingPoint, SwingType, StructurePoint, StructureType

BASE = datetime(2026, 1, 1, tzinfo=timezone.utc)


def _c(i, close, high=None, low=None):
    return Candle(
        timestamp=BASE + timedelta(minutes=15 * i),
        open=close, high=high if high is not None else close + 1,
        low=low if low is not None else close - 1, close=close,
    )


def _struct(index, price, stype, swing_type):
    return StructurePoint(
        SwingPoint(index=index, price=price, timestamp=BASE + timedelta(minutes=15 * index), type=swing_type),
        stype,
    )


def test_bullish_bos_on_close_above_higher_high():
    structures = [_struct(2, 12.0, StructureType.HIGHER_HIGH, SwingType.HIGH)]
    candles = [_c(0, 10), _c(1, 11), _c(2, 12), _c(3, 13), _c(4, 12.5)]  # close 13 > 12 at idx 3
    events = detect_bos(candles, structures)
    assert len(events) == 1
    assert events[0].direction is BosDirection.BULLISH
    assert events[0].index == 3


def test_bearish_bos_on_close_below_lower_low():
    structures = [_struct(2, 8.0, StructureType.LOWER_LOW, SwingType.LOW)]
    candles = [_c(0, 10), _c(1, 9), _c(2, 8), _c(3, 7), _c(4, 7.5)]  # close 7 < 8 at idx 3
    events = detect_bos(candles, structures)
    assert len(events) == 1
    assert events[0].direction is BosDirection.BEARISH
    assert events[0].index == 3


def test_no_break_when_price_never_exceeds_pivot():
    structures = [_struct(2, 20.0, StructureType.HIGHER_HIGH, SwingType.HIGH)]
    candles = [_c(i, 11) for i in range(5)]
    assert detect_bos(candles, structures) == []


def test_empty_structures_is_empty():
    assert detect_bos([_c(0, 10)], []) == []
