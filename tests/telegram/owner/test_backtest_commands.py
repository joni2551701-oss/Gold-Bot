"""
Phase 60.2, TASK 5 -- telegram/owner/backtest_commands.py tests. Real
repositories (SQLite, tests/conftest.py's autouse fresh_database
fixture) -- no mocks.
"""

from datetime import datetime, timedelta, timezone

from telegram.owner.backtest_commands import backtest_run
from telegram.owner.provider_commands import ProviderCommandResult
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


def test_backtest_run_returns_a_report():
    end = _seed_candles(250)

    result = backtest_run("XAUUSD", "M15", datetime(2026, 1, 1, tzinfo=timezone.utc), end)

    assert isinstance(result, ProviderCommandResult)
    assert result.success is True
    assert "XAUUSD" in result.message
    assert "Candles processed: 250" in result.message


def test_backtest_run_never_raises_on_empty_dataset():
    result = backtest_run("NONEXISTENT", "M15", datetime(2026, 1, 1, tzinfo=timezone.utc), datetime(2026, 1, 2, tzinfo=timezone.utc))

    assert result.success is True
    assert "Candles processed: 0" in result.message
