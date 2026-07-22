"""
Telegram Layer — inline keyboard foundation.

language_keyboard(), risk_keyboard(), timeframe_keyboard(),
strategy_keyboard(), and settings_keyboard() (Phase 40) are real: each
renders the options telegram/handlers.py documents in its command's
"no argument" prompt text. Their callback_data carries the value the
user would need to pass as a command argument (e.g. "risk_5" ->
"/risk 5"), but no aiogram callback_query handler consumes it yet --
these are display hints, same precedent as language_keyboard() since
Phase 34. Real settings changes happen via command arguments (e.g.
"/risk 5"), handled by telegram.handlers / telegram.user_service; see
telegram/handlers.py's module docstring for why. admin_panel_keyboard()
stays a placeholder -- no admin panel UI exists yet, only text (Phase
37's /admin).

Phase 1.5 Localized Keyboards: every USER-tier keyboard below takes an
optional `language` parameter and resolves its button labels via
translation.ui_catalog.t() (callback_data is never touched -- only the
label a user sees changes). admin_panel_keyboard() is intentionally
excluded and stays English-only -- OWNER/ADMIN keyboards are Director
decision, out of scope for USER-facing localization. Callers resolve
`language` the same way telegram/handlers.py's own handlers do (see
telegram.handlers._current_language()); see
telegram/command_router.py and telegram/callback_router.py for where
that value is supplied.
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup

from translation.ui_catalog import t


def language_keyboard(language=None):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t("keyboard.language.uz", language), callback_data="lang_uz")],
            [InlineKeyboardButton(text=t("keyboard.language.ru", language), callback_data="lang_ru")],
            [InlineKeyboardButton(text=t("keyboard.language.en", language), callback_data="lang_en")],
        ]
    )


def risk_keyboard(language=None):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t("keyboard.risk.1", language), callback_data="risk_1"),
                InlineKeyboardButton(text=t("keyboard.risk.2", language), callback_data="risk_2"),
                InlineKeyboardButton(text=t("keyboard.risk.3", language), callback_data="risk_3"),
                InlineKeyboardButton(text=t("keyboard.risk.5", language), callback_data="risk_5"),
            ]
        ]
    )


def timeframe_keyboard(language=None):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t("keyboard.timeframe.m15", language), callback_data="timeframe_m15"),
                InlineKeyboardButton(text=t("keyboard.timeframe.h1", language), callback_data="timeframe_h1"),
                InlineKeyboardButton(text=t("keyboard.timeframe.h4", language), callback_data="timeframe_h4"),
            ]
        ]
    )


def strategy_keyboard(language=None):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=t("keyboard.strategy.liquidity_sweep", language), callback_data="strategy_liquidity_sweep",
            )],
            [InlineKeyboardButton(text=t("keyboard.strategy.fvg", language), callback_data="strategy_fvg")],
            [InlineKeyboardButton(text=t("keyboard.strategy.amd", language), callback_data="strategy_amd")],
            [InlineKeyboardButton(
                text=t("keyboard.strategy.order_block", language), callback_data="strategy_order_block",
            )],
        ]
    )


def settings_keyboard(language=None):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t("keyboard.settings.language", language), callback_data="settings_language")],
            [InlineKeyboardButton(text=t("keyboard.settings.risk", language), callback_data="settings_risk")],
            [InlineKeyboardButton(text=t("keyboard.settings.strategy", language), callback_data="settings_strategy")],
            [InlineKeyboardButton(
                text=t("keyboard.settings.timeframe", language), callback_data="settings_timeframe",
            )],
            [InlineKeyboardButton(
                text=t("keyboard.settings.notifications", language), callback_data="settings_notifications",
            )],
        ]
    )


def admin_panel_keyboard():
    """
    /admin hint keyboard (Phase 41). Same command-based interaction
    model as the Phase 40 settings keyboards -- no callback_query
    handler consumes these buttons; the real commands are /users,
    /stats, /system, /broadcast, /addadmin, /removeadmin.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Users", callback_data="admin_users")],
            [InlineKeyboardButton(text="Statistics", callback_data="admin_statistics")],
            [InlineKeyboardButton(text="System", callback_data="admin_system")],
            [InlineKeyboardButton(text="Broadcast", callback_data="admin_broadcast")],
            [InlineKeyboardButton(text="Admins", callback_data="admin_admins")],
        ]
    )


def notifications_keyboard(language=None):
    """
    /notifications hint keyboard (Phase 43). Same command-based
    interaction model as the other Phase 40/41 keyboards -- no
    callback_query handler consumes these buttons; the real commands
    are /notifications on and /notifications off. telegram/
    command_router.py is out of scope for this phase (not in its
    Files restriction list), so this keyboard is not wired into
    command_router._KEYBOARD_BY_COMMAND -- it exists as a display
    asset for a future phase to attach, same as admin_panel_keyboard()
    was for several phases before Phase 41 wired it in.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t("keyboard.notifications.enable", language), callback_data="notifications_on")],
            [InlineKeyboardButton(text=t("keyboard.notifications.disable", language), callback_data="notifications_off")],
        ]
    )


def phone_share_keyboard(language=None):
    """
    /start hint keyboard (Phase 61.5: AI Production Integration
    Foundation, TASK 4). The first `ReplyKeyboardMarkup` in this
    codebase -- every keyboard above is `InlineKeyboardMarkup`, which
    cannot request a user's contact; only a `ReplyKeyboardMarkup` with
    `KeyboardButton(request_contact=True)` can. Real interaction, not a
    display hint: tapping this button makes aiogram send a Message with
    `.contact` populated, which `telegram/polling.py`'s dispatcher
    routes to `telegram.command_router.route_contact()` ->
    `telegram.handlers.contact_handler()` ->
    `telegram.user_service.UserService.register_phone()`.
    `one_time_keyboard=True` -- the keyboard hides itself after one tap,
    same "don't linger" convention a Telegram contact-request button
    normally uses.
    """
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=t("keyboard.phone_share", language), request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


# V2 Phase 5 -- the persistent Reply Keyboard shown once a user's
# Registration Wizard reaches COMPLETE (telegram/command_router.py
# decides when to attach it -- never before COMPLETE, since it would
# otherwise replace phone_share_keyboard() above; see
# docs/PHASE5_AUDIT.md Section 2). Director decision: buttons send the
# literal "/command" text -- no separate display label, no new
# label->command mapping layer in command_router.py, so every button
# routes through the exact same telegram.command_router.route_command()
# dispatch a typed command already uses. This makes the keyboard
# language-invariant (there is no label to translate), the same
# posture Phase 1.5 Localized Keyboards already gives
# admin_panel_keyboard() below -- neither takes a `language` argument.
_USER_REPLY_COMMANDS = ("start", "profile", "signal", "subscription", "settings", "help")
_ADMIN_REPLY_COMMANDS = _USER_REPLY_COMMANDS + ("admin",)
_OWNER_REPLY_COMMANDS = _ADMIN_REPLY_COMMANDS + ("owner",)


def _reply_keyboard_rows(commands):
    buttons = [KeyboardButton(text=f"/{command}") for command in commands]
    return [buttons[i:i + 2] for i in range(0, len(buttons), 2)]


def reply_keyboard():
    """USER-tier persistent Reply Keyboard (V2 Phase 5): Home/Profile/Signals/Subscription/Settings/Help."""
    return ReplyKeyboardMarkup(keyboard=_reply_keyboard_rows(_USER_REPLY_COMMANDS), resize_keyboard=True)


def admin_reply_keyboard():
    """ADMIN-tier persistent Reply Keyboard (V2 Phase 5): USER's set plus /admin -- same superset policy as Phase 4's Persistent Menu."""
    return ReplyKeyboardMarkup(keyboard=_reply_keyboard_rows(_ADMIN_REPLY_COMMANDS), resize_keyboard=True)


def owner_reply_keyboard():
    """OWNER-tier persistent Reply Keyboard (V2 Phase 5): ADMIN's set plus /owner -- same superset policy as Phase 4's Persistent Menu."""
    return ReplyKeyboardMarkup(keyboard=_reply_keyboard_rows(_OWNER_REPLY_COMMANDS), resize_keyboard=True)
