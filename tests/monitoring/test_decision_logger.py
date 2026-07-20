"""GoldBot Core Owner Monitoring Alpha, TASK 5 -- monitoring/decision_logger.py tests."""

from unittest.mock import MagicMock

from database.monitoring_models import create_decision_pipeline_entry_row
from monitoring.decision_logger import DecisionLogger
from monitoring.models import DecisionPipelineEntry


def _repository(row=None, rows=None):
    repository = MagicMock()
    repository.record_decision_entry.return_value = row or create_decision_pipeline_entry_row(
        "XAUUSD", "M15", ("STRUCTURE_ALIGNED",), 5, "NO TRADE",
    )
    repository.get_recent_decision_entries.return_value = rows or []
    return repository


def test_log_entry_returns_decision_pipeline_entry():
    logger = DecisionLogger(repository=_repository())
    entry = logger.log_entry("XAUUSD", "M15", ["STRUCTURE_ALIGNED"], 5, "NO TRADE")
    assert isinstance(entry, DecisionPipelineEntry)


def test_log_entry_relays_symbol_and_timeframe():
    logger = DecisionLogger(repository=_repository())
    entry = logger.log_entry("XAUUSD", "M15", ["STRUCTURE_ALIGNED"], 5, "NO TRADE")
    assert entry.symbol == "XAUUSD"
    assert entry.timeframe == "M15"


def test_log_entry_relays_criteria_met():
    row = create_decision_pipeline_entry_row("XAUUSD", "M15", ("STRUCTURE_ALIGNED", "LIQUIDITY_SWEPT"), 5, "BUY")
    logger = DecisionLogger(repository=_repository(row=row))
    entry = logger.log_entry("XAUUSD", "M15", ["STRUCTURE_ALIGNED", "LIQUIDITY_SWEPT"], 5, "BUY")
    assert entry.criteria_met == ("STRUCTURE_ALIGNED", "LIQUIDITY_SWEPT")


def test_log_entry_relays_decision_and_reason():
    row = create_decision_pipeline_entry_row("XAUUSD", "M15", (), 5, "NO TRADE", reason="FVG failed")
    logger = DecisionLogger(repository=_repository(row=row))
    entry = logger.log_entry("XAUUSD", "M15", [], 5, "NO TRADE", reason="FVG failed")
    assert entry.decision == "NO TRADE"
    assert entry.reason == "FVG failed"

def test_log_entry_never_raises_on_database_failure():
    repository = MagicMock()
    repository.record_decision_entry.side_effect = Exception("boom")
    logger = DecisionLogger(repository=repository)
    result = logger.log_entry("XAUUSD", "M15", [], 5, "NO TRADE")
    assert result is None


def test_log_entry_never_computes_a_decision_of_its_own():
    """This module only relays an already-made decision -- it never generates one."""
    logger = DecisionLogger(repository=_repository())
    entry = logger.log_entry("XAUUSD", "M15", [], 0, "already-decided-by-caller")
    assert entry.decision == "NO TRADE"  # relayed from the mocked repository row, unmodified


def test_get_recent_entries_returns_sequence():
    logger = DecisionLogger(repository=_repository())
    entries = logger.get_recent_entries()
    assert isinstance(entries, tuple)


def test_get_recent_entries_empty_when_nothing_recorded():
    logger = DecisionLogger(repository=_repository(rows=[]))
    entries = logger.get_recent_entries()
    assert entries == ()


def test_get_recent_entries_relays_rows():
    row = create_decision_pipeline_entry_row("XAUUSD", "H4", ("HTF_ALIGNED",), 5, "SELL")
    logger = DecisionLogger(repository=_repository(rows=[row]))
    entries = logger.get_recent_entries()
    assert len(entries) == 1
    assert entries[0].symbol == "XAUUSD"
    assert entries[0].decision == "SELL"


def test_get_recent_entries_never_raises_on_database_failure():
    repository = MagicMock()
    repository.get_recent_decision_entries.side_effect = Exception("boom")
    logger = DecisionLogger(repository=repository)
    assert logger.get_recent_entries() == ()


def test_decision_logger_default_construction_never_raises():
    assert DecisionLogger() is not None


def test_log_entry_default_reason_is_empty_string():
    row = create_decision_pipeline_entry_row("XAUUSD", "M15", (), 5, "NO TRADE")
    logger = DecisionLogger(repository=_repository(row=row))
    entry = logger.log_entry("XAUUSD", "M15", [], 5, "NO TRADE")
    assert entry.reason == ""


def test_multiple_log_entry_calls_use_repository_each_time():
    repository = _repository()
    logger = DecisionLogger(repository=repository)
    logger.log_entry("XAUUSD", "M15", [], 5, "NO TRADE")
    logger.log_entry("XAUUSD", "H4", [], 5, "BUY")
    assert repository.record_decision_entry.call_count == 2
