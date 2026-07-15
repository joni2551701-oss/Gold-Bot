"""
Phase 60.6: Learning Loop Foundation, TASK 4 --
learning/pattern_detector.py tests.
"""

from learning.models import create_learning_record
from learning.pattern_detector import (
    HIGH_FAILURE,
    HIGH_SUCCESS,
    MIXED,
    detect_patterns,
    filter_high_failure_patterns,
    filter_high_success_patterns,
    format_pattern_insight,
)


def _record(strategy_name="Liquidity Sweep", session="NY_NEWS", market_phase=None, result="SL", failure_type=None, success_pattern=None):
    return create_learning_record(
        trade_id="t", signal_id="s", strategy_name=strategy_name, session=session,
        market_phase=market_phase, result=result, failure_type=failure_type, success_pattern=success_pattern,
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
