"""
Phase 59.5, TASK 7 -- platform_layer/telegram/owner/dataset_commands.py tests. Real
RawCandleRepository/SyncStateRepository (SQLite, tests/conftest.py's
autouse fresh_database fixture), no mocks.
"""

from datetime import datetime, timedelta, timezone

from database_layer.market_repository.raw_candle_models import create_raw_candle
from database_layer.market_repository.raw_candle_repository import RawCandleRepository
from database_layer.market_repository.sync_state_repository import SyncStateRepository
from platform_layer.telegram.owner.dataset_commands import (
    get_dataset_status,
    get_history_status,
    get_provider_compare,
    get_sync_status,
)
from platform_layer.telegram.owner.provider_commands import ProviderCommandResult


def _candle(symbol, timeframe, ts, provider="twelvedata", close=2001.0):
    return create_raw_candle(
        symbol=symbol, timeframe=timeframe, timestamp=ts,
        open=2000.0, high=2005.0, low=1995.0, close=close, provider=provider,
    )


# --- get_dataset_status ---

def test_get_dataset_status_empty_never_raises():
    repo = RawCandleRepository()
    result = get_dataset_status("XAUUSD", "M15", raw_candle_repository=repo)

    assert isinstance(result, ProviderCommandResult)
    assert result.success is True
    assert "Candles: 0" in result.message


def test_get_dataset_status_reports_stored_candles():
    repo = RawCandleRepository()
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    repo.save_candles([_candle("XAUUSD", "M15", start + i * timedelta(minutes=15)) for i in range(5)])

    result = get_dataset_status("XAUUSD", "M15", raw_candle_repository=repo)

    assert "Candles: 5" in result.message


# --- get_history_status ---

def test_get_history_status_empty_reports_zero():
    repo = RawCandleRepository()
    result = get_history_status("XAUUSD", "M15", raw_candle_repository=repo)

    assert result.success is True
    assert "Candles: 0" in result.message
    assert "Oldest: N/A" in result.message


def test_get_history_status_reports_oldest_and_newest():
    repo = RawCandleRepository()
    t1 = datetime(2026, 1, 1, tzinfo=timezone.utc)
    t2 = datetime(2026, 1, 2, tzinfo=timezone.utc)
    repo.save_candles([_candle("XAUUSD", "M15", t1), _candle("XAUUSD", "M15", t2)])

    result = get_history_status("XAUUSD", "M15", raw_candle_repository=repo)

    assert "Candles: 2" in result.message
    assert t1.isoformat() in result.message
    assert t2.isoformat() in result.message


# --- get_sync_status ---

def test_get_sync_status_reports_no_state_when_absent():
    sync_repo = SyncStateRepository()
    result = get_sync_status("twelvedata", "XAUUSD", "M15", sync_state_repository=sync_repo)

    assert result.success is True
    assert "no sync state yet" in result.message


def test_get_sync_status_reports_last_timestamp():
    sync_repo = SyncStateRepository()
    ts = datetime(2026, 1, 1, tzinfo=timezone.utc)
    sync_repo.update_sync_state("twelvedata", "XAUUSD", "M15", ts)

    result = get_sync_status("twelvedata", "XAUUSD", "M15", sync_state_repository=sync_repo)

    assert ts.isoformat() in result.message


# --- get_provider_compare ---

def test_get_provider_compare_no_overlap_never_raises():
    repo = RawCandleRepository()
    result = get_provider_compare("XAUUSD", "M15", "twelvedata", "binance", raw_candle_repository=repo)

    assert result.success is True
    assert "No overlapping candles" in result.message


def test_get_provider_compare_reports_diff_summary():
    repo = RawCandleRepository()
    ts = datetime(2026, 1, 1, tzinfo=timezone.utc)
    repo.save_candles([
        _candle("XAUUSD", "M15", ts, provider="twelvedata", close=2001.0),
        _candle("XAUUSD", "M15", ts, provider="binance", close=2001.2),
    ])

    result = get_provider_compare("XAUUSD", "M15", "twelvedata", "binance", raw_candle_repository=repo)

    assert "Compared: 1" in result.message
    assert "Avg close diff" in result.message
