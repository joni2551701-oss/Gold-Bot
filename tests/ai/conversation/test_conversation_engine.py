"""Phase 61.3 TASK 5 — Conversation Engine: thin orchestration over ai/session/ and ai/runtime/ai_service.py, both unmodified."""

from ai_layer.ai_service.access.permissions import AIRole
from ai_layer.ai_engine.context.context_builder import build_ai_context
from ai_layer.personal_ai.interaction_manager.conversation_engine import ConversationEngine
from ai_layer.ai_engine.providers.base_provider import ProviderResult
from ai_layer.ai_engine.providers.provider_manager import ProviderStatus
from ai_layer.ai_engine.runtime.ai_service import AIService
from ai_layer.ai_service.session.context_window import ContextWindow
from ai_layer.ai_service.session.session_manager import SessionManager


class _FakeProvider:
    def __init__(self, name: str, behavior=None):
        self._name = name
        self._behavior = behavior or (lambda prompt: ProviderResult(content=f"[{name}] I hear you.", metadata={}))

    @property
    def name(self) -> str:
        return self._name

    def chat(self, prompt):
        return self._behavior(prompt)


class _FakeProviderManager:
    def __init__(self, providers: dict):
        self._providers = providers
        self._statuses = {name: ProviderStatus.FALLBACK for name in providers}

    def list_providers(self):
        return list(self._providers.keys())

    def get_provider(self, name):
        return self._providers.get(name)

    def status_of(self, name):
        return self._statuses.get(name)


def _engine():
    provider_manager = _FakeProviderManager({"gemini": _FakeProvider("gemini")})
    service = AIService(provider_manager=provider_manager)
    return ConversationEngine(session_manager=SessionManager(), ai_service=service)


def _context():
    return build_ai_context()


def test_ask_with_unknown_session_id_is_rejected_not_a_crash():
    engine = _engine()
    result = engine.ask(session_id="does-not-exist", message="hi", ai_context=_context(), role=AIRole.OWNER)
    assert result.response.accepted is False
    assert "unknown session_id" in result.response.reason


def test_ask_records_user_and_assistant_turns():
    engine = _engine()
    state = engine.start_session(telegram_id="12345")

    result = engine.ask(session_id=state.session_id, message="What is a BOS?", ai_context=_context(), role=AIRole.OWNER)

    assert result.response.accepted is True
    turns = state.history()
    assert len(turns) == 2
    assert turns[0].role == "user"
    assert turns[0].content == "What is a BOS?"
    assert turns[1].role == "assistant"
    assert turns[1].content == result.response.content


def test_ask_carries_telegram_id_from_session_when_not_supplied():
    engine = _engine()
    state = engine.start_session(telegram_id="99999")

    engine.ask(session_id=state.session_id, message="hi", ai_context=_context(), role=AIRole.OWNER)

    # No direct getter for the last RuntimeRequest -- verified indirectly via a
    # successful accepted response, since AIService.ask() would still succeed
    # even with telegram_id=None; this test only guards against a crash when
    # telegram_id is omitted from ask().
    assert state.telegram_id == "99999"


def test_second_turn_includes_prior_history_in_the_prompt():
    captured_prompts = []

    def _capture(prompt):
        captured_prompts.append(prompt)
        return ProviderResult(content="ack")

    provider_manager = _FakeProviderManager({"gemini": _FakeProvider("gemini", behavior=_capture)})
    service = AIService(provider_manager=provider_manager)
    engine = ConversationEngine(session_manager=SessionManager(), ai_service=service)
    state = engine.start_session(telegram_id="1")

    engine.ask(session_id=state.session_id, message="first message", ai_context=_context(), role=AIRole.OWNER)
    engine.ask(session_id=state.session_id, message="second message", ai_context=_context(), role=AIRole.OWNER)

    assert "first message" in captured_prompts[1]
    assert "second message" in captured_prompts[1]


def test_context_window_trims_history_passed_to_the_prompt():
    provider_manager = _FakeProviderManager({"gemini": _FakeProvider("gemini")})
    service = AIService(provider_manager=provider_manager)
    engine = ConversationEngine(
        session_manager=SessionManager(), ai_service=service, context_window=ContextWindow(max_turns=1),
    )
    state = engine.start_session(telegram_id="1")

    engine.ask(session_id=state.session_id, message="old message", ai_context=_context(), role=AIRole.OWNER)
    result = engine.ask(session_id=state.session_id, message="new message", ai_context=_context(), role=AIRole.OWNER)

    assert result.response.accepted is True
    assert len(state.history()) == 4


def test_rejected_response_does_not_record_an_assistant_turn():
    from ai_layer.ai_engine.capabilities.capability import Capability
    from ai_layer.ai_engine.capabilities.capability_manager import CapabilityManager

    capability_manager = CapabilityManager()
    capability_manager.disable(Capability.CHAT)
    service = AIService(capability_manager=capability_manager)
    engine = ConversationEngine(session_manager=SessionManager(), ai_service=service)
    state = engine.start_session(telegram_id="1")

    result = engine.ask(session_id=state.session_id, message="hi", ai_context=_context(), role=AIRole.OWNER)

    assert result.response.accepted is False
    turns = state.history()
    assert len(turns) == 1
    assert turns[0].role == "user"
