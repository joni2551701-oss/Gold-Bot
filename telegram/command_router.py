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

from telegram import handlers
from telegram.commands import COMMANDS, OWNER_COMMANDS, ADMIN_COMMANDS
from telegram.keyboards import (
    language_keyboard,
    risk_keyboard,
    timeframe_keyboard,
    strategy_keyboard,
    settings_keyboard,
    admin_panel_keyboard,
    phone_share_keyboard,
)
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

# Which commands get a hint keyboard attached to their reply, and which
# builder produces it (Phase 40). Not command-specific business logic --
# just display; the keyboard's buttons are not wired to a callback_query
# handler, so telegram.handlers documents the real interaction as a
# command argument (e.g. "/risk 5"). "start" and "admin" are handled by
# their own special cases below instead of this table -- "start"'s
# keyboard depends on the caller's Registration Wizard step (V2 Phase
# 3), not a fixed per-command builder.
_KEYBOARD_BY_COMMAND = {
    "settings": settings_keyboard,
    "language": language_keyboard,
    "risk": risk_keyboard,
    "strategy": strategy_keyboard,
    "timeframe": timeframe_keyboard,
    "admin": admin_panel_keyboard,
}

# V2 Phase 3: which keyboard builder to attach to /start's reply for
# each Wizard step. RegistrationStep.COMPLETE (and a BANNED user, or
# any other unrecognized/None step) intentionally has no entry here --
# _start_keyboard() falls back to None, meaning /start carries no
# keyboard once the Wizard is done or was never applicable.
_START_KEYBOARD_BY_STEP = {
    RegistrationStep.LANGUAGE: language_keyboard,
    RegistrationStep.PHONE: phone_share_keyboard,
}


def _start_keyboard(telegram_id, language):
    """
    V2 Phase 3: /start's reply keyboard follows wherever the
    Registration Wizard left off -- language_keyboard while
    registration_step is LANGUAGE, phone_share_keyboard while PHONE,
    no keyboard once COMPLETE. handlers._registration_step() already
    returns None for a BANNED user, so this naturally attaches no
    Wizard keyboard to a banned /start reply either.
    """
    step = handlers._registration_step(telegram_id)
    builder = _START_KEYBOARD_BY_STEP.get(step)
    return builder(language) if builder else None


_LEVEL_RANK = {
    PermissionLevel.USER: 0,
    PermissionLevel.ADMIN: 1,
    PermissionLevel.OWNER: 2,
}


@dataclass(frozen=True)
class RouterResult:
    text: str
    keyboard: Optional[object] = None


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
    """
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
    else:
        keyboard_builder = _KEYBOARD_BY_COMMAND.get(command)
        if keyboard_builder is None:
            keyboard = None
        elif command == "admin":
            # OWNER/ADMIN keyboard -- stays English-only (Director
            # decision, Phase 1.5 Localized Keyboards), no language passed.
            keyboard = keyboard_builder()
        else:
            keyboard = keyboard_builder(handlers._current_language(telegram_id))
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

    return RouterResult(text=text)
