from ai.strategy.journal_adapter import journal_entry_to_strategy_input
from ai.trade_journal.models import TradeJournalEntry


def _entry(**overrides):
    defaults = dict(
        journal_id="j1", chart_id="c1", trade_id="trade_1", symbol="XAUUSD",
        timeframe="H4", direction="BUY",
    )
    defaults.update(overrides)
    return TradeJournalEntry(**defaults)


def test_maps_lesson_to_notes():
    mapped = journal_entry_to_strategy_input(_entry(lesson="wait for retest"))
    assert mapped["notes"] == "wait for retest"


def test_falls_back_to_reason_when_no_lesson():
    mapped = journal_entry_to_strategy_input(_entry(lesson=None, reason="H4 BOS confirmed"))
    assert mapped["notes"] == "H4 BOS confirmed"


def test_falls_back_to_none_when_no_lesson_or_reason():
    mapped = journal_entry_to_strategy_input(_entry(lesson=None, reason=None))
    assert mapped["notes"] is None


def test_never_returns_strategy_name_type_or_version():
    """The adapter cannot infer strategy identity from a TradeJournalEntry without real inference -- a caller supplies it."""
    mapped = journal_entry_to_strategy_input(_entry())
    assert "strategy_name" not in mapped
    assert "strategy_type" not in mapped
    assert "strategy_version" not in mapped


def test_never_returns_confidence():
    """TradeJournalEntry.confidence is per-trade, not per-strategy -- relaying it would be inference."""
    mapped = journal_entry_to_strategy_input(_entry(confidence=0.9))
    assert "confidence" not in mapped


def test_never_returns_status():
    mapped = journal_entry_to_strategy_input(_entry())
    assert "status" not in mapped


def test_never_raises_for_minimal_entry():
    minimal = TradeJournalEntry(
        journal_id="j", chart_id="c", trade_id="t", symbol="X", timeframe="M15", direction="WAIT",
    )
    mapped = journal_entry_to_strategy_input(minimal)
    assert mapped["notes"] is None


def test_returns_a_plain_dict():
    mapped = journal_entry_to_strategy_input(_entry())
    assert isinstance(mapped, dict)


def test_mapping_is_deterministic():
    entry = _entry()
    assert journal_entry_to_strategy_input(entry) == journal_entry_to_strategy_input(entry)


def test_mapping_never_mutates_the_entry():
    entry = _entry(lesson="original lesson")
    journal_entry_to_strategy_input(entry)
    assert entry.lesson == "original lesson"


def test_different_entries_produce_independent_mappings():
    mapped_a = journal_entry_to_strategy_input(_entry(lesson="a"))
    mapped_b = journal_entry_to_strategy_input(_entry(lesson="b"))
    assert mapped_a["notes"] != mapped_b["notes"]


def test_mapped_output_is_accepted_by_strategy_runtime_create():
    """Integration-shaped: the dict this adapter returns must be a valid **kwargs (plus required fields) for StrategyRuntime.create()."""
    from ai.access.permissions import AIRole
    from ai.strategy.models import StrategyType
    from ai.strategy.strategy_runtime import StrategyRuntime
    from configuration.feature_flags import FeatureFlags

    runtime = StrategyRuntime(flags=FeatureFlags(enable_strategy_intelligence=True))
    mapped = journal_entry_to_strategy_input(_entry(lesson="wait for retest"))
    result = runtime.create(
        strategy_name="Liquidity Sweep", strategy_type=StrategyType.LIQUIDITY_SWEEP, role=AIRole.OWNER, **mapped,
    )
    assert result is not None
    assert result.notes == "wait for retest"
