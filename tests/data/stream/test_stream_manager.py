"""
Unit tests for data_layer/live_data/stream_manager.py (v1.1 Phase 1, module 4).

Covers multi-asset supervision (DD-030): add/get/assets, tick_all,
shutdown_all, duplicate protection.
"""

import pytest

from data_layer.live_data.stream_manager import StreamManager
from data_layer.live_data.price_stream import PriceStream, AlwaysOpenCalendar
from data_layer.live_data.stream_event import StreamState, AssetClass
from _fakes import FakeProvider, RecordingSink, ts


def _stream(asset):
    return PriceStream(asset, FakeProvider(), RecordingSink(),
                       calendar=AlwaysOpenCalendar(),
                       asset_class=AssetClass.CRYPTO)


def test_add_get_assets():
    m = StreamManager()
    m.add(_stream("XAUUSD"))
    m.add(_stream("BTCUSD"))
    assert set(m.assets()) == {"XAUUSD", "BTCUSD"}
    assert m.get("XAUUSD").asset == "XAUUSD"


def test_duplicate_rejected():
    m = StreamManager()
    m.add(_stream("XAUUSD"))
    with pytest.raises(ValueError):
        m.add(_stream("XAUUSD"))


def test_tick_all_advances_every_stream():
    m = StreamManager()
    m.add(_stream("XAUUSD"))
    m.add(_stream("BTCUSD"))
    m.tick_all(ts(0))                       # -> CONNECTING
    states = m.tick_all(ts(1))              # -> STREAMING
    assert all(s is StreamState.STREAMING for s in states.values())


def test_shutdown_all():
    m = StreamManager()
    m.add(_stream("XAUUSD"))
    m.tick_all(ts(0)); m.tick_all(ts(1))
    snaps = m.shutdown_all(ts(2))
    assert m.get("XAUUSD").state is StreamState.SHUTDOWN
    assert snaps["XAUUSD"]["state"] == "shutdown"


def test_health_aggregates():
    m = StreamManager()
    m.add(_stream("XAUUSD"))
    h = m.health()
    assert "XAUUSD" in h
    assert h["XAUUSD"]["asset"] == "XAUUSD"
