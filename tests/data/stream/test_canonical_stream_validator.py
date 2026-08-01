"""Unit tests for data/stream/stream_validator.py (TASK-ARCH-101)."""

from datetime import datetime, timedelta, timezone

from data.stream.stream_validator import StreamValidator, ValidationResult
from data.stream.stream_event import StreamEvent


def _ev(asset="XAUUSD", price=2400.0, i=0, volume=None):
    ts = datetime(2026, 7, 22, 13, tzinfo=timezone.utc) + timedelta(seconds=i)
    return StreamEvent(asset=asset, price=price, timestamp=ts, volume=volume)


def test_valid_event_passes():
    r = StreamValidator().validate(_ev())
    assert r.valid is True and bool(r) is True


def test_none_event_is_empty():
    r = StreamValidator().validate(None)
    assert not r and r.code == "empty"


def test_missing_asset_is_empty():
    r = StreamValidator().validate(_ev(asset=""))
    assert r.code == "empty"


def test_asset_mismatch():
    r = StreamValidator().validate(_ev(asset="BTCUSDT"), expected_asset="XAUUSD")
    assert r.code == "asset"


def test_non_positive_price():
    assert StreamValidator().validate(_ev(price=0)).code == "price"
    assert StreamValidator().validate(_ev(price=-5)).code == "price"


def test_non_finite_price():
    assert StreamValidator().validate(_ev(price=float("nan"))).code == "price"
    assert StreamValidator().validate(_ev(price=float("inf"))).code == "price"


def test_negative_volume():
    assert StreamValidator().validate(_ev(volume=-1)).code == "price"


def test_future_timestamp():
    future = datetime.now(timezone.utc) + timedelta(hours=1)
    ev = StreamEvent(asset="XAUUSD", price=2400.0, timestamp=future)
    assert StreamValidator().validate(ev).code == "timestamp"


def test_duplicate_timestamp():
    prev = _ev(i=5)
    cur = _ev(i=5)
    assert StreamValidator().validate(cur, previous=prev).code == "duplicate"


def test_out_of_sequence():
    prev = _ev(i=10)
    cur = _ev(i=3)
    assert StreamValidator().validate(cur, previous=prev).code == "sequence"


def test_newer_event_after_previous_passes():
    prev = _ev(i=3)
    cur = _ev(i=10)
    assert StreamValidator().validate(cur, previous=prev).valid is True


def test_different_asset_not_treated_as_duplicate():
    prev = _ev(asset="BTCUSDT", i=5)
    cur = _ev(asset="XAUUSD", i=5)
    # same timestamp but different asset -> not a duplicate
    assert StreamValidator().validate(cur, previous=prev).valid is True


def test_never_raises_returns_result():
    assert isinstance(StreamValidator().validate(None), ValidationResult)
