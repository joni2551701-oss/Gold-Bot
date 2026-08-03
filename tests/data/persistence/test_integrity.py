"""Unit tests for data_layer/market_memory/persistence/integrity.py (DD-064, module 6)."""

from data_layer.market_memory.persistence.integrity import check_series, check_integrity
from _pfakes import memory_with, candle


def test_clean_series_ok():
    series = [candle(i) for i in range(5)]
    r = check_series(series, "M1")
    assert r.ok
    assert r.missing == 0 and r.duplicates == 0 and r.out_of_order == 0


def test_detects_missing():
    series = [candle(0), candle(1), candle(4)]      # 2,3 missing
    r = check_series(series, "M1")
    assert not r.ok
    assert r.missing == 2


def test_detects_duplicate():
    series = [candle(0), candle(1), candle(1)]
    r = check_series(series, "M1")
    assert not r.ok
    assert r.duplicates == 1


def test_detects_out_of_order():
    series = [candle(0), candle(2), candle(1)]
    r = check_series(series, "M1")
    assert not r.ok
    assert r.out_of_order == 1


def test_check_integrity_over_memory():
    mem = memory_with(m1=5)
    r = check_integrity(mem)
    assert r.ok
    assert "M1" in r.per_timeframe
