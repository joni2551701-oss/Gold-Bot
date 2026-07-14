"""
Phase 59.1, TASK 8 -- data/providers/twelve_data_provider.py tests.
Monkeypatches TwelveDataClient.fetch_candles() -- no real network call
is ever made, same pattern tests/data/test_market_data.py already
uses.
"""

from datetime import datetime, timezone

from data.providers.base_provider import MarketCandle, ProviderStatus
from data.providers.twelve_data_provider import SUPPORTED_SYMBOLS, TwelveDataProvider
from data.twelve_data_client import Candle, TwelveDataClient


def _candle(price=2000.0, ts=None):
    return Candle(
        timestamp=ts or datetime(2026, 1, 1, tzinfo=timezone.utc),
        open=price, high=price + 1, low=price - 1, close=price,
    )


def test_get_candles_adapts_candle_into_market_candle(monkeypatch):
    provider = TwelveDataProvider()
    monkeypatch.setattr(provider.client, "fetch_candles", lambda *a, **k: [_candle()])

    result = provider.get_candles("XAUUSD", "M15", 10)

    assert len(result) == 1
    candle = result[0]
    assert isinstance(candle, MarketCandle)
    assert candle.symbol == "XAUUSD"
    assert candle.timeframe == "M15"
    assert candle.volume is None  # never fabricated
    assert candle.close == 2000.0


def test_get_candles_never_fabricates_volume(monkeypatch):
    provider = TwelveDataProvider()
    monkeypatch.setattr(provider.client, "fetch_candles", lambda *a, **k: [_candle(), _candle(2010.0)])

    result = provider.get_candles("XAUUSD", "M15", 10)

    assert all(c.volume is None for c in result)


def test_get_candles_empty_response_returns_empty_list_not_none(monkeypatch):
    provider = TwelveDataProvider()
    monkeypatch.setattr(provider.client, "fetch_candles", lambda *a, **k: [])

    result = provider.get_candles("XAUUSD", "M15", 10)

    assert result == []


def test_get_candles_re_raises_on_fetch_failure(monkeypatch):
    """Unlike data/market_data.py's get_candles(), TwelveDataProvider re-raises -- a thinner adapter."""
    import pytest

    provider = TwelveDataProvider()

    def _raise(*a, **k):
        raise ValueError("Twelve Data API Error: rate limit exceeded")

    monkeypatch.setattr(provider.client, "fetch_candles", _raise)

    with pytest.raises(ValueError):
        provider.get_candles("XAUUSD", "M15", 10)


def test_get_latest_price_returns_most_recent_close(monkeypatch):
    provider = TwelveDataProvider()
    monkeypatch.setattr(provider.client, "fetch_candles", lambda *a, **k: [_candle(2050.0)])
    monkeypatch.setattr(provider.client, "api_key", "fake-key")

    price = provider.get_latest_price("XAUUSD")

    assert price == 2050.0


def test_get_latest_price_returns_none_on_no_data(monkeypatch):
    provider = TwelveDataProvider()
    monkeypatch.setattr(provider.client, "fetch_candles", lambda *a, **k: [])

    assert provider.get_latest_price("XAUUSD") is None


def test_get_latest_price_never_raises_on_fetch_failure(monkeypatch):
    provider = TwelveDataProvider()

    def _raise(*a, **k):
        raise ConnectionError("network down")

    monkeypatch.setattr(provider.client, "fetch_candles", _raise)

    assert provider.get_latest_price("XAUUSD") is None  # must not raise


def test_get_market_status_unavailable_without_api_key(monkeypatch):
    provider = TwelveDataProvider()
    monkeypatch.setattr(provider.client, "api_key", None)

    status = provider.get_market_status()

    assert isinstance(status, ProviderStatus)
    assert status.available is False


def test_get_market_status_available_with_api_key(monkeypatch):
    provider = TwelveDataProvider()
    monkeypatch.setattr(provider.client, "api_key", "fake-key")

    status = provider.get_market_status()

    assert status.available is True


def test_provider_accepts_an_injected_client():
    client = TwelveDataClient()
    provider = TwelveDataProvider(client=client)
    assert provider.client is client


def test_supported_symbols_all_use_the_existing_generic_formatter():
    """Every symbol this task's brief names is a plain 6-character pair -- _format_symbol() already splits it 3+3 with no new logic."""
    client = TwelveDataClient()
    for symbol in SUPPORTED_SYMBOLS:
        formatted = client._format_symbol(symbol)
        assert "/" in formatted
        assert formatted == f"{symbol[:3]}/{symbol[3:]}"


def test_provider_never_generates_a_signal_or_knows_strategy():
    """A structural guard: TwelveDataProvider exposes no signal/strategy/decision-shaped attribute or method."""
    provider = TwelveDataProvider()
    forbidden_terms = ("signal", "strategy", "decision")
    for attr in dir(provider):
        if attr.startswith("_"):
            continue
        assert not any(term in attr.lower() for term in forbidden_terms), attr
