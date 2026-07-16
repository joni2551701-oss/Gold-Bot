"""Phase 61.1.1 TASK 3/5 — Prompt Lifecycle: ACTIVE/DEPRECATED/ARCHIVED."""

from ai.prompts.prompt_registry import PromptLifecycleState, PromptRegistry


def test_newly_registered_version_defaults_to_active():
    registry = PromptRegistry()
    record = registry.register("market_analysis", "v1")
    assert record.state == PromptLifecycleState.ACTIVE


def test_deprecate_changes_state_without_touching_active_pointer():
    registry = PromptRegistry()
    registry.register("market_analysis", "v1")
    registry.register("market_analysis", "v2")
    registry.set_active("market_analysis", "v1")

    assert registry.deprecate("market_analysis", "v2") is True
    assert registry.state_of("market_analysis", "v2") == PromptLifecycleState.DEPRECATED
    assert registry.active_version("market_analysis") == "v1"


def test_deprecated_version_never_becomes_active_via_set_active():
    registry = PromptRegistry()
    registry.register("market_analysis", "v1")
    registry.register("market_analysis", "v2")
    registry.deprecate("market_analysis", "v2")

    assert registry.set_active("market_analysis", "v2") is False
    assert registry.active_version("market_analysis") == "v1"


def test_deprecated_version_never_becomes_active_via_rollback():
    registry = PromptRegistry()
    registry.register("market_analysis", "v1")
    registry.register("market_analysis", "v2")
    registry.deprecate("market_analysis", "v1")
    registry.set_active("market_analysis", "v2")

    assert registry.rollback("market_analysis") is None
    assert registry.active_version("market_analysis") == "v2"


def test_archived_version_never_becomes_active_via_set_active():
    registry = PromptRegistry()
    registry.register("market_analysis", "v1")
    registry.archive("market_analysis", "v1")

    assert registry.set_active("market_analysis", "v1") is False


def test_archived_version_never_becomes_active_via_rollback():
    registry = PromptRegistry()
    registry.register("market_analysis", "v1")
    registry.register("market_analysis", "v2")
    registry.archive("market_analysis", "v1")
    registry.set_active("market_analysis", "v2")

    assert registry.rollback("market_analysis") is None


def test_deprecated_and_archived_versions_remain_in_list_versions():
    registry = PromptRegistry()
    registry.register("market_analysis", "v1")
    registry.register("market_analysis", "v2")
    registry.deprecate("market_analysis", "v1")
    registry.archive("market_analysis", "v2")

    versions = {r.version: r.state for r in registry.list_versions("market_analysis")}
    assert versions["v1"] == PromptLifecycleState.DEPRECATED
    assert versions["v2"] == PromptLifecycleState.ARCHIVED


def test_deprecate_unknown_version_returns_false():
    registry = PromptRegistry()
    registry.register("market_analysis", "v1")
    assert registry.deprecate("market_analysis", "v99") is False


def test_archive_unknown_version_returns_false():
    registry = PromptRegistry()
    registry.register("market_analysis", "v1")
    assert registry.archive("market_analysis", "v99") is False


def test_state_of_unknown_version_returns_none():
    registry = PromptRegistry()
    registry.register("market_analysis", "v1")
    assert registry.state_of("market_analysis", "v99") is None


def test_active_version_can_be_reactivated_if_still_active_state():
    registry = PromptRegistry()
    registry.register("market_analysis", "v1")
    registry.register("market_analysis", "v2")
    registry.set_active("market_analysis", "v2")
    assert registry.set_active("market_analysis", "v1") is True
