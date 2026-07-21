import dataclasses

from ai.performance.models import (
    PerformanceCategory,
    PerformanceMetric,
    PerformanceRecord,
    generate_performance_id,
)


def _record(**overrides):
    defaults = dict(id="p1", user_id="user_1", trade_id="trade_1")
    defaults.update(overrides)
    return PerformanceRecord(**defaults)


def _metric(**overrides):
    defaults = dict(metric_name="win_rate", value=0.5, period="all")
    defaults.update(overrides)
    return PerformanceMetric(**defaults)


def test_performance_category_has_seven_members():
    assert len(list(PerformanceCategory)) == 7


def test_performance_category_members():
    values = {m.value for m in PerformanceCategory}
    assert values == {
        "ENTRY", "EXIT", "RISK", "DISCIPLINE", "TIMING", "PSYCHOLOGY", "STRATEGY",
    }


def test_performance_record_defaults():
    record = _record()
    assert record.journal_id is None
    assert record.result is None
    assert record.direction is None
    assert record.entry_quality is None
    assert record.exit_quality is None
    assert record.discipline_score is None
    assert record.risk_score is None
    assert record.confidence_score is None
    assert record.notes is None
    assert record.archived is False
    assert record.created_at == ""


def test_performance_record_is_frozen():
    record = _record()
    try:
        record.user_id = "someone_else"
        assert False, "expected FrozenInstanceError"
    except dataclasses.FrozenInstanceError:
        pass


def test_performance_record_accepts_all_fields():
    record = _record(
        journal_id="j1", result="WIN", direction="BUY", entry_quality=0.8,
        exit_quality=0.7, discipline_score=0.9, risk_score=0.6,
        confidence_score=0.75, notes="good entry", archived=True,
        created_at="2026-01-01T00:00:00Z",
    )
    assert record.journal_id == "j1"
    assert record.result == "WIN"
    assert record.direction == "BUY"
    assert record.entry_quality == 0.8
    assert record.exit_quality == 0.7
    assert record.discipline_score == 0.9
    assert record.risk_score == 0.6
    assert record.confidence_score == 0.75
    assert record.notes == "good entry"
    assert record.archived is True
    assert record.created_at == "2026-01-01T00:00:00Z"


def test_performance_record_field_names_match_task_2_contract_plus_archived():
    field_names = {f.name for f in dataclasses.fields(PerformanceRecord)}
    assert field_names == {
        "id", "user_id", "trade_id", "journal_id", "result", "direction",
        "entry_quality", "exit_quality", "discipline_score", "risk_score",
        "confidence_score", "notes", "archived", "created_at",
    }


def test_performance_record_id_user_id_trade_id_required():
    field_by_name = {f.name: f for f in dataclasses.fields(PerformanceRecord)}
    for required in ("id", "user_id", "trade_id"):
        assert field_by_name[required].default is dataclasses.MISSING


def test_performance_record_has_no_trading_core_object_fields():
    field_names = {f.name for f in dataclasses.fields(PerformanceRecord)}
    forbidden = {"trade_decision", "risk_result", "signal_candidate", "decision", "risk", "execution"}
    assert field_names.isdisjoint(forbidden)


def test_performance_record_never_carries_a_verdict_field():
    field_names = {f.name for f in dataclasses.fields(PerformanceRecord)}
    forbidden = {"signal", "verdict", "buy_sell"}
    assert field_names.isdisjoint(forbidden)


def test_performance_record_relays_result_never_computes():
    for result in ("WIN", "LOSS", "BE"):
        record = _record(result=result)
        assert record.result == result


def test_performance_record_relays_direction_never_infers():
    for direction in ("BUY", "SELL"):
        record = _record(direction=direction)
        assert record.direction == direction


def test_performance_record_notes_relayed_verbatim():
    record = _record(notes="exact text supplied by caller")
    assert record.notes == "exact text supplied by caller"


def test_performance_record_equality():
    a = _record()
    b = _record()
    assert a == b


def test_performance_record_inequality_on_id():
    a = _record(id="p1")
    b = _record(id="p2")
    assert a != b


def test_performance_record_archived_defaults_false_not_true():
    record = _record()
    assert record.archived is False


def test_performance_metric_defaults():
    metric = _metric()
    assert metric.created_at == ""


def test_performance_metric_is_frozen():
    metric = _metric()
    try:
        metric.value = 1.0
        assert False, "expected FrozenInstanceError"
    except dataclasses.FrozenInstanceError:
        pass


def test_performance_metric_field_names_match_task_2_contract():
    field_names = {f.name for f in dataclasses.fields(PerformanceMetric)}
    assert field_names == {"metric_name", "value", "period", "created_at"}


def test_performance_metric_metric_name_value_period_required():
    field_by_name = {f.name: f for f in dataclasses.fields(PerformanceMetric)}
    for required in ("metric_name", "value", "period"):
        assert field_by_name[required].default is dataclasses.MISSING


def test_performance_metric_relays_value_verbatim():
    metric = _metric(value=0.83)
    assert metric.value == 0.83


def test_performance_metric_equality():
    a = _metric()
    b = _metric()
    assert a == b


def test_performance_metric_inequality_on_metric_name():
    a = _metric(metric_name="win_rate")
    b = _metric(metric_name="discipline_score")
    assert a != b


def test_generate_performance_id_returns_string():
    performance_id = generate_performance_id()
    assert isinstance(performance_id, str)
    assert performance_id != ""


def test_generate_performance_id_unique():
    ids = {generate_performance_id() for _ in range(20)}
    assert len(ids) == 20


def test_performance_metric_and_analytics_performance_metrics_are_distinct_types():
    """docs/PHASE66_5_AUDIT.md: PerformanceMetric (singular) is not a duplicate of analytics.performance_metrics.PerformanceMetrics (plural)."""
    from analytics.performance_metrics import PerformanceMetrics

    assert PerformanceMetric is not PerformanceMetrics
    assert {f.name for f in dataclasses.fields(PerformanceMetric)} != {f.name for f in dataclasses.fields(PerformanceMetrics)}


def test_performance_record_has_no_trading_core_object_field_type():
    """Belt-and-suspenders: no dataclass field on PerformanceRecord may be typed as a Trading Core object -- every field is a primitive/Optional only."""
    allowed_type_fragments = ("str", "float", "bool", "Optional")
    for f in dataclasses.fields(PerformanceRecord):
        type_str = str(f.type)
        assert any(fragment in type_str for fragment in allowed_type_fragments), f"PerformanceRecord.{f.name}: {type_str}"
