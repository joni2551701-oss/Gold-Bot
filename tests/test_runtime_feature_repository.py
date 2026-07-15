"""
Phase 59.7, TASK 3 -- database/runtime_feature_repository.py and
runtime_feature_models.py tests. Real SQLite (tests/conftest.py's
autouse fresh_database fixture), no mocks.
"""

from datetime import datetime

from database.runtime_feature_models import create_runtime_feature_record
from database.runtime_feature_repository import RuntimeFeatureRepository


def test_get_feature_returns_none_when_absent():
    repo = RuntimeFeatureRepository()
    assert repo.get_feature("ENABLE_AI") is None


def test_set_feature_creates_a_new_row():
    repo = RuntimeFeatureRepository()

    result = repo.set_feature("ENABLE_AI", True, updated_by="owner", reason="manual enable")

    assert result.feature == "ENABLE_AI"
    assert result.enabled is True
    assert result.updated_by == "owner"
    assert result.reason == "manual enable"


def test_set_feature_overwrites_an_existing_row():
    repo = RuntimeFeatureRepository()

    repo.set_feature("ENABLE_AI", True)
    repo.set_feature("ENABLE_AI", False, reason="rollback")

    result = repo.get_feature("ENABLE_AI")
    assert result.enabled is False
    assert result.reason == "rollback"


def test_enabled_survives_a_round_trip_as_real_bool():
    repo = RuntimeFeatureRepository()
    repo.set_feature("ENABLE_AI", True)

    result = repo.get_feature("ENABLE_AI")

    assert result.enabled is True
    assert isinstance(result.enabled, bool)


def test_get_all_features_returns_every_persisted_feature():
    repo = RuntimeFeatureRepository()
    repo.set_feature("ENABLE_AI", True)
    repo.set_feature("ENABLE_NEWS", False)

    features = repo.get_all_features()

    assert len(features) == 2
    assert {f.feature for f in features} == {"ENABLE_AI", "ENABLE_NEWS"}


def test_no_features_returns_empty_list_not_none():
    repo = RuntimeFeatureRepository()
    assert repo.get_all_features() == []


def test_simulated_restart_reads_the_same_state_back():
    """Two independent repository instances against the same DB path -- simulating a process restart."""
    first_repo = RuntimeFeatureRepository()
    first_repo.set_feature("ENABLE_AI", True, updated_by="owner")

    second_repo = RuntimeFeatureRepository()
    result = second_repo.get_feature("ENABLE_AI")

    assert result is not None
    assert result.enabled is True
    assert result.updated_by == "owner"


def test_created_at_is_preserved_across_updates():
    repo = RuntimeFeatureRepository()

    first = repo.set_feature("ENABLE_AI", True)
    second = repo.set_feature("ENABLE_AI", False, reason="rollback")

    assert first.created_at is not None
    assert second.created_at == first.created_at
    assert second.updated_at >= first.updated_at


def test_create_runtime_feature_record_stamps_updated_at():
    record = create_runtime_feature_record("ENABLE_AI", True)
    assert isinstance(record.updated_at, datetime)
    assert record.updated_at.tzinfo is not None


def test_runtime_feature_record_is_frozen():
    record = create_runtime_feature_record("ENABLE_AI", True)
    try:
        record.enabled = False
        assert False, "RuntimeFeatureRecord must be immutable"
    except AttributeError:
        pass
