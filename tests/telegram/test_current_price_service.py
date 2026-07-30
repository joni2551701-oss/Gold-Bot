"""
Tests for telegram/current_price_service.py + price_handler + wiring
(TASK-CORE-004 Phase 1). Read-only, informational; no signal/risk/AI path.
"""

import asyncio
from datetime import datetime, timezone

from data.current_price_provider import CurrentPrice
from telegram.current_price_service import CurrentPriceService, DEFAULT_ASSET
from telegram import commands as tg_commands
from telegram import reply_keyboard_manager as rkm
from translation.ui_catalog import t

BASE = datetime(2026, 1, 1, 14, 52, 8, tzinfo=timezone.utc)


class _FakeProvider:
    def __init__(self, result):
        self._r = result
    def get_current_price(self, symbol):
        return self._r


def _svc(result):
    return CurrentPriceService(provider=_FakeProvider(result))


# ---------------- rendering ----------------

def test_render_xau_block_localized_en():
    cp = CurrentPrice(asset="XAUUSD", price=3368.42, timestamp=BASE)
    text = _svc(cp).render(language="EN", symbol="XAUUSD")
    assert text == (
        "📊 Current Price\n🥇 XAU/USD\nPrice:\n3368.42\nUpdated:\n14:52:08 UTC"
    )


def test_render_uses_localized_labels_ru():
    cp = CurrentPrice(asset="XAUUSD", price=3368.42, timestamp=BASE)
    text = _svc(cp).render(language="RU", symbol="XAUUSD")
    assert t("price.title", "RU") in text        # localized header
    assert "🥇 XAU/USD" in text and "3368.42" in text and "14:52:08 UTC" in text


def test_render_no_thousands_separator():
    cp = CurrentPrice(asset="XAUUSD", price=3368.42, timestamp=BASE)
    assert "3368.42" in _svc(cp).render(symbol="XAUUSD") and "3,368" not in _svc(cp).render(symbol="XAUUSD")


def test_render_empty_state_when_no_price():
    assert _svc(None).render(language="EN") == t("price.empty", "EN")


def test_render_unknown_asset_is_empty_state():
    cp = CurrentPrice(asset="DOGEUSDT", price=1.0, timestamp=BASE)
    assert _svc(cp).render(language="EN", symbol="DOGEUSDT") == t("price.empty", "EN")


def test_render_default_asset_is_xauusd():
    assert DEFAULT_ASSET == "XAUUSD"


def test_render_failsafe_on_raising_provider():
    class _Boom:
        def get_current_price(self, s):
            raise RuntimeError("boom")
    out = CurrentPriceService(provider=_Boom()).render(language="EN")
    assert out == t("price.empty", "EN")  # never raises


def test_output_contains_no_secret_like_fields():
    cp = CurrentPrice(asset="XAUUSD", price=3368.42, timestamp=BASE)
    out = _svc(cp).render(symbol="XAUUSD")
    for forbidden in ("token", "Token", "secret", "api_key", "API_KEY", "chat_id", "bot"):
        assert forbidden not in out


# ---------------- handler ----------------

def test_price_handler_returns_string_never_raises():
    from telegram.handlers import price_handler
    # No stored price in a fresh test env -> empty-state string; must not raise.
    out = asyncio.run(price_handler("999999"))
    assert isinstance(out, str) and out


# ---------------- wiring ----------------

def test_price_command_registered_user_tier():
    assert "price" in tg_commands.COMMANDS
    assert "price" not in tg_commands.OWNER_COMMANDS
    assert "price" not in tg_commands.ADMIN_COMMANDS


def test_price_button_in_signals_section():
    assert rkm._SECTION_BY_COMMAND.get("price") == rkm.SECTION_SIGNALS
    assert rkm._SECTION_LABEL_KEYS[rkm.SECTION_SIGNALS].get("price") == "rkm.signals.price"


def test_price_button_label_localized_all_languages():
    for lang in ("EN", "UZ", "RU"):
        label = t("rkm.signals.price", lang)
        assert label and "{" not in label  # resolved, not a missing-key echo


def test_price_label_maps_back_to_command():
    # the localized button text resolves to "/price" via the section map
    for lang in ("EN", "UZ", "RU"):
        label = t("rkm.signals.price", lang)
        assert rkm._SECTION_MAPS[rkm.SECTION_SIGNALS].get(label) == "/price"
