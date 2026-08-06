"""
Telegram Layer — Owner Backtest Commands (Phase 60.2: Backtesting
Engine, TASK 5; re-wired FLOW-018).

FLOW-018 (Production Wiring): the live `/backtest` consumer now runs
through `platform_layer/telegram/handlers.backtest_handler` ->
`backtesting_layer.backtest_service.backtest_service.BacktestService`.
This module's `backtest_run()` — the original Phase 60.2 helper — now
**delegates** to that same service instead of re-composing
ReplayConfig/BacktestEngine/format itself, so there is exactly one
place the engine is driven (CLAUDE.md "No duplicate logic"). Its
`ProviderCommandResult` shape and behaviour are unchanged for any
existing caller/test.
"""

from datetime import datetime
from typing import Optional

from backtesting_layer.backtest_service.backtest_service import BacktestRequest, BacktestService
from platform_layer.telegram.owner.provider_commands import ProviderCommandResult
from core_layer.logger.logger import setup_logger

logger = setup_logger("BacktestCommands")


def backtest_run(
    symbol: str, timeframe: str, start: datetime, end: datetime,
    provider: Optional[str] = None, speed: float = 1.0,
) -> ProviderCommandResult:
    """
    Runs a full BacktestEngine pass synchronously by delegating to
    BacktestService (FLOW-018) and reformats its BacktestOutcome into
    this package's ProviderCommandResult shape. No orchestration/trading
    logic of its own — the service owns the ReplayConfig->engine->format
    composition; BacktestService.run() never raises.
    """
    outcome = BacktestService().run(BacktestRequest(
        symbol=symbol, timeframe=timeframe, start=start, end=end,
        provider=provider, speed=speed,
    ))
    return ProviderCommandResult(success=outcome.success, message=outcome.message)
