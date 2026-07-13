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
stats_handler, users_handler, userinfo_handler, and broadcast_handler
(Phase 37; finalized Phase 41) are real: they call
telegram.admin_service.AdminService (or, for /userinfo,
telegram.user_service.UserService plus telegram.subscription_service.
SubscriptionService -- it reads a *user's* profile and plan, not
admin data). admin_handler renders a different panel for OWNER vs
ADMIN via telegram.permissions.is_owner() -- command_router only
checks "at least ADMIN", so the handler still needs to know if this
specific caller is *the* owner. vipinfo_handler stays a static
placeholder -- foundation only, no VIP tier on top of the plan system.
Which permission tier (OWNER/ADMIN/USER) a command requires is decided
by telegram.command_router before a handler ever runs; a handler
itself does not check permissions (is_owner() here is a read of an
already-established fact, not a permission gate).

plan_handler, subscription_handler, and upgrade_handler (Phase 42) are
real: they call telegram.subscription_service.SubscriptionService,
which lazily creates a default FREE/ACTIVE subscription row on first
lookup for any telegram_id (also called eagerly from start_handler, so
/plan and /subscription always have data right after /start). USER
commands -- no permission tier required. upgrade_handler is a
foundation only: no payment gateway, no real plan change, just a
static confirmation.

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
from telegram.subscription_service import SubscriptionService
from telegram.permissions import is_owner


async def start_handler(telegram_id, username=None) -> str:
    """
    /start -> UserService.register_user() -> profile created, plus
    SubscriptionService ensures a default FREE/ACTIVE subscription row
    exists (Phase 42) -- so /plan and /subscription always have data
    from the very first /start. Duplicate /start (existing user)
    returns the existing profile instead of creating a second row.
    Never raises.
    """
    try:
        result = UserService().register_user(telegram_id, username)
    except Exception as e:
        return f"Could not start: {e}"

    try:
        SubscriptionService().get_plan(telegram_id)
    except Exception:
        pass  # best-effort: a subscription hiccup must not break /start

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
        "💳 Plan\n"
        "/plan\n"
        "/subscription\n"
        "/upgrade\n"
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
    plan = _current_plan(telegram_id)

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
        "Plan:\n"
        f"{plan}\n\n"
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


def _current_plan(telegram_id) -> str:
    """
    Best-effort plan lookup shared by profile_handler/userinfo_handler.
    Falls back to "FREE" (the schema default) rather than surfacing a
    subscription error inside an otherwise-successful profile display.
    """
    try:
        result = SubscriptionService().get_plan(telegram_id)
        if result.success and result.subscription is not None:
            return result.subscription.plan
    except Exception:
        pass
    return "FREE"


async def plan_handler(telegram_id=None) -> str:
    """
    /plan -> SubscriptionService.get_plan(). USER command, no
    permission required. Never raises.
    """
    try:
        result = SubscriptionService().get_plan(telegram_id)
    except Exception as e:
        return f"Could not load plan: {e}"

    if not result.success or result.subscription is None:
        return f"Could not load plan: {result.reason}"

    return (
        "GoldBot Plan\n\n"
        "Current Plan:\n"
        f"{result.subscription.plan}\n\n"
        "Features:\n"
        "✓ Basic signals\n"
        "✓ Signal history\n\n"
        "Upgrade:\n"
        "Use /upgrade"
    )


async def subscription_handler(telegram_id=None) -> str:
    """
    /subscription -> SubscriptionService.get_subscription(). USER
    command, no permission required. Never raises.
    """
    try:
        result = SubscriptionService().get_subscription(telegram_id)
    except Exception as e:
        return f"Could not load subscription: {e}"

    if not result.success or result.subscription is None:
        return f"Could not load subscription: {result.reason}"

    sub = result.subscription
    return (
        "Subscription Status\n\n"
        "Plan:\n"
        f"{sub.plan}\n\n"
        "Status:\n"
        f"{sub.status}\n\n"
        "Expires:\n"
        f"{sub.expires_at if sub.expires_at else 'N/A'}"
    )


async def upgrade_handler(telegram_id=None) -> str:
    """
    /upgrade -> SubscriptionService.upgrade_request(). Foundation
    only -- no payment gateway, no real plan change. USER command, no
    permission required. Never raises.
    """
    try:
        SubscriptionService().upgrade_request(telegram_id)
    except Exception:
        pass  # the confirmation text below is static either way

    return "Upgrade request received.\n\nPremium plans will be available soon."


def _first_arg(args) -> Optional[str]:
    """'123456789 extra text' -> '123456789'. None if args is empty/blank."""
    if not args or not args.strip():
        return None
    return args.strip().split()[0]


async def admin_handler(telegram_id=None) -> str:
    """
    /admin -> role-specific panel menu (Phase 41). ADMIN or OWNER
    (enforced by command_router); OWNER sees the full panel, ADMIN
    sees a reduced one (no Broadcast/Admin Management). Never raises.
    """
    if is_owner(telegram_id):
        return (
            "GoldBot Owner Panel\n\n"
            "👥 Users\n"
            "📊 Statistics\n"
            "🛠 System\n"
            "📢 Broadcast\n"
            "👑 Admin Management"
        )
    return (
        "GoldBot Admin Panel\n\n"
        "👥 Users\n"
        "📊 Statistics\n"
        "🛠 System"
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
    if result.reason == "Already an admin":
        return "Already admin."
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
    """
    /system -> AdminService.get_system_status(). ADMIN or OWNER.
    Never raises.
    """
    try:
        status = AdminService().get_system_status()
    except Exception:
        return "Could not load system status."

    return (
        "GoldBot System Status\n\n"
        "Database:\n"
        f"{status.database}\n\n"
        "Telegram:\n"
        f"{status.telegram}\n\n"
        "Market Data:\n"
        f"{status.market_data}\n\n"
        "AI:\n"
        f"{status.ai}\n\n"
        "API:\n"
        f"{status.api}"
    )


async def broadcast_handler(args=None) -> str:
    """
    /broadcast MESSAGE -> AdminService.broadcast() -> sent/failed
    counts. ADMIN or OWNER. Never raises.
    """
    message = (args or "").strip()
    if not message:
        return "Usage: /broadcast MESSAGE"

    try:
        result = AdminService().broadcast(message)
    except Exception as e:
        return f"Could not broadcast: {e}"

    if not result.success or result.broadcast is None:
        return f"Could not broadcast: {result.reason}"

    return (
        "Broadcast completed\n\n"
        "Sent:\n"
        f"{result.broadcast.sent}\n\n"
        "Failed:\n"
        f"{result.broadcast.failed}"
    )


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
        "Approved:\n"
        f"{stats.approved_signals}\n\n"
        "Rejected:\n"
        f"{stats.rejected_signals}\n\n"
        "Average Confidence:\n"
        f"{confidence_percent}%"
    )


async def users_handler() -> str:
    """/users -> AdminService.get_user_summary(). ADMIN or OWNER. Never raises."""
    try:
        result = AdminService().get_user_summary()
    except Exception as e:
        return f"Could not load users: {e}"

    if not result.success or result.user_summary is None:
        return f"Could not load users: {result.reason}"

    summary = result.user_summary
    return (
        "GoldBot Users\n\n"
        "Total:\n"
        f"{summary.total}\n\n"
        "Active:\n"
        f"{summary.active}\n\n"
        "Created today:\n"
        f"{summary.created_today}"
    )


async def userinfo_handler(args=None) -> str:
    """
    /userinfo USER_ID -> UserService.get_profile() for the target
    user (not the caller). ADMIN or OWNER. Never raises.
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

    try:
        sub_result = SubscriptionService().get_subscription(target_id)
        sub = sub_result.subscription if sub_result.success else None
    except Exception:
        sub = None
    plan = sub.plan if sub is not None else "FREE"
    sub_status = sub.status if sub is not None else "ACTIVE"

    return (
        "User Info\n\n"
        "ID:\n"
        f"{p.telegram_id}\n\n"
        "Username:\n"
        f"{p.username or 'N/A'}\n\n"
        "Language:\n"
        f"{p.language}\n\n"
        "Risk:\n"
        f"{p.risk_percent:g}%\n\n"
        "Strategy:\n"
        f"{p.strategy}\n\n"
        "Timeframe:\n"
        f"{p.timeframe}\n\n"
        "Plan:\n"
        f"{plan}\n\n"
        "Subscription Status:\n"
        f"{sub_status}\n\n"
        "Created:\n"
        f"{p.created_at}\n\n"
        "Notifications:\n"
        f"{'On' if p.notifications_enabled else 'Off'}"
    )


async def vipinfo_handler() -> str:
    """/vipinfo -> foundation only. No VIP tier exists on top of the Phase 42 plan/subscription system."""
    return "VIP system not enabled."
