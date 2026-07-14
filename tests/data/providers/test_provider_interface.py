"""
Phase 59.1, TASK 8 -- data/providers/base_provider.py interface tests.
Extended by Phase 59.2 TASK 1/9 for the DataProvider/MarketDataProvider
split.
"""

import pytest

from data.providers.base_provider import DataProvider, MarketCandle, MarketDataProvider, ProviderStatus
from datetime import datetime, timezone


def test_data_provider_cannot_be_instantiated_directly():
    with pytest.raises(TypeError):
        DataProvider()


def test_market_data_provider_cannot_be_instantiated_directly():
    """The abstract contract itself must not be constructible -- only a real implementation can be."""
    with pytest.raises(TypeError):
        MarketDataProvider()


def test_market_data_provider_is_a_data_provider():
    """The split is a specialization, not a parallel hierarchy."""
    assert issubclass(MarketDataProvider, DataProvider)


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


class _DummyProvider(MarketDataProvider):
    def get_provider_name(self):
        return "dummy"

    def get_supported_timeframes(self):
        return ("M15",)

    def get_candles(self, symbol, timeframe, limit):
        return []

    def get_latest_price(self, symbol):
        return None

    def get_market_status(self):
        return ProviderStatus(available=True)


def test_a_concrete_subclass_implementing_every_method_can_be_instantiated():
    provider = _DummyProvider()
    assert provider.get_candles("XAUUSD", "M15", 10) == []
    assert provider.get_latest_price("XAUUSD") is None
    assert provider.get_market_status().available is True
    assert provider.get_provider_name() == "dummy"
    assert provider.get_supported_timeframes() == ("M15",)


def test_a_subclass_missing_a_market_data_method_cannot_be_instantiated():
    class IncompleteProvider(MarketDataProvider):
        def get_provider_name(self):
            return "incomplete"

        def get_supported_timeframes(self):
            return ()

        def get_candles(self, symbol, timeframe, limit):
            return []
        # get_latest_price/get_market_status intentionally missing

    with pytest.raises(TypeError):
        IncompleteProvider()


def test_a_subclass_missing_the_new_data_provider_methods_cannot_be_instantiated():
    """get_provider_name()/get_supported_timeframes() are just as mandatory as the pre-existing three."""
    class MissingNameProvider(MarketDataProvider):
        def get_supported_timeframes(self):
            return ()

        def get_candles(self, symbol, timeframe, limit):
            return []

        def get_latest_price(self, symbol):
            return None

        def get_market_status(self):
            return ProviderStatus(available=True)
        # get_provider_name intentionally missing

    with pytest.raises(TypeError):
        MissingNameProvider()


def test_a_pure_data_provider_without_candle_methods_can_be_instantiated():
    """A non-candle provider (e.g. a fundamental data source) only needs DataProvider's two methods."""
    class MinimalProvider(DataProvider):
        def get_provider_name(self):
            return "minimal"

        def get_market_status(self):
            return ProviderStatus(available=False, reason="stub")

    provider = MinimalProvider()
    assert provider.get_provider_name() == "minimal"
    assert provider.get_market_status().available is False
