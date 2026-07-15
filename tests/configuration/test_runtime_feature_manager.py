"""
Phase 59.7, TASK 1/4/5/6/7/8 -- configuration/runtime_feature_manager.py
tests. Real repositories (SQLite, tests/conftest.py's autouse
fresh_database fixture) -- no mocks.
"""

from configuration.runtime_feature_manager import RuntimeFeatureManager, ToggleResult
from database.audit_log_repository import AuditLogRepository
from database.config_snapshot_repository import ConfigSnapshotRepository
from database.runtime_feature_repository import RuntimeFeatureRepository


# --- TASK 1/4: construction, load(), status(), list_features() ---

def test_manager_auto_loads_registry_defaults_on_construction():
    manager = RuntimeFeatureManager()

    status = manager.status("ENABLE_MT5")

    assert status is not None
    assert status.enabled is False  # config.Config.ENABLE_MT5's own default


def test_status_returns_none_for_a_completely_unknown_name():
    manager = RuntimeFeatureManager()
    assert manager.status("NOT_A_REAL_FEATURE") is None


def test_list_features_returns_every_registry_entry():
    manager = RuntimeFeatureManager()
    names = {state.name for state in manager.list_features()}
    assert "ENABLE_MT5" in names
    assert "ENABLE_EXECUTION" in names


def test_reload_reflects_a_persisted_change_made_outside_the_cache():
    manager = RuntimeFeatureManager()
    manager.repository.set_feature("ENABLE_NEWS", True, updated_by="owner")

    manager.reload()

    assert manager.status("ENABLE_NEWS").enabled is True


# --- TASK 1: enable/disable/toggle ---

def test_enable_sets_enabled_true():
    manager = RuntimeFeatureManager()
    result = manager.enable("ENABLE_NEWS", changed_by="owner")

    assert isinstance(result, ToggleResult)
    assert result.success is True
    assert result.enabled is True
    assert manager.status("ENABLE_NEWS").enabled is True


def test_disable_sets_enabled_false():
    manager = RuntimeFeatureManager()
    manager.enable("ENABLE_NEWS")
    result = manager.disable("ENABLE_NEWS")

    assert result.success is True
    assert result.enabled is False
    assert manager.status("ENABLE_NEWS").enabled is False


def test_toggle_flips_current_value():
    manager = RuntimeFeatureManager()
    assert manager.status("ENABLE_NEWS").enabled is False

    manager.toggle("ENABLE_NEWS")
    assert manager.status("ENABLE_NEWS").enabled is True

    manager.toggle("ENABLE_NEWS")
    assert manager.status("ENABLE_NEWS").enabled is False


def test_toggle_on_never_seen_name_defaults_to_enabling():
    manager = RuntimeFeatureManager()
    result = manager.toggle("BRAND_NEW_FEATURE")
    assert result.enabled is True


# --- TASK 3/4: persistence across a simulated restart ---

def test_enabled_state_survives_a_new_manager_instance():
    first = RuntimeFeatureManager()
    first.enable("ENABLE_NEWS", changed_by="owner", reason="persist me")

    second = RuntimeFeatureManager()  # simulates a fresh process/restart

    assert second.status("ENABLE_NEWS").enabled is True
    assert second.status("ENABLE_NEWS").changed_by == "owner"


def test_persisted_row_actually_exists_in_the_repository():
    manager = RuntimeFeatureManager()
    manager.enable("ENABLE_NEWS", changed_by="owner")

    record = RuntimeFeatureRepository().get_feature("ENABLE_NEWS")

    assert record is not None
    assert record.enabled is True


# --- TASK 5/6: dependency validation / dry run ---

def test_enabling_a_feature_with_unmet_dependency_is_rejected():
    manager = RuntimeFeatureManager()

    result = manager.enable("ENABLE_EXECUTION", changed_by="owner")

    assert result.success is False
    assert "ENABLE_RISK" in result.reason
    assert manager.status("ENABLE_EXECUTION").enabled is False


def test_rejected_toggle_does_not_persist_anything():
    manager = RuntimeFeatureManager()
    manager.enable("ENABLE_EXECUTION", changed_by="owner")

    record = RuntimeFeatureRepository().get_feature("ENABLE_EXECUTION")

    assert record is None


def test_enabling_with_dependencies_already_satisfied_succeeds():
    manager = RuntimeFeatureManager()
    manager.enable("ENABLE_RISK")
    manager.enable("ENABLE_DECISION")

    result = manager.enable("ENABLE_EXECUTION", changed_by="owner")

    assert result.success is True
    assert manager.status("ENABLE_EXECUTION").enabled is True


def test_disabling_a_dependency_still_needed_by_an_enabled_dependent_is_rejected():
    """The dry run is symmetric: it rejects ANY toggle (enable or disable) that would leave the overall state invalid -- disabling ENABLE_RISK while ENABLE_EXECUTION (already on) still needs it is refused, not silently allowed to create an inconsistent state. No cascading auto-disable of ENABLE_EXECUTION happens either -- the toggle is rejected outright, state stays exactly as it was."""
    manager = RuntimeFeatureManager()
    manager.enable("ENABLE_RISK")
    manager.enable("ENABLE_DECISION")
    manager.enable("ENABLE_EXECUTION")

    result = manager.disable("ENABLE_RISK")

    assert result.success is False
    assert manager.status("ENABLE_RISK").enabled is True  # unchanged
    assert manager.status("ENABLE_EXECUTION").enabled is True  # unaffected


# --- TASK 7: audit integration ---

def test_successful_enable_writes_a_feature_enabled_audit_entry():
    manager = RuntimeFeatureManager()
    manager.enable("ENABLE_NEWS", changed_by="owner", reason="test")

    entries = AuditLogRepository().get_recent()

    assert len(entries) == 1
    assert entries[0].action == "FEATURE_ENABLED"
    assert entries[0].target == "ENABLE_NEWS"
    assert entries[0].result == "SUCCESS"
    assert entries[0].actor == "owner"


def test_successful_disable_writes_a_feature_disabled_audit_entry():
    manager = RuntimeFeatureManager()
    manager.enable("ENABLE_NEWS")
    manager.disable("ENABLE_NEWS", changed_by="owner")

    entries = AuditLogRepository().get_recent()

    assert entries[0].action == "FEATURE_DISABLED"
    assert entries[0].result == "SUCCESS"


def test_rejected_toggle_writes_a_rejected_audit_entry():
    manager = RuntimeFeatureManager()
    manager.enable("ENABLE_EXECUTION", changed_by="owner")

    entries = AuditLogRepository().get_recent()

    assert len(entries) == 1
    assert entries[0].result == "REJECTED"


def test_actor_defaults_to_unknown_when_not_supplied():
    manager = RuntimeFeatureManager()
    manager.enable("ENABLE_NEWS")

    entries = AuditLogRepository().get_recent()

    assert entries[0].actor == "unknown"


# --- TASK 8: config snapshot integration ---

def test_successful_toggle_creates_a_config_snapshot():
    manager = RuntimeFeatureManager()
    manager.enable("ENABLE_NEWS", changed_by="owner")

    snapshots = ConfigSnapshotRepository().get_all()

    assert len(snapshots) == 1
    assert snapshots[0].taken_by == "owner"
    assert "ENABLE_NEWS" in snapshots[0].feature_state_dict()


def test_rejected_toggle_creates_no_snapshot():
    manager = RuntimeFeatureManager()
    manager.enable("ENABLE_EXECUTION", changed_by="owner")

    assert ConfigSnapshotRepository().get_all() == []


def test_snapshot_reflects_the_state_at_the_moment_of_the_toggle():
    manager = RuntimeFeatureManager()
    manager.enable("ENABLE_NEWS")

    snapshot = ConfigSnapshotRepository().get_latest()
    state = snapshot.feature_state_dict()

    assert state["ENABLE_NEWS"] is True
    assert state["ENABLE_MT5"] is False  # untouched, still its registry default


# --- source / created_at ---

def test_registry_only_feature_has_default_source_and_no_created_at():
    manager = RuntimeFeatureManager()
    state = manager.status("ENABLE_MT5")

    assert state.source == "default"
    assert state.created_at is None


def test_toggled_feature_has_runtime_source_and_created_at():
    manager = RuntimeFeatureManager()
    manager.enable("ENABLE_NEWS", changed_by="owner")

    state = manager.status("ENABLE_NEWS")

    assert state.source == "runtime"
    assert state.created_at is not None


def test_created_at_is_preserved_across_repeated_toggles():
    manager = RuntimeFeatureManager()
    manager.enable("ENABLE_NEWS")
    first_created_at = manager.status("ENABLE_NEWS").created_at

    manager.disable("ENABLE_NEWS")
    second_created_at = manager.status("ENABLE_NEWS").created_at

    assert first_created_at == second_created_at


# --- get_feature_state() (dict shape) ---

def test_get_feature_state_returns_none_for_unknown_name():
    manager = RuntimeFeatureManager()
    assert manager.get_feature_state("NOT_A_REAL_FEATURE") is None


def test_get_feature_state_shape_for_a_default_feature():
    manager = RuntimeFeatureManager()
    state = manager.get_feature_state("ENABLE_MT5")

    assert state["feature"] == "ENABLE_MT5"
    assert state["state"] == "INACTIVE"
    assert state["source"] == "default"
    assert isinstance(state["updated_at"], str)


def test_get_feature_state_reflects_a_runtime_toggle():
    manager = RuntimeFeatureManager()
    manager.enable("ENABLE_TWELVEDATA", changed_by="owner")

    state = manager.get_feature_state("ENABLE_TWELVEDATA")

    assert state["feature"] == "ENABLE_TWELVEDATA"
    assert state["state"] == "ACTIVE"
    assert state["source"] == "runtime"


# --- enable_feature()/disable_feature() aliases ---

def test_enable_feature_alias_behaves_like_enable():
    manager = RuntimeFeatureManager()
    result = manager.enable_feature("ENABLE_NEWS", changed_by="owner")

    assert result.success is True
    assert manager.status("ENABLE_NEWS").enabled is True


def test_disable_feature_alias_behaves_like_disable():
    manager = RuntimeFeatureManager()
    manager.enable_feature("ENABLE_NEWS")
    result = manager.disable_feature("ENABLE_NEWS", changed_by="owner")

    assert result.success is True
    assert manager.status("ENABLE_NEWS").enabled is False


# --- validate_dependencies() public API ---

def test_validate_dependencies_with_no_args_checks_current_state():
    manager = RuntimeFeatureManager()
    result = manager.validate_dependencies()
    assert result.valid is True  # nothing enabled yet that has an unmet dependency


def test_validate_dependencies_with_name_checks_the_hypothetical_toggle():
    manager = RuntimeFeatureManager()
    result = manager.validate_dependencies("ENABLE_EXECUTION", new_enabled=True)
    assert result.valid is False


def test_validate_dependencies_matches_the_actual_toggle_outcome():
    manager = RuntimeFeatureManager()
    manager.enable("ENABLE_RISK")
    manager.enable("ENABLE_DECISION")

    assert manager.validate_dependencies("ENABLE_EXECUTION", new_enabled=True).valid is True


# --- TASK 6's own worked example: friendlier disable-rejection message ---

def test_disable_rejection_message_names_the_active_dependent():
    manager = RuntimeFeatureManager()
    manager.enable("ENABLE_RISK")
    manager.enable("ENABLE_DECISION")
    manager.enable("ENABLE_EXECUTION")

    result = manager.disable("ENABLE_RISK")

    assert result.success is False
    assert result.reason == "Cannot disable ENABLE_RISK. Dependent features active: ENABLE_EXECUTION"
