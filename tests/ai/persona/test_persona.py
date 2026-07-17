"""Phase 63.0 TASK 1 — AI Persona Foundation. Pure identity data, no AI calls, no prompt building."""

from ai.persona.persona import Persona
from ai.persona.persona_manager import PersonaManager
from ai.persona.persona_registry import SENIOR_TRADING_AI, build_persona_registry


def test_persona_is_pure_data():
    persona = Persona(
        name="Test Persona", role="test role", tone="test tone",
        language_style="test style", disclaimer="test disclaimer", system_identity="test-id",
    )
    assert persona.name == "Test Persona"
    assert persona.role == "test role"


def test_build_persona_registry_returns_senior_trading_ai():
    registry = build_persona_registry()
    assert SENIOR_TRADING_AI in registry
    assert len(registry) == 1


def test_persona_manager_get_active_persona_with_no_injection():
    manager = PersonaManager()
    active = manager.get_active_persona()
    assert active.name == "Senior Trading AI"
    assert active == SENIOR_TRADING_AI


def test_persona_manager_get_by_name():
    manager = PersonaManager()
    assert manager.get("Senior Trading AI") == SENIOR_TRADING_AI
    assert manager.get("Nonexistent Persona") is None


def test_persona_manager_with_injected_registry():
    custom = Persona(name="Custom", role="r", tone="t", language_style="l", disclaimer="d", system_identity="c")
    manager = PersonaManager(personas=[custom])
    assert manager.get("Custom") == custom
    assert manager.get_active_persona() == SENIOR_TRADING_AI  # falls back, never fabricates a different active persona


def test_persona_manager_all_returns_every_registered_persona():
    manager = PersonaManager()
    assert manager.all() == [SENIOR_TRADING_AI]
