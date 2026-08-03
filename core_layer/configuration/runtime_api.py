"""
Configuration Layer — Runtime Feature Public API (Phase 59.7: Runtime
Feature Toggle Center, TASK 9).

Service-layer functions wrapping configuration.runtime_feature_manager.RuntimeFeatureManager
-- the shape a future Phase 59.8 Owner Dashboard command handler would
call. "Telegram hali ulanmaydi" per this task's own brief: nothing
here imports telegram/, and no Telegram command is registered against
these functions in this phase. Each function constructs its own
default RuntimeFeatureManager() when none is supplied (injectable for
tests, same optional-dependency convention as
telegram/owner/*_commands.py's own repository-construction pattern) --
this module intentionally does not depend on telegram/ at all, keeping
the existing one-directional telegram/ -> configuration/ dependency
(never reversed).
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from core_layer.configuration.runtime_feature_manager import RuntimeFeatureManager
from core_layer.logger.logger import setup_logger

logger = setup_logger("RuntimeApi")


@dataclass(frozen=True)
class RuntimeApiResult:
    """Never raises to a caller -- every function below catches its own exceptions and returns success=False with a message instead, matching telegram/owner/provider_commands.ProviderCommandResult's own "structured result, never propagate" convention (not reused directly -- this module has no telegram/ dependency)."""
    success: bool
    message: str
    data: Dict[str, Any] = field(default_factory=dict)


def enable_feature(
    name: str, actor: Optional[str] = None, reason: Optional[str] = None,
    manager: Optional[RuntimeFeatureManager] = None,
) -> RuntimeApiResult:
    """The future Owner Dashboard's `/feature enable <name>` payload. Never raises: a dependency-validation rejection is a normal, structured RuntimeApiResult(success=False, ...), not an exception."""
    try:
        mgr = manager or RuntimeFeatureManager()
        result = mgr.enable_feature(name, changed_by=actor, reason=reason)
        if result.success:
            return RuntimeApiResult(success=True, message=f"{name} enabled.", data={"feature": name, "enabled": True})
        return RuntimeApiResult(success=False, message=result.reason or f"{name} could not be enabled.", data={"feature": name})
    except Exception as e:
        logger.warning(f"enable_feature failed: {e}")
        return RuntimeApiResult(success=False, message=f"Error: {e}")


def disable_feature(
    name: str, actor: Optional[str] = None, reason: Optional[str] = None,
    manager: Optional[RuntimeFeatureManager] = None,
) -> RuntimeApiResult:
    """The future Owner Dashboard's `/feature disable <name>` payload. Never raises."""
    try:
        mgr = manager or RuntimeFeatureManager()
        result = mgr.disable_feature(name, changed_by=actor, reason=reason)
        if result.success:
            return RuntimeApiResult(success=True, message=f"{name} disabled.", data={"feature": name, "enabled": False})
        return RuntimeApiResult(success=False, message=result.reason or f"{name} could not be disabled.", data={"feature": name})
    except Exception as e:
        logger.warning(f"disable_feature failed: {e}")
        return RuntimeApiResult(success=False, message=f"Error: {e}")


def feature_status(name: str, manager: Optional[RuntimeFeatureManager] = None) -> RuntimeApiResult:
    """The future Owner Dashboard's `/feature status <name>` payload -- wraps RuntimeFeatureManager.get_feature_state()'s own dict shape. Never raises; an unknown name is a normal success=False result, not an exception."""
    try:
        mgr = manager or RuntimeFeatureManager()
        state = mgr.get_feature_state(name)
        if state is None:
            return RuntimeApiResult(success=False, message=f"{name} is not a known feature.")
        return RuntimeApiResult(success=True, message=f"{name}: {state['state']}", data=state)
    except Exception as e:
        logger.warning(f"feature_status failed: {e}")
        return RuntimeApiResult(success=False, message=f"Error: {e}")


def list_runtime_features(manager: Optional[RuntimeFeatureManager] = None) -> RuntimeApiResult:
    """The future Owner Dashboard's `/features` payload -- every feature's current runtime state, via RuntimeFeatureManager.list_features()/get_feature_state()."""
    try:
        mgr = manager or RuntimeFeatureManager()
        states: List[Dict[str, Any]] = [mgr.get_feature_state(state.name) for state in mgr.list_features()]
        lines = [f"{s['feature']}: {s['state']} ({s['source']})" for s in states]
        return RuntimeApiResult(success=True, message="\n".join(lines) if lines else "No features known.", data={"features": states})
    except Exception as e:
        logger.warning(f"list_runtime_features failed: {e}")
        return RuntimeApiResult(success=False, message=f"Error: {e}")
