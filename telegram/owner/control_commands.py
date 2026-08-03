"""
Telegram Layer — Owner Control Commands (Phase 59.8: Owner Control
Center). Same "real function, not live-wired" posture as every other
module in this package -- see provider_commands.py's own docstring.

A thin telegram-facing wrapper over configuration/runtime_api.py
(Phase 59.7) -- this module writes no toggle/validation/audit/
snapshot logic of its own, it only reformats RuntimeApiResult into the
ProviderCommandResult shape this package's other modules already use,
and renders the ON/OFF text this task's own worked example names:

    ENABLE_AI       ON
    ENABLE_MT5      OFF
    ENABLE_BACKTEST ON
    ENABLE_NEWS     ON

Infrastructure names only, as of Phase 60.9 (Runtime Registry
Separation) -- Trading-pipeline gates (formerly ENABLE_SIGNALS/
ENABLE_AI-uppercase/ENABLE_EXECUTION/ENABLE_DATABASE/ENABLE_RISK/
ENABLE_DECISION) no longer exist in the registry this function reads;
see docs/FEATURE_REGISTRY_SEPARATION.md.

Deliberately named get_feature_states() here, not list_features() --
telegram/owner/feature_commands.py (Phase 59.3) already has a
list_features() reporting the older, static Config/FeatureFlags text
view. This module's get_feature_states() reports the newer, Phase
59.7 *runtime* view (configuration.runtime_api.list_runtime_features())
instead -- a different function for a different question, not a
same-named competing implementation.
"""

from typing import Optional

from core_layer.configuration.runtime_api import disable_feature as _runtime_disable_feature
from core_layer.configuration.runtime_api import enable_feature as _runtime_enable_feature
from core_layer.configuration.runtime_api import list_runtime_features
from telegram.owner.provider_commands import ProviderCommandResult
from core_layer.logger.logger import setup_logger

logger = setup_logger("ControlCommands")


def get_feature_states() -> ProviderCommandResult:
    """The future `/features` command's payload -- one `NAME  ON/OFF` line per feature known to configuration.runtime_feature_manager.RuntimeFeatureManager."""
    try:
        api_result = list_runtime_features()
        if not api_result.success:
            return ProviderCommandResult(success=False, message=api_result.message)

        lines = [
            f"{entry['feature']}  {'ON' if entry['state'] == 'ACTIVE' else 'OFF'}"
            for entry in api_result.data.get("features", [])
        ]
        return ProviderCommandResult(success=True, message="\n".join(lines) if lines else "No features known.")
    except Exception as e:
        logger.warning(f"get_feature_states failed: {e}")
        return ProviderCommandResult(success=False, message=f"Error: {e}")


def enable_feature(name: str, actor: Optional[str] = None, reason: Optional[str] = None) -> ProviderCommandResult:
    """The future `/feature enable <name>` command's payload -- wraps configuration.runtime_api.enable_feature() (validated, persisted, audited, snapshotted -- see that module's own docstring)."""
    try:
        api_result = _runtime_enable_feature(name, actor=actor, reason=reason)
        return ProviderCommandResult(success=api_result.success, message=api_result.message)
    except Exception as e:
        logger.warning(f"enable_feature failed: {e}")
        return ProviderCommandResult(success=False, message=f"Error: {e}")


def disable_feature(name: str, actor: Optional[str] = None, reason: Optional[str] = None) -> ProviderCommandResult:
    """The future `/feature disable <name>` command's payload -- wraps configuration.runtime_api.disable_feature()."""
    try:
        api_result = _runtime_disable_feature(name, actor=actor, reason=reason)
        return ProviderCommandResult(success=api_result.success, message=api_result.message)
    except Exception as e:
        logger.warning(f"disable_feature failed: {e}")
        return ProviderCommandResult(success=False, message=f"Error: {e}")
