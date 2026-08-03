"""
Telegram Layer — Owner Provider Commands (Phase 59.3, TASK 5: Owner
Command Foundation).

Real, tested, standalone service-shaped functions -- NOT registered
into telegram/commands.py's OWNER_COMMANDS/ADMIN_COMMANDS dicts, NOT
wired into telegram/command_router.py's routing or telegram/handlers.py.
The live, running Telegram bot's actual command surface is completely
unaffected by this file existing -- see docs/OWNER_COMMANDS.md's own
contract for what a future implementation would still need to add
(the actual command registration + permission wiring + a real
handler calling these functions and sending the result).

Mirrors telegram/admin_service.py's own shape (a service class with
methods that never raise, each backed by a real repository/registry)
rather than inventing a new pattern.
"""

from typing import Optional

from data.providers.registry import ProviderRegistry, build_default_registry
from monitoring.provider_health import ProviderHealthStatus, check_registry_health
from core_layer.logger.logger import setup_logger

logger = setup_logger("ProviderCommands")

# The brief's own "twelve"/"binance" short names vs. this codebase's
# real get_provider_name() values ("twelvedata"/"binance") -- resolved
# here rather than requiring the owner to know the internal name
# exactly, the same "reuse real value, tolerate the brief's shorthand"
# pattern this session has used since Phase 59.1's own
# "data/twelve_data.py" -> "data/twelve_data_client.py" correction.
_NAME_ALIASES = {"twelve": "twelvedata"}


def _resolve_name(name: str) -> str:
    normalized = name.strip().lower()
    return _NAME_ALIASES.get(normalized, normalized)


class ProviderCommandResult:
    """Never raises: every function below returns one of these, matching AdminServiceResult's own "structured result, never propagate" convention."""

    def __init__(self, success: bool, message: str):
        self.success = success
        self.message = message

    def __repr__(self):
        return f"ProviderCommandResult(success={self.success}, message={self.message!r})"


def list_providers(registry: Optional[ProviderRegistry] = None) -> ProviderCommandResult:
    """
    The future /providers command's payload -- every registered
    provider's name and current availability. Never raises: an empty
    registry produces an empty (but successful) listing.
    """
    registry = registry or build_default_registry()
    try:
        names = registry.all_names()
        available = set(registry.available())
        lines = [f"{name}: {'AVAILABLE' if name in available else 'UNAVAILABLE'}" for name in names]
        return ProviderCommandResult(success=True, message="\n".join(lines) if lines else "No providers registered.")
    except Exception as e:
        logger.warning(f"list_providers failed: {e}")
        return ProviderCommandResult(success=False, message=f"Error: {e}")


def get_data_status(registry: Optional[ProviderRegistry] = None) -> ProviderCommandResult:
    """
    The future /data_status command's payload -- a full health report
    (status/latency/last-checked) per registered provider, via
    monitoring/provider_health.py's check_registry_health() (Phase
    59.2/59.3) -- not reimplemented here.
    """
    registry = registry or build_default_registry()
    try:
        reports = check_registry_health(registry)
        lines = [
            f"{r.provider_name}: {r.status.value} "
            f"(latency={r.latency_ms:.1f}ms"
            f"{', reason=' + r.reason if r.status != ProviderHealthStatus.ONLINE else ''})"
            for r in reports
        ]
        return ProviderCommandResult(success=True, message="\n".join(lines) if lines else "No providers registered.")
    except Exception as e:
        logger.warning(f"get_data_status failed: {e}")
        return ProviderCommandResult(success=False, message=f"Error: {e}")


def enable_provider(name: str) -> ProviderCommandResult:
    """
    NOT a working toggle -- disclosed honestly, matching
    docs/OWNER_COMMANDS.md's own contract: config.Config.ENABLE_MT5/
    ENABLE_TWELVEDATA are read once, at config.py import time, from
    os.getenv(). No runtime-override mechanism exists in this
    codebase today (a configuration/ settings override, or a small
    database-backed override table, would be a separate,
    explicitly-approved future step). Returns success=False with a
    clear reason rather than silently doing nothing or lying about
    success.
    """
    resolved = _resolve_name(name)
    return ProviderCommandResult(
        success=False,
        message=(
            f"Cannot enable {resolved!r} at runtime yet -- ENABLE_{resolved.upper()} is read once from "
            f"the environment at startup. See docs/OWNER_COMMANDS.md's contract for what a future "
            f"runtime-override mechanism would need."
        ),
    )


def disable_provider(name: str) -> ProviderCommandResult:
    """The disable-side mirror of enable_provider() -- same disclosed limitation, same honest, non-silent failure."""
    resolved = _resolve_name(name)
    return ProviderCommandResult(
        success=False,
        message=(
            f"Cannot disable {resolved!r} at runtime yet -- ENABLE_{resolved.upper()} is read once from "
            f"the environment at startup. See docs/OWNER_COMMANDS.md's contract for what a future "
            f"runtime-override mechanism would need."
        ),
    )
