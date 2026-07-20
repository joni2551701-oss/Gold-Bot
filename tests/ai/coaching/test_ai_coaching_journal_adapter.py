from ai.coaching.journal_adapter import journal_entry_to_coaching_input
from ai.trade_journal.models import TradeJournalEntry


def _entry(**overrides):
    defaults = dict(
        journal_id="j1", chart_id="c1", trade_id="trade_1", symbol="XAUUSD",
        timeframe="H4", direction="BUY",
    )
    defaults.update(overrides)
    return TradeJournalEntry(**defaults)


def test_maps_trade_id_to_user_id():
    mapped = journal_entry_to_coaching_input(_entry(trade_id="trade_42"))
    assert mapped["user_id"] == "trade_42"


def test_maps_journal_id_directly():
    mapped = journal_entry_to_coaching_input(_entry(journal_id="j99"))
    assert mapped["journal_id"] == "j99"


def test_maps_lesson_to_message():
    mapped = journal_entry_to_coaching_input(_entry(lesson="wait for retest"))
    assert mapped["message"] == "wait for retest"


def test_falls_back_to_reason_when_no_lesson():
    mapped = journal_entry_to_coaching_input(_entry(lesson=None, reason="H4 BOS confirmed"))
    assert mapped["message"] == "H4 BOS confirmed"


def test_falls_back_to_empty_string_when_no_lesson_or_reason():
    mapped = journal_entry_to_coaching_input(_entry(lesson=None, reason=None))
    assert mapped["message"] == ""


def test_maps_symbol_and_direction_into_metadata():
    mapped = journal_entry_to_coaching_input(_entry(symbol="XAUUSD", direction="SELL"))
    assert mapped["metadata"] == {"symbol": "XAUUSD", "direction": "SELL"}


def test_never_returns_topic():
    """The adapter cannot infer topic from a TradeJournalEntry without real AI inference -- a caller supplies it."""
    mapped = journal_entry_to_coaching_input(_entry())
    assert "topic" not in mapped


def test_never_returns_priority_type_or_recommendation():
    mapped = journal_entry_to_coaching_input(_entry())
    assert "priority" not in mapped
    assert "type" not in mapped
    assert "recommendation" not in mapped


def test_never_raises_for_minimal_entry():
    minimal = TradeJournalEntry(
        journal_id="j", chart_id="c", trade_id="t", symbol="X", timeframe="M15", direction="WAIT",
    )
    mapped = journal_entry_to_coaching_input(minimal)
    assert mapped["user_id"] == "t"
    assert mapped["message"] == ""


def test_returns_a_plain_dict():
    mapped = journal_entry_to_coaching_input(_entry())
    assert isinstance(mapped, dict)


def test_mapping_is_deterministic():
    entry = _entry()
    assert journal_entry_to_coaching_input(entry) == journal_entry_to_coaching_input(entry)


def test_mapping_never_mutates_the_entry():
    entry = _entry(lesson="original lesson")
    journal_entry_to_coaching_input(entry)
    assert entry.lesson == "original lesson"


def test_different_entries_produce_independent_mappings():
    mapped_a = journal_entry_to_coaching_input(_entry(trade_id="t1"))
    mapped_b = journal_entry_to_coaching_input(_entry(trade_id="t2"))
    assert mapped_a["user_id"] != mapped_b["user_id"]
