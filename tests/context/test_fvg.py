"""
TASK-CORE-006 gap-fill — dedicated unit tests for context_layer/fair_value_gap/fvg.py.

Read-only exercise of the existing frozen detect_fvg(): a 3-candle
imbalance. Bullish FVG when candle-1 high < candle-3 low; bearish FVG
when candle-1 low > candle-3 high.
"""

from datetime import datetime, timedelta, timezone

from data_layer.providers.twelve_data_client import Candle

from context_layer.fair_value_gap.fvg import detect_fvg, FvgType

BASE = datetime(2026, 1, 1, tzinfo=timezone.utc)


def _c(i, high, low):
    mid = (high + low) / 2
    return Candle(timestamp=BASE + timedelta(minutes=15 * i), open=mid, high=high, low=low, close=mid)


def test_bullish_fvg_gap_up():
    # c1.high (10) < c3.low (12) -> bullish FVG at index 2.
    candles = [_c(0, 10, 5), _c(1, 11, 6), _c(2, 20, 12)]
    fvgs = detect_fvg(candles)
    assert len(fvgs) == 1
    assert fvgs[0].type is FvgType.BULLISH
    assert fvgs[0].index == 2
    assert fvgs[0].bottom == 10 and fvgs[0].top == 12
    assert fvgs[0].filled is False


def test_bearish_fvg_gap_down():
    # c1.low (20) > c3.high (10) -> bearish FVG at index 2.
    candles = [_c(0, 25, 20), _c(1, 18, 15), _c(2, 10, 8)]
    fvgs = detect_fvg(candles)
    assert len(fvgs) == 1
    assert fvgs[0].type is FvgType.BEARISH
    assert fvgs[0].top == 20 and fvgs[0].bottom == 10


def test_no_gap_when_ranges_overlap():
    candles = [_c(0, 12, 8), _c(1, 13, 9), _c(2, 12, 8)]
    assert detect_fvg(candles) == []


def test_fewer_than_three_candles_is_empty():
    assert detect_fvg([_c(0, 10, 5), _c(1, 20, 12)]) == []
    assert detect_fvg([]) == []
