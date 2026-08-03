"""
Telegram Layer — Owner Backtest Commands (Phase 60.2: Backtesting
Engine, TASK 5). Same "real function, not live-wired" posture as
every other module in this package -- see provider_commands.py's own
docstring. NOT registered into telegram/commands.py, NOT called from
telegram/command_router.py or telegram/handlers.py.

A thin telegram-facing wrapper over backtesting.backtest_engine.BacktestEngine
-- this module writes no orchestration/trading logic of its own, it
only reformats BacktestResult into this package's ProviderCommandResult
shape via backtesting.backtest_result.format_backtest_report().
"""

from datetime import datetime
from typing import Optional

from backtesting.backtest_engine import BacktestEngine
from backtesting.backtest_result import format_backtest_report
from backtesting.replay_models import ReplayConfig
from telegram.owner.provider_commands import ProviderCommandResult
from core_layer.logger.logger import setup_logger

logger = setup_logger("BacktestCommands")


def backtest_run(
    symbol: str, timeframe: str, start: datetime, end: datetime,
    provider: Optional[str] = None, speed: float = 1.0,
) -> ProviderCommandResult:
    """
    The future `/backtest_run` command's payload -- builds a
    ReplayConfig, runs a full BacktestEngine pass synchronously (see
    BacktestEngine.run()'s own docstring: it replays the whole
    configured window in one call, not step-by-step like
    replay_commands.py's session-based API), and formats the result.
    """
    try:
        config = ReplayConfig(symbol=symbol, timeframe=timeframe, start=start, end=end, provider=provider, speed=speed)
        engine = BacktestEngine(config)
        result = engine.run()
        return ProviderCommandResult(success=True, message=format_backtest_report(result))
    except Exception as e:
        logger.warning(f"backtest_run failed: {e}")
        return ProviderCommandResult(success=False, message=f"Error: {e}")
