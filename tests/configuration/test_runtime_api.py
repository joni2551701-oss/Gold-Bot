"""
Phase 59.7, TASK 9 -- configuration/runtime_api.py tests. Real
RuntimeFeatureManager (backed by real SQLite repositories,
tests/conftest.py's autouse fresh_database fixture) -- no mocks.
"""

from core_layer.configuration.runtime_api import (
    RuntimeApiResult,
    disable_feature,
    enable_feature,
    feature_status,
    list_runtime_features,
)
from core_layer.configuration.runtime_feature_manager import RuntimeFeatureManager


def test_enable_feature_succeeds():
    manager = RuntimeFeatureManager()
    result = enable_feature("ENABLE_NEWS", actor="owner", manager=manager)

    assert isinstance(result, RuntimeApiResult)
    assert result.success is True
    assert result.data["enabled"] is True
    assert manager.status("ENABLE_NEWS").enabled is True


def test_enable_feature_reports_dependency_rejection():
    manager = RuntimeFeatureManager()
    result = enable_feature("ENABLE_BACKTEST", actor="owner", manager=manager)

    assert result.success is False
    assert "ENABLE_DATASET_SYNC" in result.message


def test_disable_feature_succeeds():
    manager = RuntimeFeatureManager()
    manager.enable("ENABLE_NEWS")

    result = disable_feature("ENABLE_NEWS", actor="owner", manager=manager)

    assert result.success is True
    assert result.data["enabled"] is False


def test_feature_status_unknown_name_is_a_structured_failure_not_an_exception():
    manager = RuntimeFeatureManager()
    result = feature_status("NOT_A_REAL_FEATURE", manager=manager)

    assert result.success is False
    assert "not a known feature" in result.message


def test_feature_status_reports_current_state():
    manager = RuntimeFeatureManager()
    manager.enable("ENABLE_TWELVEDATA")

    result = feature_status("ENABLE_TWELVEDATA", manager=manager)

    assert result.success is True
    assert result.data["state"] == "ACTIVE"
    assert result.data["source"] == "runtime"


def test_list_runtime_features_includes_registry_entries():
    manager = RuntimeFeatureManager()
    result = list_runtime_features(manager=manager)

    assert result.success is True
    names = {f["feature"] for f in result.data["features"]}
    assert "ENABLE_MT5" in names


def test_list_runtime_features_reflects_a_toggle():
    manager = RuntimeFeatureManager()
    manager.enable("ENABLE_NEWS", changed_by="owner")

    result = list_runtime_features(manager=manager)

    entry = next(f for f in result.data["features"] if f["feature"] == "ENABLE_NEWS")
    assert entry["state"] == "ACTIVE"
    assert entry["source"] == "runtime"


def test_functions_construct_a_default_manager_when_none_supplied():
    # Must not raise even without an explicit manager -- constructs its own real one.
    result = list_runtime_features()
    assert result.success is True
