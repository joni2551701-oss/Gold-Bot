"""
Unit tests for data/stream/price_stream.py (v1.1 Phase 1, module 4).

Covers the DD-046 lifecycle, DD-047 waiting mode (+ crypto exemption),
DD-051 provider isolation, DD-052 event ordering, DD-050 graceful
shutdown, reconnect backoff, and provider-agnostic behavior.
"""

import datetime as _dt

import pytest

from data.stream.price_stream import PriceStream, AlwaysOpenCalendar
from data.stream.stream_event import StreamState, AssetClass
from _fakes import (
    FakeProvider, FakeCalendar, RecordingSink, event, ts,
)


def _stream(provider=None, sink=None, calendar=None,
            asset_class=AssetClass.METAL, **kw):
    return PriceStream(
        "XAUUSD", provider or FakeProvider(), sink or RecordingSink(),
        calendar=calendar, asset_class=asset_class, **kw)


def test_requires_provider_and_sink():
    with pytest.raises(ValueError):
        PriceStream("XAUUSD", None, RecordingSink())
    with pytest.raises(ValueError):
        PriceStream("XAUUSD", FakeProvider(), object())


def test_naive_now_rejected():
    s = _stream()
    with pytest.raises(ValueError):
        s.tick(_dt.datetime(2026, 7, 24, 13, 0))


def test_lifecycle_to_streaming():
    p = FakeProvider()
    s = _stream(provider=p, calendar=FakeCalendar(open_flag=True))
    assert s.state is StreamState.INITIALIZING
    assert s.tick(ts(0)) is StreamState.CONNECTING
    assert s.tick(ts(1)) is StreamState.STREAMING
    assert p.connected


def test_streaming_forwards_events():
    p = FakeProvider()
    sink = RecordingSink()
    s = _stream(provider=p, sink=sink, calendar=FakeCalendar(True))
    s.tick(ts(0)); s.tick(ts(1))            # -> STREAMING
    p.batches.append([event(i=2), event(i=3)])
    s.tick(ts(4))
    assert [e.timestamp for e in sink.events] == [ts(2), ts(3)]


def test_waiting_mode_when_closed_and_resume():
    p = FakeProvider()
    cal = FakeCalendar(open_flag=False)
    s = _stream(provider=p, calendar=cal, asset_class=AssetClass.METAL)
    s.tick(ts(0))                            # INITIALIZING -> CONNECTING
    s.tick(ts(1))                            # closed -> WAITING_FOR_MARKET
    assert s.state is StreamState.WAITING_FOR_MARKET
    # no provider polling while waiting
    s.tick(ts(2))
    assert s.state is StreamState.WAITING_FOR_MARKET
    # market reopens -> CONNECTING -> STREAMING
    cal.open_flag = True
    assert s.tick(ts(3)) is StreamState.CONNECTING
    assert s.tick(ts(4)) is StreamState.STREAMING


def test_crypto_never_waits():
    p = FakeProvider()
    cal = FakeCalendar(open_flag=False)      # "closed" ignored for crypto
    s = _stream(provider=p, calendar=cal, asset_class=AssetClass.CRYPTO)
    s.tick(ts(0))                            # CONNECTING
    assert s.tick(ts(1)) is StreamState.STREAMING


def test_reconnect_backoff_and_recovery():
    p = FakeProvider()
    p.connect_should_fail = True
    s = _stream(provider=p, calendar=FakeCalendar(True),
                backoff_base_seconds=10, max_reconnect_attempts=5)
    s.tick(ts(0))                            # CONNECTING
    s.tick(ts(1))                            # connect fails -> RECONNECTING
    assert s.state is StreamState.RECONNECTING
    # still backing off
    s.tick(ts(2))
    assert s.state is StreamState.RECONNECTING
    # after backoff, provider recovers
    p.connect_should_fail = False
    assert s.tick(ts(100)) is StreamState.STREAMING


def test_reconnect_exhaustion_shuts_down():
    p = FakeProvider()
    p.connect_should_fail = True
    s = _stream(provider=p, calendar=FakeCalendar(True),
                backoff_base_seconds=0, max_reconnect_attempts=2)
    s.tick(ts(0))                            # CONNECTING
    state = None
    for i in range(1, 20):
        state = s.tick(ts(i))
        if state is StreamState.SHUTDOWN:
            break
    assert state is StreamState.SHUTDOWN


def test_provider_isolation_on_read_error():
    p = FakeProvider()
    s = _stream(provider=p, calendar=FakeCalendar(True))
    s.tick(ts(0)); s.tick(ts(1))            # STREAMING
    p.read_should_fail = True
    # must NOT raise; transitions to RECONNECTING, error counted
    s.tick(ts(2))
    assert s.state is StreamState.RECONNECTING
    assert s.stats()["provider_errors"] >= 1


def test_event_ordering_dd052():
    p = FakeProvider()
    sink = RecordingSink()
    s = _stream(provider=p, sink=sink, calendar=FakeCalendar(True))
    s.tick(ts(0)); s.tick(ts(1))            # STREAMING
    # out-of-order batch: 5, 3, 7  -> forwarded sorted 3,5,7
    p.batches.append([event(i=5), event(i=3), event(i=7)])
    s.tick(ts(8))
    assert [e.timestamp for e in sink.events] == [ts(3), ts(5), ts(7)]
    # a strictly-older event next is dropped
    p.batches.append([event(i=4)])
    s.tick(ts(9))
    assert [e.timestamp for e in sink.events] == [ts(3), ts(5), ts(7)]
    assert s.stats()["dropped_out_of_order"] == 1


def test_graceful_shutdown_dd050():
    p = FakeProvider()
    sink = RecordingSink()
    s = _stream(provider=p, sink=sink, calendar=FakeCalendar(True))
    s.tick(ts(0)); s.tick(ts(1))            # STREAMING
    p.batches.append([event(i=2)])          # pending -> flushed on shutdown
    snap = s.shutdown(ts(3))
    assert s.state is StreamState.SHUTDOWN
    assert p.disconnect_calls >= 1
    assert snap["state"] == "shutdown"
    assert sink.events                      # pending event was flushed (no candle lost)


def test_provider_agnostic_swap():
    # Two independent providers, identical stream behavior.
    for _ in range(2):
        p = FakeProvider()
        s = _stream(provider=p, calendar=AlwaysOpenCalendar())
        s.tick(ts(0))
        assert s.tick(ts(1)) is StreamState.STREAMING


def test_capabilities_exposed():
    p = FakeProvider()
    assert p.capabilities.supports_polling is True


# ---------------- TASK-ARCH-101: optional validator integration ----------------

def test_validator_drops_invalid_events():
    from data.stream.stream_validator import StreamValidator
    p = FakeProvider()
    sink = RecordingSink()
    s = _stream(provider=p, sink=sink, calendar=FakeCalendar(True),
                validator=StreamValidator())
    s.tick(ts(0)); s.tick(ts(1))            # -> STREAMING
    # one valid event (price>0) and one invalid (price<=0)
    p.batches.append([event(i=2, price=2400.0), event(i=3, price=0.0)])
    s.tick(ts(4))
    prices = [e.price for e in sink.events]
    assert 2400.0 in prices
    assert 0.0 not in prices                # invalid dropped
    assert s.stats()["dropped_invalid"] == 1


def test_no_validator_forwards_everything_unchanged():
    p = FakeProvider()
    sink = RecordingSink()
    s = _stream(provider=p, sink=sink, calendar=FakeCalendar(True))  # validator=None
    s.tick(ts(0)); s.tick(ts(1))
    p.batches.append([event(i=2, price=2400.0)])
    s.tick(ts(4))
    assert len(sink.events) == 1
    assert s.stats()["dropped_invalid"] == 0
