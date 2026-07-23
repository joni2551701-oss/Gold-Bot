"""
Telegram Layer — Reply Keyboard Manager (V2 Phase 6.3, Director
Approved: "Dynamic Reply Keyboard Navigation").

Director's final decision: the Reply Keyboard is GoldBot's sole
navigation mechanism. Inline keyboards stay only where a real *choice*
is being made (Language Selection, Signal Confirmation, future Trade
Actions) -- never for moving between screens. This module owns every
piece of that navigation: which Reply Keyboard is attached to a given
command's reply, and the reverse mapping (a submenu button's tapped
label -> the "/command" it stands for).

This retires Phase 6.1's inline Navigation Controller entirely
(telegram/navigation.py, EDITABLE_COMMANDS, edit-in-place delivery,
nav_back/nav_home callbacks) -- Director's explicit "INLINE CLEANUP"
instruction. Messages are no longer edited in place; every reply is a
new message, and the Reply Keyboard shown alongside it is what "moves"
the user between screens, same as any ordinary Telegram bot.

Module Reuse Principle: the Main-tier Reply Keyboards
(reply_keyboard()/admin_reply_keyboard()/owner_reply_keyboard()) and
the tier-selection logic that used to live in
telegram.command_router._persistent_reply_keyboard() are not
duplicated here -- reply_keyboard()/admin_reply_keyboard()/
owner_reply_keyboard() are imported from telegram.keyboards as-is
(unchanged, already tested), and main_keyboard() below is that same
tier-selection logic, moved here since Director asked for "Main
keyboard" to be one of this module's named responsibilities.

Sections and the "keyboard switch": every command that owns one of the
five submenus (Settings/Admin/Owner/Profile/Signals) or Main itself
switches the chat's Reply Keyboard to that section's buttons --
keyboard_for_command() is the single switch every such command's reply
goes through (telegram/command_router.py's only caller). A command
outside any named section (e.g. /about, /status) defaults to Main,
keeping the keyboard state predictable rather than leaving a stale
submenu attached.

Per-chat "current section" tracking: process-local only (dict, never
written to the database), the same non-persisted-state precedent
Phase 6.1's Message Lifecycle Tracker already established. Its only
job is disambiguating the one label collision Director's own UX spec
creates: "📊 Statistics" appears verbatim under both Admin (-> /stats)
and Profile (-> /profile). Since Telegram only ever shows the buttons
of whichever Reply Keyboard was sent last, a chat can only be looking
at one of those two screens at a time -- resolve_navigation_command()
uses the tracked section to pick the right destination, and falls back
to a fixed default (/profile, the less-privileged of the two -- route_
command()'s own permission check is what actually protects /stats
either way) if the section was never recorded (e.g. after a process
restart).
"""

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from telegram.keyboards import admin_reply_keyboard, owner_reply_keyboard, reply_keyboard
from translation.ui_catalog import t

SECTION_MAIN = "main"
SECTION_SETTINGS = "settings"
SECTION_ADMIN = "admin"
SECTION_OWNER = "owner"
SECTION_PROFILE = "profile"
SECTION_SIGNALS = "signals"

_NAVIGATION_LANGUAGES = ("EN", "UZ", "RU")

# Which section's Reply Keyboard follows a given command's reply.
# Anything not listed here defaults to Main (see keyboard_for_command()).
_SECTION_BY_COMMAND = {
    "start": SECTION_MAIN,
    "settings": SECTION_SETTINGS,
    "language": SECTION_SETTINGS,
    "risk": SECTION_SETTINGS,
    "strategy": SECTION_SETTINGS,
    "timeframe": SECTION_SETTINGS,
    "notifications": SECTION_SETTINGS,
    "admin": SECTION_ADMIN,
    "users": SECTION_ADMIN,
    "stats": SECTION_ADMIN,
    "system": SECTION_ADMIN,
    "broadcast": SECTION_ADMIN,
    "addadmin": SECTION_ADMIN,
    "removeadmin": SECTION_ADMIN,
    "owner": SECTION_OWNER,
    "runtime": SECTION_OWNER,
    "health": SECTION_OWNER,
    "performance": SECTION_OWNER,
    "errors": SECTION_OWNER,
    "pipeline": SECTION_OWNER,
    "report": SECTION_OWNER,
    "profile": SECTION_PROFILE,
    "subscription": SECTION_PROFILE,
    "signal": SECTION_SIGNALS,
    "history": SECTION_SIGNALS,
    "upgrade": SECTION_SIGNALS,
}

# section -> (command -> translation key), the reverse of the labels
# each section's keyboard builder below renders. "◀️ Ortga" is handled
# separately (rkm.back, section-independent -- always /start).
_SECTION_LABEL_KEYS = {
    SECTION_SETTINGS: {
        "language": "rkm.settings.language",
        "risk": "rkm.settings.risk",
        "strategy": "rkm.settings.strategy",
        "timeframe": "rkm.settings.timeframe",
        "notifications": "rkm.settings.notifications",
    },
    SECTION_ADMIN: {
        "users": "rkm.admin.users",
        "stats": "rkm.admin.statistics",
        "system": "rkm.admin.system",
        "broadcast": "rkm.admin.broadcast",
        "addadmin": "rkm.admin.admins",
    },
    SECTION_OWNER: {
        "runtime": "rkm.owner.runtime",
        "health": "rkm.owner.health",
        "performance": "rkm.owner.performance",
        "errors": "rkm.owner.errors",
        "pipeline": "rkm.owner.pipeline",
        "report": "rkm.owner.reports",
    },
    SECTION_PROFILE: {
        "profile": "rkm.profile.profile",
        "subscription": "menu.subscription",
        # "profile" is used twice deliberately: the Profile submenu's
        # own "📄 Profile" button and its "📊 Statistics" button both
        # reuse profile_handler() (Director UX spec; no separate
        # per-user statistics command exists to reuse instead -- see
        # this module's docstring / Phase 6.3 audit notes).
    },
    SECTION_SIGNALS: {
        "signal": "rkm.signals.live",
        "history": "rkm.signals.history",
        "upgrade": "rkm.signals.premium",
    },
}

# The one label Director's spec repeats verbatim across two sections.
# Resolved by tracked section, not by a flat global map (see module
# docstring).
_STATISTICS_LABEL_KEY = "rkm.admin.statistics"  # same text as rkm.profile.statistics
_STATISTICS_COMMAND_BY_SECTION = {
    SECTION_ADMIN: "stats",
    SECTION_PROFILE: "profile",
}
_STATISTICS_DEFAULT_COMMAND = "profile"


def _label_map_for_section(section):
    """
    Every localized label (any supported language) -> its "/command"
    string, for one section. Mirrors telegram.keyboards.
    _build_navigation_map()'s own shape.
    """
    mapping = {}
    for command, key in _SECTION_LABEL_KEYS[section].items():
        for language in _NAVIGATION_LANGUAGES:
            mapping[t(key, language)] = f"/{command}"
    return mapping


_SECTION_MAPS = {section: _label_map_for_section(section) for section in _SECTION_LABEL_KEYS}

_BACK_LABELS = frozenset(t("rkm.back", language) for language in _NAVIGATION_LANGUAGES)
_STATISTICS_LABELS = frozenset(t(_STATISTICS_LABEL_KEY, language) for language in _NAVIGATION_LANGUAGES)


def main_keyboard(telegram_id, level=None):
    """
    The tier-aware persistent Main Reply Keyboard (moved here from
    telegram.command_router._persistent_reply_keyboard(), V2 Phase 5 --
    Director asked for "Main keyboard" to be one of this module's own
    responsibilities). USER/ADMIN/OWNER each get their own superset,
    unchanged from Phase 5's own policy -- only the call site moved.

    `level`, when given, is used as-is instead of looking it up again
    -- telegram.command_router._start_keyboard() already computes it
    once (via its own get_permission_level import) to decide whether
    to call this function at all, so passing it through here avoids a
    second, separately-imported lookup that a caller's monkeypatch on
    command_router's own binding would not reach.
    """
    from telegram import handlers
    from telegram.permissions import PermissionLevel, get_permission_level

    language = handlers._current_language(telegram_id)
    if level is None:
        level = get_permission_level(telegram_id)
    if level == PermissionLevel.OWNER:
        return owner_reply_keyboard(language)
    if level == PermissionLevel.ADMIN:
        return admin_reply_keyboard(language)
    return reply_keyboard(language)


def _submenu_rows(section, language, label_language=None):
    """
    `label_language`, when given, overrides the language used for the
    section's own action buttons while "◀️ Ortga" still uses `language`
    (the caller's real language) -- used by the Admin/Owner submenus
    below, which stay English-only for their action labels (Phase 1.5
    Localized Keyboards precedent: "OWNER/ADMIN UI is Director
    decision, out of scope for USER-facing localization", same as the
    retired admin_panel_keyboard() this replaces), while Back still
    localizes normally, matching Phase 6.1's own precedent of
    localizing Back/Home even on admin-adjacent pages.
    """
    label_language = language if label_language is None else label_language
    buttons = [
        KeyboardButton(text=t(key, label_language)) for key in _SECTION_LABEL_KEYS[section].values()
    ]
    rows = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]
    rows.append([KeyboardButton(text=t("rkm.back", language))])
    return rows


def settings_keyboard(language=None):
    """Settings submenu Reply Keyboard: Til/Risk/Strategiya/Vaqt oralig'i/Bildirishnomalar + Ortga."""
    return ReplyKeyboardMarkup(keyboard=_submenu_rows(SECTION_SETTINGS, language), resize_keyboard=True)


def admin_submenu_keyboard(language=None):
    """Admin submenu Reply Keyboard: Users/Statistics/System/Broadcast/Admins (English-only) + Ortga (localized)."""
    return ReplyKeyboardMarkup(
        keyboard=_submenu_rows(SECTION_ADMIN, language, label_language="EN"), resize_keyboard=True,
    )


def owner_submenu_keyboard(language=None):
    """Owner submenu Reply Keyboard: Runtime/Health/Performance/Errors/Pipeline/Reports (English-only) + Ortga (localized)."""
    return ReplyKeyboardMarkup(
        keyboard=_submenu_rows(SECTION_OWNER, language, label_language="EN"), resize_keyboard=True,
    )


def profile_keyboard(language=None):
    """Profile submenu Reply Keyboard: Profile/Subscription/Statistics + Ortga."""
    rows = [
        [KeyboardButton(text=t("rkm.profile.profile", language))],
        [KeyboardButton(text=t("menu.subscription", language))],
        [KeyboardButton(text=t("rkm.profile.statistics", language))],
        [KeyboardButton(text=t("rkm.back", language))],
    ]
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def signals_keyboard(language=None):
    """Signals submenu Reply Keyboard: Live Signals/History/Premium + Ortga."""
    return ReplyKeyboardMarkup(keyboard=_submenu_rows(SECTION_SIGNALS, language), resize_keyboard=True)


_KEYBOARD_BUILDER_BY_SECTION = {
    SECTION_SETTINGS: settings_keyboard,
    SECTION_ADMIN: admin_submenu_keyboard,
    SECTION_OWNER: owner_submenu_keyboard,
    SECTION_PROFILE: profile_keyboard,
    SECTION_SIGNALS: signals_keyboard,
}


# ---------------------------------------------------------------------------
# Per-chat "current section" tracker -- process-local only (never
# persisted to the database, matching Phase 6.1's Message Lifecycle
# Tracker precedent). See module docstring for why this exists.
# ---------------------------------------------------------------------------

_LAST_SECTION: dict = {}


def record_section(telegram_id, section) -> None:
    _LAST_SECTION[str(telegram_id)] = section


def current_section(telegram_id):
    return _LAST_SECTION.get(str(telegram_id))


def keyboard_for_command(command, telegram_id):
    """
    The "keyboard switch" (Director's own naming): given the command
    that was just executed, returns the Reply Keyboard that should
    accompany its reply, and records the resulting section so a later
    ambiguous label (see _STATISTICS_LABELS) can be resolved correctly.
    """
    section = _SECTION_BY_COMMAND.get(command, SECTION_MAIN)
    record_section(telegram_id, section)

    if section == SECTION_MAIN:
        return main_keyboard(telegram_id)

    from telegram import handlers
    language = handlers._current_language(telegram_id)
    return _KEYBOARD_BUILDER_BY_SECTION[section](language)


def resolve_navigation_command(text, telegram_id=None):
    """
    Looks up a submenu Reply Keyboard tap's text and returns the
    "/command" it stands for, or None if text isn't a recognized
    submenu label (Main-tier labels are telegram.keyboards.
    resolve_navigation_command()'s own job -- callers try that one
    first). Never raises.

    "◀️ Ortga" always resolves to "/start" regardless of section
    (Director: "Alohida Home tugmasi kerak emas. Ortga -> Main
    Keyboard"). "📊 Statistics" is the one genuine collision (see
    module docstring) -- resolved via the caller's tracked section,
    falling back to _STATISTICS_DEFAULT_COMMAND if untracked.
    """
    if not text:
        return None
    text = text.strip()

    if text in _BACK_LABELS:
        return "/start"

    if text in _STATISTICS_LABELS:
        section = current_section(telegram_id) if telegram_id is not None else None
        command = _STATISTICS_COMMAND_BY_SECTION.get(section, _STATISTICS_DEFAULT_COMMAND)
        return f"/{command}"

    section = current_section(telegram_id) if telegram_id is not None else None
    if section in _SECTION_MAPS:
        command = _SECTION_MAPS[section].get(text)
        if command is not None:
            return command

    # Fallback for a stale/missing tracked section (e.g. a process
    # restart) -- check every section's map, first hit wins. Harmless
    # even if it picks the "wrong" section for an ambiguous label,
    # since route_command()'s own permission check is authoritative
    # regardless of which command this resolves to.
    for section_map in _SECTION_MAPS.values():
        command = section_map.get(text)
        if command is not None:
            return command

    return None
