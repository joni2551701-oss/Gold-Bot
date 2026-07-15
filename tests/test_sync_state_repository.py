"""
Phase 59.5, TASK 2 -- database/sync_state_repository.py and
sync_state_models.py tests. Real SQLite (tests/conftest.py's autouse
fresh_database fixture), no mocks.
"""

from datetime import datetime, timezone

from database.sync_state_models import create_sync_state
from database.sync_state_repository import SyncStateRepository


def test_get_sync_state_returns_none_when_absent():
    repo = SyncStateRepository()
    assert repo.get_sync_state("twelvedata", "XAUUSD", "M15") is None


def test_update_sync_state_creates_a_new_row():
    repo = SyncStateRepository()
    ts = datetime(2026, 1, 1, tzinfo=timezone.utc)

    result = repo.update_sync_state("twelvedata", "XAUUSD", "M15", ts)

    assert result.provider == "twelvedata"
    assert result.symbol == "XAUUSD"
    assert result.timeframe == "M15"
    assert result.last_timestamp == ts


def test_update_sync_state_overwrites_an_existing_row():
    repo = SyncStateRepository()
    t1 = datetime(2026, 1, 1, tzinfo=timezone.utc)
    t2 = datetime(2026, 1, 2, tzinfo=timezone.utc)

    repo.update_sync_state("twelvedata", "XAUUSD", "M15", t1)
    repo.update_sync_state("twelvedata", "XAUUSD", "M15", t2)

    result = repo.get_sync_state("twelvedata", "XAUUSD", "M15")
    assert result.last_timestamp == t2


def test_sync_state_is_keyed_by_provider_symbol_timeframe():
    repo = SyncStateRepository()
    ts = datetime(2026, 1, 1, tzinfo=timezone.utc)

    repo.update_sync_state("twelvedata", "XAUUSD", "M15", ts)

    assert repo.get_sync_state("binance", "XAUUSD", "M15") is None
    assert repo.get_sync_state("twelvedata", "EURUSD", "M15") is None
    assert repo.get_sync_state("twelvedata", "XAUUSD", "H1") is None


def test_get_all_sync_states_returns_every_tracked_key():
    repo = SyncStateRepository()
    ts = datetime(2026, 1, 1, tzinfo=timezone.utc)

    repo.update_sync_state("twelvedata", "XAUUSD", "M15", ts)
    repo.update_sync_state("twelvedata", "EURUSD", "H1", ts)

    states = repo.get_all_sync_states()
    assert len(states) == 2


def test_create_sync_state_stamps_updated_at():
    state = create_sync_state("twelvedata", "XAUUSD", "M15", datetime(2026, 1, 1, tzinfo=timezone.utc))
    assert isinstance(state.updated_at, datetime)
    assert state.updated_at.tzinfo is not None


def test_sync_state_is_frozen():
    state = create_sync_state("twelvedata", "XAUUSD", "M15", datetime(2026, 1, 1, tzinfo=timezone.utc))
    try:
        state.provider = "binance"
        assert False, "SyncState must be immutable"
    except AttributeError:
        pass
