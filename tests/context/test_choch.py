"""
TASK-CORE-006 gap-fill — dedicated unit tests for context_layer/market_structure/choch.py.

Read-only exercise of the existing frozen detect_choch(): a bullish
CHoCH is a close above a LOWER_HIGH pivot; a bearish CHoCH is a close
below a HIGHER_LOW pivot.
"""

from datetime import datetime, timedelta, timezone

from data_layer.providers.twelve_data_client import Candle

from context_layer.market_structure.choch import detect_choch, ChochDirection
from context_layer.market_structure.market_structure import SwingPoint, SwingType, StructurePoint, StructureType

BASE = datetime(2026, 1, 1, tzinfo=timezone.utc)


def _c(i, close):
    return Candle(
        timestamp=BASE + timedelta(minutes=15 * i),
        open=close, high=close + 1, low=close - 1, close=close,
    )


def _struct(index, price, stype, swing_type):
    return StructurePoint(
        SwingPoint(index=index, price=price, timestamp=BASE + timedelta(minutes=15 * index), type=swing_type),
        stype,
    )


def test_bullish_choch_on_close_above_lower_high():
    structures = [_struct(2, 12.0, StructureType.LOWER_HIGH, SwingType.HIGH)]
    candles = [_c(0, 10), _c(1, 11), _c(2, 12), _c(3, 13)]  # close 13 > 12 at idx 3
    events = detect_choch(candles, structures)
    assert len(events) == 1
    assert events[0].direction is ChochDirection.BULLISH
    assert events[0].index == 3


def test_bearish_choch_on_close_below_higher_low():
    structures = [_struct(2, 8.0, StructureType.HIGHER_LOW, SwingType.LOW)]
    candles = [_c(0, 10), _c(1, 9), _c(2, 8), _c(3, 7)]  # close 7 < 8 at idx 3
    events = detect_choch(candles, structures)
    assert len(events) == 1
    assert events[0].direction is ChochDirection.BEARISH
    assert events[0].index == 3


def test_no_choch_from_continuation_structure():
    # HIGHER_HIGH / LOWER_LOW are BOS pivots, not CHoCH pivots.
    structures = [_struct(2, 12.0, StructureType.HIGHER_HIGH, SwingType.HIGH)]
    candles = [_c(i, 13) for i in range(4)]
    assert detect_choch(candles, structures) == []


def test_empty_structures_is_empty():
    assert detect_choch([_c(0, 10)], []) == []
