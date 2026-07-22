"""
Telegram Layer -- keyboard localization tests (Phase 1.5 Localized
Keyboards). Every USER-tier keyboard in telegram/keyboards.py takes an
optional `language` and resolves its button labels via
translation.ui_catalog.t(); callback_data must never change with
language. admin_panel_keyboard() is deliberately excluded -- it stays
English-only (Director decision), so it keeps its original zero-arg
signature and is not covered here beyond a stability check.
"""

import asyncio

from telegram.keyboards import (
    language_keyboard,
    risk_keyboard,
    timeframe_keyboard,
    strategy_keyboard,
    settings_keyboard,
    admin_panel_keyboard,
    notifications_keyboard,
    phone_share_keyboard,
)


def _labels(markup):
    return [button.text for row in markup.inline_keyboard for button in row]


def _callback_data(markup):
    return [button.callback_data for row in markup.inline_keyboard for button in row]


def test_settings_keyboard_labels_change_with_language():
    en = _labels(settings_keyboard("EN"))
    uz = _labels(settings_keyboard("UZ"))
    ru = _labels(settings_keyboard("RU"))

    assert en == ["Language", "Risk", "Strategy", "Timeframe", "Notifications"]
    assert uz == ["Til", "Risk", "Strategiya", "Vaqt oralig'i", "Bildirishnomalar"]
    assert ru == ["Язык", "Риск", "Стратегия", "Таймфрейм", "Уведомления"]


def test_settings_keyboard_callback_data_is_unaffected_by_language():
    en_data = _callback_data(settings_keyboard("EN"))
    uz_data = _callback_data(settings_keyboard("UZ"))

    assert en_data == uz_data == [
        "settings_language", "settings_risk", "settings_strategy",
        "settings_timeframe", "settings_notifications",
    ]


def test_settings_keyboard_defaults_to_english_with_no_language():
    assert _labels(settings_keyboard()) == ["Language", "Risk", "Strategy", "Timeframe", "Notifications"]


def test_notifications_keyboard_labels_localized():
    uz = _labels(notifications_keyboard("UZ"))
    assert uz == ["Bildirishnomalarni yoqish", "Bildirishnomalarni o'chirish"]

    en_data = _callback_data(notifications_keyboard("EN"))
    assert en_data == ["notifications_on", "notifications_off"]


def test_language_keyboard_labels_are_stable_across_languages():
    # A language picker always shows each option in its own native
    # name, regardless of the caller's current language.
    en = _labels(language_keyboard("EN"))
    uz = _labels(language_keyboard("UZ"))
    ru = _labels(language_keyboard("RU"))

    assert en == uz == ru == ["🇺🇿 Uzbek", "🇷🇺 Русский", "🇬🇧 English"]

    data = _callback_data(language_keyboard("UZ"))
    assert data == ["lang_uz", "lang_ru", "lang_en"]


def test_risk_keyboard_labels_and_callback_data():
    assert _labels(risk_keyboard("UZ")) == ["1%", "2%", "3%", "5%"]
    assert _callback_data(risk_keyboard("UZ")) == ["risk_1", "risk_2", "risk_3", "risk_5"]


def test_timeframe_keyboard_labels_and_callback_data():
    assert _labels(timeframe_keyboard("RU")) == ["M15", "H1", "H4"]
    assert _callback_data(timeframe_keyboard("RU")) == ["timeframe_m15", "timeframe_h1", "timeframe_h4"]


def test_strategy_keyboard_labels_and_callback_data():
    labels = _labels(strategy_keyboard("UZ"))
    assert labels == ["Liquidity Sweep", "FVG", "AMD", "Order Block"]

    data = _callback_data(strategy_keyboard("UZ"))
    assert data == [
        "strategy_liquidity_sweep", "strategy_fvg", "strategy_amd", "strategy_order_block",
    ]


def test_phone_share_keyboard_label_localized():
    markup = phone_share_keyboard("UZ")
    button = markup.keyboard[0][0]
    assert button.text == "📱 Telefon raqamini yuborish"
    assert button.request_contact is True


def test_phone_share_keyboard_defaults_to_english_with_no_language():
    button = phone_share_keyboard().keyboard[0][0]
    assert button.text == "📱 Share Phone Number"


def test_admin_panel_keyboard_stays_english_only_and_zero_arg():
    # OWNER/ADMIN tier -- Director decision, excluded from Phase 1.5.
    labels = _labels(admin_panel_keyboard())
    assert labels == ["Users", "Statistics", "System", "Broadcast", "Admins"]


def test_command_router_attaches_a_keyboard_localized_to_the_caller():
    from telegram.command_router import route_command
    from telegram.user_service import UserService

    UserService().register_user("701", username="kbduz")
    UserService().change_language("701", "UZ")

    result = asyncio.run(route_command("/settings", telegram_id="701"))

    assert _labels(result.keyboard) == ["Til", "Risk", "Strategiya", "Vaqt oralig'i", "Bildirishnomalar"]


def test_command_router_admin_keyboard_stays_english_regardless_of_caller_language(monkeypatch):
    from telegram.command_router import route_command
    from telegram.user_service import UserService
    from telegram.permissions import PermissionLevel

    monkeypatch.setattr(
        "telegram.command_router.get_permission_level", lambda telegram_id: PermissionLevel.OWNER,
    )
    UserService().register_user("702", username="kbdadmin")
    UserService().change_language("702", "RU")

    result = asyncio.run(route_command("/admin", telegram_id="702"))

    assert _labels(result.keyboard) == ["Users", "Statistics", "System", "Broadcast", "Admins"]
