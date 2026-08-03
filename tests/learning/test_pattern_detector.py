"""
Phase 60.6: Learning Loop Foundation, TASK 4 --
ai_layer/knowledge_ai/learning_loop/pattern_detector.py tests.
"""

from ai_layer.knowledge_ai.learning_loop.models import create_learning_record
from ai_layer.knowledge_ai.learning_loop.pattern_detector import (
    HIGH_FAILURE,
    HIGH_SUCCESS,
    MIN_PATTERN_SAMPLE,
    MIXED,
    detect_patterns,
    filter_high_failure_patterns,
    filter_high_success_patterns,
    format_pattern_insight,
)


def _record(
    strategy_name="Liquidity Sweep", session="NY_NEWS", market_phase=None, result="SL",
    failure_type=None, success_pattern=None, htf_bias=None, volatility_state=None,
):
    return create_learning_record(
        trade_id="t", signal_id="s", strategy_name=strategy_name, session=session,
        market_phase=market_phase, result=result, failure_type=failure_type, success_pattern=success_pattern,
        htf_bias=htf_bias, volatility_state=volatility_state,
    )


def test_empty_input_produces_empty_list():
    assert detect_patterns([]) == []


def test_group_below_min_occurrences_is_dropped():
    records = [_record(result="SL"), _record(result="SL")]  # only 2, default min_occurrences=3

    assert detect_patterns(records) == []


def test_matches_the_directors_own_loss_pattern_worked_example():
    """Liquidity Sweep + NY session, mostly losses -> HIGH_FAILURE."""
    records = (
        [_record(strategy_name="Liquidity Sweep", session="NY_NEWS", result="SL", failure_type="Against HTF Bias") for _ in range(4)]
        + [_record(strategy_name="Liquidity Sweep", session="NY_NEWS", result="TP")]
    )

    insights = detect_patterns(records, min_occurrences=3)

    assert len(insights) == 1
    insight = insights[0]
    assert insight.classification == HIGH_FAILURE
    assert insight.strategy_name == "Liquidity Sweep"
    assert insight.session == "NY_NEWS"
    assert insight.example_failure_type == "Against HTF Bias"


def test_matches_the_directors_own_win_pattern_worked_example():
    """HTF aligned + OB reaction + FVG fill, mostly wins -> HIGH_SUCCESS."""
    records = [
        _record(strategy_name="OB Strategy", session="LONDON", result="TP", success_pattern="HTF aligned + OB reaction + FVG fill")
        for _ in range(5)
    ]

    insights = detect_patterns(records, min_occurrences=3)

    assert insights[0].classification == HIGH_SUCCESS
    assert insights[0].example_success_pattern == "HTF aligned + OB reaction + FVG fill"


def test_mixed_results_classified_as_mixed():
    records = (
        [_record(result="TP") for _ in range(2)]
        + [_record(result="SL") for _ in range(2)]
    )

    insights = detect_patterns(records, min_occurrences=3)

    assert insights[0].classification == MIXED


def test_records_without_strategy_name_are_skipped():
    records = [_record(strategy_name=None, result="SL") for _ in range(5)]

    assert detect_patterns(records) == []


def test_groups_are_keyed_by_strategy_session_and_market_phase():
    records = (
        [_record(strategy_name="A", session="LONDON", market_phase="MARKUP", result="TP") for _ in range(3)]
        + [_record(strategy_name="A", session="LONDON", market_phase="MARKDOWN", result="SL") for _ in range(3)]
    )

    insights = detect_patterns(records, min_occurrences=3)

    assert len(insights) == 2
    phases = {insight.market_phase for insight in insights}
    assert phases == {"MARKUP", "MARKDOWN"}


def test_filter_high_failure_and_high_success_patterns():
    records = (
        [_record(strategy_name="Loser", result="SL") for _ in range(3)]
        + [_record(strategy_name="Winner", result="TP") for _ in range(3)]
    )

    insights = detect_patterns(records, min_occurrences=3)
    failures = filter_high_failure_patterns(insights)
    successes = filter_high_success_patterns(insights)

    assert {i.strategy_name for i in failures} == {"Loser"}
    assert {i.strategy_name for i in successes} == {"Winner"}


def test_format_pattern_insight_matches_worked_example_shape():
    records = [_record(strategy_name="Liquidity Sweep", session="NY_NEWS", result="SL") for _ in range(3)]
    insight = detect_patterns(records, min_occurrences=3)[0]

    text = format_pattern_insight(insight)

    assert "Liquidity Sweep + NY_NEWS -> High failure probability" in text
    assert "Occurrences: 3" in text


def test_never_raises_on_records_missing_session_and_market_phase():
    records = [_record(session=None, market_phase=None, result="SL") for _ in range(3)]

    insights = detect_patterns(records, min_occurrences=3)  # must not raise

    assert insights[0].session is None
    assert insights[0].market_phase is None


# --- Phase 60.7 TASK 4: Advanced Pattern Detector ---

def test_min_pattern_sample_constant_matches_the_directors_own_value():
    assert MIN_PATTERN_SAMPLE == 20


def test_groups_are_further_split_by_htf_bias():
    """Same strategy/session/market_phase but different htf_bias must NOT be merged into one group."""
    records = (
        [_record(strategy_name="A", session="LONDON", htf_bias="BULLISH", result="TP") for _ in range(3)]
        + [_record(strategy_name="A", session="LONDON", htf_bias="BEARISH", result="SL") for _ in range(3)]
    )

    insights = detect_patterns(records, min_occurrences=3)

    assert len(insights) == 2
    biases = {insight.htf_bias for insight in insights}
    assert biases == {"BULLISH", "BEARISH"}


def test_groups_are_further_split_by_volatility_state():
    records = (
        [_record(strategy_name="A", volatility_state="HIGH_VOLATILITY", result="TP") for _ in range(3)]
        + [_record(strategy_name="A", volatility_state="LOW_VOLATILITY", result="SL") for _ in range(3)]
    )

    insights = detect_patterns(records, min_occurrences=3)

    assert len(insights) == 2
    states = {insight.volatility_state for insight in insights}
    assert states == {"HIGH_VOLATILITY", "LOW_VOLATILITY"}


def test_phase_606_shaped_records_group_identically_to_before():
    """Records with no htf_bias/volatility_state (Phase 60.6 shape) must group exactly as before -- backward-compatible."""
    records = (
        [_record(strategy_name="Liquidity Sweep", session="NY_NEWS", result="SL", failure_type="Against HTF Bias") for _ in range(4)]
        + [_record(strategy_name="Liquidity Sweep", session="NY_NEWS", result="TP")]
    )

    insights = detect_patterns(records, min_occurrences=3)

    assert len(insights) == 1
    assert insights[0].classification == HIGH_FAILURE
    assert insights[0].htf_bias is None
    assert insights[0].volatility_state is None


def test_format_pattern_insight_includes_htf_bias_and_volatility_state():
    records = [
        _record(strategy_name="Liquidity Sweep", session="NY_NEWS", htf_bias="BEARISH",
                volatility_state="HIGH_VOLATILITY", result="SL")
        for _ in range(3)
    ]
    insight = detect_patterns(records, min_occurrences=3)[0]

    text = format_pattern_insight(insight)

    assert "Liquidity Sweep + NY_NEWS + BEARISH + HIGH_VOLATILITY -> High failure probability" in text
