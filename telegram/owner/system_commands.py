"""
Telegram Layer — Owner System Commands (Phase 59.3, TASK 5). Same
"real function, not live-wired" posture as provider_commands.py (same
package) -- see that module's own docstring.
"""

from data_layer.providers.registry import build_default_registry
from monitoring.provider_health import ProviderHealthStatus, check_registry_health
from telegram.admin_service import AdminService
from telegram.owner.provider_commands import ProviderCommandResult
from core_layer.logger.logger import setup_logger

logger = setup_logger("SystemCommands")


def get_system_health() -> ProviderCommandResult:
    """
    The future /system_health command's payload -- combines the
    pre-existing telegram.admin_service.AdminService.get_system_status()
    (database/telegram/market_data/ai/api env-key reachability, Phase
    41, reused not duplicated) with the new, richer per-provider health
    report (monitoring/provider_health.py, Phase 59.2/59.3). Distinct
    from the existing /system command (still only AdminService's own
    simpler view) -- this is a superset, not a replacement; /system
    itself is untouched by this phase.
    """
    try:
        admin_status = AdminService().get_system_status()
        provider_reports = check_registry_health(build_default_registry())

        lines = [
            f"database: {admin_status.database}",
            f"telegram: {admin_status.telegram}",
            f"market_data (legacy check): {admin_status.market_data}",
            f"ai: {admin_status.ai}",
            "",
            "Providers:",
        ]
        lines += [
            f"  {r.provider_name}: {r.status.value} (latency={r.latency_ms:.1f}ms)"
            for r in provider_reports
        ]
        return ProviderCommandResult(success=True, message="\n".join(lines))
    except Exception as e:
        logger.warning(f"get_system_health failed: {e}")
        return ProviderCommandResult(success=False, message=f"Error: {e}")


def count_online_providers() -> int:
    """A small convenience read, e.g. for a future dashboard summary line ("3/4 providers online"). Never raises: an all-OFFLINE registry returns 0."""
    try:
        reports = check_registry_health(build_default_registry())
        return sum(1 for r in reports if r.status == ProviderHealthStatus.ONLINE)
    except Exception as e:
        logger.warning(f"count_online_providers failed: {e}")
        return 0
