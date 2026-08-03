"""
Unit tests for data_layer/historical_data/historical_bootstrap.py (module 5).

Covers strategies (DD-058), cold start / warm restart / incremental,
resume (DD-056), cancellation (DD-055), progress (DD-054), metrics
(DD-057), and validation failure.
"""

import datetime as _dt

import pytest

from data_layer.market_memory.market_memory import MarketMemory
from data_layer.historical_data.historical_bootstrap import HistoricalBootstrap
from data_layer.historical_data.bootstrap_state import BootstrapState, BootstrapStrategy
from data_layer.historical_data.historical_provider import InMemoryBootstrapCache
from _bfakes import FakeHistoricalProvider, candle, ts


def _mem(caps=None):
    return MarketMemory("XAUUSD", caps or {"M1": 100})


def _provider_with_recent(tf="M1", n=5):
    p = FakeHistoricalProvider()
    p.recent[("XAUUSD", tf)] = [candle(i) for i in range(n)]
    return p


def test_naive_now_rejected():
    b = HistoricalBootstrap(_mem(), FakeHistoricalProvider())
    with pytest.raises(ValueError):
        b.run(_dt.datetime(2026, 7, 24, 0, 0))


def test_cold_start_hydrates_memory():
    mem = _mem()
    prov = _provider_with_recent(n=5)
    b = HistoricalBootstrap(mem, prov, strategy=BootstrapStrategy.AUTO)
    prog = b.run(ts(10))
    assert prog.status is BootstrapState.READY
    assert prog.progress_pct == 100.0
    assert mem.timeframe("M1").closed_count() == 5
    assert prov.recent_calls == 1
    assert b.metrics().candles_loaded == 5
    assert b.metrics().api_requests >= 1
    assert b.metrics().last_bootstrap is not None


def test_full_strategy_ignores_fresh_cache():
    mem = _mem()
    prov = _provider_with_recent(n=3)
    cache = InMemoryBootstrapCache()
    cache.put("XAUUSD", "M1", [candle(0)], ts(0))     # fresh cache present
    b = HistoricalBootstrap(mem, prov, cache=cache,
                            strategy=BootstrapStrategy.FULL)
    b.run(ts(10))
    assert prov.recent_calls == 1                     # FULL still fetched
    assert mem.timeframe("M1").closed_count() == 3


def test_cache_only_no_provider_call():
    mem = _mem()
    prov = _provider_with_recent(n=5)                 # should NOT be used
    cache = InMemoryBootstrapCache()
    cache.put("XAUUSD", "M1", [candle(0), candle(1)], ts(0))
    b = HistoricalBootstrap(mem, prov, cache=cache,
                            strategy=BootstrapStrategy.CACHE_ONLY)
    b.run(ts(10))
    assert prov.recent_calls == 0
    assert mem.timeframe("M1").closed_count() == 2
    assert b.metrics().cache_hits == 1


def test_auto_warm_restart_uses_cache():
    mem = _mem()
    prov = _provider_with_recent(n=5)
    cache = InMemoryBootstrapCache(ttl_seconds=3600)
    cache.put("XAUUSD", "M1", [candle(0), candle(1), candle(2)], ts(0))
    b = HistoricalBootstrap(mem, prov, cache=cache,
                            strategy=BootstrapStrategy.AUTO)
    b.run(ts(1))                                       # cache fresh -> warm
    assert prov.recent_calls == 0
    assert mem.timeframe("M1").closed_count() == 3
    assert b.metrics().cache_hits == 1


def test_incremental_fetches_delta_only():
    mem = _mem()
    mem.timeframe("M1").hydrate([candle(0), candle(1)])   # memory warm
    prov = FakeHistoricalProvider()
    prov.range_pool[("XAUUSD", "M1")] = [candle(2), candle(3)]
    b = HistoricalBootstrap(mem, prov, strategy=BootstrapStrategy.INCREMENTAL)
    b.run(ts(4))
    assert prov.range_calls == 1
    assert prov.recent_calls == 0
    assert mem.timeframe("M1").closed_count() == 4         # 0,1 + delta 2,3


def test_recovery_only_gap_fills_no_fresh_load():
    mem = _mem()
    mem.timeframe("M1").hydrate([candle(0), candle(1)])
    prov = FakeHistoricalProvider()
    prov.range_pool[("XAUUSD", "M1")] = [candle(2), candle(3), candle(4)]
    b = HistoricalBootstrap(mem, prov, strategy=BootstrapStrategy.RECOVERY_ONLY)
    b.run(ts(5))
    assert prov.recent_calls == 0
    assert b.metrics().recovery_count == 3
    assert mem.timeframe("M1").closed_count() == 5


def test_validation_failure_marks_failed():
    mem = _mem()
    prov = FakeHistoricalProvider()
    prov.recent[("XAUUSD", "M1")] = [candle(3), candle(1)]  # out of order
    b = HistoricalBootstrap(mem, prov, strategy=BootstrapStrategy.FULL)
    prog = b.run(ts(10))
    assert b.state("M1") is BootstrapState.FAILED
    assert prog.status is BootstrapState.FAILED
    assert b.metrics().validation_errors >= 1


def test_resume_skips_ready_timeframe():
    mem = _mem({"M1": 100, "M5": 100})
    prov = FakeHistoricalProvider()
    prov.recent[("XAUUSD", "M1")] = [candle(0), candle(1)]
    prov.recent[("XAUUSD", "M5")] = [candle(3, tf_minutes=5),   # out of order
                                     candle(1, tf_minutes=5)]
    b = HistoricalBootstrap(mem, prov, strategy=BootstrapStrategy.FULL)
    b.run(ts(50))
    assert b.state("M1") is BootstrapState.READY
    assert b.state("M5") is BootstrapState.FAILED
    calls_after_first = prov.recent_calls
    # fix M5 and re-run: M1 is skipped (resume), only M5 retried
    prov.recent[("XAUUSD", "M5")] = [candle(0, tf_minutes=5),
                                     candle(1, tf_minutes=5)]
    b.run(ts(60))
    assert b.state("M1") is BootstrapState.READY
    assert b.state("M5") is BootstrapState.READY
    assert prov.recent_calls == calls_after_first + 1      # only M5 refetched


def test_cancellation_marks_cancelled():
    mem = _mem({"M1": 100, "M5": 100})
    prov = _provider_with_recent(n=3)
    b = HistoricalBootstrap(mem, prov, strategy=BootstrapStrategy.FULL)
    b.cancel()                                             # DD-055
    prog = b.run(ts(10))
    assert prog.status is BootstrapState.CANCELLED
    assert prov.recent_calls == 0                          # nothing loaded


def test_progress_remaining_and_timestamps():
    mem = _mem()
    prov = _provider_with_recent(n=2)
    b = HistoricalBootstrap(mem, prov, strategy=BootstrapStrategy.FULL)
    prog = b.run(ts(5))
    assert prog.remaining == []
    assert prog.started_at is not None
    assert prog.finished_at is not None
