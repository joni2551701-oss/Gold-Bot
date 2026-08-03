"""TASK-CORE-004 -- StreamValidator: valid/invalid/duplicate/sequence/OHLC."""

from datetime import datetime, timedelta, timezone

from data_layer.live_data.stream.stream_event import StreamEvent
from data_layer.live_data.stream.stream_validator import StreamValidator

_NOW = datetime(2026, 1, 2, 12, tzinfo=timezone.utc)


def _event(ts=_NOW, **kw):
    base = dict(symbol="XAUUSD", timeframe="M15", timestamp=ts,
                open=2000.0, high=2010.0, low=1995.0, close=2005.0)
    base.update(kw)
    return StreamEvent(**base)


def test_valid_event_passes():
    assert StreamValidator().validate(_event(), now=_NOW).valid


def test_none_event_is_empty():
    r = StreamValidator().validate(None, now=_NOW)
    assert not r.valid and r.code == "empty"


def test_missing_symbol_is_empty():
    r = StreamValidator().validate(_event(symbol=""), now=_NOW)
    assert r.code == "empty"


def test_symbol_mismatch():
    r = StreamValidator().validate(_event(), expected_symbol="EURUSD", now=_NOW)
    assert not r.valid and r.code == "symbol"


def test_high_below_low_is_candle_error():
    r = StreamValidator().validate(_event(high=1990.0, low=1995.0), now=_NOW)
    assert r.code == "candle"


def test_high_not_bounding_close():
    r = StreamValidator().validate(_event(high=2004.0, close=2005.0), now=_NOW)
    assert r.code == "candle"


def test_non_positive_price_is_candle_error():
    r = StreamValidator().validate(_event(low=-1.0), now=_NOW)
    assert r.code == "candle"


def test_negative_volume_is_candle_error():
    r = StreamValidator().validate(_event(volume=-5.0), now=_NOW)
    assert r.code == "candle"


def test_future_timestamp_rejected():
    future = _NOW + timedelta(hours=1)
    r = StreamValidator().validate(_event(ts=future), now=_NOW)
    assert not r.valid and r.code == "timestamp"


def test_small_future_skew_tolerated():
    skew = _NOW + timedelta(minutes=2)
    assert StreamValidator().validate(_event(ts=skew), now=_NOW).valid


def test_duplicate_event_rejected():
    prev = _event(ts=_NOW)
    dup = _event(ts=_NOW)
    r = StreamValidator().validate(dup, previous=prev, now=_NOW)
    assert not r.valid and r.code == "duplicate"


def test_out_of_sequence_rejected():
    prev = _event(ts=_NOW)
    older = _event(ts=_NOW - timedelta(minutes=15))
    r = StreamValidator().validate(older, previous=prev, now=_NOW)
    assert not r.valid and r.code == "sequence"


def test_newer_event_after_previous_ok():
    prev = _event(ts=_NOW - timedelta(minutes=15))
    newer = _event(ts=_NOW)
    assert StreamValidator().validate(newer, previous=prev, now=_NOW).valid


def test_naive_timestamp_treated_as_utc():
    naive = datetime(2026, 1, 2, 12)  # no tzinfo
    assert StreamValidator().validate(_event(ts=naive), now=_NOW).valid
