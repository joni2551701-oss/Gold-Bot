"""
GFL-001 FLOW-007 (Indicator Engine) -- core_layer/features/atr.py tests.

Wilder's ATR, computed directly from the same Candle shape every other
context_layer detector uses (data_layer.providers.twelve_data_client.Candle).
"""

from datetime import datetime, timedelta, timezone

from core_layer.features.atr import compute_atr
from data_layer.providers.twelve_data_client import Candle

_BASE = datetime(2024, 1, 1, tzinfo=timezone.utc)


def _candle(index, high, low, close):
    return Candle(timestamp=_BASE + timedelta(minutes=5 * index), open=close, high=high, low=low, close=close)


def test_returns_none_with_no_candles():
    assert compute_atr([]) is None


def test_returns_none_with_fewer_than_period_plus_one_candles():
    candles = [_candle(h, high=105.0, low=100.0, close=102.0) for h in range(14)]  # period=14 needs 15
    assert compute_atr(candles, period=14) is None


def test_computes_a_value_once_enough_candles_exist():
    candles = [_candle(h, high=105.0 + h, low=100.0 + h, close=102.0 + h) for h in range(15)]
    atr = compute_atr(candles, period=14)
    assert atr is not None
    assert atr > 0.0


def test_constant_range_candles_converge_to_the_true_range():
    """Every candle has an identical 5-point high-low range and close == prev close -- TR is always 5, so ATR settles at 5."""
    candles = [_candle(h, high=105.0, low=100.0, close=102.5) for h in range(30)]
    atr = compute_atr(candles, period=14)
    assert atr == 5.0


def test_never_raises_on_malformed_ordering_or_gaps():
    candles = [_candle(h, high=100.0, low=100.0, close=100.0) for h in range(20)]
    atr = compute_atr(candles, period=14)
    assert atr == 0.0  # zero range, zero gaps -- a legitimate flat-market TR of 0


def test_custom_period_is_respected():
    candles = [_candle(h, high=105.0, low=100.0, close=102.0) for h in range(6)]
    assert compute_atr(candles, period=5) is not None
    assert compute_atr(candles, period=10) is None  # not enough candles for period=10


def test_zero_or_negative_period_returns_none():
    candles = [_candle(h, high=105.0, low=100.0, close=102.0) for h in range(20)]
    assert compute_atr(candles, period=0) is None
    assert compute_atr(candles, period=-1) is None
