"""
Telegram Layer — Persistent Menu (V2 Phase 4, Stage 1).

Registers Telegram's native Menu Button command list via
Bot.set_my_commands() -- no new dispatch path: every menu entry maps
to a command already in telegram.commands' registries, routed through
the existing telegram.command_router.route_command() exactly as if
typed by hand. This module owns registration only; it never talks to
handlers/services beyond the read-only lookups needed to know who is
an ADMIN/OWNER and what language they've chosen
(database.admin_repository.AdminRepository,
database.user_repository.UserRepository) -- the same kind of direct
repository read every other telegram/*_service.py module already
performs, not new business logic.

Three menu tiers, each a fixed, small superset of the one below it
(Director decision, V2 Phase 4):
    USER:  Home, Profile, Signals, Subscription, Settings, Help
    ADMIN: USER + Admin
    OWNER: ADMIN + Owner

Scope strategy (Director decision: BotCommandScopeDefault,
BotCommandScopeChatAdministrators, BotCommandScopeChat -- only the
first and third are actually used here; see the note below):

    BotCommandScopeDefault (language_code="uz"/"ru"/"en", plus a
        language_code-less catch-all in UZ, the schema's own default
        language) -- the USER menu, for anyone Telegram hasn't been
        told otherwise about. This is the only thing every
        not-yet-registered user ever sees.

    BotCommandScopeChat(chat_id=<telegram_id>) -- set once per known
        ADMIN and once for the configured OWNER, in their own stored
        UserRecord.language, overriding the default with the ADMIN or
        OWNER menu for that one chat specifically. In a private (DM)
        chat, chat_id == the user's own telegram_id.

    BotCommandScopeChatAdministrators is deliberately NOT used: it
    targets Telegram's own "administrators of a group/supergroup
    chat" concept -- GoldBot is a private, DM-only bot with no group
    chat_id anywhere in this schema to scope it to. BotCommandScopeChat
    per known ADMIN/OWNER achieves the identical practical outcome the
    Director's brief asks for ("a specific user's command list differs
    from everyone else's") for a private chat.

Registration happens once, at bot startup (telegram/polling.py's
run_polling(), the same one-shot, best-effort, never-blocks-polling
slot _notify_owner_startup()/_log_startup_secret_presence() already
occupy) -- not on every language change or admin promotion. Reacting
to those live would require hooking into telegram/command_router.py,
telegram/handlers.py, or telegram/callback_router.py's language-change
and admin-management call paths, which V2 Phase 4's own rules forbid
touching. A per-user command menu therefore reflects that user's
ADMIN/OWNER status and chosen language as of the last bot restart --
Telegram itself caches a chat's command list client-side regardless,
so this is a startup-time registration step, not a live sync.

Never raises: a failure anywhere in here is logged and does not stop
telegram/polling.py's run_polling() from starting (same posture as
every other startup step in that module).
"""

from typing import List

from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeDefault

from database.admin_repository import AdminRepository
from database.user_repository import UserRepository
from translation.ui_catalog import t
from core.secrets import Secrets
from core.logger import setup_logger

logger = setup_logger("MenuCommands")

_LANGUAGE_CODES = {"UZ": "uz", "RU": "ru", "EN": "en"}
_DEFAULT_MENU_LANGUAGE = "UZ"  # matches database.models' own users.language schema default

# Director decision (V2 Phase 4): fixed 6-entry USER menu -- command
# name from telegram.commands.COMMANDS (the single source of truth),
# label from translation.ui_catalog (Phase 1 Language Foundation).
_USER_MENU = (
    ("start", "menu.home"),
    ("profile", "menu.profile"),
    ("signal", "menu.signals"),
    ("subscription", "menu.subscription"),
    ("settings", "menu.settings"),
    ("help", "menu.help"),
)

# ADMIN/OWNER menu labels stay language-invariant -- see module
# docstring precedent (telegram.keyboards.admin_panel_keyboard()).
_ADMIN_EXTRA = ("admin", "🛠 Admin")
_OWNER_EXTRA = ("owner", "👑 Owner")


def _user_menu(language: str) -> List[BotCommand]:
    return [BotCommand(command=command, description=t(key, language)) for command, key in _USER_MENU]


def _admin_menu(language: str) -> List[BotCommand]:
    command, description = _ADMIN_EXTRA
    return _user_menu(language) + [BotCommand(command=command, description=description)]


def _owner_menu(language: str) -> List[BotCommand]:
    command, description = _OWNER_EXTRA
    return _admin_menu(language) + [BotCommand(command=command, description=description)]


def _owner_telegram_id() -> str:
    try:
        return Secrets().TELEGRAM_OWNER_ID
    except Exception:
        return ""


def _admin_telegram_ids() -> List[str]:
    try:
        return [record.telegram_id for record in AdminRepository().get_all_admins()]
    except Exception as e:
        logger.warning(f"Failed to list admins for menu registration: {e}")
        return []


def _language_for(telegram_id: str) -> str:
    try:
        user = UserRepository().get_user(telegram_id)
    except Exception as e:
        logger.warning(f"Failed to resolve language for telegram_id={telegram_id}: {e}")
        return _DEFAULT_MENU_LANGUAGE
    if user is None or not user.language:
        return _DEFAULT_MENU_LANGUAGE
    return user.language


async def _register_default_menus(bot: Bot) -> None:
    """USER menu -- global default, plus one explicit variant per supported language_code."""
    await bot.set_my_commands(_user_menu(_DEFAULT_MENU_LANGUAGE), scope=BotCommandScopeDefault())

    for language, language_code in _LANGUAGE_CODES.items():
        await bot.set_my_commands(
            _user_menu(language), scope=BotCommandScopeDefault(), language_code=language_code
        )


async def _register_privileged_menus(bot: Bot) -> None:
    """ADMIN/OWNER menus -- per-chat override for every known admin and the configured owner."""
    owner_id = _owner_telegram_id()

    for telegram_id in _admin_telegram_ids():
        if owner_id and str(telegram_id) == str(owner_id):
            continue  # OWNER gets the richer menu below, not the ADMIN one
        try:
            chat_id = int(telegram_id)
        except (TypeError, ValueError):
            logger.warning(f"Skipping ADMIN menu registration for non-numeric telegram_id={telegram_id!r}")
            continue
        try:
            await bot.set_my_commands(
                _admin_menu(_language_for(telegram_id)), scope=BotCommandScopeChat(chat_id=chat_id)
            )
        except Exception as e:
            logger.warning(f"ADMIN menu registration failed for telegram_id={telegram_id}: {e}")

    if not owner_id:
        return
    try:
        chat_id = int(owner_id)
    except (TypeError, ValueError):
        logger.warning(f"Skipping OWNER menu registration for non-numeric TELEGRAM_OWNER_ID={owner_id!r}")
        return
    try:
        await bot.set_my_commands(
            _owner_menu(_language_for(owner_id)), scope=BotCommandScopeChat(chat_id=chat_id)
        )
    except Exception as e:
        logger.warning(f"OWNER menu registration failed for telegram_id={owner_id}: {e}")


async def register_all_menus(bot: Bot) -> None:
    """
    One-shot, best-effort registration of every Telegram-native Menu
    Button command list this bot exposes. Called once from
    telegram/polling.py's run_polling(). Never raises.
    """
    try:
        await _register_default_menus(bot)
    except Exception as e:
        logger.warning(f"Default USER menu registration failed: {e}")

    try:
        await _register_privileged_menus(bot)
    except Exception as e:
        logger.warning(f"ADMIN/OWNER menu registration failed: {e}")
