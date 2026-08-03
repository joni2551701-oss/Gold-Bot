"""Setup layer — Wyckoff strategy (TASK-CORE-007)."""

from types import SimpleNamespace

from context_layer.wyckoff.wyckoff import WyckoffEventType

from strategies.wyckoff_strategy import WyckoffStrategy
from strategies.result import StrategyDirection, SetupStatus


def _wyckoff(index, wtype, phase, sweep_price):
    return SimpleNamespace(index=index, type=wtype,
                           phase=SimpleNamespace(value=phase),
                           sweep=SimpleNamespace(sweep_price=sweep_price))


def test_spring_is_long(make_ctx):
    ctx = make_ctx(wyckoff_events=[_wyckoff(5, WyckoffEventType.SPRING, "ACCUMULATION", 99.0)])
    r = WyckoffStrategy().evaluate(ctx)
    assert r.status is SetupStatus.SETUP_FOUND
    assert r.direction is StrategyDirection.LONG
    assert r.invalidation == 99.0
    assert r.metadata["phase"] == "ACCUMULATION"


def test_upthrust_is_short(make_ctx):
    ctx = make_ctx(wyckoff_events=[_wyckoff(6, WyckoffEventType.UPTHRUST, "DISTRIBUTION", 110.0)])
    r = WyckoffStrategy().evaluate(ctx)
    assert r.direction is StrategyDirection.SHORT
    assert r.metadata["wyckoff_type"] == "UPTHRUST"


def test_no_wyckoff_is_no_setup(make_ctx):
    r = WyckoffStrategy().evaluate(make_ctx(candles=[SimpleNamespace(close=1.0)]))
    assert r.status is SetupStatus.NO_SETUP
