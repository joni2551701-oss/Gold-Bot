"""
Telegram Layer — Owner Replay Commands (Phase 60.1: Historical Replay
Engine Foundation, TASK 8). Same "real function, not live-wired"
posture as every other module in this package -- see
provider_commands.py's own docstring. NOT registered into
platform_layer/telegram/commands.py, NOT called from platform_layer/telegram/command_router.py or
platform_layer/telegram/handlers.py.

A thin telegram-facing wrapper over backtesting.replay_controller.ReplayController
-- this module writes no session/engine logic of its own, it only
reformats ReplaySession/ReplayResult into this package's
ProviderCommandResult shape. One module-level default controller
holds every session in-memory for this process's lifetime (Phase 60.1
adds no session-persistence table -- a session that outlives the
process is a future, separately-approved step, same posture as
lifecycle.paper_trade.PaperTrade's own in-memory-only phase).
"""

from datetime import datetime
from typing import Optional

from backtesting_layer.replay_controller.replay_controller import ReplayController
from backtesting_layer.replay_engine.replay_models import ReplayConfig, format_replay_report
from platform_layer.telegram.owner.provider_commands import ProviderCommandResult
from core_layer.logger.logger import setup_logger

logger = setup_logger("ReplayCommands")

_default_controller = ReplayController()


def replay_start(
    symbol: str, timeframe: str, start: datetime, end: datetime,
    provider: Optional[str] = None, speed: float = 1.0,
) -> ProviderCommandResult:
    """The future `/replay_start` command's payload -- builds a ReplayConfig and starts a new session."""
    try:
        config = ReplayConfig(symbol=symbol, timeframe=timeframe, start=start, end=end, provider=provider, speed=speed)
        session = _default_controller.start(config)
        return ProviderCommandResult(success=True, message=f"session_id={session.session_id}\n" + format_replay_report(session.to_result()))
    except Exception as e:
        logger.warning(f"replay_start failed: {e}")
        return ProviderCommandResult(success=False, message=f"Error: {e}")


def replay_pause(session_id: str) -> ProviderCommandResult:
    """The future `/replay_pause` command's payload."""
    try:
        session = _default_controller.pause(session_id)
        if session is None:
            return ProviderCommandResult(success=False, message=f"Unknown session_id: {session_id}")
        return ProviderCommandResult(success=True, message=format_replay_report(session.to_result()))
    except Exception as e:
        logger.warning(f"replay_pause failed: {e}")
        return ProviderCommandResult(success=False, message=f"Error: {e}")


def replay_stop(session_id: str) -> ProviderCommandResult:
    """The future `/replay_stop` command's payload."""
    try:
        session = _default_controller.stop(session_id)
        if session is None:
            return ProviderCommandResult(success=False, message=f"Unknown session_id: {session_id}")
        return ProviderCommandResult(success=True, message=format_replay_report(session.to_result()))
    except Exception as e:
        logger.warning(f"replay_stop failed: {e}")
        return ProviderCommandResult(success=False, message=f"Error: {e}")


def replay_status(session_id: str) -> ProviderCommandResult:
    """The future `/replay_status` command's payload -- wraps replay_models.format_replay_report() (TASK 7), unmodified."""
    try:
        result = _default_controller.get_status(session_id)
        if result is None:
            return ProviderCommandResult(success=False, message=f"Unknown session_id: {session_id}")
        return ProviderCommandResult(success=True, message=format_replay_report(result))
    except Exception as e:
        logger.warning(f"replay_status failed: {e}")
        return ProviderCommandResult(success=False, message=f"Error: {e}")
