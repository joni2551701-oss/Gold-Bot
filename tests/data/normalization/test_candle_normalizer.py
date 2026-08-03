"""
Phase 59.3, TASK 1 -- data_layer/normalization/candle_normalizer.py tests.
"""

from datetime import datetime, timezone

from data_layer.normalization.candle_normalizer import normalize_candle_list, stamp_provider
from data_layer.providers.base_provider import MarketCandle


def _candle(provider=None):
    return MarketCandle(
        symbol="XAUUSD", timeframe="M15",
        open=2000.0, high=2005.0, low=1995.0, close=2001.0,
        timestamp=datetime(2026, 1, 1, tzinfo=timezone.utc),
        provider=provider,
    )


def test_stamp_provider_sets_the_field():
    candle = _candle()
    stamped = stamp_provider(candle, "twelvedata")
    assert stamped.provider == "twelvedata"


def test_stamp_provider_does_not_mutate_the_original():
    candle = _candle()
    stamp_provider(candle, "twelvedata")
    assert candle.provider is None  # MarketCandle is frozen -- original untouched


def test_stamp_provider_overwrites_existing_value():
    candle = _candle(provider="old_provider")
    stamped = stamp_provider(candle, "new_provider")
    assert stamped.provider == "new_provider"


def test_stamp_provider_preserves_every_other_field():
    candle = _candle()
    stamped = stamp_provider(candle, "twelvedata")
    assert stamped.symbol == candle.symbol
    assert stamped.timeframe == candle.timeframe
    assert stamped.open == candle.open
    assert stamped.close == candle.close
    assert stamped.timestamp == candle.timestamp
    assert stamped.volume == candle.volume


def test_normalize_candle_list_stamps_every_candle():
    candles = [_candle(), _candle()]
    normalized = normalize_candle_list(candles, "binance")
    assert all(c.provider == "binance" for c in normalized)


def test_normalize_candle_list_empty_input_never_raises():
    assert normalize_candle_list([], "twelvedata") == []
