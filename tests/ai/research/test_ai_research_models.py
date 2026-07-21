import dataclasses

from ai.research.models import (
    ResearchCategory,
    ResearchPriority,
    ResearchRecord,
    ResearchStatus,
    generate_research_id,
)


def _record(**overrides):
    defaults = dict(research_id="r1", title="Liquidity Sweep Study", category=ResearchCategory.STRATEGY)
    defaults.update(overrides)
    return ResearchRecord(**defaults)


def test_research_status_has_two_members():
    assert len(list(ResearchStatus)) == 2


def test_research_status_members():
    values = {m.value for m in ResearchStatus}
    assert values == {"ACTIVE", "ARCHIVED"}


def test_research_priority_has_four_members():
    assert len(list(ResearchPriority)) == 4


def test_research_priority_members():
    values = {m.value for m in ResearchPriority}
    assert values == {"LOW", "MEDIUM", "HIGH", "CRITICAL"}


def test_research_category_has_six_members():
    assert len(list(ResearchCategory)) == 6


def test_research_category_members():
    values = {m.value for m in ResearchCategory}
    assert values == {"MARKET", "STRATEGY", "PERFORMANCE", "PORTFOLIO", "LEARNING", "GENERAL"}


def test_research_record_defaults():
    record = _record()
    assert record.priority == ResearchPriority.MEDIUM
    assert record.status == ResearchStatus.ACTIVE
    assert record.summary is None
    assert record.source_count == 0
    assert record.notes is None
    assert record.created_at == ""


def test_research_record_is_frozen():
    record = _record()
    try:
        record.title = "someone_else"
        assert False, "expected FrozenInstanceError"
    except dataclasses.FrozenInstanceError:
        pass


def test_research_record_accepts_all_fields():
    record = _record(
        priority=ResearchPriority.CRITICAL, status=ResearchStatus.ARCHIVED,
        summary="London liquidity sweeps outperform Asia session",
        source_count=5, notes="needs peer review", created_at="2026-01-01T00:00:00Z",
    )
    assert record.priority == ResearchPriority.CRITICAL
    assert record.status == ResearchStatus.ARCHIVED
    assert record.summary == "London liquidity sweeps outperform Asia session"
    assert record.source_count == 5
    assert record.notes == "needs peer review"
    assert record.created_at == "2026-01-01T00:00:00Z"


def test_research_record_field_names_match_task_2_contract():
    field_names = {f.name for f in dataclasses.fields(ResearchRecord)}
    assert field_names == {
        "research_id", "title", "category", "priority", "status",
        "summary", "source_count", "notes", "created_at",
    }


def test_research_record_research_id_title_category_required():
    field_by_name = {f.name: f for f in dataclasses.fields(ResearchRecord)}
    for required in ("research_id", "title", "category"):
        assert field_by_name[required].default is dataclasses.MISSING


def test_research_record_has_no_trading_core_object_fields():
    field_names = {f.name for f in dataclasses.fields(ResearchRecord)}
    forbidden = {"trade_decision", "risk_result", "signal_candidate", "decision", "risk", "execution"}
    assert field_names.isdisjoint(forbidden)


def test_research_record_never_carries_a_verdict_field():
    field_names = {f.name for f in dataclasses.fields(ResearchRecord)}
    forbidden = {"signal", "verdict", "direction", "buy_sell", "trade_decision", "lot_size"}
    assert field_names.isdisjoint(forbidden)


def test_research_record_never_carries_a_dataset_or_report_field():
    field_names = {f.name for f in dataclasses.fields(ResearchRecord)}
    forbidden = {"dataset", "report", "pattern", "regime", "version", "export_path"}
    assert field_names.isdisjoint(forbidden)


def test_research_record_relays_category_never_infers():
    for category in ResearchCategory:
        record = _record(category=category)
        assert record.category == category


def test_research_record_relays_priority_never_computes():
    for priority in ResearchPriority:
        record = _record(priority=priority)
        assert record.priority == priority


def test_research_record_relays_status_never_grades():
    for status in ResearchStatus:
        record = _record(status=status)
        assert record.status == status


def test_research_record_notes_relayed_verbatim():
    record = _record(notes="exact text supplied by caller")
    assert record.notes == "exact text supplied by caller"


def test_research_record_summary_relayed_verbatim():
    record = _record(summary="exact summary supplied by caller")
    assert record.summary == "exact summary supplied by caller"


def test_research_record_equality():
    a = _record()
    b = _record()
    assert a == b


def test_research_record_inequality_on_research_id():
    a = _record(research_id="r1")
    b = _record(research_id="r2")
    assert a != b


def test_research_record_priority_defaults_medium_not_critical():
    record = _record()
    assert record.priority == ResearchPriority.MEDIUM


def test_research_record_status_defaults_active_not_archived():
    record = _record()
    assert record.status == ResearchStatus.ACTIVE


def test_research_record_source_count_defaults_zero():
    record = _record()
    assert record.source_count == 0


def test_generate_research_id_returns_string():
    research_id = generate_research_id()
    assert isinstance(research_id, str)
    assert research_id != ""


def test_generate_research_id_unique():
    ids = {generate_research_id() for _ in range(20)}
    assert len(ids) == 20


def test_research_record_has_no_trading_core_object_field_type():
    """Belt-and-suspenders: no dataclass field on ResearchRecord may be typed as a Trading Core object -- every field is a primitive/enum/Optional only."""
    allowed_type_fragments = ("str", "int", "ResearchCategory", "ResearchPriority", "ResearchStatus", "Optional")
    for f in dataclasses.fields(ResearchRecord):
        type_str = str(f.type)
        assert any(fragment in type_str for fragment in allowed_type_fragments), f"ResearchRecord.{f.name}: {type_str}"
