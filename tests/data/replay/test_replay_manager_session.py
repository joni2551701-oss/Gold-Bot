"""ReplayManager, session bookmarks, validation, and source tests (module 8)."""

import pytest

from backtesting_layer.replay_engine.data_replay.replay_manager import ReplayManager, ReplayCreationError
from backtesting_layer.replay_engine.data_replay.replay_session import ReplaySession
from backtesting_layer.replay_engine.data_replay.replay_source import SnapshotReplaySource
from backtesting_layer.replay_engine.data_replay.replay_validation import validate_replay
from backtesting_layer.replay_engine.data_replay.replay_state import ReplayState
from _rfakes import memory, snapshot_source, candle, ts


# -- ReplayManager (SRP, amendment 5) -----------------------------------
def test_manager_creates_and_tracks_session():
    mgr = ReplayManager()
    session, ctrl = mgr.create_session("XAUUSD", snapshot_source(3), memory())
    assert session.session_id in mgr.sessions()
    assert ctrl.state is ReplayState.LOADED
    mgr.end_session(session.session_id)
    assert session.session_id not in mgr.sessions()


def test_manager_rejects_invalid_source():
    mgr = ReplayManager()
    empty = SnapshotReplaySource({})            # no data
    with pytest.raises(ReplayCreationError):
        mgr.create_session("XAUUSD", empty, memory())


def test_manager_multi_session_isolation():
    mgr = ReplayManager()
    s1, _ = mgr.create_session("XAUUSD", snapshot_source(3), memory())
    s2, _ = mgr.create_session("XAUUSD", snapshot_source(3), memory("BTCUSD"))
    assert s1.session_id != s2.session_id
    assert len(mgr.sessions()) == 2


# -- validation (amendment 4) -------------------------------------------
def test_validation_ok():
    r = validate_replay("XAUUSD", snapshot_source(4), memory())
    assert r.ok


def test_validation_empty_timeline():
    r = validate_replay("XAUUSD", SnapshotReplaySource({}), memory())
    assert not r.ok


def test_validation_integrity_failure():
    # a gap in the source -> integrity fails -> replay must not start
    gappy = SnapshotReplaySource({"M1": [candle(0), candle(1), candle(4)]})
    r = validate_replay("XAUUSD", gappy, memory())
    assert not r.ok
    assert any("integrity" in e for e in r.errors)


# -- session bookmarks (amendment 3) ------------------------------------
def test_session_bookmark_restore():
    s = ReplaySession(asset="XAUUSD", start=ts(0), end=ts(5))
    s.position = ts(3)
    s.bookmark("mark-a")
    s.position = ts(5)
    assert s.restore("mark-a") == ts(3)
    with pytest.raises(KeyError):
        s.restore("nope")


# -- source ordering ----------------------------------------------------
def test_snapshot_source_orders_frames():
    src = SnapshotReplaySource({"M1": [candle(2), candle(0), candle(1)]})
    frames = src.frames("XAUUSD")
    assert [f.timestamp for f in frames] == [ts(0), ts(1), ts(2)]
    assert src.timeline("XAUUSD") == (ts(0), ts(2))
