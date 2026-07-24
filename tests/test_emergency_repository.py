"""
Phase 59.9, TASK 2 -- database/emergency_repository.py and
emergency_models.py tests. Real SQLite (tests/conftest.py's autouse
fresh_database fixture), no mocks. Flat tests/test_emergency_repository.py
path -- matches this codebase's real convention
(tests/test_runtime_feature_repository.py, tests/test_audit_log_repository.py),
not a tests/database/ directory (none exists anywhere in this repo).
"""

from datetime import datetime

from database.emergency_models import create_emergency_state_entry
from database.emergency_repository import EmergencyRepository


def test_get_current_state_returns_none_when_empty():
    repo = EmergencyRepository()
    assert repo.get_current_state() is None


def test_record_transition_creates_a_row():
    repo = EmergencyRepository()

    entry = repo.record_transition("PAUSED", reason="manual pause", source="owner", changed_by="owner")

    assert entry.state == "PAUSED"
    assert entry.reason == "manual pause"
    assert entry.source == "owner"
    assert entry.changed_by == "owner"


def test_get_current_state_returns_the_latest_transition():
    repo = EmergencyRepository()
    repo.record_transition("PAUSED", reason="first")
    repo.record_transition("KILLED", reason="second")

    current = repo.get_current_state()

    assert current.state == "KILLED"
    assert current.reason == "second"


def test_history_is_never_overwritten():
    """NORMAL -> PAUSED -> NORMAL: all three transitions must remain in history."""
    repo = EmergencyRepository()
    repo.record_transition("NORMAL")
    repo.record_transition("PAUSED", reason="daily loss limit")
    repo.record_transition("NORMAL", reason="restored")

    history = repo.get_history()

    assert len(history) == 3
    assert [entry.state for entry in history] == ["NORMAL", "PAUSED", "NORMAL"]


def test_get_history_is_newest_first():
    repo = EmergencyRepository()
    repo.record_transition("PAUSED")
    repo.record_transition("KILLED")

    history = repo.get_history()

    assert history[0].state == "KILLED"
    assert history[1].state == "PAUSED"


def test_get_history_respects_limit():
    repo = EmergencyRepository()
    for state in ["PAUSED", "NORMAL", "PAUSED", "NORMAL", "KILLED"]:
        repo.record_transition(state)

    assert len(repo.get_history(limit=2)) == 2


def test_simulated_restart_reads_the_same_state_back():
    """Two independent repository instances against the same DB path -- simulating a process restart."""
    first_repo = EmergencyRepository()
    first_repo.record_transition("KILLED", reason="daily loss limit", changed_by="system")

    second_repo = EmergencyRepository()
    current = second_repo.get_current_state()

    assert current is not None
    assert current.state == "KILLED"
    assert current.changed_by == "system"


def test_create_emergency_state_entry_stamps_created_and_updated_at_identically():
    entry = create_emergency_state_entry("NORMAL")
    assert isinstance(entry.created_at, datetime)
    assert entry.created_at.tzinfo is not None
    assert entry.updated_at == entry.created_at


def test_emergency_state_entry_is_frozen():
    entry = create_emergency_state_entry("NORMAL")
    try:
        entry.state = "KILLED"
        assert False, "EmergencyStateEntry must be immutable"
    except AttributeError:
        pass
