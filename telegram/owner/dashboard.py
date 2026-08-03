"""
Telegram Layer — Owner Dashboard (Phase 59.8: Owner Control Center;
extended Phase 61.5 Addendum -- `get_owner_summary()`/
`get_doctor_report()`, real and LIVE-WIRED via `/owner`/`/doctor`, per
Director review of Phase 61.5). Same "real function" posture as every
other module in this package -- see provider_commands.py's own
docstring.

get_dashboard() is the future `/dashboard` command's payload -- one
consolidated overview, composing this package's own already-built
pieces (no new health/status/provider logic is written here):
    telegram.owner.status_commands.get_system_status()      -- system/pipeline/database/provider/mode/last-signal
    telegram.owner.control_commands.get_feature_states()     -- runtime feature ON/OFF count
    telegram.owner.provider_commands.list_providers()        -- every registered provider's availability

get_owner_summary() (`/owner`) is a second, compact key-value panel --
a different shape than get_dashboard()'s concatenated text blocks, so
it is a new function rather than a reformat of that one. Composes
already-existing service calls only:
    telegram.admin_service.AdminService.get_system_status()/get_user_summary()
    telegram.owner.ai_commands.ai_runtime_online()/current_provider_for()  (Phase 61.5 Addendum)
    telegram.owner.ai_commands.ai_cost()                                   (Phase 61.4 TASK 6)
    database.subscription_repository.SubscriptionRepository.count_by_plan()  (new, Phase 61.5 Addendum)
    database.signal_repository.SignalRepository.count_signals_today()/get_closed_signals_today()  (new, Phase 61.5 Addendum)
    analytics.strategy_report.compute_win_rate()                           (Phase 59.4)
    core_layer.emergency.emergency_manager.EmergencyManager.get_status()         (Phase 59.9)

get_doctor_report() (`/doctor`) is a self-diagnostic: nine subsystem
reachability checks, each independently wrapped so one failing check
never hides the rest. "Scheduler" has no in-process object to query in
this codebase (`core/pipeline.py`'s own docstring: GoldBot is "a
scheduled, one-shot pipeline run" -- scheduling is external, e.g. cron
or GitHub Actions) -- reported as "N/A (external scheduler)" rather
than a fabricated ✓/✗.
"""

from ai.cache.response_cache import ResponseCache
from ai.capabilities.capability import Capability
from analytics.strategy_report import compute_win_rate
from core_layer.emergency.emergency_manager import EmergencyManager
from core_layer.emergency.emergency_state import EmergencyState
from core_layer.logger.logger import setup_logger
from database.audit_log_repository import AuditLogRepository
from database.learning_repository import LearningRepository
from database.signal_repository import SignalRepository
from database.subscription_repository import SubscriptionRepository
from telegram.admin_service import AdminService
from telegram.owner.ai_commands import ai_cost, ai_runtime_online, current_provider_for
from telegram.owner.control_commands import get_feature_states
from telegram.owner.provider_commands import ProviderCommandResult, list_providers
from telegram.owner.status_commands import get_system_status

logger = setup_logger("Dashboard")


def get_dashboard() -> ProviderCommandResult:
    """
    Never raises: each composed section catches its own errors already
    (every function above is itself "never raises, success=False on
    failure") -- a single section failing degrades that section's own
    text rather than failing the whole dashboard.
    """
    try:
        sections = []

        status_result = get_system_status()
        sections.append(status_result.message if status_result.success else f"System status unavailable: {status_result.message}")

        features_result = get_feature_states()
        if features_result.success:
            on_count = sum(1 for line in features_result.message.splitlines() if line.rstrip().endswith("ON"))
            total_count = len(features_result.message.splitlines())
            sections.append(f"Features: {on_count}/{total_count} ON")
        else:
            sections.append(f"Features unavailable: {features_result.message}")

        providers_result = list_providers()
        sections.append("Providers:\n" + providers_result.message if providers_result.success else f"Providers unavailable: {providers_result.message}")

        return ProviderCommandResult(success=True, message="\n\n".join(sections))
    except Exception as e:
        logger.warning(f"get_dashboard failed: {e}")
        return ProviderCommandResult(success=False, message=f"Error: {e}")


def get_owner_summary() -> ProviderCommandResult:
    """
    The `/owner` command's payload (Phase 61.5 Addendum) -- a single
    compact panel, the Director's own worked example shape. Each
    section degrades independently on failure (never raises, never
    fabricates a number) -- one unavailable section reports "N/A" for
    just that field rather than failing the whole panel.

    "Premium" sums PREMIUM + VIP subscriptions (both paid tiers) --
    documented here since the Director's own mockup shows a single
    "Premium" line, not two. "Cost Today" reuses `ai_cost({})`'s own
    existing "no live audit source yet" honesty (Phase 61.4/61.5
    TASK 3) -- reports $0.00 until a future phase wires a real `ai/
    audit/` data source into this panel, never a fabricated figure.
    """
    try:
        admin_status = AdminService().get_system_status()
        system_healthy = admin_status.database == "OK" and admin_status.telegram == "OK" and admin_status.market_data == "OK"

        ai_online = ai_runtime_online()
        current_provider = current_provider_for(Capability.ANALYSIS)

        user_summary_result = AdminService().get_user_summary()
        total_users = user_summary_result.user_summary.total if user_summary_result.success else "N/A"

        try:
            subscription_repository = SubscriptionRepository()
            premium_count = subscription_repository.count_by_plan("PREMIUM") + subscription_repository.count_by_plan("VIP")
        except Exception as e:
            logger.warning(f"get_owner_summary: premium count failed: {e}")
            premium_count = "N/A"

        try:
            signal_repository = SignalRepository()
            signals_today = signal_repository.count_signals_today()
            closed_today = signal_repository.get_closed_signals_today()
            win_count = sum(1 for s in closed_today if s.get("result") == "WIN")
            loss_count = sum(1 for s in closed_today if s.get("result") == "LOSS")
            win_rate = f"{compute_win_rate(win_count, loss_count) * 100:.0f}%" if (win_count + loss_count) else "N/A"
        except Exception as e:
            logger.warning(f"get_owner_summary: signal stats failed: {e}")
            signals_today = "N/A"
            win_rate = "N/A"

        cost_result = ai_cost({})
        cost_today = cost_result.message.splitlines()[-1].replace("Total:", "").strip() if cost_result.success else "N/A"

        try:
            emergency_state = EmergencyManager().get_status().state
            emergency_label = "OFF" if emergency_state == EmergencyState.NORMAL else "ON"
        except Exception as e:
            logger.warning(f"get_owner_summary: emergency status failed: {e}")
            emergency_label = "N/A"

        lines = [
            "══════════════════════",
            "GoldBot Owner Dashboard",
            "══════════════════════",
            "System:",
            "🟢 Healthy" if system_healthy else "🔴 Degraded",
            "AI:",
            "🟢 Online" if ai_online else "🔴 Offline",
            "Provider:",
            current_provider.title() if current_provider else "None",
            "Users:",
            str(total_users),
            "Premium:",
            str(premium_count),
            "Signals Today:",
            str(signals_today),
            "Win Rate:",
            str(win_rate),
            "Cost Today:",
            str(cost_today),
            "Emergency:",
            emergency_label,
            "══════════════════════",
        ]
        return ProviderCommandResult(success=True, message="\n".join(lines))
    except Exception as e:
        logger.warning(f"get_owner_summary failed: {e}")
        return ProviderCommandResult(success=False, message=f"Error: {e}")


def get_doctor_report() -> ProviderCommandResult:
    """
    The `/doctor` command's payload (Phase 61.5 Addendum) -- nine
    subsystem reachability checks, each wrapped independently so one
    failing check never hides the rest. Never a live network call and
    never a heavy query -- each check is either an existing
    lightweight status field (Database/Market Data/Telegram, from
    `AdminService.get_system_status()`) or a cheap construction/
    reachability probe (Learning/Cache/Audit), matching this file's
    own "compose already-built pieces" convention.

    "Scheduler" has no in-process object to query in this codebase
    (GoldBot's own scheduling is external -- see this module's
    docstring) -- reported "N/A" rather than a fabricated ✓/✗.
    """
    try:
        admin_status = AdminService().get_system_status()

        def _check(label: str, ok: bool) -> str:
            return f"{'✓' if ok else '✗'} {label}"

        checks = [
            _check("Database", admin_status.database == "OK"),
            _check("AI", ai_runtime_online()),
            _check("Market Data", admin_status.market_data == "OK"),
            _check("Telegram", admin_status.telegram == "OK"),
            "◌ Scheduler (N/A -- external scheduler, no in-process instance)",
            _check("Providers", list_providers().success),
        ]

        def _reachable(construct) -> bool:
            try:
                construct()
                return True
            except Exception:
                return False

        checks.append(_check("Learning", _reachable(LearningRepository)))
        checks.append(_check("Cache", _reachable(ResponseCache)))
        checks.append(_check("Audit", _reachable(AuditLogRepository)))

        all_healthy = all(line.startswith("✓") for line in checks if line.startswith(("✓", "✗")))
        status_label = "Healthy" if all_healthy else "Degraded"

        lines = ["System"] + checks + ["Status:", status_label]
        return ProviderCommandResult(success=True, message="\n".join(lines))
    except Exception as e:
        logger.warning(f"get_doctor_report failed: {e}")
        return ProviderCommandResult(success=False, message=f"Error: {e}")
