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
/removeadmin, and /userinfo already take an argument. language_handler
is the one exception since the V1 Language Callback Fix: its
lang_uz/lang_ru/lang_en keyboard buttons are wired to a real
callback_query handler (platform_layer/telegram/callback_router.py), and V1.1
Language UX Polish gave it a fuller result -- see language_status()
next to it for the current-language display, duplicate-selection
guard, and keyboard-removal-on-success behavior callback_router.py
consumes.

signal_handler and history_handler (Phase 38) are real: they call
telegram.signal_service.SignalService (read-only) and format the
result via telegram.signal_formatter.SignalFormatter. Both are USER
commands (no command_router permission tier). signal_handler (Phase
44) additionally gates on telegram.signal_access_service.
SignalAccessService: FREE-plan users are denied with a static
upgrade message, PREMIUM/VIP and OWNER/ADMIN pass through.
history_handler is deliberately left ungated -- see its own
docstring.

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

notifications_handler (Phase 43) is real: it calls
telegram.notification_service.NotificationService. USER command -- no
permission tier required. Changes happen via command argument
("/notifications on"/"off"), same interaction model as
language_handler/risk_handler/etc. -- notifications_keyboard() exists
in platform_layer/telegram/keyboards.py but is not wired to a reply here, since
platform_layer/telegram/command_router.py (the only place a keyboard gets attached)
is out of scope for this phase.

feedback_handler and feedbacks_handler (Phase 46) are real: the
former (USER, no permission tier) submits an entry via
telegram.feedback_service.FeedbackService.send_feedback(); the latter
(ADMIN or OWNER) lists all entries via AdminService.get_feedback(),
which itself delegates to FeedbackService -- AdminService never talks
to FeedbackRepository directly.

Phase 45 (User Lifecycle State): start_handler, profile_handler,
settings_handler, signal_handler, history_handler, plan_handler, and
subscription_handler all call UserService.touch_activity() (updates
last_activity; promotes a NEW user to ACTIVE; never reactivates a
BANNED user) before doing their normal work -- best-effort, wrapped in
its own try/except so a touch_activity hiccup never blocks the
handler's real response. start_handler is the one exception with
special-cased logic: a brand new registration is left at status=NEW
(no touch_activity call for that specific branch -- see its
docstring), matching the Phase 45 spec's own state diagram. User
lifecycle status (NEW/ACTIVE/BANNED) is deliberately a separate axis
from subscription plan (FREE/PREMIUM/VIP, Phase 42) -- userinfo_handler
and users_handler show both, never conflated. No command blocks a
BANNED user yet (ban_user()/activate_user() exist on UserService for
a future phase's enforcement).

ai_status_handler, ai_provider_handler, ai_cost_handler,
ai_usage_handler, and ai_health_handler (Phase 61.5: AI Production
Integration Foundation, TASK 3) are real: they call
platform_layer.telegram.owner.ai_commands's own functions (built Phase 61.4 TASK 3,
extended 61.5 TASK 2/3), the first live callers those functions have
ever had. OWNER only. Every one of them relies on
platform_layer.telegram.owner.ai_commands's own `Optional[...] = None` defaults to
construct its `ai/` objects (ProviderManager/ProviderHealthTracker/
CapabilityManager) -- these handlers hold no `ai/` import of their
own beyond the `platform_layer.telegram.owner.ai_commands` functions themselves, same
"Handler -> Service" shape as every other owner command here.
ai_cost_handler/ai_usage_handler pass an empty provider_stats/
user_usage dict -- no live `ai/audit/` data source is wired into the
running bot yet (no live AIService call happens anywhere in this
phase either), so these report zero/"no usage" honestly rather than
fabricating history, exactly as their own docstrings already promise
for that input shape.

owner_handler and doctor_handler (Phase 61.5 Addendum, per Director
review) are real: they call platform_layer.telegram.owner.dashboard's
get_owner_summary()/get_doctor_report() -- a compact key-value
dashboard panel and a nine-subsystem self-diagnostic, respectively,
both composing already-existing service calls (AdminService,
ai_commands, SubscriptionRepository, SignalRepository,
EmergencyManager). OWNER only.

runtime_handler, runtime_events_handler, and runtime_metrics_handler
(Phase 61.6: AI Operations & Reliability Foundation, TASK 6) are real:
they call platform_layer.telegram.owner.runtime_commands's own functions (built this
phase), each with no injected RuntimeManager/EventBus/collector -- see
that module's own docstring for why a fresh construction per call
reports a fresh/default/empty state (RuntimeManager defaults to READY,
EventBus/collector default to empty) rather than a fabricated one, the
same honesty posture ai_cost_handler's own empty-dict default already
established. OWNER only.

runtime_status_handler and runtime_check_handler (Phase 61.7: AI
Platform Stabilization & Integration, TASK 7/8) are real: they call
platform_layer.telegram.owner.runtime_commands.runtime_full_status()/runtime_check()
-- a combined status panel and the AI runtime self-check,
respectively. Same fresh-construction-per-call posture as every
runtime_*_handler above. OWNER only.

contact_handler (Phase 61.5 TASK 4) is real: it calls
telegram.user_service.UserService.register_phone() -- the Phone Hash
-> UserRecord -> Trial Check -> FREE account flow. Unlike every other
handler above, it is never reached through telegram.command_router's
normal `/command` dispatch table -- a Telegram contact-share message
has `message.contact` populated and `message.text is None`, so
telegram.command_router.route_contact() (a new, separate entry point,
mirroring route_message()'s shape) calls it directly.
platform_layer/telegram/keyboards.py's new phone_share_keyboard() (attached to
/start's reply as of this phase -- see command_router.py's
_KEYBOARD_BY_COMMAND) is what makes the Telegram client show the
"Share Phone Number" button that produces this contact message in the
first place.

A handler must never import database.* or core_layer.pipeline directly --
only Handler -> Service. telegram.command_router routes incoming
commands to these functions and is the only place a keyboard
(platform_layer/telegram/keyboards.py) gets attached.

Note: Notifier.send_message() runs its own asyncio.run() internally,
so it must not be called directly from inside these (already-async)
handlers -- the same nested-event-loop crash found and fixed in
main.py (Phase 31.1) would reoccur. Handlers should talk to
TelegramBot directly (await bot.send_message(...)) or a future
async-native service.
"""

from dataclasses import dataclass
from typing import Optional

from platform_layer.telegram.user_service import UserService
from platform_layer.telegram.registration_service import RegistrationService
from platform_layer.telegram.admin_service import AdminService
from platform_layer.telegram.signal_service import SignalService
from platform_layer.telegram.signal_formatter import SignalFormatter
from platform_layer.telegram.subscription_service import SubscriptionService
from platform_layer.telegram.notification_service import NotificationService
from platform_layer.telegram.signal_access_service import SignalAccessService
from platform_layer.telegram.feedback_service import FeedbackService
from platform_layer.telegram.permissions import is_owner
from media_layer.translation.ui_catalog import t
from platform_layer.telegram.owner.ai_commands import ai_cost, ai_explanation_status, ai_health, ai_provider, ai_status, ai_usage, resolve_capability
from platform_layer.telegram.owner.dashboard import get_doctor_report, get_owner_summary
from platform_layer.telegram.owner.monitoring_commands import (
    get_daily_report,
    get_errors_report,
    get_health_report,
    get_market_report,
    get_performance_report,
    get_pipeline_report,
    get_signals_report,
    get_status_report,
)
from platform_layer.telegram.owner.runtime_commands import (
    runtime_check,
    runtime_events,
    runtime_full_status,
    runtime_metrics,
    runtime_provider,
    runtime_restart,
    runtime_status,
)
from core_layer.logger.logger import setup_logger

logger = setup_logger("Handlers")


async def start_handler(telegram_id, username=None) -> str:
    """
    /start -> UserService.register_user() -> profile created, plus
    SubscriptionService ensures a default FREE/ACTIVE subscription row
    exists (Phase 42) -- so /plan and /subscription always have data
    from the very first /start. Never raises.

    Phase 45 lifecycle: a brand new user is created with status=NEW
    and left there -- promotion to ACTIVE happens on the *next* real
    interaction, not on the registration call itself. Duplicate /start
    (existing user) is exactly that next interaction, so it calls
    touch_activity() (updates last_activity, and promotes NEW->ACTIVE;
    a BANNED user is never silently reactivated by this).

    V2 Phase 3 (Registration Wizard): a BANNED existing user is
    stopped here, before touch_activity() or SubscriptionService are
    ever called -- register_user()'s "already exists" branch already
    carries the fetched profile, so this is a free check, not a second
    query. command_router.py's keyboard selection (via
    _registration_step()) independently returns None for a BANNED
    user, so no Wizard keyboard is attached to this reply either.
    """
    try:
        result = UserService().register_user(telegram_id, username)
    except Exception as e:
        logger.warning(f"start_handler: register_user failed for telegram_id={telegram_id}: {e}")
        return t("start.error", _current_language(telegram_id), error=e)

    if (
        not result.success
        and result.reason == "User already exists"
        and result.profile is not None
        and result.profile.status == "BANNED"
    ):
        return t("start.banned", _current_language(telegram_id))

    try:
        SubscriptionService().get_plan(telegram_id)
    except Exception as e:
        # best-effort: a subscription hiccup must not break /start
        logger.warning(f"start_handler: get_plan failed for telegram_id={telegram_id}: {e}")

    if result.success:
        return t("start.created", _current_language(telegram_id))
    if result.reason == "User already exists":
        try:
            UserService().touch_activity(telegram_id)
        except Exception as e:
            logger.warning(f"start_handler: touch_activity failed for telegram_id={telegram_id}: {e}")
        return t("start.already_exists", _current_language(telegram_id))
    return t("start.error", _current_language(telegram_id), error=result.reason)


def _registration_step(telegram_id) -> Optional[str]:
    """
    Best-effort read of the Wizard step to show next (V2 Phase 3),
    mirroring _current_language()'s shape -- used by command_router.py
    to pick /start's reply keyboard. None means "no Wizard keyboard":
    the user is BANNED, already COMPLETE, or the lookup itself failed.
    Never raises.
    """
    try:
        return RegistrationService().current_step(telegram_id)
    except Exception as e:
        logger.warning(f"_registration_step failed for telegram_id={telegram_id}: {e}")
        return None


def _is_registration_complete(telegram_id) -> bool:
    """
    Best-effort check (V2 Phase 5) for whether telegram_id's
    registration has reached COMPLETE -- used by
    command_router.route_contact() to decide whether to attach the
    persistent Reply Keyboard right after a successful phone share.
    Never raises.
    """
    try:
        return RegistrationService().is_complete(telegram_id)
    except Exception as e:
        logger.warning(f"_is_registration_complete failed for telegram_id={telegram_id}: {e}")
        return False


def _is_banned(telegram_id) -> bool:
    """
    Best-effort check (V2 Phase 5) for whether telegram_id's account
    is BANNED -- used by command_router.py to attach
    ReplyKeyboardRemove() instead of any Wizard/persistent keyboard on
    /start's reply. Mirrors _current_language()'s shape. Never raises.
    """
    try:
        result = UserService().get_profile(telegram_id)
    except Exception as e:
        logger.warning(f"_is_banned failed for telegram_id={telegram_id}: {e}")
        return False
    return result.success and result.profile is not None and result.profile.status == "BANNED"


async def help_handler(telegram_id=None) -> str:
    """/help -> localized command reference. No service call beyond the language lookup."""
    return t("help.text", _current_language(telegram_id))


async def profile_handler(telegram_id) -> str:
    """
    /profile -> UserService.get_profile() -> formatted response.
    Touches activity (Phase 45: promotes a NEW user to ACTIVE, updates
    last_activity) before loading the profile, so a NEW user's very
    first /profile call already reflects their new state. Never
    raises.
    """
    try:
        UserService().touch_activity(telegram_id)
    except Exception as e:
        logger.warning(f"profile_handler: touch_activity failed for telegram_id={telegram_id}: {e}")

    try:
        result = UserService().get_profile(telegram_id)
    except Exception as e:
        logger.warning(f"profile_handler: get_profile failed for telegram_id={telegram_id}: {e}")
        return t("profile.error", _current_language(telegram_id), error=e)

    if not result.success or result.profile is None:
        return t("profile.not_found", _current_language(telegram_id))

    p = result.profile
    plan = _current_plan(telegram_id)
    language = p.language or _current_language(telegram_id)

    return t(
        "profile.display",
        language,
        telegram_id=p.telegram_id,
        username=p.username or t("common.na", language),
        profile_language=p.language,
        trading_style=p.trading_style,
        strategy=p.strategy,
        risk_percent=f"{p.risk_percent:g}",
        timeframe=p.timeframe,
        plan=plan,
        notifications=t("common.on", language) if p.notifications_enabled else t("common.off", language),
        status=p.status,
        created_at=p.created_at,
    )


async def settings_handler(telegram_id=None) -> str:
    """
    /settings -> menu (keyboard attached by command_router). USER
    command. Touches activity (Phase 45). Never raises.

    V2 Phase 6.2 (Settings Callback Completion, Stage 5): shows the
    caller's actual stored values (Language/Risk/Strategy/Timeframe/
    Notifications), read via _current_profile() -- never hardcoded.
    Falls back to common.na for each field if the profile can't be
    read (e.g. an unregistered caller), same "never raises, always
    something to show" posture _current_language() already keeps.
    """
    try:
        UserService().touch_activity(telegram_id)
    except Exception as e:
        logger.warning(f"settings_handler: touch_activity failed for telegram_id={telegram_id}: {e}")

    language = _current_language(telegram_id)
    profile = _current_profile(telegram_id)
    na = t("common.na", language)
    if profile is None:
        language_value = risk_value = strategy_value = timeframe_value = notifications_value = na
    else:
        language_value = _language_name(profile.language)
        risk_value = f"{profile.risk_percent:g}%"
        strategy_value = profile.strategy
        timeframe_value = profile.timeframe
        notifications_value = t("common.on", language) if profile.notifications_enabled else t("common.off", language)

    return t(
        "settings.menu", language,
        language_value=language_value,
        risk_value=risk_value,
        strategy_value=strategy_value,
        timeframe_value=timeframe_value,
        notifications_value=notifications_value,
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

# V1.1 Language UX Polish -- single source for the flag+name shown
# anywhere a language code appears in Language-module text, so no
# handler or the callback router ever spells one out inline.
_LANGUAGE_NAMES = {
    "UZ": "🇺🇿 Uzbek",
    "RU": "🇷🇺 Русский",
    "EN": "🇬🇧 English",
}


def _language_name(code: str) -> str:
    return _LANGUAGE_NAMES.get(code, code)


def _current_language(telegram_id) -> str:
    """Best-effort read of the caller's stored language; falls back to
    the database column's own default ('UZ') on any lookup failure so
    the Language screen always has something to show. Never raises."""
    try:
        result = UserService().get_profile(telegram_id)
    except Exception as e:
        logger.warning(f"language_handler: get_profile failed for telegram_id={telegram_id}: {e}")
        return "UZ"
    if not result.success or result.profile is None:
        return "UZ"
    return result.profile.language or "UZ"


def _current_profile(telegram_id):
    """
    V2 Phase 6.2 (Settings Callback Completion) -- best-effort read of
    the caller's full stored profile (UserRecord), or None on any
    lookup failure. Shared by every "_current_*" accessor below and by
    settings_handler()'s current-value display, so a DB round trip
    isn't repeated per field. Never raises.
    """
    try:
        result = UserService().get_profile(telegram_id)
    except Exception as e:
        logger.warning(f"_current_profile failed for telegram_id={telegram_id}: {e}")
        return None
    if not result.success or result.profile is None:
        return None
    return result.profile


def _current_risk(telegram_id):
    """Caller's stored risk_percent as a bare string ('1'/'2'/'3'/'5'), or None. Matches _RISK_OPTIONS' own string shape."""
    profile = _current_profile(telegram_id)
    return f"{profile.risk_percent:g}" if profile else None


def _current_timeframe(telegram_id):
    """Caller's stored timeframe ('M15'/'H1'/'H4'), or None."""
    profile = _current_profile(telegram_id)
    return profile.timeframe if profile else None


def _current_strategy_slug(telegram_id):
    """Caller's stored strategy as a keyboard callback_data slug (e.g. 'Liquidity Sweep' -> 'liquidity_sweep'), or None."""
    profile = _current_profile(telegram_id)
    return profile.strategy.lower().replace(" ", "_") if profile else None


def _current_notifications_choice(telegram_id):
    """Caller's stored notification preference ('on'/'off'), or None."""
    profile = _current_profile(telegram_id)
    if profile is None:
        return None
    return "on" if profile.notifications_enabled else "off"


@dataclass(frozen=True)
class LanguageUpdateResult:
    """
    text: the message to show the caller.
    show_keyboard: whether the language picker should stay attached --
        True while the picker's job isn't finished (first prompt,
        invalid input, re-selecting the current language, or an update
        failure the caller may want to retry), False once a language
        change actually took effect (the picker's job is done).
    """
    text: str
    show_keyboard: bool


async def language_status(telegram_id=None, args=None) -> LanguageUpdateResult:
    """
    Full result behind /language and its inline keyboard's lang_*
    callbacks (V1.1 Language UX Polish): the reply text plus whether
    the picker keyboard should remain visible. language_handler()
    below is the plain str wrapper telegram.command_router's
    text-command path already expects (its contract predates this
    phase and stays str); telegram.callback_router uses this richer
    form to decide whether to remove the keyboard after a tap. Never
    raises.
    """
    current = _current_language(telegram_id)
    choice = _first_arg(args)
    if choice is None:
        return LanguageUpdateResult(
            text=t("language.prompt", current, name=_language_name(current)),
            show_keyboard=True,
        )

    normalized = choice.upper()
    if normalized not in _LANGUAGE_OPTIONS:
        return LanguageUpdateResult(
            text=t("language.invalid", current),
            show_keyboard=True,
        )

    if current == normalized:
        return LanguageUpdateResult(
            text=t("language.already_selected", current, name=_language_name(normalized)),
            show_keyboard=True,
        )

    try:
        result = UserService().change_language(telegram_id, normalized)
    except Exception as e:
        logger.warning(f"language_handler: change_language failed for telegram_id={telegram_id}: {e}")
        return LanguageUpdateResult(text=t("language.update_error", current), show_keyboard=True)

    if not result.success:
        logger.warning(f"language_handler: change_language rejected for telegram_id={telegram_id}: {result.reason}")
        return LanguageUpdateResult(text=t("language.update_error", current), show_keyboard=True)

    return LanguageUpdateResult(
        text=t("language.updated", normalized, name=_language_name(normalized)),
        show_keyboard=False,
    )


async def language_handler(telegram_id=None, args=None) -> str:
    """
    /language [UZ|RU|EN] -> UserService.change_language(). No argument
    shows the current language plus the inline picker prompt (the
    keyboard itself is attached by command_router for the text-command
    path). Never raises. See language_status() above for the full
    result, including whether the picker should stay visible.

    V2 Phase 3.1: a valid language code given via this text-command
    path (e.g. "/language UZ") advances the Registration Wizard past
    LANGUAGE exactly like tapping the inline picker button already
    does in telegram.callback_router._handle_language() -- unconditionally
    on a valid choice, even one that re-selects the already-current
    language (matching that same unconditional-on-a-real-selection
    behavior), never on a bare "/language" (no choice made) or an
    invalid code. Before this phase, only the inline-button path
    advanced the Wizard, so a user who typed the command instead of
    tapping could get permanently stuck being re-shown the Language
    step by every subsequent /start. advance_past_language() is a
    no-op (and never raises) for anyone not currently at the LANGUAGE
    step, so this check is what to call it on, not whether it's safe
    to call.
    """
    result = await language_status(telegram_id, args)

    choice = _first_arg(args)
    if choice is not None and choice.upper() in _LANGUAGE_OPTIONS:
        try:
            RegistrationService().advance_past_language(telegram_id)
        except Exception as e:
            logger.warning(f"language_handler: registration advance failed for telegram_id={telegram_id}: {e}")

    return result.text


async def risk_status(telegram_id=None, args=None) -> LanguageUpdateResult:
    """
    Full result behind /risk and its inline keyboard's risk_* callbacks
    (V2 Phase 6.2: Settings Callback Completion) -- the reply text plus
    whether the picker should stay open. Reuses LanguageUpdateResult
    as-is (V1.1 Language UX Polish): its (text, show_keyboard) shape is
    already generic, not language-specific, so no new result type is
    introduced here. risk_handler() below is the plain str wrapper
    telegram.command_router's text-command path already expects. Never
    raises.
    """
    language = _current_language(telegram_id)
    choice = _first_arg(args)
    if choice is None:
        return LanguageUpdateResult(text=t("risk.prompt", language), show_keyboard=True)

    normalized = choice.rstrip("%")
    if normalized not in _RISK_OPTIONS:
        return LanguageUpdateResult(text=t("risk.invalid", language), show_keyboard=True)

    try:
        result = UserService().change_risk(telegram_id, float(normalized))
    except Exception as e:
        logger.warning(f"risk_handler: change_risk failed for telegram_id={telegram_id}: {e}")
        return LanguageUpdateResult(text=t("risk.error", language, error=e), show_keyboard=True)

    if not result.success:
        return LanguageUpdateResult(text=t("risk.error", language, error=result.reason), show_keyboard=True)
    return LanguageUpdateResult(text=t("risk.updated", language, percent=normalized), show_keyboard=False)


async def risk_handler(telegram_id=None, args=None) -> str:
    """
    /risk [1|2|3|5] -> UserService.change_risk(). No argument shows
    the option keyboard (attached by command_router) plus a usage
    hint. Never raises. See risk_status() above for the full result.
    """
    return (await risk_status(telegram_id, args)).text


async def strategy_status(telegram_id=None, args=None) -> LanguageUpdateResult:
    """
    Full result behind /strategy and its inline keyboard's strategy_*
    callbacks (V2 Phase 6.2). See risk_status()'s docstring for why
    LanguageUpdateResult is reused as-is. Never raises.
    """
    language = _current_language(telegram_id)
    choice = (args or "").strip()
    if not choice:
        return LanguageUpdateResult(text=t("strategy.prompt", language), show_keyboard=True)

    normalized = _STRATEGY_OPTIONS.get(choice.lower())
    if normalized is None:
        return LanguageUpdateResult(text=t("strategy.invalid", language), show_keyboard=True)

    try:
        result = UserService().change_strategy(telegram_id, normalized)
    except Exception as e:
        logger.warning(f"strategy_handler: change_strategy failed for telegram_id={telegram_id}: {e}")
        return LanguageUpdateResult(text=t("strategy.error", language, error=e), show_keyboard=True)

    if not result.success:
        return LanguageUpdateResult(text=t("strategy.error", language, error=result.reason), show_keyboard=True)
    return LanguageUpdateResult(text=t("strategy.updated", language, strategy=normalized), show_keyboard=False)


async def strategy_handler(telegram_id=None, args=None) -> str:
    """
    /strategy [Liquidity Sweep|FVG|AMD|Order Block] ->
    UserService.change_strategy(). No argument shows the option
    keyboard (attached by command_router) plus a usage hint. Never
    raises. See strategy_status() above for the full result.
    """
    return (await strategy_status(telegram_id, args)).text


async def timeframe_status(telegram_id=None, args=None) -> LanguageUpdateResult:
    """
    Full result behind /timeframe and its inline keyboard's
    timeframe_* callbacks (V2 Phase 6.2). See risk_status()'s
    docstring for why LanguageUpdateResult is reused as-is. Never
    raises.
    """
    language = _current_language(telegram_id)
    choice = _first_arg(args)
    if choice is None:
        return LanguageUpdateResult(text=t("timeframe.prompt", language), show_keyboard=True)

    normalized = choice.upper()
    if normalized not in _TIMEFRAME_OPTIONS:
        return LanguageUpdateResult(text=t("timeframe.invalid", language), show_keyboard=True)

    try:
        result = UserService().change_timeframe(telegram_id, normalized)
    except Exception as e:
        logger.warning(f"timeframe_handler: change_timeframe failed for telegram_id={telegram_id}: {e}")
        return LanguageUpdateResult(text=t("timeframe.error", language, error=e), show_keyboard=True)

    if not result.success:
        return LanguageUpdateResult(text=t("timeframe.error", language, error=result.reason), show_keyboard=True)
    return LanguageUpdateResult(text=t("timeframe.updated", language, timeframe=normalized), show_keyboard=False)


async def timeframe_handler(telegram_id=None, args=None) -> str:
    """
    /timeframe [M15|H1|H4] -> UserService.change_timeframe(). No
    argument shows the option keyboard (attached by command_router)
    plus a usage hint. Never raises. See timeframe_status() above for
    the full result.
    """
    return (await timeframe_status(telegram_id, args)).text


async def notifications_status(telegram_id=None, args=None) -> LanguageUpdateResult:
    """
    Full result behind /notifications and its inline keyboard's
    notifications_* callbacks (V2 Phase 6.2). See risk_status()'s
    docstring for why LanguageUpdateResult is reused as-is. Never
    raises.
    """
    language = _current_language(telegram_id)
    choice = _first_arg(args)
    if choice is None:
        try:
            enabled = NotificationService().is_enabled(telegram_id)
        except Exception as e:
            logger.warning(f"notifications_handler: is_enabled failed for telegram_id={telegram_id}: {e}")
            enabled = True  # schema default
        status_text = t("notifications.status_on", language) if enabled else t("notifications.status_off", language)
        return LanguageUpdateResult(text=t("notifications.status", language, status=status_text), show_keyboard=True)

    normalized = choice.lower()
    if normalized not in {"on", "off"}:
        return LanguageUpdateResult(text=t("notifications.invalid", language), show_keyboard=True)

    try:
        service = NotificationService()
        result = service.enable_notifications(telegram_id) if normalized == "on" else service.disable_notifications(telegram_id)
    except Exception as e:
        logger.warning(f"notifications_handler: update failed for telegram_id={telegram_id}: {e}")
        return LanguageUpdateResult(text=t("notifications.error", language, error=e), show_keyboard=True)

    if not result.success:
        return LanguageUpdateResult(text=t("notifications.error", language, error=result.reason), show_keyboard=True)
    text = t("notifications.enabled", language) if normalized == "on" else t("notifications.disabled", language)
    return LanguageUpdateResult(text=text, show_keyboard=False)


async def notifications_handler(telegram_id=None, args=None) -> str:
    """
    /notifications [on|off] -> NotificationService.enable_notifications()
    / disable_notifications(). No argument shows current status plus a
    usage hint. Never raises. See notifications_status() above for the
    full result.
    """
    return (await notifications_status(telegram_id, args)).text


async def signal_handler(telegram_id=None) -> str:
    """
    /signal -> SignalAccessService gate (Phase 44: FREE plan denied;
    PREMIUM/VIP plans and OWNER/ADMIN allowed) -> SignalService.
    get_latest_signal() -> SignalFormatter. No command_router
    permission tier (still USER-level routing) -- the plan check
    happens inside the handler, not at the command-router layer, since
    it depends on subscription state, not Telegram admin/owner role.
    Touches activity (Phase 45). Never raises.
    """
    try:
        UserService().touch_activity(telegram_id)
    except Exception as e:
        logger.warning(f"signal_handler: touch_activity failed for telegram_id={telegram_id}: {e}")

    language = _current_language(telegram_id)
    try:
        access_service = SignalAccessService()
        if not access_service.can_access_signal(telegram_id):
            return access_service.denied_message(telegram_id)
    except Exception as e:
        logger.warning(f"signal_handler: can_access_signal failed for telegram_id={telegram_id}: {e}")
        return t("signal.access_error", language, error=e)

    try:
        result = SignalService().get_latest_signal()
    except Exception as e:
        logger.warning(f"signal_handler: get_latest_signal failed for telegram_id={telegram_id}: {e}")
        return t("signal.load_error", language, error=e)

    if not result.success or result.signal is None:
        return t("signal.none", language)

    return SignalFormatter().format_signal_row(result.signal)


async def history_handler(telegram_id=None) -> str:
    """
    /history -> SignalService.get_signal_history() -> SignalFormatter.
    USER command, no permission required. Deliberately NOT gated by
    SignalAccessService (Phase 44 design decision): a FREE user can
    browse past signals but not the live one -- /history is the
    product-discovery funnel that shows GoldBot's output is real
    before a user decides whether to upgrade, while /signal is the
    thing worth paying for. Touches activity (Phase 45). Never raises.
    """
    try:
        UserService().touch_activity(telegram_id)
    except Exception as e:
        logger.warning(f"history_handler: touch_activity failed for telegram_id={telegram_id}: {e}")

    language = _current_language(telegram_id)
    try:
        result = SignalService().get_signal_history(limit=5)
    except Exception as e:
        logger.warning(f"history_handler: get_signal_history failed for telegram_id={telegram_id}: {e}")
        return t("history.error", language, error=e)

    if not result.success or not result.signals:
        return t("history.none", language)

    return SignalFormatter().format_signal_history(result.signals)


async def status_handler(telegram_id=None) -> str:
    """/status -> localized static bot status."""
    return t("status.running", _current_language(telegram_id))


async def about_handler(telegram_id=None) -> str:
    """/about -> localized static bot description."""
    return t("about.text", _current_language(telegram_id))


async def price_handler(telegram_id=None) -> str:
    """
    /price -> the localized "Current Price" for the tracked asset
    (TASK-CORE-004 Phase 1). Read-only and informational: reads the
    existing production cache via CurrentPriceService -> CurrentPriceProvider
    (never the cache directly, Director Decision 1), never fetches, and
    never touches any signal/trade/risk/AI/strategy path (Director
    Decision 2). Fail-safe: any error degrades to the empty-state string.
    """
    from platform_layer.telegram.current_price_service import CurrentPriceService
    try:
        return CurrentPriceService().render(_current_language(telegram_id))
    except Exception as e:  # noqa: BLE001 -- never raise into the event loop
        logger.warning(f"price_handler failed for telegram_id={telegram_id}: {e}")
        return t("price.empty", _current_language(telegram_id))


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
    except Exception as e:
        logger.warning(f"_current_plan: get_plan failed for telegram_id={telegram_id}: {e}")
    return "FREE"


async def plan_handler(telegram_id=None) -> str:
    """
    /plan -> SubscriptionService.get_plan(). USER command, no
    permission required. Touches activity (Phase 45). Never raises.
    """
    try:
        UserService().touch_activity(telegram_id)
    except Exception as e:
        logger.warning(f"plan_handler: touch_activity failed for telegram_id={telegram_id}: {e}")

    language = _current_language(telegram_id)
    try:
        result = SubscriptionService().get_plan(telegram_id)
    except Exception as e:
        logger.warning(f"plan_handler: get_plan failed for telegram_id={telegram_id}: {e}")
        return t("plan.error", language, detail=e)

    if not result.success or result.subscription is None:
        return t("plan.error", language, detail=result.reason)

    return t("plan.display", language, plan=result.subscription.plan)


async def subscription_handler(telegram_id=None) -> str:
    """
    /subscription -> SubscriptionService.get_subscription(). USER
    command, no permission required. Touches activity (Phase 45).
    Never raises.
    """
    try:
        UserService().touch_activity(telegram_id)
    except Exception as e:
        logger.warning(f"subscription_handler: touch_activity failed for telegram_id={telegram_id}: {e}")

    language = _current_language(telegram_id)
    try:
        result = SubscriptionService().get_subscription(telegram_id)
    except Exception as e:
        logger.warning(f"subscription_handler: get_subscription failed for telegram_id={telegram_id}: {e}")
        return t("subscription.error", language, detail=e)

    if not result.success or result.subscription is None:
        return t("subscription.error", language, detail=result.reason)

    sub = result.subscription
    return t(
        "subscription.display",
        language,
        plan=sub.plan,
        status=sub.status,
        expires=sub.expires_at if sub.expires_at else t("common.na", language),
    )


async def upgrade_handler(telegram_id=None) -> str:
    """
    /upgrade -> SubscriptionService.upgrade_request(). Foundation
    only -- no payment gateway, no real plan change. USER command, no
    permission required. Never raises.
    """
    try:
        SubscriptionService().upgrade_request(telegram_id)
    except Exception as e:
        # the confirmation text below is static either way
        logger.warning(f"upgrade_handler: upgrade_request failed for telegram_id={telegram_id}: {e}")

    return t("upgrade.confirmation", _current_language(telegram_id))


async def feedback_handler(telegram_id=None, args=None) -> str:
    """
    /feedback MESSAGE -> FeedbackService.send_feedback(). No argument
    shows a prompt instead of submitting an empty entry. USER command,
    no permission required. Touches activity (Phase 45). Never raises.
    """
    try:
        UserService().touch_activity(telegram_id)
    except Exception as e:
        logger.warning(f"feedback_handler: touch_activity failed for telegram_id={telegram_id}: {e}")

    language = _current_language(telegram_id)
    message = (args or "").strip()
    if not message:
        return t("feedback.prompt", language)

    try:
        result = FeedbackService().send_feedback(telegram_id, message)
    except Exception as e:
        logger.warning(f"feedback_handler: send_feedback failed for telegram_id={telegram_id}: {e}")
        return t("feedback.error", language, error=e)

    if not result.success or result.feedback is None:
        return t("feedback.error", language, error=result.reason)

    return t("feedback.received", language, id=result.feedback.id, status=result.feedback.status)


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
        logger.warning(f"addadmin_handler: add_admin failed for target_id={target_id}: {e}")
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
        logger.warning(f"removeadmin_handler: remove_admin failed for target_id={target_id}: {e}")
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
    except Exception as e:
        logger.warning(f"system_handler: get_system_status failed: {e}")
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

    Phase 47 audit fix: AdminService.broadcast() is async now (it used
    to wrap its own asyncio.run() call, which crashed with "asyncio.run()
    cannot be called from a running event loop" when invoked from here --
    this handler already runs inside platform_layer/telegram/polling.py's event loop).
    Must be awaited, not called synchronously.
    """
    message = (args or "").strip()
    if not message:
        return "Usage: /broadcast MESSAGE"

    try:
        result = await AdminService().broadcast(message)
    except Exception as e:
        # message content intentionally not logged (Phase 51 privacy rule)
        logger.warning(f"broadcast_handler: broadcast failed: {e}")
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
        logger.warning(f"stats_handler: get_statistics failed: {e}")
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
        logger.warning(f"users_handler: get_user_summary failed: {e}")
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
        "New:\n"
        f"{summary.new}\n\n"
        "Banned:\n"
        f"{summary.banned}\n\n"
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
        logger.warning(f"userinfo_handler: get_profile failed for target_id={target_id}: {e}")
        return f"Could not load user info: {e}"

    if not result.success or result.profile is None:
        return "User not found."

    p = result.profile

    try:
        sub_result = SubscriptionService().get_subscription(target_id)
        sub = sub_result.subscription if sub_result.success else None
    except Exception as e:
        logger.warning(f"userinfo_handler: get_subscription failed for target_id={target_id}: {e}")
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
        "Status:\n"
        f"{p.status}\n\n"
        "Last activity:\n"
        f"{p.last_activity or 'N/A'}\n\n"
        "Created:\n"
        f"{p.created_at}\n\n"
        "Notifications:\n"
        f"{'On' if p.notifications_enabled else 'Off'}"
    )


async def vipinfo_handler() -> str:
    """/vipinfo -> foundation only. No VIP tier exists on top of the Phase 42 plan/subscription system."""
    return "VIP system not enabled."


async def feedbacks_handler() -> str:
    """
    /feedbacks -> AdminService.get_feedback(). ADMIN or OWNER. Never
    raises.
    """
    try:
        result = AdminService().get_feedback()
    except Exception as e:
        logger.warning(f"feedbacks_handler: get_feedback failed: {e}")
        return f"Could not load feedback: {e}"

    if not result.success:
        return f"Could not load feedback: {result.reason}"

    if not result.feedback_list:
        return "📩 Feedback List\n\nNo feedback yet."

    lines = ["📩 Feedback List"]
    for item in result.feedback_list:
        lines.append(
            f"\n#{item.id}\n\n"
            "User:\n"
            f"{item.telegram_id}\n\n"
            "Message:\n"
            f"{item.message}\n\n"
            "Status:\n"
            f"{item.status}\n\n"
            "Date:\n"
            f"{item.created_at}"
        )
    return "\n".join(lines)


async def ai_status_handler() -> str:
    """/ai_status -> platform_layer.telegram.owner.ai_commands.ai_status(). OWNER only. Never raises (ai_status() itself never raises)."""
    return ai_status().message


async def ai_provider_handler(args=None) -> str:
    """/ai_provider CAPABILITY -> platform_layer.telegram.owner.ai_commands.ai_provider(). OWNER only. Never raises."""
    capability_name = _first_arg(args)
    if capability_name is None:
        return "Usage: /ai_provider CAPABILITY"

    capability = resolve_capability(capability_name)
    if capability is None:
        return f"Unknown capability: {capability_name}"

    return ai_provider(capability).message


async def ai_cost_handler() -> str:
    """/ai_cost -> platform_layer.telegram.owner.ai_commands.ai_cost(). OWNER only. Never raises."""
    return ai_cost({}).message


async def ai_usage_handler(args=None) -> str:
    """/ai_usage TELEGRAM_ID -> platform_layer.telegram.owner.ai_commands.ai_usage(). OWNER only. Never raises."""
    target_id = _first_arg(args)
    if target_id is None:
        return "Usage: /ai_usage TELEGRAM_ID"

    return ai_usage(target_id, {}).message


async def ai_health_handler() -> str:
    """/ai_health -> platform_layer.telegram.owner.ai_commands.ai_health(). OWNER only. Never raises."""
    return ai_health().message


async def ai_explanation_status_handler() -> str:
    """/ai_explanation_status -> platform_layer.telegram.owner.ai_commands.ai_explanation_status() (Phase 63.1 TASK 7). OWNER only. Never raises."""
    return ai_explanation_status().message


async def owner_handler() -> str:
    """/owner -> platform_layer.telegram.owner.dashboard.get_owner_summary(). OWNER only. Never raises."""
    return get_owner_summary().message


async def doctor_handler() -> str:
    """/doctor -> platform_layer.telegram.owner.dashboard.get_doctor_report(). OWNER only. Never raises."""
    return get_doctor_report().message


async def owner_status_handler() -> str:
    """
    /owner_status -> platform_layer.telegram.owner.monitoring_commands.get_status_report()
    (GoldBot Core Owner Monitoring Alpha). Named `owner_status` rather
    than the brief's own literal `/status` -- `/status` is already a
    live, public, USER-level command (`status_handler` above, "GoldBot
    is running.", `platform_layer.telegram.commands.COMMANDS["status"]`) and command
    names are never renamed/reused (Article 9). OWNER only. Never
    raises.
    """
    return get_status_report().message


async def health_handler() -> str:
    """/health -> platform_layer.telegram.owner.monitoring_commands.get_health_report() (reuses platform_layer.telegram.owner.system_commands.get_system_health(), GoldBot Core Owner Monitoring Alpha). OWNER only. Never raises."""
    return get_health_report().message


async def market_handler() -> str:
    """/market -> platform_layer.telegram.owner.monitoring_commands.get_market_report() (GoldBot Core Owner Monitoring Alpha). OWNER only. Never raises."""
    return get_market_report().message


async def signals_handler() -> str:
    """/signals -> platform_layer.telegram.owner.monitoring_commands.get_signals_report() (GoldBot Core Owner Monitoring Alpha). OWNER only. Never raises."""
    return get_signals_report().message


async def errors_handler() -> str:
    """/errors -> platform_layer.telegram.owner.monitoring_commands.get_errors_report() (GoldBot Core Owner Monitoring Alpha). OWNER only. Never raises."""
    return get_errors_report().message


async def pipeline_handler() -> str:
    """/pipeline -> platform_layer.telegram.owner.monitoring_commands.get_pipeline_report() (GoldBot Core Owner Monitoring Alpha). OWNER only. Never raises."""
    return get_pipeline_report().message


async def report_handler() -> str:
    """/report -> platform_layer.telegram.owner.monitoring_commands.get_daily_report() (GoldBot Core Owner Monitoring Alpha). OWNER only. Never raises."""
    return get_daily_report().message


async def performance_handler() -> str:
    """/performance -> platform_layer.telegram.owner.monitoring_commands.get_performance_report() (Phase B.0 TASK 7 -- pure counters, Owner-gated by enable_owner_monitoring). OWNER only. Never raises."""
    return get_performance_report().message


async def runtime_handler() -> str:
    """/runtime -> platform_layer.telegram.owner.runtime_commands.runtime_status(). OWNER only. Never raises."""
    return runtime_status().message


async def runtime_events_handler() -> str:
    """/runtime_events -> platform_layer.telegram.owner.runtime_commands.runtime_events(). OWNER only. Never raises."""
    return runtime_events().message


async def runtime_metrics_handler() -> str:
    """/runtime_metrics -> platform_layer.telegram.owner.runtime_commands.runtime_metrics(). OWNER only. Never raises."""
    return runtime_metrics().message


async def runtime_status_handler() -> str:
    """/runtime_status -> platform_layer.telegram.owner.runtime_commands.runtime_full_status(). OWNER only. Never raises."""
    return runtime_full_status().message


async def runtime_check_handler() -> str:
    """/runtime_check -> platform_layer.telegram.owner.runtime_commands.runtime_check(). OWNER only. Never raises."""
    return runtime_check().message


async def runtime_restart_handler(telegram_id) -> str:
    """/runtime_restart -> platform_layer.telegram.owner.runtime_commands.runtime_restart(). OWNER only (checked again inside runtime_restart itself via require_role). Never raises."""
    return runtime_restart(telegram_id).message


async def runtime_provider_handler(args=None) -> str:
    """/runtime_provider PROVIDER -> platform_layer.telegram.owner.runtime_commands.runtime_provider(). OWNER only. Never raises."""
    provider_name = _first_arg(args)
    if provider_name is None:
        return "Usage: /runtime_provider PROVIDER"

    return runtime_provider(provider_name).message


# Phase 1.6 -- UserService.register_phone()'s two known failure
# reasons, mapped to localized catalog keys so contact_handler never
# echoes UserService's raw (always-English) reason string back to the
# caller. An unrecognized reason (future service change) falls back to
# the generic contact.error text rather than leaking raw English.
_CONTACT_FAILURE_KEYS = {
    "User not found -- send /start first": "contact.not_registered",
    "This phone number is already registered on another account.": "contact.phone_reused",
}


async def contact_handler(telegram_id, phone_number: str) -> str:
    """
    Phone Share Button reply -> UserService.register_phone() (Phase
    61.5 TASK 4). Called from telegram.command_router.route_contact(),
    not from the normal /command dispatch table (a contact message has
    no `.text`, so it never reaches route_command()/_ALL_COMMANDS at
    all). USER-level, no permission tier -- never raises.

    V2 Phase 3 (Registration Wizard): a successful phone registration
    is also the Wizard's completion trigger -- RegistrationService.
    complete() is called best-effort (a failure here never changes
    this handler's reply; the Wizard simply stays at its current step
    and the next /start re-offers it, same resilience posture as every
    other best-effort call in this file).
    """
    language = _current_language(telegram_id)
    try:
        result = UserService().register_phone(telegram_id, phone_number)
    except Exception as e:
        logger.warning(f"contact_handler: register_phone failed for telegram_id={telegram_id}: {e}")
        return t("contact.error", language)

    if not result.success:
        key = _CONTACT_FAILURE_KEYS.get(result.reason, "contact.error")
        return t(key, language)

    try:
        RegistrationService().complete(telegram_id)
    except Exception as e:
        logger.warning(f"contact_handler: registration complete failed for telegram_id={telegram_id}: {e}")

    if result.trial_active:
        return t("contact.trial_active", language, expires=result.trial_expires_at)
    return t("contact.trial_ended", language)


async def ask_handler(telegram_id=None, args=None) -> str:
    """/ask <savol> -> Personal AI Core, Memory-First (FLOW-017 Production
    Wiring). OWNER only (command_router gates OWNER_COMMANDS to OWNER).
    Never raises.

    Memory-first (Director order): Memory is checked first; the External
    AI API is called ONLY on a memory miss; the answer is then stored for
    reuse. Composes ai_layer.personal_ai.interaction_manager.memory_first_query
    (a composition root over the existing ConversationEngine + MemoryRuntime
    + Owner-Mode gate) -- no new AI/memory logic here."""
    question = (args or "").strip()
    if not question:
        return "Savolingizni yozing: /ask <savol>"
    try:
        from ai_layer.personal_ai.interaction_manager.memory_first_query import answer_question
        from ai_layer.ai_service.access.permissions import AIRole
        result = answer_question(
            question,
            role=AIRole.OWNER,
            telegram_id=str(telegram_id) if telegram_id is not None else None,
        )
    except Exception as e:
        logger.warning(f"ask_handler: personal AI failed: {e}")
        return "Personal AI hozircha javob bera olmadi."
    if result.source == "denied":
        return (
            "🔒 Personal AI hozircha o'chirilgan. Uni Owner Mode'da "
            "`enable_personal_ai` bayrog'i orqali yoqing."
        )
    if not result.accepted:
        return f"🤖 AI hozircha javob bera olmadi ({result.reason})."
    tag = "🧠 Xotiradan" if result.from_memory else "🤖 AI"
    return f"{tag}:\n\n{result.answer}"
