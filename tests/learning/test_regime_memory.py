"""
Phase 60.7: Adaptive Intelligence Layer Foundation, TASK 7 --
learning/regime_memory.py tests.
"""

from datetime import datetime, timedelta, timezone

from context_layer.context_engine.context_orchestrator import ContextSnapshot
from context_layer.trend.market_regime import MarketRegime, MarketRegimeResult, RegimeDirection
from learning.regime_memory import (
    REGIME_HIGH_VOLATILITY,
    REGIME_LOW_VOLATILITY,
    REGIME_NEWS_EVENT,
    REGIME_RANGE,
    REGIME_TRENDING,
    RegimeMemory,
    RegimeObservation,
    format_regime_summary,
    record_from_context,
)

NOW = datetime(2026, 1, 1, tzinfo=timezone.utc)


def _context(regime: MarketRegime) -> ContextSnapshot:
    return ContextSnapshot(
        candles=(), structure=(), bos_events=(), choch_events=(),
        liquidity_zones=(), liquidity_sweeps=(), order_blocks=(), fair_value_gaps=(),
        amd_events=(), wyckoff_events=(), session_events=(),
        market_regime=MarketRegimeResult(regime=regime, direction=RegimeDirection.NEUTRAL, confidence=0.0, reasons=[]),
    )


def test_record_appends_and_returns_an_observation():
    memory = RegimeMemory()

    observation = memory.record(REGIME_TRENDING, session="LONDON", observed_at=NOW)

    assert isinstance(observation, RegimeObservation)
    assert observation.regime == REGIME_TRENDING
    assert observation.session == "LONDON"
    assert memory.all() == [observation]


def test_record_accepts_news_event_even_though_no_detector_exists():
    memory = RegimeMemory()

    observation = memory.record(REGIME_NEWS_EVENT, notes="FOMC statement", observed_at=NOW)

    assert observation.regime == REGIME_NEWS_EVENT
    assert observation.notes == "FOMC statement"


def test_count_by_regime_tallies_correctly():
    memory = RegimeMemory()
    memory.record(REGIME_TRENDING, observed_at=NOW)
    memory.record(REGIME_TRENDING, observed_at=NOW)
    memory.record(REGIME_RANGE, observed_at=NOW)

    counts = memory.count_by_regime()

    assert counts == {REGIME_TRENDING: 2, REGIME_RANGE: 1}


def test_most_recent_returns_newest_first():
    memory = RegimeMemory()
    memory.record(REGIME_TRENDING, observed_at=NOW)
    memory.record(REGIME_RANGE, observed_at=NOW + timedelta(hours=1))
    memory.record(REGIME_HIGH_VOLATILITY, observed_at=NOW + timedelta(hours=2))

    recent = memory.most_recent(limit=2)

    assert [o.regime for o in recent] == [REGIME_HIGH_VOLATILITY, REGIME_RANGE]


def test_empty_memory_produces_no_observations():
    memory = RegimeMemory()

    assert memory.all() == []
    assert memory.count_by_regime() == {}
    assert memory.most_recent() == []


def test_record_from_context_relays_trending():
    memory = RegimeMemory()
    context = _context(MarketRegime.TRENDING)

    observation = record_from_context(memory, context, session="LONDON")

    assert observation.regime == REGIME_TRENDING
    assert observation.session == "LONDON"


def test_record_from_context_relays_all_four_covered_regimes():
    memory = RegimeMemory()

    for regime, label in (
        (MarketRegime.TRENDING, REGIME_TRENDING),
        (MarketRegime.RANGE, REGIME_RANGE),
        (MarketRegime.HIGH_VOLATILITY, REGIME_HIGH_VOLATILITY),
        (MarketRegime.LOW_VOLATILITY, REGIME_LOW_VOLATILITY),
    ):
        observation = record_from_context(memory, _context(regime))
        assert observation.regime == label


def test_record_from_context_returns_none_for_uncovered_regimes():
    memory = RegimeMemory()

    for regime in (MarketRegime.ACCUMULATION, MarketRegime.DISTRIBUTION, MarketRegime.UNKNOWN):
        observation = record_from_context(memory, _context(regime))
        assert observation is None

    assert memory.all() == []


def test_format_regime_summary_matches_expected_shape():
    memory = RegimeMemory()
    memory.record(REGIME_TRENDING, observed_at=NOW)
    memory.record(REGIME_TRENDING, observed_at=NOW)
    memory.record(REGIME_RANGE, observed_at=NOW)

    summary = format_regime_summary(memory)

    assert summary[0] == "TRENDING: 2 observation(s)"
    assert "RANGE: 1 observation(s)" in summary


def test_format_regime_summary_empty_for_empty_memory():
    memory = RegimeMemory()

    assert format_regime_summary(memory) == []


def test_format_regime_summary_feeds_directly_into_learning_context():
    from ai.learning_context import build_learning_context

    memory = RegimeMemory()
    memory.record(REGIME_TRENDING, observed_at=NOW)

    context = build_learning_context([], regimes=format_regime_summary(memory))

    assert context.regimes == ["TRENDING: 1 observation(s)"]
