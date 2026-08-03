"""
Phase A13 -- Configuration Layer tests: ApplicationSettings
(configuration/settings.py).
"""

import dataclasses

import pytest

from config import Config
from core_layer.configuration.environment import Environment
from core_layer.configuration.settings import ApplicationSettings, build_settings_from_config


def test_settings_creation_matches_director_example():
    settings = ApplicationSettings(
        environment=Environment.PRODUCTION,
        symbol="XAUUSD",
        default_timeframe="M15",
        timezone="UTC",
    )

    assert settings.environment == Environment.PRODUCTION
    assert settings.symbol == "XAUUSD"
    assert settings.default_timeframe == "M15"
    assert settings.timezone == "UTC"


def test_settings_is_immutable():
    settings = ApplicationSettings(
        environment=Environment.DEVELOPMENT, symbol="XAUUSD",
        default_timeframe="M15", timezone="UTC",
    )
    with pytest.raises(dataclasses.FrozenInstanceError):
        settings.symbol = "EURUSD"


def test_build_settings_from_config_uses_real_symbol_and_timeframe():
    """
    symbol/default_timeframe must match the exact literals main.py's
    TradingPipeline(symbol="XAUUSD", interval="M15", ...) already
    uses -- not an invented value.
    """
    settings = build_settings_from_config()

    assert settings.symbol == "XAUUSD"
    assert settings.default_timeframe == "M15"


def test_build_settings_from_config_reflects_real_timezone():
    """timezone must be derived from config.Config.TIMEZONE, not a separately hardcoded literal."""
    settings = build_settings_from_config()

    assert settings.timezone == str(Config.TIMEZONE)
    assert settings.timezone == "UTC"


def test_build_settings_from_config_resolves_known_app_env(monkeypatch):
    monkeypatch.setattr(Config, "APP_ENV", "production")
    assert build_settings_from_config().environment == Environment.PRODUCTION

    monkeypatch.setattr(Config, "APP_ENV", "testing")
    assert build_settings_from_config().environment == Environment.TESTING


def test_build_settings_from_config_degrades_safely_on_unrecognized_app_env(monkeypatch):
    """An unrecognized Config.APP_ENV value must not crash settings construction."""
    monkeypatch.setattr(Config, "APP_ENV", "staging")
    settings = build_settings_from_config()
    assert settings.environment == Environment.DEVELOPMENT
