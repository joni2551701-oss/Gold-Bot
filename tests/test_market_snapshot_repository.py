"""
Phase 59.3, TASK 2 -- database/market_snapshot_repository.py and
market_snapshot_models.py tests.
"""

from datetime import datetime, timezone

from data_layer.live_data.market_data_snapshot import capture_market_data_snapshot
from database.market_snapshot_models import MarketSnapshotRecord, from_market_data_snapshot
from database.market_snapshot_repository import MarketSnapshotRepository


def _record(snapshot_id="snap-1", symbol="XAUUSD", timeframe="M15"):
    return MarketSnapshotRecord(
        market_snapshot_id=snapshot_id, symbol=symbol, timeframe=timeframe,
        candle_count=10, candles_reference="abc123",
        created_at=datetime.now(timezone.utc), provider="twelvedata",
    )


def test_save_snapshot_returns_true_on_first_insert():
    repo = MarketSnapshotRepository()
    assert repo.save_snapshot(_record()) is True


def test_save_snapshot_returns_false_on_duplicate_id():
    repo = MarketSnapshotRepository()
    record = _record()
    repo.save_snapshot(record)
    assert repo.save_snapshot(record) is False


def test_get_snapshot_returns_the_saved_record():
    repo = MarketSnapshotRepository()
    repo.save_snapshot(_record(snapshot_id="snap-42"))

    result = repo.get_snapshot("snap-42")

    assert result is not None
    assert result.market_snapshot_id == "snap-42"
    assert result.provider == "twelvedata"


def test_get_snapshot_returns_none_for_missing_id():
    repo = MarketSnapshotRepository()
    assert repo.get_snapshot("does-not-exist") is None


def test_get_recent_snapshots_orders_newest_first():
    repo = MarketSnapshotRepository()
    import time

    repo.save_snapshot(_record(snapshot_id="snap-a"))
    time.sleep(0.01)
    repo.save_snapshot(_record(snapshot_id="snap-b"))

    result = repo.get_recent_snapshots("XAUUSD", "M15")

    assert [r.market_snapshot_id for r in result] == ["snap-b", "snap-a"]


def test_get_recent_snapshots_filters_by_symbol_and_timeframe():
    repo = MarketSnapshotRepository()
    repo.save_snapshot(_record(snapshot_id="snap-1", symbol="XAUUSD", timeframe="M15"))
    repo.save_snapshot(_record(snapshot_id="snap-2", symbol="EURUSD", timeframe="M15"))

    result = repo.get_recent_snapshots("XAUUSD", "M15")

    assert len(result) == 1
    assert result[0].market_snapshot_id == "snap-1"


def test_optional_fields_default_to_none_and_round_trip():
    repo = MarketSnapshotRepository()
    record = MarketSnapshotRecord(
        market_snapshot_id="snap-minimal", symbol="XAUUSD", timeframe="M15",
        candle_count=0, candles_reference="ref", created_at=datetime.now(timezone.utc),
    )
    repo.save_snapshot(record)

    result = repo.get_snapshot("snap-minimal")

    assert result.provider is None
    assert result.first_timestamp is None
    assert result.last_timestamp is None
    assert result.data_quality is None


# --- from_market_data_snapshot() bridge ---

def test_from_market_data_snapshot_copies_every_field():
    snapshot = capture_market_data_snapshot(
        [], "XAUUSD", "M15", provider="twelvedata", data_quality="OK"
    )

    record = from_market_data_snapshot(snapshot)

    assert record.market_snapshot_id == snapshot.market_snapshot_id
    assert record.symbol == snapshot.symbol
    assert record.timeframe == snapshot.timeframe
    assert record.candle_count == snapshot.candle_count
    assert record.candles_reference == snapshot.candles_reference
    assert record.provider == "twelvedata"
    assert record.data_quality == "OK"


def test_from_market_data_snapshot_result_is_persistable():
    snapshot = capture_market_data_snapshot([], "XAUUSD", "M15", provider="twelvedata")
    record = from_market_data_snapshot(snapshot)

    repo = MarketSnapshotRepository()
    assert repo.save_snapshot(record) is True
    assert repo.get_snapshot(snapshot.market_snapshot_id) is not None
