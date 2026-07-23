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
    reply_keyboard,
    admin_reply_keyboard,
    owner_reply_keyboard,
    resolve_navigation_command,
)


def _reply_texts(markup):
    return [button.text for row in markup.keyboard for button in row]


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


# ---------------------------------------------------------------------------
# V2 Phase 5.1 (Director Approved) -- persistent Reply Keyboard, localized
# labels. Reverses Phase 5's "literal /command text" decision: buttons
# now show the same localized labels telegram.menu_commands' Persistent
# Menu (Phase 4) uses, resolved back to a command by Navigation Mapping
# (resolve_navigation_command()) inside command_router.route_command().
# ---------------------------------------------------------------------------


def test_reply_keyboard_labels_localized():
    en = _reply_texts(reply_keyboard("EN"))
    uz = _reply_texts(reply_keyboard("UZ"))
    ru = _reply_texts(reply_keyboard("RU"))

    assert en == ["🏠 Home", "👤 Profile", "📊 Signals", "💳 Subscription", "⚙️ Settings", "❓ Help"]
    assert uz == ["🏠 Bosh sahifa", "👤 Profil", "📊 Signallar", "💳 Obuna", "⚙️ Sozlamalar", "❓ Yordam"]
    assert ru == ["🏠 Главная", "👤 Профиль", "📊 Сигналы", "💳 Подписка", "⚙️ Настройки", "❓ Помощь"]


def test_reply_keyboard_defaults_to_english_with_no_language():
    assert _reply_texts(reply_keyboard()) == [
        "🏠 Home", "👤 Profile", "📊 Signals", "💳 Subscription", "⚙️ Settings", "❓ Help",
    ]


def test_reply_keyboard_is_resizable_and_not_one_time():
    markup = reply_keyboard()
    assert markup.resize_keyboard is True
    assert not markup.one_time_keyboard


def test_admin_reply_keyboard_is_user_set_plus_admin():
    assert _reply_texts(admin_reply_keyboard("UZ")) == [
        "🏠 Bosh sahifa", "👤 Profil", "📊 Signallar", "💳 Obuna", "⚙️ Sozlamalar", "❓ Yordam", "🛠 Admin",
    ]


def test_owner_reply_keyboard_is_admin_set_plus_owner():
    assert _reply_texts(owner_reply_keyboard("UZ")) == [
        "🏠 Bosh sahifa", "👤 Profil", "📊 Signallar", "💳 Obuna", "⚙️ Sozlamalar", "❓ Yordam", "🛠 Admin", "👑 Owner",
    ]


def test_navigation_map_resolves_every_localized_label_to_its_command():
    assert resolve_navigation_command("👤 Profil") == "/profile"
    assert resolve_navigation_command("👤 Profile") == "/profile"
    assert resolve_navigation_command("👤 Профиль") == "/profile"
    assert resolve_navigation_command("📊 Signallar") == "/signal"
    assert resolve_navigation_command("💳 Obuna") == "/subscription"
    assert resolve_navigation_command("⚙️ Sozlamalar") == "/settings"
    assert resolve_navigation_command("🏠 Bosh sahifa") == "/start"
    assert resolve_navigation_command("❓ Yordam") == "/help"
    assert resolve_navigation_command("🛠 Admin") == "/admin"
    assert resolve_navigation_command("👑 Owner") == "/owner"


def test_navigation_map_returns_none_for_non_navigation_text():
    assert resolve_navigation_command("random text") is None
    assert resolve_navigation_command("/profile") is None
    assert resolve_navigation_command("") is None
    assert resolve_navigation_command(None) is None


def test_command_router_routes_a_localized_navigation_label_like_its_command():
    from telegram.command_router import route_command

    by_label = asyncio.run(route_command("👤 Profil", telegram_id="703"))
    by_command = asyncio.run(route_command("/profile", telegram_id="703"))

    assert by_label.text == by_command.text


def test_command_router_attaches_a_keyboard_localized_to_the_caller():
    from telegram.command_router import route_command
    from telegram.user_service import UserService

    UserService().register_user("701", username="kbduz")
    UserService().change_language("701", "UZ")

    result = asyncio.run(route_command("/settings", telegram_id="701"))

    # V2 Phase 6.1 Director Decision 4: Settings is an editable page, so
    # its five categories now carry a trailing Back/Home row too.
    assert _labels(result.keyboard) == [
        "Til", "Risk", "Strategiya", "Vaqt oralig'i", "Bildirishnomalar", "⬅️ Orqaga", "🏠 Bosh sahifa",
    ]


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


# ---------------------------------------------------------------------------
# V2 Phase 6.1 (Director Approved) -- Navigation Controller / Unified
# Message Lifecycle: the six editable pages (telegram.navigation.
# EDITABLE_COMMANDS) carry the mandatory Back/Home inline row and are
# flagged editable=True on RouterResult.
# ---------------------------------------------------------------------------


def test_command_router_marks_editable_pages_per_director_decision_3():
    from telegram.command_router import route_command
    from telegram.user_service import UserService

    UserService().register_user("704", username="editableuser")

    for command in ("/profile", "/subscription", "/settings", "/help", "/about", "/history"):
        result = asyncio.run(route_command(command, telegram_id="704"))
        assert result.editable is True, f"{command} must be editable"


def test_command_router_start_and_signal_are_not_editable():
    from telegram.command_router import route_command
    from telegram.user_service import UserService

    UserService().register_user("705", username="notedituser")

    for command in ("/start", "/signal"):
        result = asyncio.run(route_command(command, telegram_id="705"))
        assert result.editable is False


def test_command_router_editable_pages_carry_the_back_home_row():
    from telegram.command_router import route_command
    from telegram.user_service import UserService

    UserService().register_user("706", username="backhomeuser")

    result = asyncio.run(route_command("/profile", telegram_id="706"))

    last_row = result.keyboard.inline_keyboard[-1]
    assert [b.callback_data for b in last_row] == ["nav_back", "nav_home"]
