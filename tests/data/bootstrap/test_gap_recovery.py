"""Unit tests for data/bootstrap/gap_recovery.py (module 5)."""

from data.memory.market_memory import MarketMemory
from data.memory.candle_record import CandleSource
from data.bootstrap.gap_recovery import GapRecovery
from _bfakes import FakeHistoricalProvider, candle, ts


def _memory():
    return MarketMemory("XAUUSD", {"M1": 100})


def test_no_gap_when_recent():
    mem = _memory()
    mem.timeframe("M1").hydrate([candle(0), candle(1), candle(2)])
    prov = FakeHistoricalProvider()
    gr = GapRecovery(mem, prov)
    # now within the window right after candle 2 -> no gap
    assert gr.has_gap("M1", ts(3)) is False
    assert gr.recover("M1", ts(3)) == 0


def test_detects_and_fills_gap():
    mem = _memory()
    mem.timeframe("M1").hydrate([candle(0), candle(1)])   # last = minute 1
    prov = FakeHistoricalProvider()
    # provider can supply the missing 2,3,4
    prov.range_pool[("XAUUSD", "M1")] = [candle(2), candle(3), candle(4)]
    gr = GapRecovery(mem, prov)
    # now at minute 5 -> windows 2,3,4 are missing
    assert gr.has_gap("M1", ts(5)) is True
    filled = gr.recover("M1", ts(5))
    assert filled == 3
    series = mem.timeframe("M1").get_series()
    assert [c.timestamp for c in series] == [ts(i) for i in range(5)]
    # backfilled candles are tagged RECOVERY
    assert series[-1].source is CandleSource.RECOVERY


def test_recover_empty_when_no_history():
    mem = _memory()
    gr = GapRecovery(mem, FakeHistoricalProvider())
    assert gr.recover("M1", ts(5)) == 0
