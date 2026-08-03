"""Unit tests for data_layer/event_system/replay_log.py (amendment 5, module 7)."""

from data_layer.event_system.replay_log import (
    ReplayLog, RingBufferPolicy, TimeBasedPolicy,
)
from data_layer.event_system.event_model import EventType
from _efakes import make_event, ts


def test_ring_buffer_policy_bounds():
    log = ReplayLog(RingBufferPolicy(capacity=3))
    for i in range(5):
        log.record(make_event(when=ts(i)))
    assert len(log) == 3


def test_time_based_policy_evicts_old():
    log = ReplayLog(TimeBasedPolicy(window_seconds=10))
    log.record(make_event(when=ts(0)), now=ts(0))
    log.record(make_event(when=ts(5)), now=ts(5))
    # now jumps to 100 -> both older than the 10s window
    log.record(make_event(when=ts(100)), now=ts(100))
    assert len(log) == 1


def test_replay_filter_by_type():
    log = ReplayLog(RingBufferPolicy(capacity=10))
    log.record(make_event(EventType.MARKET_CANDLE_OPENED, when=ts(0)))
    log.record(make_event(EventType.MARKET_CANDLE_CLOSED, when=ts(1)))
    got = []
    n = log.replay_to(lambda e: got.append(e.type),
                      event_type=EventType.MARKET_CANDLE_CLOSED)
    assert n == 1
    assert got == [EventType.MARKET_CANDLE_CLOSED]
