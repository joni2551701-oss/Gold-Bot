"""
Phase 59.5, TASK 6 -- data_layer/providers/provider_comparison.py tests.
"""

from datetime import datetime, timezone

from data_layer.providers.provider_comparison import compare_providers
from database_layer.market_repository.raw_candle_models import create_raw_candle


def _candle(provider, ts, open=2000.0, high=2005.0, low=1995.0, close=2001.0, symbol="XAUUSD", timeframe="M15"):
    return create_raw_candle(
        symbol=symbol, timeframe=timeframe, timestamp=ts,
        open=open, high=high, low=low, close=close, provider=provider,
    )


def test_empty_inputs_never_raise():
    assert compare_providers([], []) == []


def test_no_overlapping_timestamps_returns_empty():
    ts_a = datetime(2026, 1, 1, tzinfo=timezone.utc)
    ts_b = datetime(2026, 1, 2, tzinfo=timezone.utc)

    result = compare_providers([_candle("twelvedata", ts_a)], [_candle("binance", ts_b)])

    assert result == []


def test_matching_timestamp_produces_one_comparison():
    ts = datetime(2026, 1, 1, tzinfo=timezone.utc)
    candle_a = _candle("twelvedata", ts, close=2001.0)
    candle_b = _candle("binance", ts, close=2001.2)

    result = compare_providers([candle_a], [candle_b])

    assert len(result) == 1
    comparison = result[0]
    assert comparison.provider_a == "twelvedata"
    assert comparison.provider_b == "binance"
    assert round(comparison.close_diff, 2) == 0.2


def test_within_tolerance_true_for_small_diff():
    ts = datetime(2026, 1, 1, tzinfo=timezone.utc)
    result = compare_providers(
        [_candle("twelvedata", ts, close=2001.0)],
        [_candle("binance", ts, close=2001.1)],
        tolerance=0.5,
    )
    assert result[0].within_tolerance is True


def test_within_tolerance_false_for_large_diff():
    ts = datetime(2026, 1, 1, tzinfo=timezone.utc)
    result = compare_providers(
        [_candle("twelvedata", ts, close=2001.0)],
        [_candle("binance", ts, close=2010.0)],
        tolerance=0.5,
    )
    assert result[0].within_tolerance is False


def test_spread_is_high_minus_low_per_provider():
    ts = datetime(2026, 1, 1, tzinfo=timezone.utc)
    candle_a = _candle("twelvedata", ts, high=2010.0, low=1990.0)
    candle_b = _candle("binance", ts, high=2005.0, low=1995.0)

    result = compare_providers([candle_a], [candle_b])

    assert result[0].spread_a == 20.0
    assert result[0].spread_b == 10.0
    assert result[0].spread_diff == 10.0


def test_results_are_chronologically_ascending():
    ts1 = datetime(2026, 1, 1, tzinfo=timezone.utc)
    ts2 = datetime(2026, 1, 2, tzinfo=timezone.utc)
    candles_a = [_candle("twelvedata", ts2), _candle("twelvedata", ts1)]
    candles_b = [_candle("binance", ts1), _candle("binance", ts2)]

    result = compare_providers(candles_a, candles_b)

    assert [c.timestamp for c in result] == [ts1, ts2]


def test_never_mutates_or_merges_input_candles():
    """Foundation-only: no auto-correction -- both original candles' own values stay in the report untouched."""
    ts = datetime(2026, 1, 1, tzinfo=timezone.utc)
    candle_a = _candle("twelvedata", ts, close=2001.0)
    candle_b = _candle("binance", ts, close=2005.0)

    result = compare_providers([candle_a], [candle_b])

    assert result[0].close_a == 2001.0
    assert result[0].close_b == 2005.0
