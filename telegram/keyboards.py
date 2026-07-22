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
# docs/PHASE5_AUDIT.md Section 2).
#
# V2 Phase 5.1 (Director Approved) -- UX Polish & Command Abstraction:
# reverses Phase 5's "literal /command text" decision. A user must
# never see "/profile"/"/signal"/etc. on the Reply Keyboard; buttons
# now show the same localized labels telegram.menu_commands' Persistent
# Menu (Phase 4) already uses (translation.ui_catalog's "menu.*" keys
# -- reused here rather than duplicated, per the Module Reuse
# Principle). A tap sends that localized label as plain text, which
# telegram.command_router.route_command() resolves back to its
# "/command" via NAVIGATION_MAP/resolve_navigation_command() below
# *before* parsing -- no handler rewrite, no second execution path:
# command_router remains the single authoritative dispatcher every
# typed "/command" already goes through.
_USER_REPLY_COMMANDS = ("start", "profile", "signal", "subscription", "settings", "help")
_ADMIN_REPLY_COMMANDS = _USER_REPLY_COMMANDS + ("admin",)
_OWNER_REPLY_COMMANDS = _ADMIN_REPLY_COMMANDS + ("owner",)

# command -> translation.ui_catalog key. The USER-tier six reuse Phase
# 4's own "menu.*" keys verbatim (identical labels, Director decision);
# "menu.admin"/"menu.owner" are Phase 5.1's own additions, language-
# invariant like menu_commands.py's _ADMIN_EXTRA/_OWNER_EXTRA.
_REPLY_LABEL_KEYS = {
    "start": "menu.home",
    "profile": "menu.profile",
    "signal": "menu.signals",
    "subscription": "menu.subscription",
    "settings": "menu.settings",
    "help": "menu.help",
    "admin": "menu.admin",
    "owner": "menu.owner",
}

_NAVIGATION_LANGUAGES = ("EN", "UZ", "RU")


def _build_navigation_map():
    """Every localized label (any supported language) -> its "/command" string."""
    mapping = {}
    for command, key in _REPLY_LABEL_KEYS.items():
        for language in _NAVIGATION_LANGUAGES:
            mapping[t(key, language)] = f"/{command}"
    return mapping


NAVIGATION_MAP = _build_navigation_map()


def resolve_navigation_command(text):
    """
    Looks up a Reply Keyboard tap's text against NAVIGATION_MAP and
    returns the "/command" it stands for, or None if text isn't a
    known navigation label (e.g. an ordinary typed message, or a
    literal "/command" already -- those are not navigation labels and
    are left to _parse_command() as before). Never raises.
    """
    if not text:
        return None
    return NAVIGATION_MAP.get(text.strip())


def _reply_keyboard_rows(commands, language):
    buttons = [KeyboardButton(text=t(_REPLY_LABEL_KEYS[command], language)) for command in commands]
    return [buttons[i:i + 2] for i in range(0, len(buttons), 2)]


def reply_keyboard(language=None):
    """USER-tier persistent Reply Keyboard (V2 Phase 5.1): localized Home/Profile/Signals/Subscription/Settings/Help labels."""
    return ReplyKeyboardMarkup(keyboard=_reply_keyboard_rows(_USER_REPLY_COMMANDS, language), resize_keyboard=True)


def admin_reply_keyboard(language=None):
    """ADMIN-tier persistent Reply Keyboard (V2 Phase 5.1): USER's set plus Admin -- same superset policy as Phase 4's Persistent Menu."""
    return ReplyKeyboardMarkup(keyboard=_reply_keyboard_rows(_ADMIN_REPLY_COMMANDS, language), resize_keyboard=True)


def owner_reply_keyboard(language=None):
    """OWNER-tier persistent Reply Keyboard (V2 Phase 5.1): ADMIN's set plus Owner -- same superset policy as Phase 4's Persistent Menu."""
    return ReplyKeyboardMarkup(keyboard=_reply_keyboard_rows(_OWNER_REPLY_COMMANDS, language), resize_keyboard=True)
