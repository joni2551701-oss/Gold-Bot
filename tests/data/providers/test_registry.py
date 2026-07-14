"""
Phase 59.2, TASK 5/9 -- data/providers/registry.py tests.
"""

from data.providers.base_provider import DataProvider, ProviderStatus
from data.providers.binance_provider import BinanceProvider
from data.providers.fred_provider import FredProvider
from data.providers.mt5_provider import MT5Provider
from data.providers.registry import ProviderRegistry, build_default_registry
from data.providers.twelve_data_provider import TwelveDataProvider


def test_empty_registry_has_no_providers():
    registry = ProviderRegistry()
    assert registry.all_names() == []
    assert registry.available() == []


def test_register_keys_by_the_providers_own_name():
    registry = ProviderRegistry()
    registry.register(MT5Provider())
    assert registry.get("mt5") is not None
    assert isinstance(registry.get("mt5"), MT5Provider)


def test_get_is_case_and_whitespace_insensitive():
    registry = ProviderRegistry()
    registry.register(MT5Provider())
    assert registry.get(" MT5 ") is not None


def test_get_returns_none_for_unregistered_name():
    registry = ProviderRegistry()
    assert registry.get("nonexistent") is None


def test_register_twice_under_same_name_replaces_not_duplicates():
    registry = ProviderRegistry()
    first = MT5Provider()
    second = MT5Provider()
    registry.register(first)
    registry.register(second)

    assert registry.all_names() == ["mt5"]
    assert registry.get("mt5") is second


def test_build_default_registry_registers_all_four_stubs_and_real_provider():
    registry = build_default_registry()

    assert set(registry.all_names()) == {"twelvedata", "mt5", "binance", "fred"}
    assert isinstance(registry.get("twelvedata"), TwelveDataProvider)
    assert isinstance(registry.get("mt5"), MT5Provider)
    assert isinstance(registry.get("binance"), BinanceProvider)
    assert isinstance(registry.get("fred"), FredProvider)


def test_build_default_registry_does_not_include_tradingview():
    registry = build_default_registry()
    assert registry.get("tradingview") is None


def test_available_lists_only_providers_reporting_available_true(monkeypatch):
    registry = ProviderRegistry()

    class AlwaysOnline(DataProvider):
        def get_provider_name(self):
            return "always_online"

        def get_market_status(self):
            return ProviderStatus(available=True)

    registry.register(AlwaysOnline())
    registry.register(MT5Provider())  # always unavailable

    assert registry.available() == ["always_online"]


def test_available_never_raises_even_with_every_stub_registered():
    registry = build_default_registry()
    registry.available()  # must not raise, regardless of any provider's real status


def test_disabled_provider_is_registered_but_not_available():
    """A registered-but-unimplemented provider (MT5/Binance/FRED) stays discoverable via all_names(), just not available()."""
    registry = build_default_registry()

    assert "mt5" in registry.all_names()
    assert "mt5" not in registry.available()
    assert "binance" in registry.all_names()
    assert "binance" not in registry.available()
    assert "fred" in registry.all_names()
    assert "fred" not in registry.available()
