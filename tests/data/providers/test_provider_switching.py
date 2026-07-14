"""
Phase 59.1, TASK 8 -- data/providers/__init__.py's get_provider()
factory tests.
"""

import pytest

from config import Config
from data.providers import get_provider
from data.providers.mt5_provider import MT5Provider
from data.providers.twelve_data_provider import TwelveDataProvider


def test_get_provider_defaults_to_config_market_data_provider(monkeypatch):
    monkeypatch.setattr(Config, "MARKET_DATA_PROVIDER", "twelvedata")
    monkeypatch.setattr(Config, "ENABLE_TWELVEDATA", True)

    provider = get_provider()

    assert isinstance(provider, TwelveDataProvider)


def test_get_provider_accepts_an_explicit_name_override(monkeypatch):
    monkeypatch.setattr(Config, "MARKET_DATA_PROVIDER", "twelvedata")
    monkeypatch.setattr(Config, "ENABLE_MT5", True)

    provider = get_provider("mt5")

    assert isinstance(provider, MT5Provider)


def test_get_provider_is_case_insensitive(monkeypatch):
    monkeypatch.setattr(Config, "ENABLE_TWELVEDATA", True)

    provider = get_provider("TwelveData")

    assert isinstance(provider, TwelveDataProvider)


def test_get_provider_rejects_unknown_name():
    with pytest.raises(ValueError):
        get_provider("bogus_provider")


def test_get_provider_rejects_mt5_without_enable_flag(monkeypatch):
    monkeypatch.setattr(Config, "ENABLE_MT5", False)

    with pytest.raises(ValueError):
        get_provider("mt5")


def test_get_provider_accepts_mt5_with_enable_flag(monkeypatch):
    monkeypatch.setattr(Config, "ENABLE_MT5", True)

    provider = get_provider("mt5")

    assert isinstance(provider, MT5Provider)
    # System does not crash even though MT5 is not really implemented:
    status = provider.get_market_status()
    assert status.available is False


def test_get_provider_rejects_twelvedata_without_enable_flag(monkeypatch):
    monkeypatch.setattr(Config, "ENABLE_TWELVEDATA", False)

    with pytest.raises(ValueError):
        get_provider("twelvedata")


def test_switching_between_providers_produces_independent_instances(monkeypatch):
    monkeypatch.setattr(Config, "ENABLE_TWELVEDATA", True)
    monkeypatch.setattr(Config, "ENABLE_MT5", True)

    twelvedata = get_provider("twelvedata")
    mt5 = get_provider("mt5")

    assert type(twelvedata) is not type(mt5)
    assert isinstance(twelvedata, TwelveDataProvider)
    assert isinstance(mt5, MT5Provider)


def test_mt5_absence_never_crashes_the_system_when_disabled(monkeypatch):
    """MARKET_DATA_PROVIDER defaults to twelvedata -- MT5 being unimplemented must not affect a normal run."""
    monkeypatch.setattr(Config, "MARKET_DATA_PROVIDER", "twelvedata")
    monkeypatch.setattr(Config, "ENABLE_TWELVEDATA", True)

    provider = get_provider()  # must not raise, must not touch MT5 at all

    assert isinstance(provider, TwelveDataProvider)


def test_default_config_values_are_twelvedata_live_mt5_disabled():
    """The real, unmocked Config defaults -- confirms production configuration matches this phase's intent."""
    assert Config.MARKET_DATA_PROVIDER == "twelvedata"
    assert Config.ENABLE_TWELVEDATA is True
    assert Config.ENABLE_MT5 is False
