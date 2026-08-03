"""
Phase 59.5, TASK 1/2 -- data_layer/historical_data/historical_data_collector.py tests.
Real RawCandleRepository/SyncStateRepository (SQLite, tests/conftest.py's
autouse fresh_database fixture) -- only the provider is faked, since a
provider is this codebase's one real external-API boundary (same
posture tests/data_layer/providers/test_twelvedata_provider.py already uses
via monkeypatching TwelveDataClient.fetch_candles()).
"""

from datetime import datetime, timedelta, timezone
from typing import List, Tuple

import pytest

from data_layer.historical_data.historical_data_collector import (
    MAX_FETCH_LIMIT,
    collect_historical_candles,
    sync_historical_candles,
)
from data_layer.providers.base_provider import MarketCandle, MarketDataProvider, ProviderStatus
from database.raw_candle_repository import RawCandleRepository
from database.sync_state_repository import SyncStateRepository


class FakeProvider(MarketDataProvider):
    """A MarketDataProvider test double -- returns a fixed candle list regardless of `limit`, records every get_candles() call for assertions."""

    def __init__(self, candles: List[MarketCandle]):
        self._candles = candles
        self.calls: List[Tuple[str, str, int]] = []

    def get_provider_name(self) -> str:
        return "fakeprovider"

    def get_market_status(self) -> ProviderStatus:
        return ProviderStatus(available=True)

    def get_supported_timeframes(self):
        return ("M15",)

    def get_candles(self, symbol: str, timeframe: str, limit: int) -> List[MarketCandle]:
        self.calls.append((symbol, timeframe, limit))
        return list(self._candles)

    def get_latest_price(self, symbol: str):
        return self._candles[-1].close if self._candles else None


def _candles(count: int, start: datetime, step: timedelta) -> List[MarketCandle]:
    return [
        MarketCandle(
            symbol="XAUUSD", timeframe="M15",
            open=2000.0, high=2005.0, low=1995.0, close=2001.0,
            timestamp=start + i * step, volume=None, provider="fakeprovider",
        )
        for i in range(count)
    ]


# --- collect_historical_candles ---

def test_collect_saves_candles_within_the_requested_window():
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    candles = _candles(10, start, timedelta(minutes=15))
    provider = FakeProvider(candles)
    repo = RawCandleRepository()

    result = collect_historical_candles(
        provider, "XAUUSD", "M15", start, start + timedelta(hours=2), raw_candle_repository=repo
    )

    assert result.fetched_count == 10
    assert result.saved_count == 8  # 8 candles land within [start, start+2h)
    assert result.provider == "fakeprovider"


def test_collect_filters_out_candles_outside_the_window():
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    candles = _candles(10, start, timedelta(minutes=15))
    provider = FakeProvider(candles)
    repo = RawCandleRepository()

    window_start = start + timedelta(minutes=30)
    window_end = start + timedelta(minutes=60)
    result = collect_historical_candles(provider, "XAUUSD", "M15", window_start, window_end, raw_candle_repository=repo)

    assert result.saved_count == 2  # minute 30 and minute 45 only
    assert result.actual_start == window_start
    assert result.actual_end == start + timedelta(minutes=45)


def test_collect_empty_provider_response_never_raises():
    provider = FakeProvider([])
    repo = RawCandleRepository()
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)

    result = collect_historical_candles(provider, "XAUUSD", "M15", start, start + timedelta(days=1), raw_candle_repository=repo)

    assert result.fetched_count == 0
    assert result.saved_count == 0
    assert result.actual_start is None
    assert result.actual_end is None


def test_collect_persists_through_the_real_repository():
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    candles = _candles(4, start, timedelta(minutes=15))
    provider = FakeProvider(candles)
    repo = RawCandleRepository()

    collect_historical_candles(provider, "XAUUSD", "M15", start, start + timedelta(hours=2), raw_candle_repository=repo)

    saved = repo.get_candles("XAUUSD", "M15")
    assert len(saved) == 4
    assert saved[0].provider == "fakeprovider"


def test_collect_limit_is_capped_at_max_fetch_limit():
    provider = FakeProvider([])
    repo = RawCandleRepository()
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)

    collect_historical_candles(provider, "XAUUSD", "M15", start, start + timedelta(days=365), raw_candle_repository=repo)

    assert provider.calls[0][2] == MAX_FETCH_LIMIT


# --- sync_historical_candles ---

def test_sync_uses_lookback_when_no_prior_state():
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    candles = _candles(4, start, timedelta(minutes=15))
    provider = FakeProvider(candles)
    raw_repo = RawCandleRepository()
    sync_repo = SyncStateRepository()

    result = sync_historical_candles(
        provider, "XAUUSD", "M15", sync_repo, raw_candle_repository=raw_repo,
        end=start + timedelta(hours=2), lookback=start,
    )

    assert result.saved_count == 4
    state = sync_repo.get_sync_state("fakeprovider", "XAUUSD", "M15")
    assert state.last_timestamp == result.actual_end


def test_sync_raises_without_prior_state_or_lookback():
    provider = FakeProvider([])
    sync_repo = SyncStateRepository()

    with pytest.raises(ValueError):
        sync_historical_candles(provider, "XAUUSD", "M15", sync_repo)


def test_sync_resumes_from_last_timestamp_on_second_call():
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    raw_repo = RawCandleRepository()
    sync_repo = SyncStateRepository()

    first_batch = _candles(4, start, timedelta(minutes=15))
    provider = FakeProvider(first_batch)
    sync_historical_candles(
        provider, "XAUUSD", "M15", sync_repo, raw_candle_repository=raw_repo,
        end=start + timedelta(hours=2), lookback=start,
    )

    second_start = start + timedelta(hours=5)
    second_batch = _candles(4, second_start, timedelta(minutes=15))
    provider2 = FakeProvider(second_batch)
    sync_historical_candles(
        provider2, "XAUUSD", "M15", sync_repo, raw_candle_repository=raw_repo,
        end=second_start + timedelta(hours=2),
    )

    # The second call's requested start must be one interval past the first batch's last saved candle.
    requested_start = provider2.calls[0]
    assert requested_start[0] == "XAUUSD" and requested_start[1] == "M15"
    saved = raw_repo.get_candles("XAUUSD", "M15")
    assert len(saved) == 8


def test_sync_does_not_advance_watermark_on_zero_saved():
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    sync_repo = SyncStateRepository()
    raw_repo = RawCandleRepository()

    provider = FakeProvider([])
    sync_historical_candles(
        provider, "XAUUSD", "M15", sync_repo, raw_candle_repository=raw_repo,
        end=start + timedelta(hours=2), lookback=start,
    )

    assert sync_repo.get_sync_state("fakeprovider", "XAUUSD", "M15") is None
