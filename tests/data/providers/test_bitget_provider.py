"""
TASK-CORE-003 -- tests for the Bitget provider stub
(data/providers/bitget_provider.py).
"""

import pytest

from config import build_settings
from data.providers.base_provider import MarketDataProvider, ProviderStatus
from data.providers.bitget_provider import SUPPORTED_SYMBOLS, BitgetProvider


def test_is_a_market_data_provider():
    assert isinstance(BitgetProvider(), MarketDataProvider)


def test_provider_name_is_stable():
    assert BitgetProvider().get_provider_name() == "bitget"


def test_market_status_never_raises_and_is_unavailable():
    status = BitgetProvider().get_market_status()
    assert isinstance(status, ProviderStatus)
    assert status.available is False
    assert status.reason


def test_supported_timeframes_declared():
    tfs = BitgetProvider().get_supported_timeframes()
    assert "M15" in tfs


def test_get_candles_valid_symbol_raises_not_implemented():
    with pytest.raises(NotImplementedError):
        BitgetProvider().get_candles("BTCUSDT", "M15", 10)


def test_get_candles_invalid_symbol_raises_value_error():
    with pytest.raises(ValueError):
        BitgetProvider().get_candles("XAUUSD", "M15", 10)


def test_get_latest_price_invalid_symbol_raises_value_error():
    with pytest.raises(ValueError):
        BitgetProvider().get_latest_price("NOTREAL")


def test_supported_symbols_are_bitget_format():
    assert all(s.endswith("USDT") for s in SUPPORTED_SYMBOLS)


def test_api_key_read_from_config_and_masked(monkeypatch):
    monkeypatch.setenv("BITGET_API_KEY", "BITGET-secret-123")
    settings = build_settings()
    provider = BitgetProvider(settings=settings)
    # The key is a MaskedSecret -- reveal() returns it, repr never does.
    assert provider._api_key.reveal() == "BITGET-secret-123"
    assert "BITGET-secret-123" not in repr(provider._api_key)
    assert repr(provider._api_key) == "MaskedSecret(***)"
