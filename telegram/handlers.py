"""
Telegram Layer — command handlers.

Shape:

    Telegram Message -> Handler -> Service -> Database/Core

start_handler() and profile_handler() are minimally real (Phase 33 --
User Profile Foundation): they call telegram.user_service.UserService
and return plain text. No aiogram Dispatcher registration yet, no
inline keyboard, no language selection -- just user creation/lookup.
The remaining handlers stay empty stubs pending later phases.

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


async def help_handler():
    pass


async def profile_handler(telegram_id) -> str:
    """/profile -> UserService.get_profile() -> formatted response. Never raises."""
    try:
        result = UserService().get_profile(telegram_id)
    except Exception as e:
        return f"Could not load profile: {e}"

    if not result.success or result.profile is None:
        return "No profile found. Send /start first."

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


async def signal_handler():
    pass


async def history_handler():
    pass


async def admin_handler():
    pass
