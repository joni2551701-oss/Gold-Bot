"""
Phase 59.7, TASK 2 -- configuration/runtime_state.py tests.
"""

from datetime import datetime

from goldbot.core_layer.configuration.runtime_state import (
    FeatureRuntimeState,
    RuntimeStateCache,
    create_feature_runtime_state,
)


def test_create_feature_runtime_state_stamps_last_changed():
    state = create_feature_runtime_state("ENABLE_AI", True)

    assert isinstance(state, FeatureRuntimeState)
    assert state.name == "ENABLE_AI"
    assert state.enabled is True
    assert isinstance(state.last_changed, datetime)
    assert state.last_changed.tzinfo is not None


def test_create_feature_runtime_state_accepts_changed_by_and_reason():
    state = create_feature_runtime_state("ENABLE_AI", True, changed_by="owner", reason="manual enable")
    assert state.changed_by == "owner"
    assert state.reason == "manual enable"


def test_feature_runtime_state_is_frozen():
    state = create_feature_runtime_state("ENABLE_AI", True)
    try:
        state.enabled = False
        assert False, "FeatureRuntimeState must be immutable"
    except AttributeError:
        pass


def test_cache_get_returns_none_when_absent():
    cache = RuntimeStateCache()
    assert cache.get("ENABLE_AI") is None


def test_cache_set_and_get_round_trip():
    cache = RuntimeStateCache()
    state = create_feature_runtime_state("ENABLE_AI", True)

    cache.set(state)

    assert cache.get("ENABLE_AI") == state


def test_cache_set_overwrites_existing_entry():
    cache = RuntimeStateCache()
    cache.set(create_feature_runtime_state("ENABLE_AI", True))
    cache.set(create_feature_runtime_state("ENABLE_AI", False))

    assert cache.get("ENABLE_AI").enabled is False


def test_cache_all_returns_every_entry():
    cache = RuntimeStateCache()
    cache.set(create_feature_runtime_state("ENABLE_AI", True))
    cache.set(create_feature_runtime_state("ENABLE_NEWS", False))

    assert len(cache.all()) == 2


def test_cache_is_enabled_returns_default_when_absent():
    cache = RuntimeStateCache()
    assert cache.is_enabled("ENABLE_AI") is False
    assert cache.is_enabled("ENABLE_AI", default=True) is True


def test_cache_is_enabled_reflects_cached_state():
    cache = RuntimeStateCache()
    cache.set(create_feature_runtime_state("ENABLE_AI", True))
    assert cache.is_enabled("ENABLE_AI") is True


def test_cache_clear_empties_all_entries():
    cache = RuntimeStateCache()
    cache.set(create_feature_runtime_state("ENABLE_AI", True))

    cache.clear()

    assert cache.all() == []
    assert cache.get("ENABLE_AI") is None


def test_create_feature_runtime_state_defaults_source_to_default():
    state = create_feature_runtime_state("ENABLE_AI", True)
    assert state.source == "default"
    assert state.created_at is None


def test_create_feature_runtime_state_accepts_runtime_source():
    from datetime import datetime, timezone

    created = datetime(2026, 1, 1, tzinfo=timezone.utc)
    state = create_feature_runtime_state("ENABLE_AI", True, source="runtime", created_at=created)

    assert state.source == "runtime"
    assert state.created_at == created


def test_two_cache_instances_never_share_state():
    cache_a = RuntimeStateCache()
    cache_b = RuntimeStateCache()

    cache_a.set(create_feature_runtime_state("ENABLE_AI", True))

    assert cache_b.get("ENABLE_AI") is None
