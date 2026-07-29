"""
market/ facade — RegimeState projection (TASK-CORE-005).

Proves the regime view copies context.market_regime's already-classified
label through unchanged (never re-derived), and exposes advisory
convenience flags -- it is market context, NOT a strategy choice.
"""

from types import SimpleNamespace

from market.regime_state import RegimeState


def _schema(regime):
    return SimpleNamespace(regime=regime)


def test_regime_copied_through_and_normalised():
    st = RegimeState.from_context(_schema("trending"))
    assert st.regime == "TRENDING"
    assert st.is_trending is True
    assert st.is_ranging is False
    assert st.is_known is True


def test_range_flags():
    st = RegimeState.from_context(_schema("RANGE"))
    assert st.is_ranging is True
    assert st.is_trending is False


def test_absent_regime_is_unknown():
    st = RegimeState.from_context(SimpleNamespace())
    assert st.regime == "UNKNOWN"
    assert st.is_known is False


def test_none_regime_is_unknown():
    st = RegimeState.from_context(_schema(None))
    assert st.regime == "UNKNOWN"
    assert st.is_known is False
