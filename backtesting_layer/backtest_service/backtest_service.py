"""Backtesting Layer — Backtest Service (FLOW-018 Production Wiring).

The Director's Production Pipeline names a **Backtesting Service** layer
that sits between the Telegram Backtest Handler and the Backtesting
Engine:

    Telegram -> /backtest -> Command Router -> Backtest Handler
        -> Backtesting Service -> Backtesting Engine -> Result -> Telegram

This module is that service. It is a **composition root only**: it writes
no new Backtesting Engine, no new Statistics Engine, no new trading
logic. It composes the EXISTING, unmodified:

    backtesting_layer.backtest_engine.backtest_engine.BacktestEngine  (.run())
    backtesting_layer.replay_engine.replay_models.ReplayConfig
    backtesting_layer.backtest_report.backtest_result.format_backtest_report

Reuse note (Module Reuse Principle / CLAUDE.md): this file lands inside
the pre-existing `backtest_service` package (Foundation Freeze skeleton),
not a new top-level package. `platform_layer/telegram/owner/backtest_commands.py`
(Phase 60.2) already held the ReplayConfig->BacktestEngine.run()->format
composition but was orphaned (never wired to a router/handler/registry);
to avoid duplicate composition logic it now delegates to this service
(see that module), so there is exactly one place the engine is driven.

Tool-First (Director FLOW-018 standard): running a backtest invokes the
local **Backtesting Tool** (the engine), which reads Historical Data from
the **Database** (RawCandleRepository, via ReplayEngine) — never an
external API. This is the Director's "Backtesting Tool -> Database ->
Result. API emas." contract expressed in code: no network/API call
exists anywhere on this path.

Input Contract  : Strategy(optional) / Symbol / Timeframe / Date Range /
                  Historical Data(DB) / Configuration(provider, speed).
Output Contract : BacktestOutcome{success, message, result, reason} —
                  the BacktestResult carries Performance Summary
                  (counts + overall_win_rate), Statistics (strategy_report),
                  Trade List (performances) and the Validation Status.
Consumer        : Telegram (`backtest_handler`); future consumers
                  (Personal AI / Chart / Replay / Desktop / Web / Mobile)
                  reuse this same service, never the engine directly.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable, Optional

from backtesting_layer.backtest_engine.backtest_engine import BacktestEngine
from backtesting_layer.backtest_report.backtest_result import (
    BacktestResult,
    format_backtest_report,
)
from backtesting_layer.replay_engine.replay_models import ReplayConfig
from core_layer.logger.logger import setup_logger

logger = setup_logger("BacktestService")

_DATE_FORMATS = ("%Y-%m-%d", "%Y-%m-%dT%H:%M", "%Y-%m-%dT%H:%M:%S")

USAGE_TEXT = (
    "Foydalanish: /backtest <SYMBOL> <TIMEFRAME> <START> <END>\n"
    "Masalan: /backtest XAUUSD M15 2026-01-01 2026-02-01\n"
    "Sana formati: YYYY-MM-DD"
)


# --- Input Contract -------------------------------------------------------
@dataclass(frozen=True)
class BacktestRequest:
    """What to backtest. `strategy` is optional — the engine runs every
    registered strategy and reports each one's performance separately;
    a per-strategy filter is a future extension, not required for the
    Production chain."""

    symbol: str
    timeframe: str
    start: datetime
    end: datetime
    provider: Optional[str] = None
    speed: float = 1.0
    strategy: Optional[str] = None


# --- Output Contract ------------------------------------------------------
@dataclass(frozen=True)
class BacktestOutcome:
    """What the Telegram consumer receives. `result` is the full
    BacktestResult (Performance Summary + Statistics + Trade List +
    Equity Curve reference) on success; `message` is its formatted,
    ready-to-send text. `success=False` + `reason` on a validation or
    runtime problem — this service never raises into the handler."""

    success: bool
    message: str
    result: Optional[BacktestResult] = None
    reason: str = ""


def _parse_date(value: str) -> Optional[datetime]:
    for fmt in _DATE_FORMATS:
        try:
            return datetime.strptime(value, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return None


def parse_backtest_request(args: str) -> "tuple[Optional[BacktestRequest], Optional[str]]":
    """Parses a raw `/backtest` argument string into a BacktestRequest.

    Returns (request, None) on success, or (None, usage_error) when the
    arguments are missing/malformed — never raises. Accepts:

        SYMBOL TIMEFRAME START END  [PROVIDER]
    """
    parts = (args or "").split()
    if len(parts) < 4:
        return None, USAGE_TEXT

    symbol, timeframe, start_raw, end_raw = parts[0], parts[1], parts[2], parts[3]
    provider = parts[4] if len(parts) >= 5 else None

    start = _parse_date(start_raw)
    end = _parse_date(end_raw)
    if start is None or end is None:
        return None, f"Sana noto'g'ri.\n{USAGE_TEXT}"
    if end <= start:
        return None, "END sanasi START'dan keyin bo'lishi kerak."

    return BacktestRequest(
        symbol=symbol.upper(), timeframe=timeframe.upper(),
        start=start, end=end, provider=provider,
    ), None


class BacktestService:
    """One entry point per backtest run. Every dependency is injectable
    (same optional-dependency convention as the engine and every Phase
    59.x/60.x manager); the default `engine_factory` builds the real,
    unmodified `BacktestEngine`, so running with defaults reproduces
    exactly what the engine would decide for the same candle window."""

    def __init__(
        self,
        engine_factory: Optional[Callable[[ReplayConfig], BacktestEngine]] = None,
    ):
        self._engine_factory = engine_factory or (lambda config: BacktestEngine(config))

    def run(self, request: BacktestRequest) -> BacktestOutcome:
        """Validation -> ReplayConfig -> BacktestEngine.run() (reads
        Historical Data from the DB) -> Result -> formatted response.
        Never raises: a bad config or engine error becomes a
        `success=False` outcome, so the Telegram handler always gets a
        safe value."""
        try:
            config = ReplayConfig(
                symbol=request.symbol, timeframe=request.timeframe,
                start=request.start, end=request.end,
                provider=request.provider, speed=request.speed,
            )
            engine = self._engine_factory(config)
            result = engine.run()
        except Exception as exc:  # noqa: BLE001 - never raise into the consumer
            logger.warning(f"backtest run failed: {exc}")
            return BacktestOutcome(success=False, message=f"Backtest xatosi: {exc}",
                                   result=None, reason=str(exc))

        return BacktestOutcome(success=True, message=format_backtest_report(result),
                               result=result, reason="ok")

    def run_from_args(self, args: str) -> BacktestOutcome:
        """Parse a raw `/backtest` argument string, then run. The single
        method the Telegram handler calls — parsing + execution in one
        Tool-First step."""
        request, error = parse_backtest_request(args)
        if request is None:
            return BacktestOutcome(success=False, message=error or USAGE_TEXT,
                                   result=None, reason="invalid arguments")
        return self.run(request)


_SHARED_SERVICE: Optional[BacktestService] = None


def get_backtest_service() -> BacktestService:
    """One BacktestService per process for the live Telegram consumer."""
    global _SHARED_SERVICE
    if _SHARED_SERVICE is None:
        _SHARED_SERVICE = BacktestService()
    return _SHARED_SERVICE
