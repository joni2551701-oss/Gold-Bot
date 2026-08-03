"""
Phase 59.6, TASK 6 -- database_layer/journal_repository/config_snapshot_repository.py and
config_snapshot_models.py tests. Real SQLite (tests/conftest.py's
autouse fresh_database fixture), no mocks.
"""

from datetime import datetime

from core_layer.configuration.feature_registry import build_feature_registry
from database_layer.journal_repository.config_snapshot_models import create_config_snapshot
from database_layer.journal_repository.config_snapshot_repository import ConfigSnapshotRepository


def test_create_config_snapshot_serializes_registry_state():
    registry = build_feature_registry()

    snapshot = create_config_snapshot(registry, taken_by="owner", reason="before feature toggle")

    state = snapshot.feature_state_dict()
    assert state["ENABLE_MT5"] is False
    assert isinstance(snapshot.snapshot_id, str)
    assert len(snapshot.snapshot_id) == 36


def test_save_snapshot_persists_and_returns_it():
    repo = ConfigSnapshotRepository()
    snapshot = create_config_snapshot(build_feature_registry(), taken_by="owner")

    result = repo.save_snapshot(snapshot)

    assert result.snapshot_id == snapshot.snapshot_id


def test_get_latest_returns_none_when_empty():
    repo = ConfigSnapshotRepository()
    assert repo.get_latest() is None


def test_get_latest_returns_the_most_recent_snapshot():
    repo = ConfigSnapshotRepository()
    first = create_config_snapshot(build_feature_registry(), reason="first")
    second = create_config_snapshot(build_feature_registry(), reason="second")

    repo.save_snapshot(first)
    repo.save_snapshot(second)

    latest = repo.get_latest()
    assert latest.reason == "second"


def test_get_all_returns_newest_first():
    repo = ConfigSnapshotRepository()
    repo.save_snapshot(create_config_snapshot(build_feature_registry(), reason="a"))
    repo.save_snapshot(create_config_snapshot(build_feature_registry(), reason="b"))
    repo.save_snapshot(create_config_snapshot(build_feature_registry(), reason="c"))

    snapshots = repo.get_all()

    assert [s.reason for s in snapshots] == ["c", "b", "a"]


def test_get_all_respects_limit():
    repo = ConfigSnapshotRepository()
    for i in range(5):
        repo.save_snapshot(create_config_snapshot(build_feature_registry(), reason=str(i)))

    assert len(repo.get_all(limit=2)) == 2


def test_feature_state_round_trips_exactly():
    registry = build_feature_registry()
    snapshot = create_config_snapshot(registry)

    state = snapshot.feature_state_dict()

    assert state == {entry.name: entry.enabled for entry in registry}


def test_config_snapshot_record_is_frozen():
    snapshot = create_config_snapshot(build_feature_registry())
    try:
        snapshot.reason = "changed"
        assert False, "ConfigSnapshotRecord must be immutable"
    except AttributeError:
        pass


def test_taken_at_is_stamped_and_utc():
    snapshot = create_config_snapshot(build_feature_registry())
    assert isinstance(snapshot.taken_at, datetime)
    assert snapshot.taken_at.tzinfo is not None
