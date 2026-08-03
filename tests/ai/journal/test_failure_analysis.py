"""
Phase 59 Real Market Validation Foundation, TASK 7 --
ai/journal/failure_analysis.py tests.
"""

import json
from datetime import datetime

from ai_layer.knowledge_ai.knowledge_base.journal.failure_analysis import FailureAnalysisEntry, create_failure_analysis_entry


def test_create_failure_analysis_entry_matches_the_briefs_own_worked_example():
    entry = create_failure_analysis_entry(
        signal_id="sig-1",
        reason="M15 structure break against H4 bias",
        context="H4 bullish but M15 failed",
        result="SL",
    )

    assert entry.signal_id == "sig-1"
    assert entry.reason == "M15 structure break against H4 bias"
    assert entry.context == "H4 bullish but M15 failed"
    assert entry.result == "SL"


def test_create_failure_analysis_entry_stamps_created_at():
    entry = create_failure_analysis_entry(signal_id="sig-1", reason="r", context="c", result="SL")
    assert isinstance(entry.created_at, datetime)
    assert entry.created_at.tzinfo is not None


def test_entry_is_frozen():
    entry = create_failure_analysis_entry(signal_id="sig-1", reason="r", context="c", result="SL")
    try:
        entry.result = "TP"
        assert False, "FailureAnalysisEntry must be immutable"
    except AttributeError:
        pass


def test_to_dict_and_to_json_never_raise():
    entry = create_failure_analysis_entry(signal_id="sig-1", reason="r", context="c", result="SL")

    data = entry.to_dict()
    json.loads(entry.to_json())

    assert data["signal_id"] == "sig-1"
    assert data["created_at"] is not None


def test_created_at_defaults_to_none_when_constructed_directly():
    entry = FailureAnalysisEntry(signal_id="sig-1", reason="r", context="c", result="SL")
    assert entry.created_at is None
    assert entry.to_dict()["created_at"] is None
