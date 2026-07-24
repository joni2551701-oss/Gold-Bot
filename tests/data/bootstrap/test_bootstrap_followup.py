"""
Tests for the Module 5 follow-up: bootstrap completion barrier (DD-063)
and lifecycle event hooks (DD-066).
"""

from data.memory.market_memory import MarketMemory
from data.bootstrap.historical_bootstrap import HistoricalBootstrap
from data.bootstrap.bootstrap_state import BootstrapState, BootstrapStrategy
from data.bootstrap.bootstrap_events import BootstrapEventHook
from _bfakes import FakeHistoricalProvider, candle, ts


def _mem(caps=None):
    return MarketMemory("XAUUSD", caps or {"M1": 100})


def _provider(tf="M1", n=3):
    p = FakeHistoricalProvider()
    p.recent[("XAUUSD", tf)] = [candle(i) for i in range(n)]
    return p


class _RecordingHook(BootstrapEventHook):
    def __init__(self):
        self.events = []

    def on_bootstrap_started(self, asset):
        self.events.append(("started", asset))

    def on_timeframe_completed(self, asset, timeframe, state):
        self.events.append(("tf_done", timeframe, state))

    def on_progress_updated(self, progress):
        self.events.append(("progress", progress.progress_pct))

    def on_bootstrap_completed(self, asset):
        self.events.append(("completed", asset))

    def on_bootstrap_failed(self, asset):
        self.events.append(("failed", asset))

    def on_bootstrap_cancelled(self, asset):
        self.events.append(("cancelled", asset))


def test_completion_barrier_dd063():
    mem = _mem({"M1": 100, "M5": 100})
    prov = _provider("M1", 2)
    prov.recent[("XAUUSD", "M5")] = [candle(0, tf_minutes=5)]
    b = HistoricalBootstrap(mem, prov, strategy=BootstrapStrategy.FULL)
    assert b.bootstrap_ready is False        # before run
    b.run(ts(10))
    assert b.bootstrap_ready is True         # all TFs READY


def test_barrier_false_when_a_timeframe_fails():
    mem = _mem({"M1": 100, "M5": 100})
    prov = FakeHistoricalProvider()
    prov.recent[("XAUUSD", "M1")] = [candle(0), candle(1)]
    prov.recent[("XAUUSD", "M5")] = [candle(3, tf_minutes=5),   # out of order
                                     candle(1, tf_minutes=5)]
    b = HistoricalBootstrap(mem, prov, strategy=BootstrapStrategy.FULL)
    b.run(ts(50))
    assert b.state("M5") is BootstrapState.FAILED
    assert b.bootstrap_ready is False


def test_event_hooks_started_and_completed():
    hook = _RecordingHook()
    b = HistoricalBootstrap(_mem(), _provider(n=3),
                            strategy=BootstrapStrategy.FULL, event_hook=hook)
    b.run(ts(10))
    kinds = [e[0] for e in hook.events]
    assert kinds[0] == "started"
    assert "tf_done" in kinds
    assert "progress" in kinds
    assert kinds[-1] == "completed"


def test_event_hooks_cancelled():
    hook = _RecordingHook()
    b = HistoricalBootstrap(_mem(), _provider(n=3),
                            strategy=BootstrapStrategy.FULL, event_hook=hook)
    b.cancel()
    b.run(ts(10))
    assert ("cancelled", "XAUUSD") in hook.events


def test_event_hooks_failed():
    hook = _RecordingHook()
    prov = FakeHistoricalProvider()
    prov.recent[("XAUUSD", "M1")] = [candle(3), candle(1)]      # out of order
    b = HistoricalBootstrap(_mem(), prov,
                            strategy=BootstrapStrategy.FULL, event_hook=hook)
    b.run(ts(10))
    assert ("failed", "XAUUSD") in hook.events


def test_hook_exception_isolated():
    class _Boom(BootstrapEventHook):
        def on_bootstrap_started(self, asset):
            raise RuntimeError("boom")

    b = HistoricalBootstrap(_mem(), _provider(n=2),
                            strategy=BootstrapStrategy.FULL, event_hook=_Boom())
    # must not raise
    prog = b.run(ts(10))
    assert prog.status is BootstrapState.READY
