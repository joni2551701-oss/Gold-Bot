"""Phase 61.1 TASK 5 — Prompt Registry Extension. PromptManager itself is not replaced."""

from ai_layer.ai_engine.prompts.prompt_manager import PromptManager
from ai_layer.ai_engine.prompts.prompt_registry import PromptRegistry


def test_prompt_manager_is_unmodified_by_the_registry():
    manager = PromptManager()
    assert hasattr(manager, "get_market_analysis_prompt")
    assert hasattr(manager, "get_user_assistant_prompt")
    assert hasattr(manager, "get_fundamental_analysis_prompt")


def test_first_registered_version_becomes_active_automatically():
    registry = PromptRegistry()
    registry.register("market_analysis", "v1")
    assert registry.active_version("market_analysis") == "v1"


def test_registering_a_second_version_does_not_change_active():
    registry = PromptRegistry()
    registry.register("market_analysis", "v1")
    registry.register("market_analysis", "v2")
    assert registry.active_version("market_analysis") == "v1"


def test_set_active_switches_to_a_registered_version():
    registry = PromptRegistry()
    registry.register("market_analysis", "v1")
    registry.register("market_analysis", "v2")
    assert registry.set_active("market_analysis", "v2") is True
    assert registry.active_version("market_analysis") == "v2"


def test_set_active_rejects_an_unregistered_version():
    registry = PromptRegistry()
    registry.register("market_analysis", "v1")
    assert registry.set_active("market_analysis", "v99") is False
    assert registry.active_version("market_analysis") == "v1"


def test_rollback_moves_active_to_the_previous_version():
    registry = PromptRegistry()
    registry.register("market_analysis", "v1")
    registry.register("market_analysis", "v2")
    registry.register("market_analysis", "v3")
    registry.set_active("market_analysis", "v3")
    assert registry.rollback("market_analysis") == "v2"
    assert registry.active_version("market_analysis") == "v2"


def test_rollback_at_the_first_version_returns_none():
    registry = PromptRegistry()
    registry.register("market_analysis", "v1")
    assert registry.rollback("market_analysis") is None
    assert registry.active_version("market_analysis") == "v1"


def test_rollback_on_unknown_prompt_returns_none():
    registry = PromptRegistry()
    assert registry.rollback("unknown_prompt") is None


def test_list_versions_returns_registration_order():
    registry = PromptRegistry()
    registry.register("market_analysis", "v1")
    registry.register("market_analysis", "v2")
    versions = [record.version for record in registry.list_versions("market_analysis")]
    assert versions == ["v1", "v2"]


def test_register_carries_metadata():
    registry = PromptRegistry()
    record = registry.register("market_analysis", "v1", metadata={"author": "worker"})
    assert record.metadata["author"] == "worker"
