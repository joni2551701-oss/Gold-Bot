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


# ---------------------------------------------------------------------------
# V2 Phase 6.2 (Settings Callback Completion) -- `selected=` radio markers.
# `selected=None` (every pre-existing call site above) must stay
# byte-identical to pre-Phase-6.2 output; passing a value prefixes each
# button with a "●" (match) or "○" (no match) radio marker.
# ---------------------------------------------------------------------------


def test_risk_keyboard_selected_none_is_unchanged_from_pre_phase_6_2():
    assert _labels(risk_keyboard("UZ", selected=None)) == ["1%", "2%", "3%", "5%"]


def test_risk_keyboard_selected_marks_the_matching_option():
    labels = _labels(risk_keyboard("UZ", selected="3"))
    assert labels == ["○ 1%", "○ 2%", "● 3%", "○ 5%"]


def test_risk_keyboard_selected_callback_data_is_unaffected():
    assert _callback_data(risk_keyboard("UZ", selected="3")) == ["risk_1", "risk_2", "risk_3", "risk_5"]


def test_timeframe_keyboard_selected_marks_the_matching_option():
    labels = _labels(timeframe_keyboard("RU", selected="H1"))
    assert labels == ["○ M15", "● H1", "○ H4"]


def test_strategy_keyboard_selected_marks_the_matching_option():
    labels = _labels(strategy_keyboard("UZ", selected="fvg"))
    assert labels == ["○ Liquidity Sweep", "● FVG", "○ AMD", "○ Order Block"]


def test_notifications_keyboard_selected_marks_the_matching_option():
    labels = _labels(notifications_keyboard("EN", selected="off"))
    assert labels == ["○ Enable Notifications", "● Disable Notifications"]


def test_notifications_keyboard_selected_none_is_unchanged_from_pre_phase_6_2():
    uz = _labels(notifications_keyboard("UZ", selected=None))
    assert uz == ["Bildirishnomalarni yoqish", "Bildirishnomalarni o'chirish"]


def test_language_keyboard_accepts_but_ignores_selected():
    # language has no "current value you are adjusting" radio concept
    # (Director's spec) -- selected is accepted so command_router's
    # generic builder(language, selected=...) call site works uniformly,
    # but it never changes language_keyboard's output.
    assert _labels(language_keyboard("UZ", selected="uz")) == ["🇺🇿 Uzbek", "🇷🇺 Русский", "🇬🇧 English"]


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

    # V2 Phase 6.3: Settings is a Reply Keyboard section now, not an
    # inline value-picker with a Back/Home row.
    assert _reply_texts(result.keyboard) == [
        "🌐 Til", "💰 Risk", "📈 Strategiya", "⏰ Vaqt oralig'i", "🔔 Bildirishnomalar", "◀️ Ortga",
    ]


def test_command_router_admin_keyboard_localizes_to_the_callers_language(monkeypatch):
    from telegram.command_router import route_command
    from telegram.user_service import UserService
    from telegram.permissions import PermissionLevel

    monkeypatch.setattr(
        "telegram.command_router.get_permission_level", lambda telegram_id: PermissionLevel.OWNER,
    )
    UserService().register_user("702", username="kbdadmin")
    UserService().change_language("702", "RU")

    result = asyncio.run(route_command("/admin", telegram_id="702"))

    # V2 Phase 6.3 Addendum (Director Review correction 3): Admin/Owner
    # submenus localize like every other submenu -- no more English-only.
    assert _reply_texts(result.keyboard) == [
        "👥 Пользователи", "📊 Статистика", "🛠 Система", "📢 Рассылка",
        "👑 Управление администраторами", "◀️ Назад",
    ]


# ---------------------------------------------------------------------------
# V2 Phase 6.3 (Director Approved: "Dynamic Reply Keyboard Navigation") --
# Reply Keyboard is GoldBot's sole navigation; Director's mandatory test
# list: Main->Settings, Settings->Back, Main->Profile, Profile->Back,
# Main->Admin, Main->Owner, USER doesn't see admin, USER doesn't see owner.
# ("Registration-completion keyboard switch" and "BANNED gets no keyboard"
# are already covered by tests/telegram/test_phone_registration.py's
# existing test_route_contact_attaches_the_persistent_reply_keyboard_on_completion
# and test_start_keyboard_is_reply_keyboard_remove_for_a_banned_user -- that
# behavior is unchanged by Phase 6.3, only the keyboard's source moved to
# telegram.reply_keyboard_manager.)
# ---------------------------------------------------------------------------


def test_navigation_main_to_settings_switches_to_the_settings_reply_keyboard():
    from telegram.command_router import route_command
    from telegram.user_service import UserService

    UserService().register_user("710", username="navsettings")
    UserService().change_language("710", "EN")

    result = asyncio.run(route_command("/settings", telegram_id="710"))

    assert _reply_texts(result.keyboard) == [
        "🌐 Language", "💰 Risk", "📈 Strategy", "⏰ Timeframe", "🔔 Notifications", "◀️ Back",
    ]


def test_navigation_settings_back_returns_to_the_main_reply_keyboard():
    from telegram.command_router import route_command
    from telegram.user_service import UserService
    from telegram.registration_service import RegistrationService

    UserService().register_user("711", username="navsettingsback")
    UserService().change_language("711", "EN")
    RegistrationService().complete("711")
    asyncio.run(route_command("/settings", telegram_id="711"))

    result = asyncio.run(route_command("◀️ Back", telegram_id="711"))

    assert _reply_texts(result.keyboard) == [
        "🏠 Home", "👤 Profile", "📊 Signals", "💳 Subscription", "⚙️ Settings", "❓ Help",
    ]


def test_navigation_main_to_profile_switches_to_the_profile_reply_keyboard():
    from telegram.command_router import route_command
    from telegram.user_service import UserService

    UserService().register_user("712", username="navprofile")
    UserService().change_language("712", "EN")

    result = asyncio.run(route_command("/profile", telegram_id="712"))

    # V2 Phase 6.3 Addendum (Director Review correction 2): no Statistics
    # button on Profile -- no per-user statistics feature exists yet.
    assert _reply_texts(result.keyboard) == [
        "📄 Profile", "💳 Subscription", "◀️ Back",
    ]


def test_navigation_profile_back_returns_to_the_main_reply_keyboard():
    from telegram.command_router import route_command
    from telegram.user_service import UserService
    from telegram.registration_service import RegistrationService

    UserService().register_user("713", username="navprofileback")
    UserService().change_language("713", "EN")
    RegistrationService().complete("713")
    asyncio.run(route_command("/profile", telegram_id="713"))

    result = asyncio.run(route_command("◀️ Back", telegram_id="713"))

    assert _reply_texts(result.keyboard) == [
        "🏠 Home", "👤 Profile", "📊 Signals", "💳 Subscription", "⚙️ Settings", "❓ Help",
    ]


def test_navigation_main_to_admin_switches_to_the_admin_submenu_reply_keyboard(monkeypatch):
    from telegram.command_router import route_command
    from telegram.user_service import UserService
    from telegram.permissions import PermissionLevel

    monkeypatch.setattr(
        "telegram.command_router.get_permission_level", lambda telegram_id: PermissionLevel.ADMIN,
    )
    UserService().register_user("714", username="navadmin")
    UserService().change_language("714", "EN")

    result = asyncio.run(route_command("/admin", telegram_id="714"))

    assert _reply_texts(result.keyboard) == [
        "👥 Users", "📊 Statistics", "🛠 System", "📢 Broadcast", "👑 Admin Management", "◀️ Back",
    ]


def test_navigation_admin_management_button_reopens_the_admin_panel_not_addadmin(monkeypatch):
    """V2 Phase 6.3 Addendum (Director Review correction 1): tapping
    "👑 Admin Management" must re-open the Admin Panel (/admin), never
    directly invoke /addadmin (an action, not a menu destination)."""
    from telegram.command_router import route_command
    from telegram.user_service import UserService
    from telegram.permissions import PermissionLevel

    monkeypatch.setattr(
        "telegram.command_router.get_permission_level", lambda telegram_id: PermissionLevel.OWNER,
    )
    UserService().register_user("718", username="navadminmgmt")
    UserService().change_language("718", "EN")

    asyncio.run(route_command("/admin", telegram_id="718"))
    result = asyncio.run(route_command("👑 Admin Management", telegram_id="718"))

    assert result.text != "Usage: /addadmin USER_ID"
    assert _reply_texts(result.keyboard) == [
        "👥 Users", "📊 Statistics", "🛠 System", "📢 Broadcast", "👑 Admin Management", "◀️ Back",
    ]


def test_navigation_main_to_owner_switches_to_the_owner_submenu_reply_keyboard(monkeypatch):
    from telegram.command_router import route_command
    from telegram.user_service import UserService
    from telegram.permissions import PermissionLevel

    monkeypatch.setattr(
        "telegram.command_router.get_permission_level", lambda telegram_id: PermissionLevel.OWNER,
    )
    UserService().register_user("715", username="navowner")
    UserService().change_language("715", "EN")

    result = asyncio.run(route_command("/owner", telegram_id="715"))

    assert _reply_texts(result.keyboard) == [
        "⚙️ Runtime", "❤️ Health", "📈 Performance", "🚨 Errors", "📦 Pipeline", "📋 Reports", "◀️ Back",
    ]


def test_navigation_regular_user_does_not_see_the_admin_keyboard():
    from telegram.command_router import route_command, PERMISSION_DENIED_TEXT
    from telegram.user_service import UserService

    UserService().register_user("716", username="navuseradmin")

    result = asyncio.run(route_command("/admin", telegram_id="716"))

    assert result.text == PERMISSION_DENIED_TEXT
    assert result.keyboard is None


def test_navigation_regular_user_does_not_see_the_owner_keyboard():
    from telegram.command_router import route_command, PERMISSION_DENIED_TEXT
    from telegram.user_service import UserService

    UserService().register_user("717", username="navuserowner")

    result = asyncio.run(route_command("/owner", telegram_id="717"))

    assert result.text == PERMISSION_DENIED_TEXT
    assert result.keyboard is None
