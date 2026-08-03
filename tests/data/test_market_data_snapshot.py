"""
Phase 59 Preparation, TASK 1 -- data_layer/live_data/market_data_snapshot.py tests.
"""

from datetime import datetime, timezone

from data_layer.live_data.market_data_snapshot import (
    capture_market_data_snapshot,
    compute_candles_reference,
    generate_market_snapshot_id,
)
from data_layer.providers.twelve_data_client import Candle


def _candle(ts: datetime, price: float = 2000.0) -> Candle:
    return Candle(timestamp=ts, open=price, high=price + 1, low=price - 1, close=price)


def test_capture_from_empty_candles_never_raises():
    snapshot = capture_market_data_snapshot([], "XAUUSD", "M15")
    assert snapshot.candle_count == 0
    assert snapshot.first_timestamp is None
    assert snapshot.last_timestamp is None
    assert isinstance(snapshot.candles_reference, str) and snapshot.candles_reference


def test_capture_records_window_bounds():
    t1 = datetime(2026, 1, 1, tzinfo=timezone.utc)
    t2 = datetime(2026, 1, 1, 0, 15, tzinfo=timezone.utc)
    t3 = datetime(2026, 1, 1, 0, 30, tzinfo=timezone.utc)
    candles = [_candle(t1), _candle(t2), _candle(t3)]

    snapshot = capture_market_data_snapshot(candles, "XAUUSD", "M15")

    assert snapshot.candle_count == 3
    assert snapshot.first_timestamp == t1
    assert snapshot.last_timestamp == t3
    assert snapshot.symbol == "XAUUSD"
    assert snapshot.timeframe == "M15"


def test_market_snapshot_id_is_unique_per_call():
    a = capture_market_data_snapshot([], "XAUUSD", "M15")
    b = capture_market_data_snapshot([], "XAUUSD", "M15")
    assert a.market_snapshot_id != b.market_snapshot_id


def test_candles_reference_is_deterministic_for_same_window():
    t1 = datetime(2026, 1, 1, tzinfo=timezone.utc)
    t2 = datetime(2026, 1, 1, 0, 15, tzinfo=timezone.utc)

    ref_a = compute_candles_reference("XAUUSD", "M15", 2, t1, t2)
    ref_b = compute_candles_reference("XAUUSD", "M15", 2, t1, t2)

    assert ref_a == ref_b


def test_candles_reference_differs_for_different_windows():
    t1 = datetime(2026, 1, 1, tzinfo=timezone.utc)
    t2 = datetime(2026, 1, 1, 0, 15, tzinfo=timezone.utc)
    t3 = datetime(2026, 1, 1, 0, 30, tzinfo=timezone.utc)

    ref_a = compute_candles_reference("XAUUSD", "M15", 2, t1, t2)
    ref_b = compute_candles_reference("XAUUSD", "M15", 2, t1, t3)

    assert ref_a != ref_b


def test_two_snapshots_of_same_window_have_matching_reference():
    """The point of candles_reference: two independent captures of the identical window are comparable."""
    t1 = datetime(2026, 1, 1, tzinfo=timezone.utc)
    t2 = datetime(2026, 1, 1, 0, 15, tzinfo=timezone.utc)
    candles = [_candle(t1), _candle(t2)]

    snap_a = capture_market_data_snapshot(candles, "XAUUSD", "M15")
    snap_b = capture_market_data_snapshot(candles, "XAUUSD", "M15")

    assert snap_a.candles_reference == snap_b.candles_reference
    assert snap_a.market_snapshot_id != snap_b.market_snapshot_id  # identity still unique per capture


def test_to_dict_is_json_safe_and_round_trips_timestamps():
    t1 = datetime(2026, 1, 1, tzinfo=timezone.utc)
    snapshot = capture_market_data_snapshot([_candle(t1)], "XAUUSD", "M15")

    data = snapshot.to_dict()

    assert data["first_timestamp"] == t1.isoformat()
    assert data["last_timestamp"] == t1.isoformat()
    assert isinstance(data["created_at"], str)


def test_to_json_never_raises():
    import json

    snapshot = capture_market_data_snapshot([], "XAUUSD", "M15")
    json.loads(snapshot.to_json())  # must not raise


def test_generate_market_snapshot_id_returns_uuid_shaped_string():
    value = generate_market_snapshot_id()
    assert isinstance(value, str)
    assert len(value) == 36  # str(uuid.uuid4()) shape, same convention as generate_signal_id()/generate_snapshot_id()


def test_dataclass_is_frozen():
    snapshot = capture_market_data_snapshot([], "XAUUSD", "M15")
    try:
        snapshot.symbol = "EURUSD"
        assert False, "MarketDataSnapshot must be immutable"
    except AttributeError:
        pass


# --- Phase 59.1 TASK 4: provider/data_quality extension ---

def test_provider_and_data_quality_default_to_none():
    snapshot = capture_market_data_snapshot([], "XAUUSD", "M15")
    assert snapshot.provider is None
    assert snapshot.data_quality is None


def test_provider_and_data_quality_can_be_supplied():
    snapshot = capture_market_data_snapshot(
        [], "XAUUSD", "M15", provider="twelvedata", data_quality="OK"
    )
    assert snapshot.provider == "twelvedata"
    assert snapshot.data_quality == "OK"


def test_provider_and_data_quality_appear_in_to_dict():
    snapshot = capture_market_data_snapshot(
        [], "XAUUSD", "M15", provider="twelvedata", data_quality="WARNING_GAP"
    )
    data = snapshot.to_dict()
    assert data["provider"] == "twelvedata"
    assert data["data_quality"] == "WARNING_GAP"
