"""
Setup layer — AMD / Liquidity / FVG wrappers (TASK-CORE-007).

The three existing live strategies are exposed to the setup layer by
REUSING their frozen analyze() detection (no duplicated logic). These
tests confirm the wrappers delegate correctly: empty context -> NO_SETUP,
a crafted context that the inner detector recognizes -> SETUP_FOUND with
the adapted direction.
"""

from types import SimpleNamespace

from context_layer.amd.amd import AmdEventType
from context_layer.fair_value_gap.fvg import FvgType
from context_layer.market_structure.bos import BosDirection

from strategies.amd_strategy import AMDSetupStrategy
from strategies.liquidity_strategy import LiquiditySetupStrategy
from strategies.fvg_strategy import FVGSetupStrategy
from strategies.result import StrategyDirection, SetupStatus


def _swing(price):
    return SimpleNamespace(broken_structure=SimpleNamespace(swing=SimpleNamespace(price=price)))


# ---- empty -> NO_SETUP ---------------------------------------------------

def test_wrappers_no_setup_on_empty(make_ctx):
    # A well-formed but empty context carries no usable data, so the base
    # guard short-circuits to INVALID before delegating to the frozen
    # detector; either way the wrapper yields no setup and never raises.
    ctx = make_ctx()
    for strat in (AMDSetupStrategy(), LiquiditySetupStrategy(), FVGSetupStrategy()):
        r = strat.evaluate(ctx)
        assert r.status in (SetupStatus.NO_SETUP, SetupStatus.INVALID)
        assert not r.has_setup


# ---- crafted -> SETUP_FOUND (reusing the frozen detection) ---------------

def test_fvg_wrapper_setup_found(make_ctx):
    ctx = make_ctx(
        fair_value_gaps=[SimpleNamespace(filled=False, type=FvgType.BULLISH, top=110.0, bottom=105.0, index=10)],
        bos_events=[SimpleNamespace(index=12, **_swing(120.0).__dict__)],
    )
    r = FVGSetupStrategy().evaluate(ctx)
    assert r.status is SetupStatus.SETUP_FOUND
    assert r.direction is StrategyDirection.LONG
    assert r.strategy_name == "FVG_SETUP"
    assert r.rr is not None


def test_amd_wrapper_setup_found(make_ctx):
    ctx = make_ctx(
        amd_events=[SimpleNamespace(type=AmdEventType.DISTRIBUTION, index=10, is_bullish=True)],
        bos_events=[SimpleNamespace(index=12, **_swing(120.0).__dict__)],
        order_blocks=[SimpleNamespace(index=11, high=105.0, low=100.0)],
    )
    r = AMDSetupStrategy().evaluate(ctx)
    assert r.status is SetupStatus.SETUP_FOUND
    assert r.direction is StrategyDirection.LONG
    assert r.strategy_name == "AMD_SETUP"


def test_liquidity_wrapper_setup_found(make_ctx):
    ctx = make_ctx(
        liquidity_sweeps=[SimpleNamespace(index=5, sweep_price=95.0)],
        bos_events=[SimpleNamespace(index=7, direction=BosDirection.BULLISH, **_swing(120.0).__dict__)],
        order_blocks=[SimpleNamespace(index=6, high=105.0, low=100.0)],
    )
    r = LiquiditySetupStrategy().evaluate(ctx)
    assert r.status is SetupStatus.SETUP_FOUND
    assert r.direction is StrategyDirection.LONG
    assert r.strategy_name == "LIQUIDITY_SETUP"
