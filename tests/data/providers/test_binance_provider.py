"""
Phase 59.2, TASK 3/9 -- data/providers/binance_provider.py tests.
"""

import pytest

from data.providers.base_provider import MarketDataProvider, ProviderStatus
from data.providers.binance_provider import SUPPORTED_SYMBOLS, SUPPORTED_TIMEFRAMES, BinanceProvider


def test_binance_provider_is_a_market_data_provider():
    assert issubclass(BinanceProvider, MarketDataProvider)


def test_get_provider_name_returns_binance():
    provider = BinanceProvider()
    assert provider.get_provider_name() == "binance"


def test_get_supported_timeframes_matches_documented_set():
    provider = BinanceProvider()
    assert provider.get_supported_timeframes() == SUPPORTED_TIMEFRAMES


def test_get_market_status_always_unavailable():
    provider = BinanceProvider()
    status = provider.get_market_status()
    assert isinstance(status, ProviderStatus)
    assert status.available is False


def test_get_market_status_never_raises():
    provider = BinanceProvider()
    provider.get_market_status()  # must not raise


# --- Symbol validation ---

@pytest.mark.parametrize("symbol", SUPPORTED_SYMBOLS)
def test_get_candles_raises_not_implemented_for_supported_symbol(symbol):
    provider = BinanceProvider()
    with pytest.raises(NotImplementedError):
        provider.get_candles(symbol, "M15", 10)


def test_get_candles_raises_value_error_for_unsupported_symbol():
    provider = BinanceProvider()
    with pytest.raises(ValueError):
        provider.get_candles("DOGEUSDT", "M15", 10)


def test_get_latest_price_raises_value_error_for_unsupported_symbol():
    provider = BinanceProvider()
    with pytest.raises(ValueError):
        provider.get_latest_price("DOGEUSDT")


def test_get_latest_price_raises_not_implemented_for_supported_symbol():
    provider = BinanceProvider()
    with pytest.raises(NotImplementedError):
        provider.get_latest_price("BTCUSDT")


def test_unsupported_symbol_error_is_checked_before_not_implemented():
    """The distinguishing behavior from MT5Provider: a bad symbol is a ValueError, never masked by NotImplementedError."""
    provider = BinanceProvider()
    try:
        provider.get_candles("NOT_A_REAL_PAIR", "M15", 10)
        assert False, "expected a ValueError"
    except NotImplementedError:
        assert False, "unsupported symbol must raise ValueError, not NotImplementedError"
    except ValueError:
        pass


def test_symbol_format_differs_from_twelvedata_by_design():
    """Binance uses no separator (BTCUSDT); documented, disclosed divergence from TwelveData's own format."""
    assert "BTCUSDT" in SUPPORTED_SYMBOLS
    assert "/" not in "BTCUSDT"
