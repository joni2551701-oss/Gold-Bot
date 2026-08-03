"""
market/ facade — VolatilityLevel projection (TASK-CORE-005).

context/ exposes no standalone volatility label -- volatility only lives
inside context.market_regime's regime enum (HIGH_VOLATILITY /
LOW_VOLATILITY). This proves market/ PROJECTS the level from that regime
(a pure relabel, no new math) and is honest (UNKNOWN) when the regime
carries no volatility signal, and never fabricates EXTREME.
"""

from types import SimpleNamespace

from data_layer.live_data.market.volatility_state import VolatilityLevel


def _schema(regime):
    return SimpleNamespace(regime=regime)


def test_high_and_low_volatility_regimes_map_through():
    assert VolatilityLevel.from_context(_schema("HIGH_VOLATILITY")) is VolatilityLevel.HIGH
    assert VolatilityLevel.from_context(_schema("LOW_VOLATILITY")) is VolatilityLevel.LOW


def test_known_non_volatility_regime_is_normal():
    for regime in ("TRENDING", "RANGE", "ACCUMULATION", "DISTRIBUTION"):
        assert VolatilityLevel.from_context(_schema(regime)) is VolatilityLevel.NORMAL


def test_unknown_or_absent_regime_is_unknown():
    assert VolatilityLevel.from_context(_schema("UNKNOWN")) is VolatilityLevel.UNKNOWN
    assert VolatilityLevel.from_context(_schema(None)) is VolatilityLevel.UNKNOWN
    assert VolatilityLevel.from_context(SimpleNamespace()) is VolatilityLevel.UNKNOWN


def test_extreme_is_never_fabricated_from_todays_regime():
    for regime in ("HIGH_VOLATILITY", "LOW_VOLATILITY", "TRENDING", "RANGE", "UNKNOWN", None):
        assert VolatilityLevel.from_context(_schema(regime)) is not VolatilityLevel.EXTREME
