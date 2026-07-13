"""
Telegram Layer — command handlers.

Shape:

    Telegram Message -> Handler -> Service -> Database/Core

start_handler() and profile_handler() are real (Phase 33 -- User
Profile Foundation; Phase 34 -- Command Wiring Foundation): they call
telegram.user_service.UserService and return plain text. help_handler,
signal_handler, history_handler, status_handler, about_handler
(Phase 34), and settings_handler, language_handler, risk_handler,
strategy_handler, timeframe_handler (Phase 36) return static text --
no service backs them yet, so they stay simple and dependency-free
until a later phase adds one.

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

from telegram.user_service import UserService


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
    """/signal -> placeholder. Real signal delivery is a later phase."""
    return "No signal feature available yet."


async def history_handler() -> str:
    """/history -> placeholder. Real signal history is a later phase."""
    return "No history feature available yet."


async def status_handler() -> str:
    """/status -> static bot status. No service call needed yet."""
    return "GoldBot is running."


async def about_handler() -> str:
    """/about -> static bot description."""
    return (
        "GoldBot is a semi-automatic XAUUSD (Gold) trading signal assistant.\n"
        "It analyzes market structure and delivers signals via Telegram."
    )


async def admin_handler():
    pass
