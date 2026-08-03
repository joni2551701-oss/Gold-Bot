"""
Telegram Layer — Owner Execution Commands (Phase 60.3: Execution
Simulator Foundation, TASK 7). Same "real function, not live-wired"
posture as every other module in this package -- see
provider_commands.py's own docstring. NOT registered into
telegram/commands.py, NOT called from telegram/command_router.py or
telegram/handlers.py.

A thin telegram-facing wrapper over execution_layer/execution_engine/simulator/ -- this
module writes no slippage/spread/latency logic of its own, it only
reports already-computed config and a selected simulation mode. The
selected mode is an in-memory-only holder (module-level dict), same
"no persistence yet, foundation phase" posture as
backtesting/replay_commands.py's own default controller -- it does
not survive a process restart.
"""

from typing import Dict, Optional

from execution_layer.execution_engine.simulator.simulator_engine import ExecutionSimulator
from execution_layer.execution_engine.simulator.slippage import SlippageConfig
from telegram.owner.provider_commands import ProviderCommandResult
from core_layer.logger.logger import setup_logger

logger = setup_logger("ExecutionCommands")

_DEFAULT_MODE = "DEFAULT"
_MODE_SESSIONS: Dict[str, Optional[str]] = {"DEFAULT": None, "LONDON": "LONDON", "NY_NEWS": "NY_NEWS"}
_current_mode = {"mode": _DEFAULT_MODE}


def execution_status() -> ProviderCommandResult:
    """The future `/execution_status` command's payload -- current simulator config + a reminder that live execution stays inert."""
    try:
        simulator = ExecutionSimulator()
        lines = [
            "Execution Simulator Status",
            f"Mode: {_current_mode['mode']}",
            f"Slippage: {simulator.slippage_config.points} pts (max {simulator.slippage_config.max_points})",
            f"Spread (default): {simulator.spread_config.default_points} pts (max {simulator.spread_config.max_points})",
            f"Latency: {simulator.latency_config.execution_latency_ms}ms",
            "Live execution: INERT (execution_layer/execution_engine/execution_engine.py unchanged)",
        ]
        return ProviderCommandResult(success=True, message="\n".join(lines))
    except Exception as e:
        logger.warning(f"execution_status failed: {e}")
        return ProviderCommandResult(success=False, message=f"Error: {e}")


def slippage_status() -> ProviderCommandResult:
    """The future `/slippage_status` command's payload."""
    try:
        config = SlippageConfig()
        return ProviderCommandResult(success=True, message=f"Slippage: {config.points} pts (max {config.max_points})")
    except Exception as e:
        logger.warning(f"slippage_status failed: {e}")
        return ProviderCommandResult(success=False, message=f"Error: {e}")


def set_simulation_mode(mode: str) -> ProviderCommandResult:
    """
    The future `/set_simulation_mode` command's payload -- selects
    which named session spread (`execution_layer.execution_engine.simulator.spread.SpreadConfig.session_spreads`)
    a future simulate() call should be run under. Does not itself call
    ExecutionSimulator.simulate() -- a future caller reads
    _MODE_SESSIONS[mode] and passes it as simulate()'s own `session`
    argument.
    """
    try:
        if mode not in _MODE_SESSIONS:
            return ProviderCommandResult(
                success=False,
                message=f"Unknown mode: {mode}. Valid: {', '.join(_MODE_SESSIONS)}",
            )
        _current_mode["mode"] = mode
        return ProviderCommandResult(success=True, message=f"Simulation mode set to {mode}")
    except Exception as e:
        logger.warning(f"set_simulation_mode failed: {e}")
        return ProviderCommandResult(success=False, message=f"Error: {e}")
