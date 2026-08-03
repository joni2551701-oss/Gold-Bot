"""
Phase 54 — secret-exposure security tests.

Distinct from tests/security/test_secrets.py (Phase 52, which covers
missing-secret graceful degradation). This file covers the opposite
direction: when a secret IS present, does anything ever leak its
value into a log line, an exception message, or a Telegram response?
"""

import logging

from core_layer.secrets import Secrets


def test_config_class_has_no_hardcoded_secret_looking_values():
    """
    config.py must never hardcode a token/key -- only Secrets (backed
    by environment variables) may hold credential material.
    """
    import config

    for name in dir(config.Config):
        if name.startswith("_"):
            continue
        value = getattr(config.Config, name)
        if isinstance(value, str):
            assert not value.startswith("AIza"), f"config.Config.{name} looks like a hardcoded Google API key"
            assert ":" not in value or len(value) < 20, (
                f"config.Config.{name} looks like a hardcoded bot-token-shaped value: {name}"
            )


def test_secrets_class_exposes_only_named_properties_not_a_bulk_dump():
    """
    No .get_all()/.__dict__ style bulk-export exists on Secrets that
    could leak everything at once. `get_optional` (Phase 61.2 TASK 2)
    is allowed alongside `get` -- both take one explicit key argument
    and return exactly that one value; neither can be called with no
    argument to dump every secret at once, which is the property this
    test actually guards.
    """
    public_callables = [
        name for name in dir(Secrets)
        if not name.startswith("_") and callable(getattr(Secrets, name, None))
    ]
    assert set(public_callables) == {"get", "get_optional"}, (
        f"Secrets exposes unexpected bulk/dump-style methods: {public_callables}"
    )


def test_telegram_bot_init_failure_log_does_not_contain_the_token_value(monkeypatch, caplog):
    """
    A real (fake-but-realistic) token is deliberately set, then the
    underlying Bot() construction is forced to fail -- the resulting
    log line must describe the failure, never echo the token itself.
    """
    from telegram.bot import TelegramBot

    fake_token = "123456789:AAFakeTokenThatMustNeverAppearInLogsXYZ"
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", fake_token)
    monkeypatch.setattr(
        "telegram.bot.Bot",
        lambda *a, **k: (_ for _ in ()).throw(ValueError("simulated aiogram construction failure")),
    )

    with caplog.at_level(logging.WARNING, logger="TelegramBot"):
        bot = TelegramBot()

    assert bot._bot is None
    assert fake_token not in caplog.text


def test_market_data_normalizer_error_log_does_not_contain_the_api_key(monkeypatch, caplog):
    fake_key = "FAKE_TWELVE_DATA_KEY_MUST_NOT_LEAK_9f8e7d"
    monkeypatch.setenv("TWELVE_DATA_API_KEY", fake_key)
    monkeypatch.setattr(
        "data.twelve_data_client.TwelveDataClient.fetch_candles",
        lambda self, *a, **k: (_ for _ in ()).throw(ConnectionError("simulated network failure")),
    )

    from data.market_data import MarketDataNormalizer

    with caplog.at_level(logging.ERROR, logger="MarketDataNormalizer"):
        candles = MarketDataNormalizer().get_candles("XAUUSD", "M15", 200)

    assert candles == []
    assert fake_key not in caplog.text


def test_handler_error_responses_never_contain_a_secret_value(monkeypatch):
    """
    telegram/handlers.py's f"...: {e}" error responses echo the
    *exception message*, not any secret -- confirm no code path can
    smuggle a secret into an exception raised from user-facing service
    calls.
    """
    import asyncio
    from telegram.command_router import route_command

    fake_owner_id = "SUPER_SECRET_OWNER_TOKEN_abc123"
    monkeypatch.setenv("TELEGRAM_OWNER_ID", fake_owner_id)

    result = asyncio.run(route_command("/profile", telegram_id="9401"))
    assert fake_owner_id not in result.text
