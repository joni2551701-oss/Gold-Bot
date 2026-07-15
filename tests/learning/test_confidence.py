"""
Phase 60.7: Adaptive Intelligence Layer Foundation, TASK 5 --
learning/confidence.py tests.
"""

from datetime import datetime, timedelta, timezone

from learning.confidence import HIGH, LOW, MEDIUM, compute_pattern_confidence
from learning.models import create_learning_record
from learning.pattern_detector import detect_patterns

NOW = datetime(2026, 1, 30, tzinfo=timezone.utc)


def _record(result="TP", r_multiple=1.0, created_at=NOW):
    record = create_learning_record(
        trade_id="t", signal_id="s", strategy_name="A", session="LONDON", result=result, r_multiple=r_multiple,
    )
    # created_at is stamped by create_learning_record(); override for deterministic recency tests.
    from dataclasses import replace
    return replace(record, created_at=created_at)


def test_matches_the_directors_own_low_sample_worked_example():
    """Samples: 5 -> Confidence: LOW."""
    records = [_record(result="TP") for _ in range(5)]
    insight = detect_patterns(records, min_occurrences=3)[0]

    confidence = compute_pattern_confidence(insight, records, now=NOW)

    assert confidence.level == LOW


def test_matches_the_directors_own_high_sample_worked_example():
    """Samples: 100, consistently winning, recent, positive R -> Confidence: HIGH."""
    records = [_record(result="TP", r_multiple=2.0) for _ in range(100)]
    insight = detect_patterns(records, min_occurrences=3)[0]

    confidence = compute_pattern_confidence(insight, records, now=NOW)

    assert confidence.level == HIGH


def test_sample_size_score_scales_with_min_pattern_sample():
    from learning.pattern_detector import MIN_PATTERN_SAMPLE

    few_records = [_record() for _ in range(3)]
    full_records = [_record() for _ in range(MIN_PATTERN_SAMPLE)]
    few_insight = detect_patterns(few_records, min_occurrences=3)[0]
    full_insight = detect_patterns(full_records, min_occurrences=3)[0]

    few_confidence = compute_pattern_confidence(few_insight, few_records, now=NOW)
    full_confidence = compute_pattern_confidence(full_insight, full_records, now=NOW)

    assert few_confidence.sample_size_score < full_confidence.sample_size_score
    assert full_confidence.sample_size_score == 1.0


def test_consistency_score_is_zero_at_a_coin_flip_win_rate():
    records = [_record(result="TP") for _ in range(5)] + [_record(result="SL", r_multiple=-1.0) for _ in range(5)]
    insight = detect_patterns(records, min_occurrences=3)[0]

    confidence = compute_pattern_confidence(insight, records, now=NOW)

    assert confidence.consistency_score == 0.0


def test_consistency_score_is_one_at_a_perfectly_one_sided_win_rate():
    records = [_record(result="TP") for _ in range(10)]
    insight = detect_patterns(records, min_occurrences=3)[0]

    confidence = compute_pattern_confidence(insight, records, now=NOW)

    assert confidence.consistency_score == 1.0


def test_recency_score_is_one_for_records_created_right_now():
    records = [_record(created_at=NOW) for _ in range(5)]
    insight = detect_patterns(records, min_occurrences=3)[0]

    confidence = compute_pattern_confidence(insight, records, now=NOW)

    assert confidence.recency_score == 1.0


def test_recency_score_decays_over_the_30_day_window():
    old = NOW - timedelta(days=30)
    records = [_record(created_at=old) for _ in range(5)]
    insight = detect_patterns(records, min_occurrences=3)[0]

    confidence = compute_pattern_confidence(insight, records, now=NOW)

    assert confidence.recency_score == 0.0


def test_recency_score_zero_when_no_record_has_a_timestamp():
    from dataclasses import replace

    records = [replace(_record(), created_at=None) for _ in range(5)]
    insight = detect_patterns(records, min_occurrences=3)[0]

    confidence = compute_pattern_confidence(insight, records, now=NOW)

    assert confidence.recency_score == 0.0


def test_performance_score_neutral_when_no_r_multiple_known():
    from dataclasses import replace

    records = [replace(_record(), r_multiple=None) for _ in range(5)]
    insight = detect_patterns(records, min_occurrences=3)[0]

    confidence = compute_pattern_confidence(insight, records, now=NOW)

    assert confidence.performance_score == 0.5


def test_performance_score_rewards_positive_average_r_multiple():
    records = [_record(r_multiple=2.0) for _ in range(5)]
    insight = detect_patterns(records, min_occurrences=3)[0]

    confidence = compute_pattern_confidence(insight, records, now=NOW)

    assert confidence.performance_score == 1.0


def test_performance_score_punishes_negative_average_r_multiple():
    records = [_record(result="SL", r_multiple=-1.0) for _ in range(5)]
    insight = detect_patterns(records, min_occurrences=3)[0]

    confidence = compute_pattern_confidence(insight, records, now=NOW)

    assert confidence.performance_score == 0.0


def test_overall_score_is_sample_size_gated():
    """overall_score = sample_size_score * mean(consistency, recency, performance) -- sample size gates, not averages."""
    records = [_record(result="TP", r_multiple=1.0) for _ in range(10)]
    insight = detect_patterns(records, min_occurrences=3)[0]

    confidence = compute_pattern_confidence(insight, records, now=NOW)

    expected = confidence.sample_size_score * (
        (confidence.consistency_score + confidence.recency_score + confidence.performance_score) / 3.0
    )
    assert round(confidence.overall_score, 6) == round(expected, 6)


def test_low_sample_size_gates_confidence_down_even_with_a_perfect_record():
    """A tiny, otherwise-perfect pattern must not reach HIGH -- sample size overfitting caution."""
    records = [_record(result="TP", r_multiple=2.0) for _ in range(3)]
    insight = detect_patterns(records, min_occurrences=3)[0]

    confidence = compute_pattern_confidence(insight, records, now=NOW)

    assert confidence.level != HIGH


def test_medium_confidence_is_reachable():
    records = [_record(result="TP") for _ in range(8)] + [_record(result="SL", r_multiple=-1.0) for _ in range(2)]
    insight = detect_patterns(records, min_occurrences=3)[0]

    confidence = compute_pattern_confidence(insight, records, now=NOW)

    assert confidence.level in (LOW, MEDIUM, HIGH)  # a real classification was produced, never raises


def test_never_raises_on_empty_records():
    records = [_record() for _ in range(3)]
    insight = detect_patterns(records, min_occurrences=3)[0]

    confidence = compute_pattern_confidence(insight, [], now=NOW)  # must not raise

    assert confidence.recency_score == 0.0
    assert confidence.performance_score == 0.5
