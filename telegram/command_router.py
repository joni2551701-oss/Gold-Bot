"""
Telegram Layer — command router foundation (Phase 34; permission
gating added Phase 37).

Routes an incoming Telegram command to its handler function in
telegram.handlers. Command names come from telegram.commands.COMMANDS
/ OWNER_COMMANDS / ADMIN_COMMANDS -- the single source of truth -- so
there is no second hardcoded command list here: the handler for
"start" is looked up dynamically as telegram.handlers.start_handler,
and so on for every key across those three registries. The required
permission tier for a command is likewise derived from registry
membership, not a separate hardcoded list.

    Telegram Update -> Command Router -> permissions.py (role check)
        -> Handler -> Service -> Database

No aiogram Dispatcher/polling wiring here -- that lives in
telegram/polling.py. This module turns (command text, Telegram user
info) into a response, so it can be called from any update-receiving
entry point (polling loop, webhook handler, or a Dispatcher
registration).

Never raises: a broken handler, an unexpected error, or a permission
failure all become a safe text response here, so an exception never
reaches the Telegram event loop (Phase 34, Part 10).
"""

import inspect
from dataclasses import dataclass
from typing import Optional, Tuple

from aiogram.types import ReplyKeyboardRemove

from telegram import handlers
from telegram.commands import COMMANDS, OWNER_COMMANDS, ADMIN_COMMANDS
from telegram.keyboards import (
    language_keyboard,
    risk_keyboard,
    timeframe_keyboard,
    strategy_keyboard,
    notifications_keyboard,
    phone_share_keyboard,
    resolve_navigation_command,
)
from telegram import reply_keyboard_manager
from telegram.permissions import PermissionLevel, get_permission_level
from telegram.registration_service import RegistrationStep
from translation.ui_catalog import t
from core.logger import setup_logger

logger = setup_logger("CommandRouter")

UNKNOWN_COMMAND_TEXT = "Unknown command. Use /help to see available commands."
SERVICE_UNAVAILABLE_TEXT = "Service temporarily unavailable."
PERMISSION_DENIED_TEXT = "Permission denied."

# Union of all three registries: the single source of truth for "does
# this command exist at all" (regardless of who is allowed to use it).
_ALL_COMMANDS = {**COMMANDS, **OWNER_COMMANDS, **ADMIN_COMMANDS}

# Which commands get an inline VALUE-PICKER keyboard attached to their
# reply (Phase 40; scope narrowed by V2 Phase 6.3; notifications wired
# in by V2 Phase 6.2 -- see module note below). Not command-specific
# business logic -- just display. Only real-choice screens stay here:
# picking a language/risk percent/strategy/timeframe/notification
# preference is a genuine selection (Director's own inline allow-list),
# never a between-screen navigation, so these keyboards are untouched
# by Phase 6.3's Reply-Keyboard-is-navigation policy. "start"/
# "settings"/"admin" are NOT here -- their replies now go through
# telegram.reply_keyboard_manager.keyboard_for_command() instead (V2
# Phase 6.3), since Settings/Admin/Owner/Profile/Signals are Reply
# Keyboard sections, not inline hints, as of this phase.
#
# V2 Phase 6.2 (Settings Callback Completion): each builder is paired
# with an optional "current value" accessor (telegram.handlers'
# _current_risk()/_current_strategy_slug()/_current_timeframe()/
# _current_notifications_choice()) so the picker opens already showing
# a ●/○ radio marker on the caller's actual stored value (Stage 5/6:
# "Current Value" + "Inline UX"), not a bare unmarked list. language
# has no such accessor -- language selection has no "current value you
# are adjusting" radio concept in Director's spec, unchanged from
# Phase 40.
_KEYBOARD_BY_COMMAND = {
    "language": (language_keyboard, None),
    "risk": (risk_keyboard, handlers._current_risk),
    "strategy": (strategy_keyboard, handlers._current_strategy_slug),
    "timeframe": (timeframe_keyboard, handlers._current_timeframe),
    "notifications": (notifications_keyboard, handlers._current_notifications_choice),
}

# V2 Phase 3: which keyboard builder to attach to /start's reply for
# each Wizard step. RegistrationStep.COMPLETE has no entry here --
# _start_keyboard() handles that case separately (V2 Phase 5: the
# persistent Reply Keyboard, tier-aware; V2 Phase 6.3: that keyboard
# now lives in telegram.reply_keyboard_manager.main_keyboard()).
_START_KEYBOARD_BY_STEP = {
    RegistrationStep.LANGUAGE: language_keyboard,
    RegistrationStep.PHONE: phone_share_keyboard,
}


def _start_keyboard(telegram_id, language):
    """
    V2 Phase 3/5: /start's reply keyboard follows wherever the
    Registration Wizard left off -- language_keyboard while
    registration_step is LANGUAGE, phone_share_keyboard while PHONE,
    the persistent Main Reply Keyboard once COMPLETE (V2 Phase 5; V2
    Phase 6.3: telegram.reply_keyboard_manager.main_keyboard()).
    ReplyKeyboardRemove() for a BANNED user -- checked first and
    independently of registration_step, since
    handlers._registration_step() already collapses BANNED and
    COMPLETE to the same None and cannot distinguish them on its own.

    V2 Phase 6.1.1 (Director-reported bug, root-caused): OWNER/ADMIN
    always get the tier-aware persistent Reply Keyboard, regardless of
    registration_step. database/models.py's _backfill_registration_state()
    (V2 Phase 3) permanently set registration_step='PHONE' for any
    pre-existing row with no phone_hash -- which includes operator
    accounts (e.g. the account matching TELEGRAM_OWNER_ID) that were
    created before the mandatory Phone Share Wizard existed and were
    never going to complete it. Without this check, such an account's
    /start reply keeps re-attaching phone_share_keyboard() forever,
    which is what actually produced the reported "Phone Share button
    never goes away" / "Owner buttons missing from the Reply Keyboard"
    symptoms -- the ReplyKeyboardRemove()->Persistent Reply Keyboard
    sequence in route_contact() was already correct and is untouched
    by this fix. is_owner()/is_admin() (telegram/permissions.py) are
    already the stronger identity check (TELEGRAM_OWNER_ID env var /
    admins table), so gating an operator's own UI behind the same
    anti-abuse Phone Share requirement (V2 Phase 3/61.4) meant for
    anonymous free-tier signups was never the intent. Command routing
    itself was never affected -- permission checks in route_command()
    already only consult get_permission_level(), never registration_step.
    """
    if handlers._is_banned(telegram_id):
        return ReplyKeyboardRemove()

    level = get_permission_level(telegram_id)
    if level in (PermissionLevel.OWNER, PermissionLevel.ADMIN):
        return reply_keyboard_manager.main_keyboard(telegram_id, level=level)

    step = handlers._registration_step(telegram_id)
    builder = _START_KEYBOARD_BY_STEP.get(step)
    if builder is not None:
        return builder(language)
    return reply_keyboard_manager.main_keyboard(telegram_id, level=level)


_LEVEL_RANK = {
    PermissionLevel.USER: 0,
    PermissionLevel.ADMIN: 1,
    PermissionLevel.OWNER: 2,
}


@dataclass(frozen=True)
class RouterResult:
    text: str
    keyboard: Optional[object] = None
    # V2 Phase 6.1 (Director Decision 7) -- an optional second message
    # to send right after this one (e.g. the persistent Reply Keyboard
    # attached after an explicit ReplyKeyboardRemove()). RouterResult
    # carries exactly one keyboard field, so a "remove then reattach"
    # sequence needs a second RouterResult to send as a follow-up.
    # V2 Phase 6.3 retired the sibling `editable` field this dataclass
    # used to carry (Phase 6.1's edit-in-place delivery mechanism) --
    # every reply is now a new message; see telegram/polling.py's
    # _deliver() and telegram.reply_keyboard_manager's module docstring.
    followup: Optional["RouterResult"] = None


def _parse_command(text: str) -> Tuple[Optional[str], str]:
    """'/addadmin@GoldBotBot 123456789' -> ('addadmin', '123456789')."""
    if not text or not text.startswith("/"):
        return None, ""
    parts = text.strip().split(maxsplit=1)
    command = parts[0][1:].split("@")[0].lower()
    args = parts[1].strip() if len(parts) > 1 else ""
    return (command or None), args


def _required_level(command: str) -> PermissionLevel:
    """
    Derives the minimum tier a command needs from which registry it's
    in -- OWNER_COMMANDS-only commands need OWNER; anything listed in
    ADMIN_COMMANDS needs at least ADMIN (OWNER inherits ADMIN access
    via the rank check below, so a command in both registries, e.g.
    /broadcast, correctly resolves to ADMIN-or-above).
    """
    if command in ADMIN_COMMANDS:
        return PermissionLevel.ADMIN
    if command in OWNER_COMMANDS:
        return PermissionLevel.OWNER
    return PermissionLevel.USER


def _level_satisfies(user_level: PermissionLevel, required_level: PermissionLevel) -> bool:
    return _LEVEL_RANK[user_level] >= _LEVEL_RANK[required_level]


async def _call_handler(handler, telegram_id, username, args) -> str:
    """Calls handler with only the keyword arguments its signature accepts."""
    params = inspect.signature(handler).parameters
    kwargs = {}
    if "telegram_id" in params:
        kwargs["telegram_id"] = telegram_id
    if "username" in params:
        kwargs["username"] = username
    if "args" in params:
        kwargs["args"] = args
    return await handler(**kwargs)


async def route_command(command_text: str, telegram_id=None, username=None) -> RouterResult:
    """
    Routes a raw command string (e.g. "/start" or "/addadmin 123") to
    its handler. Unknown commands, permission failures, and handler
    failures all return a safe text response instead of raising.

    V2 Phase 5.1: command_text may also be a Reply Keyboard's localized
    label (e.g. "👤 Profil") rather than a literal "/command" -- Navigation
    Mapping (telegram.keyboards.resolve_navigation_command()) translates
    it back to its "/command" here, before parsing, so this remains the
    single dispatch path every typed command already goes through (no
    second handler-lookup path, no business-logic duplication).

    V2 Phase 6.3: a submenu Reply Keyboard's own label (e.g. "💰 Risk"
    from the Settings section, or "◀️ Ortga" from any section) is tried
    next if the Main-tier map above doesn't recognize it --
    telegram.reply_keyboard_manager.resolve_navigation_command() owns
    that second map, using the caller's tracked current section to
    resolve it.
    """
    resolved_command_text = resolve_navigation_command(command_text)
    if resolved_command_text is None:
        resolved_command_text = reply_keyboard_manager.resolve_navigation_command(command_text, telegram_id)
    if resolved_command_text is not None:
        command_text = resolved_command_text

    command, args = _parse_command(command_text)
    if command is None or command not in _ALL_COMMANDS:
        return RouterResult(text=UNKNOWN_COMMAND_TEXT)

    required_level = _required_level(command)
    user_level = get_permission_level(telegram_id)
    if not _level_satisfies(user_level, required_level):
        logger.info(
            f"Permission denied: telegram_id={telegram_id} ({user_level.value}) "
            f"attempted /{command} (requires {required_level.value})."
        )
        return RouterResult(text=PERMISSION_DENIED_TEXT)

    handler = getattr(handlers, f"{command}_handler", None)
    if handler is None:
        return RouterResult(text=UNKNOWN_COMMAND_TEXT)

    try:
        text = await _call_handler(handler, telegram_id, username, args)
    except Exception as e:
        logger.warning(f"Handler for /{command} failed: {e}")
        return RouterResult(text=SERVICE_UNAVAILABLE_TEXT)

    if command == "start":
        # V2 Phase 3: depends on the caller's Registration Wizard step,
        # not a fixed per-command builder -- see _start_keyboard().
        keyboard = _start_keyboard(telegram_id, handlers._current_language(telegram_id))
        reply_keyboard_manager.record_section(telegram_id, reply_keyboard_manager.SECTION_MAIN)
    else:
        keyboard_entry = _KEYBOARD_BY_COMMAND.get(command)
        if keyboard_entry is not None:
            # Inline value-picker (Language/Risk/Strategy/Timeframe/
            # Notifications) -- a real choice, Director's own inline
            # allow-list; never a navigation switch, so the Reply
            # Keyboard section tracker is deliberately left untouched
            # here (whatever section the caller was already in stays
            # current).
            builder, current_value_accessor = keyboard_entry
            selected = current_value_accessor(telegram_id) if current_value_accessor is not None else None
            keyboard = builder(handlers._current_language(telegram_id), selected=selected)
        else:
            # V2 Phase 6.3 (Director Approved: Dynamic Reply Keyboard
            # Navigation) -- every other command's reply carries the
            # Reply Keyboard for the section it belongs to (Main/
            # Settings/Admin/Owner/Profile/Signals), switching the
            # chat's persistent keyboard exactly like a native Telegram
            # app screen transition. Retires Phase 6.1's inline Back/
            # Home row entirely (see telegram.reply_keyboard_manager's
            # module docstring).
            keyboard = reply_keyboard_manager.keyboard_for_command(command, telegram_id)

    return RouterResult(text=text, keyboard=keyboard)


async def route_message(message) -> RouterResult:
    """
    Routes an aiogram Message-like object. Extracts telegram_id/username
    the same way a future Dispatcher handler would:

        telegram_id = message.from_user.id
        username = message.from_user.username
    """
    telegram_id = message.from_user.id
    username = message.from_user.username
    return await route_command(message.text, telegram_id=telegram_id, username=username)


async def route_contact(message) -> RouterResult:
    """
    Routes an aiogram Message-like object whose `.contact` is populated
    (Phase 61.5 TASK 4) -- the Phone Share Button's reply, a
    structurally different message shape than a text command
    (`message.text` is `None` here). Mirrors `route_message()`'s own
    shape: resolve identity, delegate to a handler, never raise.

    Never raises: a handler failure becomes SERVICE_UNAVAILABLE_TEXT,
    same posture as `route_command()`. No permission tier is checked --
    sharing your own contact is a USER-level action, available to
    anyone `/start` already let in.

    V2 Phase 3: rejects a contact whose `contact.user_id` doesn't match
    the sender's own id -- tapping the Phone Share button always
    populates `contact.user_id` with the sender's own id, so a mismatch
    only happens when someone forwards a contact card for a different
    person. contact_handler()/register_phone() is never called in that
    case, so a stranger's phone number is never attached to the wrong
    account.
    """
    telegram_id = message.from_user.id
    contact_owner_id = message.contact.user_id
    phone_number = message.contact.phone_number

    if contact_owner_id is None or contact_owner_id != telegram_id:
        language = handlers._current_language(telegram_id)
        return RouterResult(text=t("contact.wrong_owner", language))

    try:
        text = await handlers.contact_handler(telegram_id=telegram_id, phone_number=phone_number)
    except Exception as e:
        logger.warning(f"contact_handler failed for telegram_id={telegram_id}: {e}")
        return RouterResult(text=SERVICE_UNAVAILABLE_TEXT)

    # V2 Phase 5: a successful phone share is also the Wizard's
    # completion trigger (contact_handler() already called
    # RegistrationService.complete() internally). No-op (keyboard
    # stays None, no followup) if registration did not actually
    # complete this call (e.g. the phone number was already registered
    # elsewhere).
    #
    # V2 Phase 6.1 (Director Decision 7) reverses Phase 5's direct
    # attachment: the persistent Reply Keyboard no longer replaces
    # phone_share_keyboard() on the same reply. Instead this reply
    # carries an explicit ReplyKeyboardRemove(), and the persistent
    # keyboard is attached to a follow-up message -- RouterResult has
    # exactly one keyboard field, so satisfying "Phone Share ->
    # ReplyKeyboardRemove() -> Persistent Reply Keyboard" literally
    # requires two sequential messages (see
    # docs/PHASE6_NAVIGATION_AUDIT.md, Director Decision 7). Telegram
    # itself never required the explicit removal step (Phase 5's own
    # docs/PHASE5_AUDIT.md Section 3 finding still holds technically),
    # but the Director's decision is followed as given.
    if not handlers._is_registration_complete(telegram_id):
        return RouterResult(text=text, keyboard=None)

    language = handlers._current_language(telegram_id)
    reply_keyboard_manager.record_section(telegram_id, reply_keyboard_manager.SECTION_MAIN)
    return RouterResult(
        text=text,
        keyboard=ReplyKeyboardRemove(),
        followup=RouterResult(
            text=t("navigation.menu_ready", language), keyboard=reply_keyboard_manager.main_keyboard(telegram_id),
        ),
    )
