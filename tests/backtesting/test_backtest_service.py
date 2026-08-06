"""FLOW-018 Backtesting Engine -- Production Wiring tests.

Unit + Integration + End-to-End for the Backtesting Service and its live
Telegram consumer (`/backtest`). The engine is exercised through the real
BacktestEngine over a real SQLite DB (tests/conftest.py's autouse
fresh_database fixture) for the integration path, and through an injected
fake engine for deterministic service-layer unit tests.
"""

import asyncio
from datetime import datetime, timedelta, timezone

from backtesting_layer.backtest_service.backtest_service import (
    BacktestOutcome,
    BacktestRequest,
    BacktestService,
    get_backtest_service,
    parse_backtest_request,
)
from backtesting_layer.backtest_report.backtest_result import BacktestResult
from database_layer.market_repository.raw_candle_models import create_raw_candle
from database_layer.market_repository.raw_candle_repository import RawCandleRepository


def _seed_candles(n=250):
    repo = RawCandleRepository()
    base = datetime(2026, 1, 1, tzinfo=timezone.utc)
    for i in range(n):
        repo.save_candle(create_raw_candle(
            symbol="XAUUSD", timeframe="M15",
            timestamp=base + timedelta(minutes=15 * i),
            open=2000.0, high=2005.0, low=1995.0, close=2001.0,
            provider="twelvedata",
        ))
    return base + timedelta(minutes=15 * (n - 1))


class FakeEngine:
    """Stand-in for BacktestEngine -- returns a canned BacktestResult so
    the service layer can be tested without touching candle data."""

    def __init__(self, config):
        self.config = config

    def run(self):
        return BacktestResult(
            symbol=self.config.symbol, timeframe=self.config.timeframe,
            candles_processed=42, signals_generated=3, trades_opened=1,
        )


# --- Unit -----------------------------------------------------------------
def test_parse_valid_request():
    req, err = parse_backtest_request("XAUUSD M15 2026-01-01 2026-02-01")
    assert err is None
    assert isinstance(req, BacktestRequest)
    assert req.symbol == "XAUUSD" and req.timeframe == "M15"
    assert req.start == datetime(2026, 1, 1, tzinfo=timezone.utc)
    assert req.end == datetime(2026, 2, 1, tzinfo=timezone.utc)


def test_parse_lowercases_are_normalized():
    req, err = parse_backtest_request("xauusd m15 2026-01-01 2026-02-01")
    assert err is None
    assert req.symbol == "XAUUSD" and req.timeframe == "M15"


def test_parse_too_few_args_returns_usage():
    req, err = parse_backtest_request("XAUUSD M15")
    assert req is None
    assert err is not None and "/backtest" in err


def test_parse_bad_date_returns_error():
    req, err = parse_backtest_request("XAUUSD M15 not-a-date 2026-02-01")
    assert req is None and err is not None


def test_parse_end_before_start_rejected():
    req, err = parse_backtest_request("XAUUSD M15 2026-02-01 2026-01-01")
    assert req is None and "END" in err


def test_service_run_uses_injected_engine():
    service = BacktestService(engine_factory=lambda config: FakeEngine(config))
    outcome = service.run(BacktestRequest(
        symbol="XAUUSD", timeframe="M15",
        start=datetime(2026, 1, 1, tzinfo=timezone.utc),
        end=datetime(2026, 2, 1, tzinfo=timezone.utc),
    ))
    assert isinstance(outcome, BacktestOutcome)
    assert outcome.success is True
    assert outcome.result.candles_processed == 42
    assert "XAUUSD" in outcome.message
    assert "Candles processed: 42" in outcome.message


def test_service_run_never_raises_on_engine_error():
    def boom(config):
        raise RuntimeError("engine exploded")

    outcome = BacktestService(engine_factory=boom).run(BacktestRequest(
        symbol="XAUUSD", timeframe="M15",
        start=datetime(2026, 1, 1, tzinfo=timezone.utc),
        end=datetime(2026, 2, 1, tzinfo=timezone.utc),
    ))
    assert outcome.success is False
    assert "engine exploded" in outcome.reason


def test_run_from_args_invalid_returns_usage_outcome():
    outcome = BacktestService(engine_factory=lambda c: FakeEngine(c)).run_from_args("bad")
    assert outcome.success is False
    assert "/backtest" in outcome.message


# --- Integration (real engine + real DB) ----------------------------------
def test_service_runs_real_engine_over_seeded_candles():
    end = _seed_candles(250)
    outcome = BacktestService().run(BacktestRequest(
        symbol="XAUUSD", timeframe="M15",
        start=datetime(2026, 1, 1, tzinfo=timezone.utc), end=end,
    ))
    assert outcome.success is True
    assert outcome.result.candles_processed == 250
    assert "Candles processed: 250" in outcome.message


def test_service_empty_dataset_is_success_zero_candles():
    outcome = BacktestService().run(BacktestRequest(
        symbol="NONEXISTENT", timeframe="M15",
        start=datetime(2026, 1, 1, tzinfo=timezone.utc),
        end=datetime(2026, 1, 2, tzinfo=timezone.utc),
    ))
    assert outcome.success is True
    assert outcome.result.candles_processed == 0
    assert "Candles processed: 0" in outcome.message


# --- End-to-End (live Telegram consumer) ----------------------------------
def test_backtest_command_is_registered_and_owner_only():
    from platform_layer.telegram.commands import OWNER_COMMANDS, COMMANDS
    from platform_layer.telegram import handlers
    assert "backtest" in OWNER_COMMANDS
    assert "backtest" not in COMMANDS
    assert hasattr(handlers, "backtest_handler")


def test_backtest_handler_bad_args_returns_usage():
    from platform_layer.telegram import handlers
    out = asyncio.run(handlers.backtest_handler(telegram_id=111, args=""))
    assert "/backtest" in out


def test_route_owner_backtest_runs_end_to_end():
    from platform_layer.telegram.command_router import route_command
    end = _seed_candles(250)
    end_str = end.strftime("%Y-%m-%d")
    res = asyncio.run(route_command(
        f"/backtest XAUUSD M15 2026-01-01 {end_str}", telegram_id=111, username="owner"))
    # Owner (111 per tests/conftest) reaches the Backtesting Service and
    # gets a real formatted report back through the live router chain.
    assert "Backtest natijasi" in res.text
    assert "XAUUSD" in res.text


def test_route_non_owner_backtest_permission_denied():
    from platform_layer.telegram.command_router import route_command
    res = asyncio.run(route_command(
        "/backtest XAUUSD M15 2026-01-01 2026-02-01", telegram_id=222, username="user"))
    assert "denied" in res.text.lower()


def test_shared_service_is_singleton():
    assert get_backtest_service() is get_backtest_service()
