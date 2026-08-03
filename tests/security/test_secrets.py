"""
Phase 52 — Secrets/missing-credential security tests.

Every test in the rest of the suite runs with tests/conftest.py's fake
(but present) secrets -- meaning the "missing secret" code paths in
core/secrets.py and its callers had zero test coverage before this
phase. Uses monkeypatch.delenv() (auto-restored after each test) to
exercise the real missing-secret behavior without affecting any other
test's environment.
"""

import pytest

from core_layer.secrets import Secrets


def test_secrets_get_raises_when_required_value_missing(monkeypatch):
    monkeypatch.delenv("TWELVE_DATA_API_KEY", raising=False)
    with pytest.raises(ValueError):
        Secrets().TWELVE_DATA_API_KEY


def test_secrets_get_returns_default_when_missing_and_default_given(monkeypatch):
    monkeypatch.delenv("TELEGRAM_OWNER_ID", raising=False)
    assert Secrets().TELEGRAM_OWNER_ID == ""  # fail-closed default, never raises


def test_twelve_data_client_handles_missing_api_key_gracefully(monkeypatch):
    """Construction must never raise; fetch_candles() reports the failure per-call instead."""
    monkeypatch.delenv("TWELVE_DATA_API_KEY", raising=False)
    from data_layer.providers.twelve_data_client import TwelveDataClient

    client = TwelveDataClient()
    assert client.api_key is None

    with pytest.raises(ValueError, match="TWELVE_DATA_API_KEY not configured"):
        client.fetch_candles("XAUUSD", "M15")


def test_market_data_normalizer_returns_empty_list_when_api_key_missing(monkeypatch):
    """The layer TradingPipeline actually calls must degrade to [] candles, never raise."""
    monkeypatch.delenv("TWELVE_DATA_API_KEY", raising=False)
    from data_layer.live_data.market_data import MarketDataNormalizer

    candles = MarketDataNormalizer().get_candles("XAUUSD", "M15", 200)
    assert candles == []


def test_telegram_bot_handles_missing_token_gracefully(monkeypatch):
    """Construction must never raise; send_message() reports the failure per-call instead."""
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    from platform_layer.telegram.bot import TelegramBot
    import asyncio

    bot = TelegramBot()
    assert bot._bot is None

    result = asyncio.run(bot.send_message("hello", chat_id="123"))
    assert result.sent is False
    assert "not configured" in result.reason


def test_owner_permission_fails_closed_when_owner_id_unset(monkeypatch):
    """No TELEGRAM_OWNER_ID configured -> nobody is OWNER, ever (fail-closed)."""
    monkeypatch.delenv("TELEGRAM_OWNER_ID", raising=False)
    from platform_layer.telegram.permissions import is_owner

    assert is_owner("111") is False  # even the ID conftest normally treats as OWNER
    assert is_owner(None) is False
