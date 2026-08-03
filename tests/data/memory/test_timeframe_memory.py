"""
Unit tests for data_layer/market_memory/timeframe_memory.py (MarketMemory Core).

Covers ring-buffer bounding, revision versioning (DD-029), forming
lifecycle, copy-on-read isolation, hydrate, and thread-safety under
concurrent writers/readers.
"""

from datetime import datetime, timezone, timedelta
import threading

import pytest

from data_layer.providers.twelve_data_client import Candle
from data_layer.market_memory.timeframe_memory import TimeframeMemory
from data_layer.market_memory.candle_record import CandleStatus, CandleSource


def _ts(i):
    return datetime(2026, 7, 24, tzinfo=timezone.utc) + timedelta(minutes=i)


def test_capacity_must_be_positive():
    with pytest.raises(ValueError):
        TimeframeMemory("XAUUSD", "M1", 0)


def test_open_update_close_lifecycle():
    tfm = TimeframeMemory("XAUUSD", "M1", capacity=10)
    tfm.open_candle(_ts(0), price=100.0)
    assert tfm.get_forming().status is CandleStatus.FORMING
    tfm.update_forming(105.0)
    tfm.update_forming(95.0)
    closed = tfm.close_forming()
    assert closed.status is CandleStatus.CLOSED
    assert closed.high == 105.0 and closed.low == 95.0
    assert tfm.get_forming() is None
    assert tfm.closed_count() == 1
    assert tfm.get_last_closed().close == 95.0


def test_revision_increments_on_every_mutation():
    tfm = TimeframeMemory("XAUUSD", "M1", capacity=10)
    r0 = tfm.revision()
    tfm.open_candle(_ts(0), 100.0)
    tfm.update_forming(101.0)
    tfm.close_forming()
    assert tfm.revision() == r0 + 3


def test_update_without_forming_raises():
    tfm = TimeframeMemory("XAUUSD", "M1", capacity=10)
    with pytest.raises(ValueError):
        tfm.update_forming(100.0)


def test_open_auto_closes_previous_forming():
    tfm = TimeframeMemory("XAUUSD", "M1", capacity=10)
    tfm.open_candle(_ts(0), 100.0)
    tfm.open_candle(_ts(1), 200.0)   # should close the first
    assert tfm.closed_count() == 1
    assert tfm.get_forming().open == 200.0


def test_ring_buffer_bounds_history():
    tfm = TimeframeMemory("XAUUSD", "M1", capacity=3)
    for i in range(5):
        tfm.open_candle(_ts(i), float(i))
        tfm.close_forming()
    assert tfm.closed_count() == 3
    series = tfm.get_series()
    # only the last 3 survive, oldest -> newest
    assert [c.open for c in series] == [2.0, 3.0, 4.0]


def test_sequence_numbers_are_monotonic():
    tfm = TimeframeMemory("XAUUSD", "M1", capacity=10)
    seqs = []
    for i in range(3):
        rec = tfm.open_candle(_ts(i), float(i))
        seqs.append(rec.sequence_number)
        tfm.close_forming()
    assert seqs == sorted(seqs)
    assert len(set(seqs)) == 3


def test_hydrate_replaces_history():
    tfm = TimeframeMemory("XAUUSD", "M1", capacity=10)
    candles = [Candle(timestamp=_ts(i), open=i, high=i, low=i, close=i)
               for i in range(4)]
    n = tfm.hydrate(candles, source=CandleSource.BOOTSTRAP)
    assert n == 4
    assert tfm.closed_count() == 4
    assert tfm.get_last_closed().source is CandleSource.BOOTSTRAP


def test_hydrate_sorts_and_caps():
    tfm = TimeframeMemory("XAUUSD", "M1", capacity=2)
    candles = [Candle(timestamp=_ts(i), open=i, high=i, low=i, close=i)
               for i in (3, 1, 2, 0)]
    tfm.hydrate(candles)
    series = tfm.get_series()
    assert [c.open for c in series] == [2, 3]   # last 2 after sort


def test_get_series_include_forming():
    tfm = TimeframeMemory("XAUUSD", "M1", capacity=10)
    tfm.open_candle(_ts(0), 1.0)
    tfm.close_forming()
    tfm.open_candle(_ts(1), 2.0)
    without = tfm.get_series(include_forming=False)
    with_f = tfm.get_series(include_forming=True)
    assert len(without) == 1
    assert len(with_f) == 2
    assert with_f[-1].status is CandleStatus.FORMING


def test_copy_on_read_isolation():
    tfm = TimeframeMemory("XAUUSD", "M1", capacity=10)
    tfm.open_candle(_ts(0), 100.0)
    snap = tfm.get_forming()
    snap.apply_price(999.0)              # mutate the copy
    assert tfm.get_forming().close == 100.0   # internal state unchanged


def test_thread_safety_concurrent_writes_and_reads():
    tfm = TimeframeMemory("XAUUSD", "M1", capacity=1000)
    errors = []

    def writer():
        try:
            for i in range(200):
                tfm.open_candle(_ts(i), float(i))
                tfm.update_forming(float(i) + 0.5)
                tfm.close_forming()
        except Exception as e:  # pragma: no cover - failure path
            errors.append(e)

    def reader():
        try:
            for _ in range(200):
                tfm.get_series(n=10)
                tfm.revision()
                tfm.get_last()
        except Exception as e:  # pragma: no cover - failure path
            errors.append(e)

    threads = [threading.Thread(target=writer),
               threading.Thread(target=reader),
               threading.Thread(target=reader)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert not errors
    assert tfm.closed_count() == 200
    # revision advanced by exactly 3 per candle (open+update+close)
    assert tfm.revision() == 600
