"""
Telegram Layer — command handlers.

Shape:

    Telegram Message -> Handler -> Service -> Database/Core

start_handler() and profile_handler() are real (Phase 33 -- User
Profile Foundation; Phase 34 -- Command Wiring Foundation): they call
telegram.user_service.UserService and return plain text. help_handler,
status_handler, and about_handler (Phase 34) return static text -- no
service backs them yet, so they stay simple and dependency-free.

settings_handler, language_handler, risk_handler, strategy_handler,
and timeframe_handler (Phase 40) are real: called with no argument
they show the option keyboard (attached by command_router) plus a
usage hint; called with an argument (e.g. "/risk 5") they validate it
and call telegram.user_service.UserService's change_*() methods.
Settings change via command argument, not an aiogram callback_query
handler -- keyboards here are still display hints (same precedent as
language_keyboard() since Phase 34), consistent with how /addadmin,
/removeadmin, and /userinfo already take an argument.

signal_handler and history_handler (Phase 38) are real: they call
telegram.signal_service.SignalService (read-only) and format the
result via telegram.signal_formatter.SignalFormatter. Both are USER
commands -- no permission tier required.

admin_handler, addadmin_handler, removeadmin_handler, system_handler,
stats_handler, users_handler, and userinfo_handler (Phase 37) are real:
they call telegram.admin_service.AdminService (or, for /userinfo,
telegram.user_service.UserService -- it reads a *user's* profile, not
admin data). broadcast_handler and vipinfo_handler stay static
placeholders -- foundation only, no mass-messaging or VIP system yet.
Which permission tier (OWNER/ADMIN/USER) a command requires is decided
by telegram.command_router before a handler ever runs; a handler
itself does not check permissions.

A handler must never import database.* or core.pipeline directly --
only Handler -> Service. telegram.command_router routes incoming
commands to these functions and is the only place a keyboard
(telegram/keyboards.py) gets attached.

Note: Notifier.send_message() runs its own asyncio.run() internally,
so it must not be called directly from inside these (already-async)
handlers -- the same nested-event-loop crash found and fixed in
main.py (Phase 31.1) would reoccur. Handlers should talk to
TelegramBot directly (await bot.send_message(...)) or a future
async-native service.
"""

from typing import Optional

from telegram.user_service import UserService
from telegram.admin_service import AdminService
from telegram.signal_service import SignalService
from telegram.signal_formatter import SignalFormatter


async def start_handler(telegram_id, username=None) -> str:
    """
    /start -> UserService.register_user() -> profile created.
    Duplicate /start (existing user) returns the existing profile
    instead of creating a second row. Never raises.
    """
    try:
        result = UserService().register_user(telegram_id, username)
    except Exception as e:
        return f"Could not start: {e}"

    if result.success:
        return "Profile created."
    if result.reason == "User already exists":
        return "User already exists."
    return f"Could not start: {result.reason}"


async def help_handler() -> str:
    """/help -> static command reference. No service call needed."""
    return (
        "GoldBot Commands\n"
        "📊 Trading\n"
        "/signal\n"
        "/history\n"
        "/status\n"
        "👤 Profile\n"
        "/profile\n"
        "/settings\n"
        "/language\n"
        "/risk\n"
        "/strategy\n"
        "/timeframe\n"
        "ℹ️ Info\n"
        "/help\n"
        "/about"
    )


async def profile_handler(telegram_id) -> str:
    """/profile -> UserService.get_profile() -> formatted response. Never raises."""
    try:
        result = UserService().get_profile(telegram_id)
    except Exception as e:
        return f"Could not load profile: {e}"

    if not result.success or result.profile is None:
        return "No profile found.\nUse /start first."

    p = result.profile
    return (
        "GoldBot Profile\n\n"
        "ID:\n"
        f"{p.telegram_id}\n\n"
        "Username:\n"
        f"{p.username or 'N/A'}\n\n"
        "Language:\n"
        f"{p.language}\n\n"
        "Trading Style:\n"
        f"{p.trading_style}\n\n"
        "Strategy:\n"
        f"{p.strategy}\n\n"
        "Risk:\n"
        f"{p.risk_percent:g}%\n\n"
        "Timeframe:\n"
        f"{p.timeframe}\n\n"
        "Created:\n"
        f"{p.created_at}"
    )


async def settings_handler() -> str:
    """/settings -> menu (keyboard attached by command_router). USER command. Never raises."""
    return (
        "Settings\n\n"
        "Language\n"
        "Risk\n"
        "Strategy\n"
        "Timeframe\n"
        "Notifications\n\n"
        "Use /language, /risk, /strategy, or /timeframe to change a setting."
    )


_LANGUAGE_OPTIONS = {"UZ", "RU", "EN"}
_RISK_OPTIONS = {"1", "2", "3", "5"}
_TIMEFRAME_OPTIONS = {"M15", "H1", "H4"}
_STRATEGY_OPTIONS = {
    "liquidity sweep": "Liquidity Sweep",
    "fvg": "FVG",
    "amd": "AMD",
    "order block": "Order Block",
}


async def language_handler(telegram_id=None, args=None) -> str:
    """
    /language [UZ|RU|EN] -> UserService.change_language(). No argument
    shows the option keyboard (attached by command_router) plus a
    usage hint. Never raises.
    """
    choice = _first_arg(args)
    if choice is None:
        return (
            "Choose language:\n"
            "🇺🇿 Uzbek (UZ)\n"
            "🇷🇺 Русский (RU)\n"
            "🇬🇧 English (EN)\n\n"
            "Use /language UZ, /language RU, or /language EN."
        )

    normalized = choice.upper()
    if normalized not in _LANGUAGE_OPTIONS:
        return "Invalid language. Choose one of: UZ, RU, EN."

    try:
        result = UserService().change_language(telegram_id, normalized)
    except Exception as e:
        return f"Could not update language: {e}"

    if not result.success:
        return f"Could not update language: {result.reason}"
    return f"Language updated to {normalized}."


async def risk_handler(telegram_id=None, args=None) -> str:
    """
    /risk [1|2|3|5] -> UserService.change_risk(). No argument shows
    the option keyboard (attached by command_router) plus a usage
    hint. Never raises.
    """
    choice = _first_arg(args)
    if choice is None:
        return "Choose risk percent:\n1%\n2%\n3%\n5%\n\nUse /risk 1, /risk 2, /risk 3, or /risk 5."

    normalized = choice.rstrip("%")
    if normalized not in _RISK_OPTIONS:
        return "Invalid risk percent. Choose one of: 1, 2, 3, 5."

    try:
        result = UserService().change_risk(telegram_id, float(normalized))
    except Exception as e:
        return f"Could not update risk: {e}"

    if not result.success:
        return f"Could not update risk: {result.reason}"
    return f"Risk updated to {normalized}%."


async def strategy_handler(telegram_id=None, args=None) -> str:
    """
    /strategy [Liquidity Sweep|FVG|AMD|Order Block] ->
    UserService.change_strategy(). No argument shows the option
    keyboard (attached by command_router) plus a usage hint. Never
    raises.
    """
    choice = (args or "").strip()
    if not choice:
        return (
            "Choose strategy:\n"
            "Liquidity Sweep\n"
            "FVG\n"
            "AMD\n"
            "Order Block\n\n"
            "Use /strategy Liquidity Sweep, /strategy FVG, /strategy AMD, or /strategy Order Block."
        )

    normalized = _STRATEGY_OPTIONS.get(choice.lower())
    if normalized is None:
        return "Invalid strategy. Choose one of: Liquidity Sweep, FVG, AMD, Order Block."

    try:
        result = UserService().change_strategy(telegram_id, normalized)
    except Exception as e:
        return f"Could not update strategy: {e}"

    if not result.success:
        return f"Could not update strategy: {result.reason}"
    return f"Strategy updated to {normalized}."


async def timeframe_handler(telegram_id=None, args=None) -> str:
    """
    /timeframe [M15|H1|H4] -> UserService.change_timeframe(). No
    argument shows the option keyboard (attached by command_router)
    plus a usage hint. Never raises.
    """
    choice = _first_arg(args)
    if choice is None:
        return "Choose timeframe:\nM15\nH1\nH4\n\nUse /timeframe M15, /timeframe H1, or /timeframe H4."

    normalized = choice.upper()
    if normalized not in _TIMEFRAME_OPTIONS:
        return "Invalid timeframe. Choose one of: M15, H1, H4."

    try:
        result = UserService().change_timeframe(telegram_id, normalized)
    except Exception as e:
        return f"Could not update timeframe: {e}"

    if not result.success:
        return f"Could not update timeframe: {result.reason}"
    return f"Timeframe updated to {normalized}."


async def signal_handler() -> str:
    """
    /signal -> SignalService.get_latest_signal() -> SignalFormatter.
    USER command, no permission required. Never raises.
    """
    try:
        result = SignalService().get_latest_signal()
    except Exception as e:
        return f"Could not load signal: {e}"

    if not result.success or result.signal is None:
        return "No active signal available."

    return SignalFormatter().format_signal_row(result.signal)


async def history_handler() -> str:
    """
    /history -> SignalService.get_signal_history() -> SignalFormatter.
    USER command, no permission required. Never raises.
    """
    try:
        result = SignalService().get_signal_history(limit=5)
    except Exception as e:
        return f"Could not load history: {e}"

    if not result.success or not result.signals:
        return "No signal history available."

    return SignalFormatter().format_signal_history(result.signals)


async def status_handler() -> str:
    """/status -> static bot status. No service call needed yet."""
    return "GoldBot is running."


async def about_handler() -> str:
    """/about -> static bot description."""
    return (
        "GoldBot is a semi-automatic XAUUSD (Gold) trading signal assistant.\n"
        "It analyzes market structure and delivers signals via Telegram."
    )


def _first_arg(args) -> Optional[str]:
    """'123456789 extra text' -> '123456789'. None if args is empty/blank."""
    if not args or not args.strip():
        return None
    return args.strip().split()[0]


async def admin_handler() -> str:
    """/admin -> owner panel static menu. OWNER only (enforced by command_router)."""
    return (
        "Owner Panel\n\n"
        "Users\n"
        "Statistics\n"
        "Admins\n"
        "System"
    )


async def addadmin_handler(args=None) -> str:
    """/addadmin USER_ID -> AdminService.add_admin(). OWNER only. Never raises."""
    target_id = _first_arg(args)
    if target_id is None:
        return "Usage: /addadmin USER_ID"

    try:
        result = AdminService().add_admin(target_id)
    except Exception as e:
        return f"Could not add admin: {e}"

    if result.success:
        return "Admin added."
    return f"Could not add admin: {result.reason}"


async def removeadmin_handler(args=None) -> str:
    """/removeadmin USER_ID -> AdminService.remove_admin(). OWNER only. Never raises."""
    target_id = _first_arg(args)
    if target_id is None:
        return "Usage: /removeadmin USER_ID"

    try:
        result = AdminService().remove_admin(target_id)
    except Exception as e:
        return f"Could not remove admin: {e}"

    if result.success:
        return "Admin removed."
    return f"Could not remove admin: {result.reason}"


async def system_handler() -> str:
    """/system -> lightweight status summary. OWNER only. Never raises."""
    try:
        db_ok = AdminService().check_database()
    except Exception:
        db_ok = False
    db_status = "OK" if db_ok else "FAIL"

    return (
        "System Status\n\n"
        f"Database: {db_status}\n"
        "API: OK\n"
        "AI: OK\n"
        "Telegram: OK"
    )


async def broadcast_handler() -> str:
    """/broadcast -> placeholder. Real mass-message delivery is a later phase."""
    return "Broadcast is not available yet."


async def stats_handler() -> str:
    """/stats -> AdminService.get_statistics(). ADMIN or OWNER. Never raises."""
    try:
        result = AdminService().get_statistics()
    except Exception as e:
        return f"Could not load statistics: {e}"

    if not result.success or result.statistics is None:
        return f"Could not load statistics: {result.reason}"

    stats = result.statistics
    confidence_percent = round(stats.average_confidence * 100)
    return (
        "GoldBot Statistics\n\n"
        "Users:\n"
        f"{stats.total_users}\n\n"
        "Signals:\n"
        f"{stats.total_signals}\n\n"
        "Average Confidence:\n"
        f"{confidence_percent}%"
    )


async def users_handler() -> str:
    """/users -> total registered user count. ADMIN or OWNER. Never raises."""
    try:
        result = AdminService().get_statistics()
    except Exception as e:
        return f"Could not load users: {e}"

    if not result.success or result.statistics is None:
        return f"Could not load users: {result.reason}"

    return f"Total users:\n{result.statistics.total_users}"


async def userinfo_handler(args=None) -> str:
    """
    /userinfo USER_ID -> UserService.get_profile() for the target
    user (not the caller). ADMIN or OWNER. Never raises. "Plan: Trial"
    is a static placeholder -- no subscription/VIP system exists yet.
    """
    target_id = _first_arg(args)
    if target_id is None:
        return "Usage: /userinfo USER_ID"

    try:
        result = UserService().get_profile(target_id)
    except Exception as e:
        return f"Could not load user info: {e}"

    if not result.success or result.profile is None:
        return "User not found."

    p = result.profile
    return (
        "User Info\n\n"
        "ID:\n"
        f"{p.telegram_id}\n"
        "Username:\n"
        f"{p.username or 'N/A'}\n"
        "Plan:\n"
        "Trial\n"
        "Risk:\n"
        f"{round(p.risk_percent)}%"
    )


async def vipinfo_handler() -> str:
    """/vipinfo -> foundation only. No VIP/subscription system exists yet."""
    return "VIP system not enabled."
