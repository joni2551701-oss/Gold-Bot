"""
Phase 60.6: Learning Loop Foundation, TASK 6 --
analytics/learning_report.py tests.
"""

from analytics.learning_report import build_learning_report, format_learning_report
from learning.models import create_learning_record


def _record(strategy_name, session, market_phase=None, result="SL"):
    return create_learning_record(
        trade_id="t", signal_id="s", strategy_name=strategy_name,
        session=session, market_phase=market_phase, result=result,
    )


def test_empty_input_produces_a_report_with_no_conditions():
    report = build_learning_report([])

    assert report.total_records == 0
    assert report.best_condition is None
    assert report.worst_condition is None


def test_below_min_occurrences_produces_no_conditions():
    records = [_record("A", "LONDON", result="TP"), _record("A", "LONDON", result="SL")]

    report = build_learning_report(records, min_occurrences=3)

    assert report.total_records == 2
    assert report.best_condition is None


def test_matches_the_directors_own_worked_example_shape():
    records = (
        [_record("Liquidity Sweep", "London", result="TP") for _ in range(4)]
        + [_record("Liquidity Sweep", "London", result="SL")]
        + [_record("Counter Trend", "NY_NEWS", result="SL") for _ in range(4)]
        + [_record("Counter Trend", "NY_NEWS", result="TP")]
    )

    report = build_learning_report(records, min_occurrences=3)

    assert report.total_records == 10
    assert report.best_condition.strategy_name == "Liquidity Sweep"
    assert report.best_condition.session == "London"
    assert report.worst_condition.strategy_name == "Counter Trend"
    assert report.worst_condition.session == "NY_NEWS"


def test_best_and_worst_are_the_same_when_only_one_pattern_exists():
    records = [_record("A", "LONDON", result="TP") for _ in range(3)]

    report = build_learning_report(records, min_occurrences=3)

    assert report.best_condition == report.worst_condition


def test_format_learning_report_matches_worked_example_shape():
    records = (
        [_record("Liquidity Sweep", "London", result="TP") for _ in range(3)]
        + [_record("Counter Trend", "NY_NEWS", result="SL") for _ in range(3)]
    )
    report = build_learning_report(records, min_occurrences=3)

    text = format_learning_report(report)

    assert "Last 6 trades" in text
    assert "Best condition:" in text
    assert "Worst condition:" in text
    assert "Liquidity Sweep" in text
    assert "Counter Trend" in text


def test_format_learning_report_never_raises_with_no_conditions():
    report = build_learning_report([])

    text = format_learning_report(report)  # must not raise

    assert "Last 0 trades" in text
    assert "Not enough data" in text
