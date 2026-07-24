from ai.trade_journal.memory_adapter import memory_reference_key
from ai.trade_journal.models import TradeJournalEntry


def _entry(**overrides):
    defaults = dict(
        journal_id="journal_123", chart_id="chart_1", trade_id="trade_1",
        symbol="XAUUSD", timeframe="H4", direction="BUY",
    )
    defaults.update(overrides)
    return TradeJournalEntry(**defaults)


def test_memory_reference_key_includes_journal_id():
    key = memory_reference_key(_entry(journal_id="journal_123"))
    assert "journal_123" in key


def test_memory_reference_key_has_trade_journal_prefix():
    key = memory_reference_key(_entry())
    assert key.startswith("trade_journal:")


def test_memory_reference_key_is_deterministic():
    entry = _entry()
    assert memory_reference_key(entry) == memory_reference_key(entry)


def test_memory_reference_key_different_for_different_entries():
    key_a = memory_reference_key(_entry(journal_id="j1"))
    key_b = memory_reference_key(_entry(journal_id="j2"))
    assert key_a != key_b


def test_memory_reference_key_returns_string():
    assert isinstance(memory_reference_key(_entry()), str)


def test_memory_reference_key_never_raises_for_minimal_entry():
    minimal = TradeJournalEntry(
        journal_id="j", chart_id="c", trade_id="t", symbol="X", timeframe="M15", direction="WAIT",
    )
    assert memory_reference_key(minimal) == "trade_journal:j"
