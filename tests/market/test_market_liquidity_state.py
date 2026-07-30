"""
market/ facade — LiquidityState projection (TASK-CORE-005).

Proves the liquidity view reads context.liquidity (sweep_detected +
liquidity_type) and derives buy/sell-side presence booleans without
running any liquidity detection of its own.
"""

from types import SimpleNamespace

from market.liquidity_state import LiquidityState


def test_buy_side_sweep():
    schema = SimpleNamespace(liquidity=SimpleNamespace(
        sweep_detected=True, liquidity_type="BUY_SIDE_LIQUIDITY"))
    st = LiquidityState.from_context(schema)
    assert st.sweep_detected is True
    assert st.liquidity_type == "BUY_SIDE_LIQUIDITY"
    assert st.buy_side is True
    assert st.sell_side is False


def test_sell_side_sweep():
    schema = SimpleNamespace(liquidity=SimpleNamespace(
        sweep_detected=True, liquidity_type="SELL_SIDE_LIQUIDITY"))
    st = LiquidityState.from_context(schema)
    assert st.sell_side is True
    assert st.buy_side is False


def test_no_liquidity_is_empty_state():
    st = LiquidityState.from_context(SimpleNamespace())
    assert st == LiquidityState()
    assert st.sweep_detected is False
    assert st.liquidity_type is None
    assert st.buy_side is False and st.sell_side is False


def test_none_group_does_not_raise():
    st = LiquidityState.from_context(SimpleNamespace(liquidity=None))
    assert st == LiquidityState()
