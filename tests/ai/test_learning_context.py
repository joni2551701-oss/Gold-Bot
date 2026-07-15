"""
Phase 60.6: Learning Loop Foundation, TASK 7 --
ai/learning_context.py tests.
"""

from ai.learning_context import LearningContext, build_learning_context
from learning.models import create_learning_record


def _record(strategy_name="A", session="LONDON", result="SL", failure_type=None, success_pattern=None):
    return create_learning_record(
        trade_id="t", signal_id="s", strategy_name=strategy_name, session=session,
        result=result, failure_type=failure_type, success_pattern=success_pattern,
    )


def test_empty_input_produces_an_all_empty_context():
    context = build_learning_context([])

    assert isinstance(context, LearningContext)
    assert context.recent_failures == []
    assert context.successful_patterns == []
    assert context.strategy_stats == []


def test_recent_failures_relayed_directly():
    records = [
        _record(result="SL", failure_type="No HTF confirmation"),
        _record(result="TP"),  # no failure_type, excluded
    ]

    context = build_learning_context(records)

    assert context.recent_failures == ["No HTF confirmation"]


def test_recent_failures_respects_limit():
    records = [_record(result="SL", failure_type=f"reason {i}") for i in range(10)]

    context = build_learning_context(records, limit=3)

    assert len(context.recent_failures) == 3


def test_successful_patterns_only_include_high_success_classification():
    records = (
        [_record(strategy_name="Winner", session="LONDON", result="TP") for _ in range(3)]
        + [_record(strategy_name="Loser", session="NY_NEWS", result="SL") for _ in range(3)]
    )

    context = build_learning_context(records)

    assert len(context.successful_patterns) == 1
    assert "Winner" in context.successful_patterns[0]
    assert "Loser" not in "".join(context.successful_patterns)


def test_strategy_stats_reports_win_rate_per_strategy():
    records = (
        [_record(strategy_name="A", result="TP") for _ in range(3)]
        + [_record(strategy_name="A", result="SL")]
    )

    context = build_learning_context(records)

    assert context.strategy_stats == ["A: 75%"]


def test_strategy_stats_skips_strategies_with_no_decided_trades():
    records = [_record(strategy_name="A", result="EXPIRED")]

    context = build_learning_context(records)

    assert context.strategy_stats == []


def test_to_dict_matches_the_directors_own_phase_606_json_shape():
    records = [_record(result="SL", failure_type="No HTF confirmation")]

    context = build_learning_context(records)
    data = context.to_dict()

    assert {"recent_failures", "successful_patterns", "strategy_stats"} <= set(data.keys())

    import json
    json.dumps(data)  # must not raise


def test_to_dict_includes_the_phase_607_fields():
    records = [_record(result="SL", failure_type="No HTF confirmation")]

    context = build_learning_context(records)
    data = context.to_dict()

    assert set(data.keys()) == {
        "recent_failures", "successful_patterns", "strategy_stats",
        "patterns", "failures", "regimes", "confidence",
    }


def test_never_raises_on_records_with_no_strategy_name():
    records = [_record(strategy_name=None, result="SL", failure_type="x")]

    build_learning_context(records)  # must not raise


def test_precomputed_patterns_can_be_supplied_directly():
    from learning.pattern_detector import detect_patterns

    records = [_record(strategy_name="Winner", session="LONDON", result="TP") for _ in range(3)]
    patterns = detect_patterns(records)

    context = build_learning_context(records, patterns=patterns)

    assert len(context.successful_patterns) == 1


# --- Phase 60.7 TASK 6: AI Memory Adapter ---

def test_patterns_field_includes_every_classification():
    records = (
        [_record(strategy_name="Winner", session="LONDON", result="TP") for _ in range(3)]
        + [_record(strategy_name="Loser", session="NY_NEWS", result="SL") for _ in range(3)]
    )

    context = build_learning_context(records)

    assert len(context.patterns) == 2
    joined = " ".join(context.patterns)
    assert "Winner" in joined
    assert "Loser" in joined


def test_failures_field_only_includes_high_failure_patterns():
    records = (
        [_record(strategy_name="Winner", session="LONDON", result="TP") for _ in range(3)]
        + [_record(strategy_name="Loser", session="NY_NEWS", result="SL") for _ in range(3)]
    )

    context = build_learning_context(records)

    assert len(context.failures) == 1
    assert "Loser" in context.failures[0]
    assert "Winner" not in "".join(context.failures)


def test_regimes_field_defaults_to_empty_and_relays_when_supplied():
    records = [_record(result="TP")]

    default_context = build_learning_context(records)
    with_regimes = build_learning_context(records, regimes=["TRENDING: 5 days", "RANGE: 2 days"])

    assert default_context.regimes == []
    assert with_regimes.regimes == ["TRENDING: 5 days", "RANGE: 2 days"]


def test_confidence_field_has_one_entry_per_pattern():
    records = (
        [_record(strategy_name="Winner", session="LONDON", result="TP") for _ in range(3)]
        + [_record(strategy_name="Loser", session="NY_NEWS", result="SL") for _ in range(3)]
    )

    context = build_learning_context(records)

    assert len(context.confidence) == 2
    for entry in context.confidence:
        assert entry.split(": ")[-1] in ("LOW", "MEDIUM", "HIGH")


def test_confidence_field_empty_when_no_patterns():
    context = build_learning_context([])

    assert context.confidence == []
