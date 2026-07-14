"""
Phase 59.1, TASK 8 -- data/providers/base_provider.py interface tests.
"""

import pytest

from data.providers.base_provider import MarketCandle, MarketDataProvider, ProviderStatus
from datetime import datetime, timezone


def test_market_data_provider_cannot_be_instantiated_directly():
    """The abstract contract itself must not be constructible -- only a real implementation can be."""
    with pytest.raises(TypeError):
        MarketDataProvider()


def test_market_candle_volume_defaults_to_none():
    candle = MarketCandle(
        symbol="XAUUSD", timeframe="M15",
        open=2000.0, high=2005.0, low=1995.0, close=2001.0,
        timestamp=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )
    assert candle.volume is None  # fake volume is never fabricated


def test_market_candle_is_frozen():
    candle = MarketCandle(
        symbol="XAUUSD", timeframe="M15",
        open=2000.0, high=2005.0, low=1995.0, close=2001.0,
        timestamp=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )
    with pytest.raises(Exception):
        candle.close = 9999.0


def test_market_candle_to_dict_is_json_safe():
    import json

    candle = MarketCandle(
        symbol="XAUUSD", timeframe="M15",
        open=2000.0, high=2005.0, low=1995.0, close=2001.0,
        timestamp=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )
    data = candle.to_dict()
    json.dumps(data)  # must not raise
    assert data["volume"] is None
    assert isinstance(data["timestamp"], str)


def test_provider_status_available_true_has_no_reason_required():
    status = ProviderStatus(available=True)
    assert status.available is True
    assert status.reason == ""


def test_provider_status_unavailable_carries_a_reason():
    status = ProviderStatus(available=False, reason="no API key")
    assert status.available is False
    assert status.reason == "no API key"


def test_a_concrete_subclass_implementing_all_three_methods_can_be_instantiated():
    class DummyProvider(MarketDataProvider):
        def get_candles(self, symbol, timeframe, limit):
            return []

        def get_latest_price(self, symbol):
            return None

        def get_market_status(self):
            return ProviderStatus(available=True)

    provider = DummyProvider()
    assert provider.get_candles("XAUUSD", "M15", 10) == []
    assert provider.get_latest_price("XAUUSD") is None
    assert provider.get_market_status().available is True


def test_a_subclass_missing_a_method_cannot_be_instantiated():
    class IncompleteProvider(MarketDataProvider):
        def get_candles(self, symbol, timeframe, limit):
            return []
        # get_latest_price/get_market_status intentionally missing

    with pytest.raises(TypeError):
        IncompleteProvider()
