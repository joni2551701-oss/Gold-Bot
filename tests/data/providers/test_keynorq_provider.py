"""
TASK-CORE-003 -- tests for the Keynorq provider stub
(data_layer/providers/keynorq_provider.py).
"""

import pytest

from config import build_settings
from data_layer.providers.base_provider import MarketDataProvider, ProviderStatus
from data_layer.providers.keynorq_provider import KeynorqProvider


def test_is_a_market_data_provider():
    assert isinstance(KeynorqProvider(), MarketDataProvider)


def test_provider_name_is_stable():
    assert KeynorqProvider().get_provider_name() == "keynorq"


def test_market_status_never_raises_and_is_unavailable():
    status = KeynorqProvider().get_market_status()
    assert isinstance(status, ProviderStatus)
    assert status.available is False
    assert status.reason


def test_supported_timeframes_empty_honest_stub():
    # Custom source, universe unknown -> honest empty tuple (MT5 pattern).
    assert KeynorqProvider().get_supported_timeframes() == ()


def test_get_candles_raises_not_implemented():
    with pytest.raises(NotImplementedError):
        KeynorqProvider().get_candles("ANYTHING", "M15", 10)


def test_get_latest_price_raises_not_implemented():
    with pytest.raises(NotImplementedError):
        KeynorqProvider().get_latest_price("ANYTHING")


def test_api_key_read_from_config_and_masked(monkeypatch):
    monkeypatch.setenv("KEYNORQ_API_KEY", "KEYNORQ-secret-xyz")
    settings = build_settings()
    provider = KeynorqProvider(settings=settings)
    assert provider._api_key.reveal() == "KEYNORQ-secret-xyz"
    assert "KEYNORQ-secret-xyz" not in repr(provider._api_key)
