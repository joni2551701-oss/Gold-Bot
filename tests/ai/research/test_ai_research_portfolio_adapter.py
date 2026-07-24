from ai.portfolio.models import PortfolioRecord
from ai.research.models import ResearchCategory
from ai.research.portfolio_adapter import portfolio_record_to_research_input


def _record(**overrides):
    defaults = dict(portfolio_id="p1", portfolio_name="Main Portfolio")
    defaults.update(overrides)
    return PortfolioRecord(**defaults)


def test_maps_category_to_portfolio():
    mapped = portfolio_record_to_research_input(_record())
    assert mapped["category"] == ResearchCategory.PORTFOLIO


def test_maps_notes_directly():
    mapped = portfolio_record_to_research_input(_record(notes="rebalancing needed"))
    assert mapped["notes"] == "rebalancing needed"


def test_none_notes_relayed_as_none():
    mapped = portfolio_record_to_research_input(_record(notes=None))
    assert mapped["notes"] is None


def test_never_returns_title_priority_status_summary_source_count():
    mapped = portfolio_record_to_research_input(_record())
    assert "title" not in mapped
    assert "priority" not in mapped
    assert "status" not in mapped
    assert "summary" not in mapped
    assert "source_count" not in mapped


def test_never_raises_for_minimal_record():
    minimal = PortfolioRecord(portfolio_id="p", portfolio_name="n")
    mapped = portfolio_record_to_research_input(minimal)
    assert mapped["category"] == ResearchCategory.PORTFOLIO
    assert mapped["notes"] is None


def test_returns_a_plain_dict():
    mapped = portfolio_record_to_research_input(_record())
    assert isinstance(mapped, dict)


def test_mapping_is_deterministic():
    record = _record()
    assert portfolio_record_to_research_input(record) == portfolio_record_to_research_input(record)


def test_mapping_never_mutates_the_record():
    record = _record(notes="original notes")
    portfolio_record_to_research_input(record)
    assert record.notes == "original notes"


def test_different_records_produce_independent_mappings():
    mapped_a = portfolio_record_to_research_input(_record(notes="a"))
    mapped_b = portfolio_record_to_research_input(_record(notes="b"))
    assert mapped_a["notes"] != mapped_b["notes"]


def test_category_always_portfolio_regardless_of_content():
    from ai.portfolio.models import PortfolioRiskLevel

    mapped_a = portfolio_record_to_research_input(_record(risk_level=PortfolioRiskLevel.LOW))
    mapped_b = portfolio_record_to_research_input(_record(risk_level=PortfolioRiskLevel.CRITICAL))
    assert mapped_a["category"] == mapped_b["category"] == ResearchCategory.PORTFOLIO
