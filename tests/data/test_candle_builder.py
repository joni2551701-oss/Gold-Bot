"""
Unit tests for data_layer/live_data/candle_builder.py (v1.1 Phase 1, module 3).

Covers OHLC aggregation, boundary close/open, DD-045 timeframe ordering,
DD-044 clock independence, DD-042 monotonic + replay-identical sequence,
DD-043 source, event hooks, failure handling, and thread-safety.
"""

from datetime import datetime, timezone, timedelta
import threading

import pytest

from data_layer.live_data.candle_builder import CandleBuilder, CandleEventHook
from data_layer.market_memory.market_memory import MarketMemory
from data_layer.market_memory.candle_record import CandleStatus, CandleSource


def _dt(minute, second=0):
    return datetime(2026, 7, 24, 13, tzinfo=timezone.utc) + timedelta(
        minutes=minute, seconds=second)


def _memory(caps=None):
    return MarketMemory("XAUUSD", caps or {"M1": 100, "M5": 100})


class _RecordingHook(CandleEventHook):
    def __init__(self):
        self.events = []   # list of (kind, timeframe, candle_id)

    def on_new_candle(self, r):
        self.events.append(("new", r.timeframe, r.candle_id))

    def on_candle_update(self, r):
        self.events.append(("update", r.timeframe, r.candle_id))

    def on_candle_close(self, r):
        self.events.append(("close", r.timeframe, r.candle_id))


def test_requires_memory():
    with pytest.raises(ValueError):
        CandleBuilder("XAUUSD", None)


def test_ohlc_aggregation_within_window():
    b = CandleBuilder("XAUUSD", _memory({"M1": 100}))
    b.on_price(100.0, _dt(0, 1))
    b.on_price(105.0, _dt(0, 20))
    b.on_price(95.0, _dt(0, 40))
    b.on_price(101.0, _dt(0, 59))
    forming = b._memory.timeframe("M1").get_forming()
    assert (forming.open, forming.high, forming.low, forming.close) == (
        100.0, 105.0, 95.0, 101.0)


def test_boundary_closes_and_opens():
    b = CandleBuilder("XAUUSD", _memory({"M1": 100}))
    b.on_price(100.0, _dt(0, 10))    # window 13:00
    b.on_price(110.0, _dt(1, 5))     # window 13:01 -> close+open
    m1 = b._memory.timeframe("M1")
    assert m1.closed_count() == 1
    assert m1.get_last_closed().close == 100.0
    assert m1.get_forming().open == 110.0
    assert m1.get_last_closed().status is CandleStatus.CLOSED


def test_timeframe_ordering_m1_before_m5(monkeypatch):
    hook = _RecordingHook()
    b = CandleBuilder("XAUUSD", _memory({"M1": 100, "M5": 100}),
                      event_hook=hook)
    b.on_price(100.0, _dt(0))
    # first events are the opens; M1 must be emitted before M5 (DD-045)
    tfs_in_order = [tf for (_kind, tf, _id) in hook.events]
    assert tfs_in_order.index("M1") < tfs_in_order.index("M5")


def test_source_is_recorded():
    b = CandleBuilder("XAUUSD", _memory({"M1": 100}))
    b.on_price(100.0, _dt(0), source=CandleSource.REPLAY)
    assert b._memory.timeframe("M1").get_forming().source is CandleSource.REPLAY


def test_clock_independence_last_update_is_event_time():
    # DD-044: last_update_time is the event timestamp, not wall-clock.
    b = CandleBuilder("XAUUSD", _memory({"M1": 100}))
    ts = _dt(0, 30)
    b.on_price(100.0, ts)
    assert b._memory.timeframe("M1").get_forming().last_update_time == ts


def test_out_of_order_event_dropped():
    b = CandleBuilder("XAUUSD", _memory({"M1": 100}))
    b.on_price(100.0, _dt(5))         # window 13:05
    b.on_price(999.0, _dt(2))         # older -> dropped
    assert b.stats()["dropped_out_of_order"] == 1
    assert b._memory.timeframe("M1").get_forming().close == 100.0


def test_gap_does_not_fabricate_candles():
    b = CandleBuilder("XAUUSD", _memory({"M1": 100}))
    b.on_price(100.0, _dt(0))         # 13:00
    b.on_price(110.0, _dt(5))         # 13:05 -> jump of 5 windows
    m1 = b._memory.timeframe("M1")
    assert m1.closed_count() == 1     # only the one real close; no fabricated candles
    assert b.stats()["gaps"] == 1


def test_invalid_price_and_time_rejected():
    b = CandleBuilder("XAUUSD", _memory({"M1": 100}))
    b.on_price(float("nan"), _dt(0))
    b.on_price(100.0, datetime(2026, 7, 24, 13, 0))   # naive tz
    assert b.stats()["rejected"] == 2
    assert b._memory.timeframe("M1").get_forming() is None


def test_flush_closes_stale_forming():
    b = CandleBuilder("XAUUSD", _memory({"M1": 100}))
    b.on_price(100.0, _dt(0, 10))
    b.flush(_dt(2))                   # well past 13:01 boundary
    assert b._memory.timeframe("M1").closed_count() == 1
    assert b._memory.timeframe("M1").get_forming() is None


def test_hook_exception_isolated():
    class _Boom(CandleEventHook):
        def on_new_candle(self, r):
            raise RuntimeError("boom")

    b = CandleBuilder("XAUUSD", _memory({"M1": 100}), event_hook=_Boom())
    b.on_price(100.0, _dt(0))         # must not raise
    assert b.stats()["hook_errors"] == 1
    assert b._memory.timeframe("M1").get_forming() is not None


def _run_sequence(prices_times, source=CandleSource.STREAM, caps=None):
    """Build from a fixed event list; return the M1 closed series + seqs."""
    b = CandleBuilder("XAUUSD", _memory(caps or {"M1": 500, "M5": 500}))
    for price, t in prices_times:
        b.on_price(price, t, source=source)
    m1 = b._memory.timeframe("M1").get_series(include_forming=True)
    return [(c.open, c.high, c.low, c.close, c.sequence_number) for c in m1]


def test_replay_determinism_identical_series_and_sequence():
    # DD-042: same input sequence -> identical candles AND sequence numbers.
    events = [(100.0 + (i % 7), _dt(i // 3, (i % 3) * 20)) for i in range(30)]
    live = _run_sequence(events, source=CandleSource.STREAM)
    replay = _run_sequence(events, source=CandleSource.REPLAY)
    # OHLC + sequence numbers identical regardless of source (LIVE == REPLAY)
    assert [t[:5] for t in live] == [t[:5] for t in replay]


def test_sequence_monotonic_non_decreasing():
    events = [(100.0 + (i % 5), _dt(i, 0)) for i in range(10)]
    b = CandleBuilder("XAUUSD", _memory({"M1": 500}))
    for p, t in events:
        b.on_price(p, t)
    seqs = [c.sequence_number
            for c in b._memory.timeframe("M1").get_series(include_forming=True)]
    assert seqs == sorted(seqs)
    assert len(seqs) == len(set(seqs))


def test_single_writer_with_concurrent_readers():
    from data_layer.market_memory.memory_reader import MemoryReader
    from data_layer.market_memory.market_memory_registry import MarketMemoryRegistry

    reg = MarketMemoryRegistry()
    mem = reg.register("XAUUSD", {"M1": 2000})
    reader = MemoryReader(reg)
    b = CandleBuilder("XAUUSD", mem)
    errors = []

    def writer():
        try:
            for i in range(300):
                b.on_price(100.0 + (i % 10), _dt(i, i % 60))
        except Exception as e:   # pragma: no cover
            errors.append(e)

    def read_loop():
        try:
            for _ in range(300):
                reader.get_series("XAUUSD", "M1", n=10)
                reader.revision("XAUUSD", "M1")
        except Exception as e:   # pragma: no cover
            errors.append(e)

    threads = [threading.Thread(target=writer),
               threading.Thread(target=read_loop),
               threading.Thread(target=read_loop)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert not errors
    assert b.stats()["processed"] == 300
