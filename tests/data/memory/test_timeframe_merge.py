"""
Tests for TimeframeMemory.merge_closed (Module 1 extension enabling
module-5 gap recovery). Backward-compatible: inserts missing candles by
timestamp, preserves existing candles/provenance, maintains sort/capacity.
"""

from datetime import datetime, timezone, timedelta

from data_layer.providers.twelve_data_client import Candle
from data_layer.market_memory.timeframe_memory import TimeframeMemory
from data_layer.market_memory.candle_record import CandleSource


def _ts(i):
    return datetime(2026, 7, 24, tzinfo=timezone.utc) + timedelta(minutes=i)


def _c(i, close=100.0):
    return Candle(timestamp=_ts(i), open=close, high=close, low=close, close=close)


def test_merge_inserts_missing_only():
    tfm = TimeframeMemory("XAUUSD", "M1", capacity=10)
    tfm.hydrate([_c(0), _c(1), _c(4)], source=CandleSource.BOOTSTRAP)
    inserted = tfm.merge_closed([_c(2), _c(3), _c(4)],  # 4 already present
                                source=CandleSource.RECOVERY)
    assert inserted == 2
    series = tfm.get_series()
    assert [c.timestamp for c in series] == [_ts(i) for i in (0, 1, 2, 3, 4)]


def test_merge_preserves_existing_provenance():
    tfm = TimeframeMemory("XAUUSD", "M1", capacity=10)
    tfm.hydrate([_c(0)], source=CandleSource.BOOTSTRAP)
    tfm.merge_closed([_c(1)], source=CandleSource.RECOVERY)
    series = {c.timestamp: c for c in tfm.get_series()}
    assert series[_ts(0)].source is CandleSource.BOOTSTRAP   # untouched
    assert series[_ts(1)].source is CandleSource.RECOVERY    # new


def test_merge_respects_capacity_and_sort():
    tfm = TimeframeMemory("XAUUSD", "M1", capacity=3)
    tfm.hydrate([_c(0), _c(1)], source=CandleSource.BOOTSTRAP)
    tfm.merge_closed([_c(2), _c(3)], source=CandleSource.RECOVERY)
    series = tfm.get_series()
    assert [c.timestamp for c in series] == [_ts(1), _ts(2), _ts(3)]  # last 3


def test_merge_no_new_returns_zero():
    tfm = TimeframeMemory("XAUUSD", "M1", capacity=10)
    tfm.hydrate([_c(0), _c(1)], source=CandleSource.BOOTSTRAP)
    assert tfm.merge_closed([_c(0), _c(1)]) == 0


def test_merge_bumps_revision():
    tfm = TimeframeMemory("XAUUSD", "M1", capacity=10)
    tfm.hydrate([_c(0)])
    r = tfm.revision()
    tfm.merge_closed([_c(1)])
    assert tfm.revision() == r + 1
