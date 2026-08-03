"""
Phase 59.6, TASK 2 -- database_layer/audit_log/audit_log_repository.py and
audit_log_models.py tests. Real SQLite (tests/conftest.py's autouse
fresh_database fixture), no mocks.
"""

from datetime import datetime

from database_layer.audit_log.audit_log_models import create_audit_log_entry
from database_layer.audit_log.audit_log_repository import AuditLogRepository


def test_log_action_persists_and_returns_the_entry():
    repo = AuditLogRepository()

    entry = repo.log_action("owner", "ENABLE_PROVIDER", target="BITGET", details="manual switch")

    assert entry.actor == "owner"
    assert entry.action == "ENABLE_PROVIDER"
    assert entry.target == "BITGET"
    assert entry.result == "SUCCESS"


def test_log_action_defaults_result_to_success():
    repo = AuditLogRepository()
    entry = repo.log_action("owner", "PANIC")
    assert entry.result == "SUCCESS"


def test_log_action_accepts_explicit_failure_result():
    repo = AuditLogRepository()
    entry = repo.log_action("owner", "ENABLE_PROVIDER", result="FAILURE", details="invalid provider name")
    assert entry.result == "FAILURE"


def test_get_recent_returns_newest_first():
    repo = AuditLogRepository()
    repo.log_action("owner", "ACTION_1")
    repo.log_action("owner", "ACTION_2")
    repo.log_action("owner", "ACTION_3")

    recent = repo.get_recent()

    assert [e.action for e in recent] == ["ACTION_3", "ACTION_2", "ACTION_1"]


def test_get_recent_respects_limit():
    repo = AuditLogRepository()
    for i in range(5):
        repo.log_action("owner", f"ACTION_{i}")

    recent = repo.get_recent(limit=2)

    assert len(recent) == 2


def test_get_by_actor_filters_correctly():
    repo = AuditLogRepository()
    repo.log_action("owner", "ACTION_A")
    repo.log_action("admin_1", "ACTION_B")

    owner_entries = repo.get_by_actor("owner")

    assert len(owner_entries) == 1
    assert owner_entries[0].action == "ACTION_A"


def test_count_reflects_total_entries():
    repo = AuditLogRepository()
    assert repo.count() == 0
    repo.log_action("owner", "ACTION_A")
    repo.log_action("owner", "ACTION_B")
    assert repo.count() == 2


def test_no_entries_returns_empty_list_not_none():
    repo = AuditLogRepository()
    assert repo.get_recent() == []
    assert repo.get_by_actor("nobody") == []


def test_create_audit_log_entry_stamps_created_at():
    entry = create_audit_log_entry("owner", "PANIC")
    assert isinstance(entry.created_at, datetime)
    assert entry.created_at.tzinfo is not None


def test_audit_log_entry_is_frozen():
    entry = create_audit_log_entry("owner", "PANIC")
    try:
        entry.action = "RESUME"
        assert False, "AuditLogEntry must be immutable"
    except AttributeError:
        pass
