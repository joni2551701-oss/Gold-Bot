"""ReplayController tests (module 8): controls, seek/step, events, transition."""

from datetime import timedelta

from backtesting_layer.replay_engine.data_replay.replay_session import ReplaySession
from backtesting_layer.replay_engine.data_replay.replay_controller import ReplayController
from backtesting_layer.replay_engine.data_replay.replay_state import ReplayState
from data_layer.market_memory.candle_record import MemoryMode
from data_layer.event_system.event_bus import EventBus
from data_layer.event_system.event_model import EventType
from _rfakes import memory, snapshot_source, ts


def _controller(n=5, bus=None):
    src = snapshot_source(n)
    mem = memory()
    start, end = src.timeline("XAUUSD")
    session = ReplaySession(asset="XAUUSD", start=start, end=end)
    return ReplayController(session, src, mem, bus=bus), mem, session


def test_loads_in_replay_mode():
    ctrl, mem, _ = _controller()
    assert ctrl.state is ReplayState.LOADED
    assert mem.mode is MemoryMode.REPLAY


def test_play_tick_delivers_due_frames():
    ctrl, mem, _ = _controller(n=5)
    ctrl.play()
    assert ctrl.state is ReplayState.PLAYING
    ctrl.tick(timedelta(minutes=2))     # virtual now = ts(2) -> frames 0,1,2
    assert mem.timeframe("M1").closed_count() == 3
    ctrl.tick(timedelta(minutes=10))    # deliver the rest -> FINISHED
    assert mem.timeframe("M1").closed_count() == 5
    assert ctrl.state is ReplayState.FINISHED


def test_pause_blocks_tick():
    ctrl, mem, _ = _controller()
    ctrl.play()
    ctrl.pause()
    ctrl.tick(timedelta(minutes=10))    # paused -> nothing delivered
    assert mem.timeframe("M1").closed_count() == 0
    ctrl.resume()
    ctrl.tick(timedelta(minutes=10))
    assert mem.timeframe("M1").closed_count() == 5


def test_step_forward_is_frame_precise():
    ctrl, mem, _ = _controller(n=5)
    ctrl.play(); ctrl.pause()
    ctrl.step_forward(2)
    assert mem.timeframe("M1").closed_count() == 2


def test_seek_and_step_back_rebuild():
    ctrl, mem, _ = _controller(n=5)
    ctrl.play()
    ctrl.tick(timedelta(minutes=10))    # all 5 delivered
    assert mem.timeframe("M1").closed_count() == 5
    ctrl.seek(ts(1))                     # rebuild up to ts(1) -> frames 0,1
    assert mem.timeframe("M1").closed_count() == 2
    ctrl.step_back(1)                    # back one more
    assert mem.timeframe("M1").closed_count() == 1


def test_set_speed():
    ctrl, mem, session = _controller()
    ctrl.set_speed(5.0)
    assert session.speed == 5.0
    ctrl.play()
    ctrl.tick(timedelta(minutes=1))     # 1 min * 5x = 5 -> frames 0..4? ts<=5
    assert mem.timeframe("M1").closed_count() == 5


def test_transition_to_live():
    ctrl, mem, _ = _controller(n=2)
    ctrl.play()
    ctrl.tick(timedelta(minutes=10))    # FINISHED
    assert ctrl.state is ReplayState.FINISHED
    ctrl.transition_to_live(ts(100))
    assert ctrl.state is ReplayState.LIVE
    assert mem.mode is MemoryMode.LIVE


def test_events_published_with_session_correlation():
    bus = EventBus()
    seen = []
    bus.subscribe("REPLAY", lambda e: seen.append((e.type, e.correlation_id)))
    ctrl, mem, session = _controller(n=2, bus=bus)
    ctrl.play()
    ctrl.pause()
    ctrl.resume()
    ctrl.tick(timedelta(minutes=10))    # FINISHED
    types = [t for (t, _c) in seen]
    assert EventType.REPLAY_STARTED in types
    assert EventType.REPLAY_PAUSED in types
    assert EventType.REPLAY_RESUMED in types
    assert EventType.REPLAY_FINISHED in types
    # all replay events of the session share the session id as correlation
    assert {c for (_t, c) in seen} == {session.session_id}
