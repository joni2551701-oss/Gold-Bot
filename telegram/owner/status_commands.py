"""
Telegram Layer — Owner Status Commands (Phase 59.8: Owner Control
Center, part of `status_commands.py`). Same "real function, not
live-wired" posture as every other module in this package -- see
provider_commands.py's own docstring.

get_system_status() is the future `/system_status` command's payload,
matching this task's own worked example:

    GoldBot Status
    System: ONLINE
    Pipeline: READY
    Database: CONNECTED
    Provider: TwelveData
    Mode: VALIDATION
    Last Signal: 12 min ago

Composes only already-existing, already-tested pieces -- no new
health-check logic is written here:
    telegram.admin_service.AdminService.get_system_status()   -- database/telegram/market_data/ai reachability (Phase 41)
    data.providers.registry.build_default_registry()           -- per-provider status (Phase 59.1/59.2)
    config.Config.MARKET_DATA_PROVIDER/VALIDATION_MODE          -- the configured provider name + Phase 59 validation flag
    core_layer.system_state.system_state.SystemState                               -- the Phase 59.6 operating-mode vocabulary, reused for "Mode" only as a display label (no SystemState instance is held or mutated anywhere -- see that module's own docstring on why no holder exists yet)
    database.signal_repository.SignalRepository.get_latest_signal() -- the most recently persisted signal's timestamp
"""

from datetime import datetime, timezone

from config import Config
from core_layer.system_state.system_state import SystemState
from data.providers.registry import build_default_registry
from database.signal_repository import SignalRepository
from telegram.admin_service import AdminService
from telegram.owner.provider_commands import ProviderCommandResult
from core_layer.logger.logger import setup_logger

logger = setup_logger("StatusCommands")


def _format_time_ago(timestamp: datetime) -> str:
    """A small, self-contained "N min/hours/days ago" renderer -- no existing helper in this codebase does this generically enough to reuse (monitoring/performance.py's own age calculations are private to that module's own report shape)."""
    now = datetime.now(timezone.utc)
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)
    delta_seconds = (now - timestamp).total_seconds()
    if delta_seconds < 0:
        delta_seconds = 0

    minutes = int(delta_seconds // 60)
    if minutes < 60:
        return f"{minutes} min ago" if minutes != 1 else "1 min ago"
    hours = minutes // 60
    if hours < 24:
        return f"{hours} hour ago" if hours == 1 else f"{hours} hours ago"
    days = hours // 24
    return f"{days} day ago" if days == 1 else f"{days} days ago"


def _last_signal_text() -> str:
    """Never raises: no persisted signal, or a repository failure, both fall back to 'N/A' -- a status command must never itself error out over a missing history."""
    try:
        latest = SignalRepository().get_latest_signal()
        if not latest or not latest.get("created_at"):
            return "N/A"
        created_at = datetime.fromisoformat(latest["created_at"])
        return _format_time_ago(created_at)
    except Exception as e:
        logger.warning(f"_last_signal_text failed: {e}")
        return "N/A"


def get_system_status() -> ProviderCommandResult:
    """
    Never raises: every sub-check below is already independently
    "never raises" (AdminService.get_system_status(),
    check_registry_health() via provider_commands' own
    get_data_status() precedent) or is wrapped in its own try/except
    (_last_signal_text()) -- this function only formats their combined
    output.

    "Pipeline: READY" is a derived label, not a live pipeline dry-run
    -- READY means the configured provider (Config.MARKET_DATA_PROVIDER)
    reports available=True; core/pipeline.py itself is never
    constructed or called by this function.
    """
    try:
        admin_status = AdminService().get_system_status()
        system_label = "ONLINE" if admin_status.database == "OK" else "OFFLINE"

        registry = build_default_registry()
        provider = registry.get(Config.MARKET_DATA_PROVIDER)
        provider_available = provider.get_market_status().available if provider else False
        pipeline_label = "READY" if provider_available else "NOT READY"

        mode = SystemState.VALIDATION if Config.VALIDATION_MODE else SystemState.RUNNING

        lines = [
            "GoldBot Status",
            f"System: {system_label}",
            f"Pipeline: {pipeline_label}",
            f"Database: {'CONNECTED' if admin_status.database == 'OK' else 'DISCONNECTED'}",
            f"Provider: {Config.MARKET_DATA_PROVIDER}",
            f"Mode: {mode.value}",
            f"Last Signal: {_last_signal_text()}",
        ]
        return ProviderCommandResult(success=True, message="\n".join(lines))
    except Exception as e:
        logger.warning(f"get_system_status failed: {e}")
        return ProviderCommandResult(success=False, message=f"Error: {e}")
