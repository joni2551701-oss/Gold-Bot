"""Setup layer — BOS/CHoCH strategy (TASK-CORE-007)."""

from types import SimpleNamespace

from context.bos import BosDirection
from context.choch import ChochDirection

from strategies.bos_strategy import BOSStrategy
from strategies.result import StrategyDirection, SetupStatus


def _bos(index, direction, price=110.0):
    return SimpleNamespace(index=index, direction=direction,
                           broken_structure=SimpleNamespace(swing=SimpleNamespace(price=price)))


def test_bos_continuation_long(make_ctx):
    ctx = make_ctx(bos_events=[_bos(5, BosDirection.BULLISH)])
    r = BOSStrategy().evaluate(ctx)
    assert r.status is SetupStatus.SETUP_FOUND
    assert r.direction is StrategyDirection.LONG
    assert r.metadata["kind"] == "bos"


def test_choch_reversal_takes_precedence_when_more_recent(make_ctx):
    ctx = make_ctx(
        bos_events=[_bos(5, BosDirection.BULLISH)],
        choch_events=[SimpleNamespace(index=8, direction=ChochDirection.BEARISH,
                                      broken_structure=SimpleNamespace(swing=SimpleNamespace(price=90.0)))],
    )
    r = BOSStrategy().evaluate(ctx)
    assert r.metadata["kind"] == "choch"
    assert r.direction is StrategyDirection.SHORT


def test_no_events_is_no_setup(make_ctx):
    r = BOSStrategy().evaluate(make_ctx(candles=[SimpleNamespace(close=1.0)]))
    assert r.status is SetupStatus.NO_SETUP
