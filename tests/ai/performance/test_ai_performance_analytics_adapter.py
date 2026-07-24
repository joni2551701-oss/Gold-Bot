from ai.performance.analytics_adapter import performance_records_to_win_rate_metric
from ai.performance.models import PerformanceMetric, PerformanceRecord


def _record(**overrides):
    defaults = dict(id="p1", user_id="user_1", trade_id="trade_1")
    defaults.update(overrides)
    return PerformanceRecord(**defaults)


def test_returns_a_performance_metric():
    metric = performance_records_to_win_rate_metric([])
    assert isinstance(metric, PerformanceMetric)


def test_metric_name_is_win_rate():
    metric = performance_records_to_win_rate_metric([])
    assert metric.metric_name == "win_rate"


def test_empty_records_produce_zero_win_rate_not_an_exception():
    metric = performance_records_to_win_rate_metric([])
    assert metric.value == 0.0


def test_all_wins_produce_one_win_rate():
    records = [_record(id="p1", result="WIN"), _record(id="p2", result="WIN")]
    metric = performance_records_to_win_rate_metric(records)
    assert metric.value == 1.0


def test_all_losses_produce_zero_win_rate():
    records = [_record(id="p1", result="LOSS"), _record(id="p2", result="LOSS")]
    metric = performance_records_to_win_rate_metric(records)
    assert metric.value == 0.0


def test_mixed_wins_and_losses_produce_correct_ratio():
    records = [
        _record(id="p1", result="WIN"),
        _record(id="p2", result="WIN"),
        _record(id="p3", result="LOSS"),
    ]
    metric = performance_records_to_win_rate_metric(records)
    assert metric.value == 2 / 3


def test_undecided_results_are_not_counted_as_wins_or_losses():
    records = [_record(id="p1", result="BE"), _record(id="p2", result=None)]
    metric = performance_records_to_win_rate_metric(records)
    assert metric.value == 0.0


def test_period_defaults_to_all():
    metric = performance_records_to_win_rate_metric([])
    assert metric.period == "all"


def test_period_relayed_when_supplied():
    metric = performance_records_to_win_rate_metric([], period="weekly")
    assert metric.period == "weekly"


def test_created_at_is_stamped():
    metric = performance_records_to_win_rate_metric([])
    assert metric.created_at != ""


def test_never_mutates_input_records():
    records = [_record(id="p1", result="WIN")]
    performance_records_to_win_rate_metric(records)
    assert records[0].result == "WIN"


def test_never_raises_for_any_result_vocabulary():
    records = [_record(id="p1", result="unexpected_value")]
    metric = performance_records_to_win_rate_metric(records)
    assert metric.value == 0.0
