from ai.performance.journal_adapter import journal_entry_to_performance_input
from ai.trade_journal.models import TradeJournalEntry


def _entry(**overrides):
    defaults = dict(
        journal_id="j1", chart_id="c1", trade_id="trade_1", symbol="XAUUSD",
        timeframe="H4", direction="BUY",
    )
    defaults.update(overrides)
    return TradeJournalEntry(**defaults)


def test_maps_trade_id_to_user_id():
    mapped = journal_entry_to_performance_input(_entry(trade_id="trade_42"))
    assert mapped["user_id"] == "trade_42"


def test_maps_trade_id_directly():
    mapped = journal_entry_to_performance_input(_entry(trade_id="trade_42"))
    assert mapped["trade_id"] == "trade_42"


def test_maps_journal_id_directly():
    mapped = journal_entry_to_performance_input(_entry(journal_id="j99"))
    assert mapped["journal_id"] == "j99"


def test_maps_result_directly():
    mapped = journal_entry_to_performance_input(_entry(result="WIN"))
    assert mapped["result"] == "WIN"


def test_maps_direction_directly():
    mapped = journal_entry_to_performance_input(_entry(direction="SELL"))
    assert mapped["direction"] == "SELL"


def test_maps_confidence_to_confidence_score():
    mapped = journal_entry_to_performance_input(_entry(confidence=0.85))
    assert mapped["confidence_score"] == 0.85


def test_maps_lesson_to_notes():
    mapped = journal_entry_to_performance_input(_entry(lesson="wait for retest"))
    assert mapped["notes"] == "wait for retest"


def test_falls_back_to_reason_when_no_lesson():
    mapped = journal_entry_to_performance_input(_entry(lesson=None, reason="H4 BOS confirmed"))
    assert mapped["notes"] == "H4 BOS confirmed"


def test_falls_back_to_none_when_no_lesson_or_reason():
    mapped = journal_entry_to_performance_input(_entry(lesson=None, reason=None))
    assert mapped["notes"] is None


def test_never_returns_entry_quality_exit_quality_discipline_score_risk_score():
    """The adapter cannot infer these four without real scoring -- a caller supplies them."""
    mapped = journal_entry_to_performance_input(_entry())
    assert "entry_quality" not in mapped
    assert "exit_quality" not in mapped
    assert "discipline_score" not in mapped
    assert "risk_score" not in mapped


def test_never_raises_for_minimal_entry():
    minimal = TradeJournalEntry(
        journal_id="j", chart_id="c", trade_id="t", symbol="X", timeframe="M15", direction="WAIT",
    )
    mapped = journal_entry_to_performance_input(minimal)
    assert mapped["user_id"] == "t"
    assert mapped["notes"] is None


def test_returns_a_plain_dict():
    mapped = journal_entry_to_performance_input(_entry())
    assert isinstance(mapped, dict)


def test_mapping_is_deterministic():
    entry = _entry()
    assert journal_entry_to_performance_input(entry) == journal_entry_to_performance_input(entry)


def test_mapping_never_mutates_the_entry():
    entry = _entry(lesson="original lesson")
    journal_entry_to_performance_input(entry)
    assert entry.lesson == "original lesson"


def test_different_entries_produce_independent_mappings():
    mapped_a = journal_entry_to_performance_input(_entry(trade_id="t1"))
    mapped_b = journal_entry_to_performance_input(_entry(trade_id="t2"))
    assert mapped_a["user_id"] != mapped_b["user_id"]


def test_mapped_output_is_accepted_by_performance_runtime_create():
    """Integration-shaped: the dict this adapter returns must be a valid **kwargs for PerformanceRuntime.create()."""
    from ai.access.permissions import AIRole
    from ai.performance.performance_runtime import PerformanceRuntime
    from goldbot.core_layer.configuration.feature_flags import FeatureFlags

    runtime = PerformanceRuntime(flags=FeatureFlags(enable_performance_intelligence=True))
    mapped = journal_entry_to_performance_input(_entry())
    result = runtime.create(role=AIRole.OWNER, **mapped)
    assert result is not None
    assert result.trade_id == "trade_1"
