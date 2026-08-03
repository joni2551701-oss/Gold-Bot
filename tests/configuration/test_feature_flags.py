"""
Phase A13 -- Configuration Layer tests: FeatureFlags
(configuration/feature_flags.py).
"""

import dataclasses

import pytest

from core_layer.configuration.feature_flags import FeatureFlags, DEFAULT_FLAGS


def test_default_feature_flags_are_all_false():
    flags = FeatureFlags()

    assert flags.enable_ai is False
    assert flags.enable_crypto is False
    assert flags.enable_swing is False
    assert flags.enable_ai_memory is False
    assert flags.enable_replay is False


def test_default_flags_constant_matches_defaults():
    assert DEFAULT_FLAGS == FeatureFlags()


def test_feature_flags_matches_director_example():
    flags = FeatureFlags(
        enable_ai=False,
        enable_crypto=False,
        enable_swing=False,
        enable_ai_memory=False,
    )

    assert flags.enable_ai is False
    assert flags.enable_crypto is False
    assert flags.enable_swing is False
    assert flags.enable_ai_memory is False
    assert flags.enable_replay is False  # not passed -- default still applies


def test_feature_flags_is_immutable():
    flags = FeatureFlags()
    with pytest.raises(dataclasses.FrozenInstanceError):
        flags.enable_ai = True


def test_feature_flags_toggle_support_via_replace():
    """Frozen dataclass -- 'toggling' means constructing a new object, not mutating one in place."""
    base = FeatureFlags()
    toggled = dataclasses.replace(base, enable_ai=True)

    assert base.enable_ai is False  # original untouched
    assert toggled.enable_ai is True
    # every other flag stays at its safe default
    assert toggled.enable_crypto is False
    assert toggled.enable_swing is False
    assert toggled.enable_ai_memory is False
    assert toggled.enable_replay is False


def test_feature_flags_field_names_are_exactly_the_sixteen_foundation_flags():
    """Phase 65.3 added enable_personal_ai (Personal AI Assistant, assistant/); Phase 66.0 added enable_trading_analyst (AI Trading Analyst, ai/trading_analyst/); Phase 66.1 added enable_chart_intelligence (AI Chart Intelligence, ai/chart_intelligence/); Phase 66.2 added enable_trade_journal (AI Trade Journal Intelligence, ai/trade_journal/); Phase 66.3 added enable_learning_intelligence (AI Learning Intelligence, ai/learning/); Phase 66.4 added enable_coaching_intelligence (AI Coaching Intelligence, ai/coaching/); Phase 66.5 added enable_performance_intelligence (AI Performance Intelligence, ai/performance/); Phase 66.6 added enable_strategy_intelligence (AI Strategy Intelligence, ai/strategy/); Phase 66.7 added enable_portfolio_intelligence (AI Portfolio Intelligence, ai/portfolio/); Phase 66.8 added enable_research_intelligence (AI Research Intelligence, ai/research/, the final phase of the 66.x AI Foundation sub-sequence); Phase B.0 added enable_owner_monitoring (GoldBot Core Owner Monitoring Alpha's own genuine-gap additions, monitoring/)."""
    field_names = {f.name for f in dataclasses.fields(FeatureFlags)}
    assert field_names == {
        "enable_ai", "enable_crypto", "enable_swing", "enable_ai_memory", "enable_replay",
        "enable_personal_ai", "enable_trading_analyst", "enable_chart_intelligence",
        "enable_trade_journal", "enable_learning_intelligence", "enable_coaching_intelligence",
        "enable_performance_intelligence", "enable_strategy_intelligence",
        "enable_portfolio_intelligence", "enable_research_intelligence", "enable_owner_monitoring",
    }
