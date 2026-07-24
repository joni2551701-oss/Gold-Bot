from ai.research.models import ResearchCategory
from ai.research.strategy_adapter import strategy_record_to_research_input
from ai.strategy.models import StrategyRecord, StrategyType


def _record(**overrides):
    defaults = dict(strategy_id="s1", strategy_name="Liquidity Sweep", strategy_type=StrategyType.LIQUIDITY_SWEEP)
    defaults.update(overrides)
    return StrategyRecord(**defaults)


def test_maps_category_to_strategy():
    mapped = strategy_record_to_research_input(_record())
    assert mapped["category"] == ResearchCategory.STRATEGY


def test_maps_notes_directly():
    mapped = strategy_record_to_research_input(_record(notes="works well in London session"))
    assert mapped["notes"] == "works well in London session"


def test_none_notes_relayed_as_none():
    mapped = strategy_record_to_research_input(_record(notes=None))
    assert mapped["notes"] is None


def test_never_returns_title_priority_status_summary_source_count():
    mapped = strategy_record_to_research_input(_record())
    assert "title" not in mapped
    assert "priority" not in mapped
    assert "status" not in mapped
    assert "summary" not in mapped
    assert "source_count" not in mapped


def test_never_raises_for_minimal_record():
    minimal = StrategyRecord(strategy_id="s", strategy_name="n", strategy_type=StrategyType.CUSTOM)
    mapped = strategy_record_to_research_input(minimal)
    assert mapped["category"] == ResearchCategory.STRATEGY
    assert mapped["notes"] is None


def test_returns_a_plain_dict():
    mapped = strategy_record_to_research_input(_record())
    assert isinstance(mapped, dict)


def test_mapping_is_deterministic():
    record = _record()
    assert strategy_record_to_research_input(record) == strategy_record_to_research_input(record)


def test_mapping_never_mutates_the_record():
    record = _record(notes="original notes")
    strategy_record_to_research_input(record)
    assert record.notes == "original notes"


def test_different_records_produce_independent_mappings():
    mapped_a = strategy_record_to_research_input(_record(notes="a"))
    mapped_b = strategy_record_to_research_input(_record(notes="b"))
    assert mapped_a["notes"] != mapped_b["notes"]


def test_category_always_strategy_regardless_of_strategy_type():
    mapped_a = strategy_record_to_research_input(_record(strategy_type=StrategyType.FVG))
    mapped_b = strategy_record_to_research_input(_record(strategy_type=StrategyType.WYCKOFF))
    assert mapped_a["category"] == mapped_b["category"] == ResearchCategory.STRATEGY
