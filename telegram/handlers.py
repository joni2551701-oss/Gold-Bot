"""
Telegram Layer — command handlers.

Shape:

    Telegram Message -> Handler -> Service -> Database/Core

start_handler() and profile_handler() are real (Phase 33 -- User
Profile Foundation; Phase 34 -- Command Wiring Foundation): they call
telegram.user_service.UserService and return plain text. help_handler,
status_handler, about_handler (Phase 34), and settings_handler,
language_handler, risk_handler, strategy_handler, timeframe_handler
(Phase 36) return static text -- no service backs them yet, so they
stay simple and dependency-free until a later phase adds one.

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
        "/risk\n"
        "/strategy\n"
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
        "GoldBot Profile\n"
        f"ID: {p.telegram_id}\n"
        f"Username: {p.username or 'N/A'}\n"
        f"Language: {p.language}\n"
        f"Trading Style: {p.trading_style}\n"
        f"Risk: {p.risk_percent}\n"
        f"Timeframe: {p.timeframe}\n"
        f"Created: {p.created_at}"
    )


async def settings_handler() -> str:
    """/settings -> placeholder. Real settings editor is a later phase."""
    return "Settings management is not available yet."


async def language_handler() -> str:
    """/language -> placeholder. Real language switching is a later phase."""
    return "Language selection is not available yet."


async def risk_handler() -> str:
    """/risk -> placeholder. Real risk-percent editing is a later phase."""
    return "Risk settings are not available yet."


async def strategy_handler() -> str:
    """/strategy -> placeholder. Real trading-style editing is a later phase."""
    return "Strategy settings are not available yet."


async def timeframe_handler() -> str:
    """/timeframe -> placeholder. Real timeframe editing is a later phase."""
    return "Timeframe settings are not available yet."


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
