"""
Telegram Layer — Owner Emergency Commands (Phase 59.9: Emergency Safety
Layer Foundation, TASK 7). Same "real function, not live-wired" posture
as every other module in this package -- see provider_commands.py's
own docstring. NOT registered into telegram/commands.py, NOT called
from telegram/command_router.py or telegram/handlers.py.

A thin telegram-facing wrapper over core_layer.emergency.emergency_manager.EmergencyManager
-- this module writes no state/persistence/audit logic of its own, it
only reformats EmergencyStateRecord into this package's
ProviderCommandResult shape.
"""

from typing import Optional

from core_layer.emergency.emergency_manager import EmergencyManager
from core_layer.emergency.emergency_state import EmergencyStateRecord
from telegram.owner.provider_commands import ProviderCommandResult
from core_layer.logger.logger import setup_logger

logger = setup_logger("EmergencyCommands")


def _format_record(record: EmergencyStateRecord) -> str:
    lines = [f"State: {record.state.value}"]
    if record.reason:
        lines.append(f"Reason: {record.reason}")
    return "\n".join(lines)


def kill_system(actor: Optional[str] = None, reason: Optional[str] = None) -> ProviderCommandResult:
    """The future `/panic`/`/kill` command's payload -- activates EmergencyState.KILLED, persisted + audited (KILL_ACTIVATED)."""
    try:
        record = EmergencyManager().activate_kill(reason=reason, activated_by=actor, source="owner" if actor else "system")
        return ProviderCommandResult(success=True, message=_format_record(record))
    except Exception as e:
        logger.warning(f"kill_system failed: {e}")
        return ProviderCommandResult(success=False, message=f"Error: {e}")


def pause_system(actor: Optional[str] = None, reason: Optional[str] = None) -> ProviderCommandResult:
    """The future `/pause` command's payload -- activates EmergencyState.PAUSED, persisted + audited (PAUSE_ACTIVATED)."""
    try:
        record = EmergencyManager().activate_pause(reason=reason, activated_by=actor, source="owner" if actor else "system")
        return ProviderCommandResult(success=True, message=_format_record(record))
    except Exception as e:
        logger.warning(f"pause_system failed: {e}")
        return ProviderCommandResult(success=False, message=f"Error: {e}")


def maintenance_on(actor: Optional[str] = None, reason: Optional[str] = None) -> ProviderCommandResult:
    """The future `/maintenance on` command's payload -- activates EmergencyState.MAINTENANCE, persisted + audited (MAINTENANCE_ENABLED)."""
    try:
        record = EmergencyManager().activate_maintenance(reason=reason, activated_by=actor, source="owner" if actor else "system")
        return ProviderCommandResult(success=True, message=_format_record(record))
    except Exception as e:
        logger.warning(f"maintenance_on failed: {e}")
        return ProviderCommandResult(success=False, message=f"Error: {e}")


def restore_system(actor: Optional[str] = None, reason: Optional[str] = None) -> ProviderCommandResult:
    """The future `/restore` command's payload -- activates EmergencyState.NORMAL, persisted + audited (SYSTEM_RESTORED)."""
    try:
        record = EmergencyManager().restore_normal(reason=reason, activated_by=actor, source="owner" if actor else "system")
        return ProviderCommandResult(success=True, message=_format_record(record))
    except Exception as e:
        logger.warning(f"restore_system failed: {e}")
        return ProviderCommandResult(success=False, message=f"Error: {e}")


def get_emergency_status() -> ProviderCommandResult:
    """The future `/emergency_status` command's payload -- the current EmergencyState, never raises."""
    try:
        record = EmergencyManager().get_status()
        return ProviderCommandResult(success=True, message=_format_record(record))
    except Exception as e:
        logger.warning(f"get_emergency_status failed: {e}")
        return ProviderCommandResult(success=False, message=f"Error: {e}")
