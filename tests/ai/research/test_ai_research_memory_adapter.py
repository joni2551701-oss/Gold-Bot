from ai_layer.fundamental_ai.memory_adapter import research_reference_key
from ai_layer.fundamental_ai.models import ResearchCategory, ResearchRecord


def _record(**overrides):
    defaults = dict(research_id="r1", title="Liquidity Sweep Study", category=ResearchCategory.STRATEGY)
    defaults.update(overrides)
    return ResearchRecord(**defaults)


def test_research_reference_key_includes_research_id():
    key = research_reference_key(_record(research_id="r_123"))
    assert "r_123" in key


def test_research_reference_key_has_research_prefix():
    key = research_reference_key(_record())
    assert key.startswith("research:")


def test_research_reference_key_is_deterministic():
    record = _record()
    assert research_reference_key(record) == research_reference_key(record)


def test_research_reference_key_different_for_different_records():
    key_a = research_reference_key(_record(research_id="r1"))
    key_b = research_reference_key(_record(research_id="r2"))
    assert key_a != key_b


def test_research_reference_key_returns_string():
    assert isinstance(research_reference_key(_record()), str)


def test_research_reference_key_never_raises_for_minimal_record():
    minimal = ResearchRecord(research_id="r", title="t", category=ResearchCategory.GENERAL)
    assert research_reference_key(minimal) == "research:r"
