"""
TASK-CORE-001 -- tests for the central structured configuration in
config.py (parse helpers, MaskedSecret, Settings blocks, required
validation, platform flags, backward compatibility).
"""

import pytest

import config as config_module
from config import (
    Config,
    ConfigError,
    MaskedSecret,
    Settings,
    build_settings,
    get_settings,
    parse_bool,
    parse_int,
    parse_list,
)


# --------------------------- parse helpers ---------------------------------
@pytest.mark.parametrize("value,expected", [
    ("true", True), ("True", True), ("1", True), ("yes", True), ("on", True),
    ("false", False), ("0", False), ("no", False), ("off", False),
    ("", False), (None, False), ("garbage", False),
])
def test_parse_bool(value, expected):
    assert parse_bool(value, default=False) is expected


def test_parse_bool_default_applies_only_on_unknown():
    assert parse_bool(None, default=True) is True
    assert parse_bool("false", default=True) is False  # explicit wins over default


@pytest.mark.parametrize("value,expected", [
    ("5", 5), ("  42 ", 42), ("-3", -3), ("", 7), (None, 7), ("x", 7), ("1.5", 7),
])
def test_parse_int(value, expected):
    assert parse_int(value, default=7) == expected


def test_parse_list_basic():
    assert parse_list("a,b, c ,,d") == ["a", "b", "c", "d"]
    assert parse_list("", ["x"]) == ["x"]
    assert parse_list(None, ["x"]) == ["x"]
    assert parse_list(None) == []


def test_parse_list_custom_separator():
    assert parse_list("a|b|c", sep="|") == ["a", "b", "c"]


# --------------------------- MaskedSecret ----------------------------------
def test_masked_secret_never_reveals_in_repr_or_str():
    secret = MaskedSecret("super-secret-value")
    assert "super-secret-value" not in repr(secret)
    assert "super-secret-value" not in str(secret)
    assert repr(secret) == "MaskedSecret(***)"
    assert bool(secret) is True
    assert secret.is_set is True
    assert secret.reveal() == "super-secret-value"


def test_masked_secret_unset():
    secret = MaskedSecret(None)
    assert secret.reveal() is None
    assert bool(secret) is False
    assert secret.is_set is False
    assert repr(secret) == "MaskedSecret(unset)"


def test_settings_repr_masks_all_secrets(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "TOKEN-abc123")
    monkeypatch.setenv("TWELVE_DATA_API_KEY", "TD-key-xyz")
    monkeypatch.setenv("GEMINI_API_KEY", "GM-key-789")
    settings = build_settings()
    blob = repr(settings)
    assert "TOKEN-abc123" not in blob
    assert "TD-key-xyz" not in blob
    assert "GM-key-789" not in blob
    # but the real values are still retrievable explicitly
    assert settings.telegram.bot_token.reveal() == "TOKEN-abc123"
    assert settings.providers.twelve_data_api_key.reveal() == "TD-key-xyz"
    assert settings.ai.gemini_api_key.reveal() == "GM-key-789"


# --------------------------- required validation ---------------------------
def test_required_missing_reports_all(monkeypatch):
    for name in ("TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID", "TWELVE_DATA_API_KEY"):
        monkeypatch.delenv(name, raising=False)
    settings = build_settings()
    missing = settings.required_missing()
    assert set(missing) == {"TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID", "TWELVE_DATA_API_KEY"}


def test_validate_required_raises_with_names_not_values(monkeypatch):
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "999")
    monkeypatch.setenv("TWELVE_DATA_API_KEY", "td")
    settings = build_settings()
    with pytest.raises(ConfigError) as excinfo:
        settings.validate_required(raise_error=True)
    assert "TELEGRAM_BOT_TOKEN" in str(excinfo.value)


def test_validate_required_all_present(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "t")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "c")
    monkeypatch.setenv("TWELVE_DATA_API_KEY", "d")
    settings = build_settings()
    assert settings.validate_required(raise_error=True) == []


# --------------------------- blocks / defaults -----------------------------
def test_defaults_when_env_unset(monkeypatch):
    for name in ("APP_ENV", "MARKET_DATA_PROVIDER", "DEFAULT_SYMBOL",
                 "AI_MODEL", "PLATFORM_MODE", "LOG_LEVEL"):
        monkeypatch.delenv(name, raising=False)
    s = build_settings()
    assert s.core.app_name == "GoldBot"
    assert s.core.mode == "development"
    assert s.providers.market_data_provider == "twelvedata"
    assert s.providers.enable_twelvedata is True
    assert s.market.default_symbol == "XAUUSD"
    assert "M15" in s.market.supported_timeframes
    assert s.ai.model_name == "gemini-2.5-flash"
    assert s.monitoring.log_level == "INFO"
    assert s.stream.polling_interval == 60


def test_env_overrides_are_applied(monkeypatch):
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("MARKET_DATA_PROVIDER", "bitget")
    monkeypatch.setenv("ENABLE_BITGET", "true")
    monkeypatch.setenv("SUPPORTED_SYMBOLS", "XAUUSD,BTCUSDT")
    monkeypatch.setenv("STREAM_INTERVAL", "3")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    s = build_settings()
    assert s.core.mode == "production"
    assert s.providers.market_data_provider == "bitget"
    assert s.providers.enable_bitget is True
    assert s.market.supported_symbols == ["XAUUSD", "BTCUSDT"]
    assert s.stream.stream_interval == 3
    assert s.monitoring.log_level == "DEBUG"


# --------------------------- platform flags --------------------------------
def test_platform_flags_default(monkeypatch):
    for name in ("ENABLE_PLATFORM_TELEGRAM", "ENABLE_PLATFORM_MINI_APP",
                 "ENABLE_PLATFORM_IOS", "ENABLE_PLATFORM_ANDROID",
                 "ENABLE_PLATFORM_DESKTOP"):
        monkeypatch.delenv(name, raising=False)
    s = build_settings()
    assert s.platform.enable_telegram is True
    assert s.platform.enable_mini_app is False
    assert s.platform.enable_ios is False
    assert s.platform.enable_android is False
    assert s.platform.enable_desktop is False


def test_platform_flags_future_enable(monkeypatch):
    monkeypatch.setenv("ENABLE_PLATFORM_MINI_APP", "true")
    monkeypatch.setenv("ENABLE_PLATFORM_IOS", "true")
    monkeypatch.setenv("ENABLE_PLATFORM_ANDROID", "true")
    monkeypatch.setenv("ENABLE_PLATFORM_DESKTOP", "true")
    s = build_settings()
    assert s.platform.enable_mini_app is True
    assert s.platform.enable_ios is True
    assert s.platform.enable_android is True
    assert s.platform.enable_desktop is True


# --------------------------- feature flags ---------------------------------
def test_feature_flags(monkeypatch):
    monkeypatch.setenv("FEATURE_AI_ANALYSIS", "true")
    monkeypatch.setenv("FEATURE_CHART_SUPPORT", "true")
    s = build_settings()
    assert s.features.signals is True          # default True
    assert s.features.ai_analysis is True      # overridden
    assert s.features.chart_support is True     # overridden


# --------------------------- singleton / interface -------------------------
def test_get_settings_returns_singleton():
    assert get_settings() is config_module.SETTINGS
    assert isinstance(get_settings(), Settings)


# --------------------------- backward compatibility ------------------------
def test_legacy_config_preserved():
    # The original flat Config contract that 12 modules depend on.
    # NB: conftest.py monkeypatches Config.DB_PATH to an isolated temp
    # *.db for the whole test session, so assert the stable shape (a
    # non-empty ".db" path) rather than the production filename.
    assert isinstance(Config.DB_PATH, str) and Config.DB_PATH.endswith(".db")
    assert Config.MARKET_DATA_PROVIDER
    assert Config.TIMEFRAME_HISTORY["M15"] == 200
    assert hasattr(Config, "TIMEZONE")
    assert hasattr(Config, "APP_ENV")
    assert hasattr(Config, "BASE_DIR")


def test_build_settings_never_raises_and_is_typed():
    # The root module invariant: building settings must always succeed.
    s = build_settings()
    assert isinstance(s, Settings)
    assert isinstance(config_module.SETTINGS, Settings)
