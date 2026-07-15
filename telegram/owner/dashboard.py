"""
Telegram Layer — Owner Dashboard (Phase 59.8: Owner Control Center).
Same "real function, not live-wired" posture as every other module in
this package -- see provider_commands.py's own docstring.

get_dashboard() is the future `/dashboard` command's payload -- one
consolidated overview, composing this package's own already-built
pieces (no new health/status/provider logic is written here):
    telegram.owner.status_commands.get_system_status()      -- system/pipeline/database/provider/mode/last-signal
    telegram.owner.control_commands.get_feature_states()     -- runtime feature ON/OFF count
    telegram.owner.provider_commands.list_providers()        -- every registered provider's availability
"""

from telegram.owner.control_commands import get_feature_states
from telegram.owner.provider_commands import ProviderCommandResult, list_providers
from telegram.owner.status_commands import get_system_status
from core.logger import setup_logger

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
