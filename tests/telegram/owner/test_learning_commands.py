"""
Phase 60.6, TASK 8 -- platform_layer/telegram/owner/learning_commands.py tests. No
mocks: real LearningRecord construction, same convention as every
other platform_layer/telegram/owner/ test.
"""

from platform_layer.telegram.owner.learning_commands import (
    get_best_conditions_report,
    get_failures_report,
    get_learning_status,
    get_patterns_report,
)
from platform_layer.telegram.owner.provider_commands import ProviderCommandResult
from learning.models import create_learning_record


def _record(strategy_name="A", session="LONDON", result="SL", failure_type=None, success_pattern=None):
    return create_learning_record(
        trade_id="t", signal_id="s", strategy_name=strategy_name, session=session,
        result=result, failure_type=failure_type, success_pattern=success_pattern,
    )


def test_get_learning_status_returns_a_report():
    records = [_record(result="TP") for _ in range(3)]

    result = get_learning_status(records)

    assert isinstance(result, ProviderCommandResult)
    assert result.success is True
    assert "Last 3 trades" in result.message


def test_get_learning_status_never_raises_on_empty_input():
    result = get_learning_status([])

    assert result.success is True
    assert "Last 0 trades" in result.message


def test_get_patterns_report_returns_every_classification():
    records = (
        [_record(strategy_name="Winner", result="TP") for _ in range(3)]
        + [_record(strategy_name="Loser", result="SL") for _ in range(3)]
    )

    result = get_patterns_report(records)

    assert result.success is True
    assert "Winner" in result.message
    assert "Loser" in result.message


def test_get_patterns_report_never_raises_with_no_patterns():
    result = get_patterns_report([])

    assert result.success is True
    assert "No patterns found yet." in result.message


def test_get_failures_report_only_includes_high_failure():
    records = (
        [_record(strategy_name="Winner", result="TP") for _ in range(3)]
        + [_record(strategy_name="Loser", result="SL") for _ in range(3)]
    )

    result = get_failures_report(records)

    assert "Loser" in result.message
    assert "Winner" not in result.message


def test_get_failures_report_never_raises_with_no_failures():
    result = get_failures_report([_record(result="TP") for _ in range(3)])

    assert result.success is True
    assert "No high-failure conditions" in result.message


def test_get_best_conditions_report_only_includes_high_success():
    records = (
        [_record(strategy_name="Winner", result="TP") for _ in range(3)]
        + [_record(strategy_name="Loser", result="SL") for _ in range(3)]
    )

    result = get_best_conditions_report(records)

    assert "Winner" in result.message
    assert "Loser" not in result.message


def test_get_best_conditions_report_never_raises_with_no_successes():
    result = get_best_conditions_report([_record(result="SL") for _ in range(3)])

    assert result.success is True
    assert "No high-success conditions" in result.message
