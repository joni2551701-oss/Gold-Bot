from ai_layer.knowledge_ai.learning_engine.journal_adapter import journal_entry_to_learning_input
from ai_layer.knowledge_ai.learning_engine.models import LearningSource
from ai_layer.knowledge_ai.knowledge_base.trade_journal.models import TradeJournalEntry


def _entry(**overrides):
    defaults = dict(
        journal_id="j1", chart_id="c1", trade_id="trade_1", symbol="XAUUSD",
        timeframe="H4", direction="BUY",
    )
    defaults.update(overrides)
    return TradeJournalEntry(**defaults)


def test_maps_trade_id_to_user_id():
    mapped = journal_entry_to_learning_input(_entry(trade_id="trade_42"))
    assert mapped["user_id"] == "trade_42"


def test_maps_confidence_directly():
    mapped = journal_entry_to_learning_input(_entry(confidence=0.7))
    assert mapped["confidence"] == 0.7


def test_maps_lesson_to_notes():
    mapped = journal_entry_to_learning_input(_entry(lesson="wait for retest"))
    assert mapped["notes"] == "wait for retest"


def test_falls_back_to_reason_when_no_lesson():
    mapped = journal_entry_to_learning_input(_entry(lesson=None, reason="H4 BOS confirmed"))
    assert mapped["notes"] == "H4 BOS confirmed"


def test_source_is_always_journal():
    mapped = journal_entry_to_learning_input(_entry())
    assert mapped["source"] == LearningSource.JOURNAL


def test_never_returns_topic_or_level():
    """The adapter cannot infer topic/level without real AI inference (Rule 10) -- a caller supplies those."""
    mapped = journal_entry_to_learning_input(_entry())
    assert "topic" not in mapped
    assert "level" not in mapped


def test_never_raises_for_minimal_entry():
    minimal = TradeJournalEntry(
        journal_id="j", chart_id="c", trade_id="t", symbol="X", timeframe="M15", direction="WAIT",
    )
    mapped = journal_entry_to_learning_input(minimal)
    assert mapped["user_id"] == "t"
    assert mapped["notes"] is None
    assert mapped["confidence"] is None


def test_returns_a_plain_dict():
    mapped = journal_entry_to_learning_input(_entry())
    assert isinstance(mapped, dict)


def test_mapping_is_deterministic():
    entry = _entry()
    assert journal_entry_to_learning_input(entry) == journal_entry_to_learning_input(entry)


def test_mapping_never_mutates_the_entry():
    entry = _entry(lesson="original lesson")
    journal_entry_to_learning_input(entry)
    assert entry.lesson == "original lesson"


def test_different_entries_produce_independent_mappings():
    mapped_a = journal_entry_to_learning_input(_entry(trade_id="t1"))
    mapped_b = journal_entry_to_learning_input(_entry(trade_id="t2"))
    assert mapped_a["user_id"] != mapped_b["user_id"]
