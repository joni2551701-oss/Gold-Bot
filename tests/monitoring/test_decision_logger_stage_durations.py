"""Phase B.0 TASK 5 -- monitoring/decision_logger.py stage_durations_ms extension tests."""

from unittest.mock import MagicMock

from database.monitoring_models import create_decision_pipeline_entry_row
from monitoring.decision_logger import DecisionLogger


def _repository(row=None):
    repository = MagicMock()
    repository.record_decision_entry.return_value = row or create_decision_pipeline_entry_row(
        "XAUUSD", "M15", ("STRUCTURE_ALIGNED",), 5, "NO TRADE",
    )
    return repository


def test_log_entry_relays_stage_durations_ms():
    row = create_decision_pipeline_entry_row(
        "XAUUSD", "M15", (), 5, "NO TRADE",
        stage_durations_ms=(("context", 4.2), ("signal", 1.1)),
    )
    logger = DecisionLogger(repository=_repository(row=row))
    entry = logger.log_entry(
        "XAUUSD", "M15", [], 5, "NO TRADE",
        stage_durations_ms=[("context", 4.2), ("signal", 1.1)],
    )
    assert entry.stage_durations_ms == (("context", 4.2), ("signal", 1.1))


def test_log_entry_defaults_stage_durations_ms_to_empty_tuple():
    logger = DecisionLogger(repository=_repository())
    logger.log_entry("XAUUSD", "M15", [], 5, "NO TRADE")
    repository = logger._repository
    _, kwargs = repository.record_decision_entry.call_args
    assert kwargs["stage_durations_ms"] == ()


def test_log_entry_passes_stage_durations_ms_to_repository():
    repository = _repository()
    logger = DecisionLogger(repository=repository)
    logger.log_entry("XAUUSD", "M15", [], 5, "NO TRADE", stage_durations_ms=[("ai", 812.0)])
    _, kwargs = repository.record_decision_entry.call_args
    assert kwargs["stage_durations_ms"] == [("ai", 812.0)]


def test_log_entry_never_computes_a_stage_duration_of_its_own():
    """The module only relays caller-supplied durations -- it never measures a stage itself."""
    row = create_decision_pipeline_entry_row(
        "XAUUSD", "M15", (), 5, "NO TRADE", stage_durations_ms=(("decision", 0.3),),
    )
    logger = DecisionLogger(repository=_repository(row=row))
    entry = logger.log_entry("XAUUSD", "M15", [], 5, "NO TRADE", stage_durations_ms=[("decision", 0.3)])
    assert entry.stage_durations_ms == (("decision", 0.3),)


def test_log_entry_never_raises_when_stage_durations_ms_omitted():
    logger = DecisionLogger(repository=_repository())
    entry = logger.log_entry("XAUUSD", "M15", [], 5, "NO TRADE")
    assert entry is not None
