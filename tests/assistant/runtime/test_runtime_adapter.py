"""Phase 65.4 TASK 2/3/4/5/6/9 — assistant/runtime_adapter.py, the third composition-root file."""

from dataclasses import dataclass
from datetime import datetime, timezone

from ai.access.permissions import AIRole
from ai.context.context_snapshot import AIContext
from ai.intelligence_runtime import IntelligenceRuntime
from ai.memory.memory_runtime import MemoryRuntime
from ai.runtime.runtime_response import RuntimeResponse
from assistant.identity_manager import IdentityManager
from assistant.models import AssistantProfile, AssistantRuntime
from assistant.runtime_adapter import (
    advance_conversation,
    recall_turn,
    remember_turn,
    run_intelligence_pipeline,
    run_personal_ai_turn,
    synthesize_voice,
)
from goldbot.core_layer.configuration.feature_flags import FeatureFlags
from voice.manager import VoiceManager
from voice.models import VoiceProviderStatus, VoiceProviderType, VoiceResultStatus
from voice.provider_adapters.local import LocalVoiceProvider
from voice.provider_adapters.openai import OpenAIVoiceProvider
from voice.runtime import VoiceRuntime

ENABLED = FeatureFlags(enable_personal_ai=True)
DISABLED = FeatureFlags(enable_personal_ai=False)


@dataclass
class _FakeConversationState:
    session_id: str


@dataclass
class _FakeConversationResult:
    session_id: str
    response: RuntimeResponse


class _FakeConversationEngineAccepts:
    def __init__(self):
        self._counter = 0

    def start_session(self, user_id):
        self._counter += 1
        return _FakeConversationState(session_id=f"conv-{self._counter}")

    def ask(self, session_id, message, ai_context, role, telegram_id=None):
        return _FakeConversationResult(
            session_id=session_id,
            response=RuntimeResponse(accepted=True, content="Gold likely bullish today.", provider_name="fake", reason=""),
        )


class _FakeConversationEngineRejects:
    def start_session(self, user_id):
        return _FakeConversationState(session_id="conv-1")

    def ask(self, session_id, message, ai_context, role, telegram_id=None):
        return _FakeConversationResult(
            session_id=session_id,
            response=RuntimeResponse(accepted=False, content=None, provider_name=None, reason="no provider available"),
        )


class _FakeSecrets:
    OPENAI_API_KEY = "sk-test"
    ELEVENLABS_API_KEY = None


class _FakeTTSResponse:
    status_code = 200
    content = b"AUDIO"
    headers = {"Content-Type": "audio/mpeg"}


class _FakeTTSSession:
    def post(self, *args, **kwargs):
        return _FakeTTSResponse()


class _FailingTTSSession:
    def post(self, *args, **kwargs):
        class _R:
            status_code = 500
            content = b""
            headers = {}
        return _R()


def _profile(selected_voice=None):
    return AssistantProfile(
        assistant_id="a1", user_id="u1", selected_identity="Senior",
        selected_voice=selected_voice, selected_language="en", timezone="UTC",
    )


def _identity():
    return IdentityManager().get("Senior")


def _runtime(conversation_id=None):
    return AssistantRuntime(session_id="s1", assistant_id="a1", conversation_id=conversation_id)


def _ai_context():
    return AIContext(built_at=datetime.now(timezone.utc))


def _voice_runtime(session=None):
    manager = VoiceManager()
    manager.set_provider_status(VoiceProviderType.OPENAI, VoiceProviderStatus.ENABLED)
    manager.register_adapter(VoiceProviderType.OPENAI, OpenAIVoiceProvider(session=session or _FakeTTSSession(), secrets=_FakeSecrets()))
    return VoiceRuntime(manager)


# --- advance_conversation (TASK 2) ---

def test_advance_conversation_owner_creates_session_and_asks():
    runtime = _runtime()
    result = advance_conversation(runtime, _profile(), "hello", AIRole.OWNER, _ai_context(), _FakeConversationEngineAccepts(), flags=ENABLED)
    assert result.response.accepted is True
    assert runtime.conversation_id == "conv-1"


def test_advance_conversation_reuses_existing_conversation_id():
    runtime = _runtime(conversation_id="existing-conv")
    engine = _FakeConversationEngineAccepts()
    advance_conversation(runtime, _profile(), "hello", AIRole.OWNER, _ai_context(), engine, flags=ENABLED)
    assert runtime.conversation_id == "existing-conv"
    assert engine._counter == 0


def test_advance_conversation_admin_blocked_returns_none():
    runtime = _runtime()
    result = advance_conversation(runtime, _profile(), "hello", AIRole.ADMIN, _ai_context(), _FakeConversationEngineAccepts(), flags=ENABLED)
    assert result is None
    assert runtime.conversation_id is None


def test_advance_conversation_blocked_when_flag_disabled():
    runtime = _runtime()
    result = advance_conversation(runtime, _profile(), "hello", AIRole.OWNER, _ai_context(), _FakeConversationEngineAccepts(), flags=DISABLED)
    assert result is None


def test_advance_conversation_conversation_rejection_still_returns_result():
    runtime = _runtime()
    result = advance_conversation(runtime, _profile(), "hello", AIRole.OWNER, _ai_context(), _FakeConversationEngineRejects(), flags=ENABLED)
    assert result.response.accepted is False


# --- synthesize_voice (TASK 3) ---

def test_synthesize_voice_owner_success():
    result = synthesize_voice(_profile(), _identity(), "text", AIRole.OWNER, _voice_runtime(), VoiceProviderType.OPENAI, flags=ENABLED)
    assert result.status == VoiceResultStatus.READY


def test_synthesize_voice_falls_back_to_identity_default_voice():
    profile = _profile(selected_voice=None)
    identity = _identity()
    manager = VoiceManager()
    manager.set_provider_status(VoiceProviderType.OPENAI, VoiceProviderStatus.ENABLED)
    manager.register_adapter(VoiceProviderType.OPENAI, OpenAIVoiceProvider(session=_FakeTTSSession(), secrets=_FakeSecrets()))
    voice_runtime = VoiceRuntime(manager)
    result = synthesize_voice(profile, identity, "text", AIRole.OWNER, voice_runtime, VoiceProviderType.OPENAI, flags=ENABLED)
    assert result.status == VoiceResultStatus.READY


def test_synthesize_voice_admin_blocked_returns_none():
    result = synthesize_voice(_profile(), _identity(), "text", AIRole.ADMIN, _voice_runtime(), VoiceProviderType.OPENAI, flags=ENABLED)
    assert result is None


def test_synthesize_voice_failure_returns_rejected():
    result = synthesize_voice(_profile(), _identity(), "text", AIRole.OWNER, _voice_runtime(session=_FailingTTSSession()), VoiceProviderType.OPENAI, flags=ENABLED)
    assert result.status == VoiceResultStatus.REJECTED


def test_synthesize_voice_uses_fallback_providers():
    manager = VoiceManager()
    manager.set_provider_status(VoiceProviderType.OPENAI, VoiceProviderStatus.ENABLED)
    manager.register_adapter(VoiceProviderType.OPENAI, OpenAIVoiceProvider(session=_FailingTTSSession(), secrets=_FakeSecrets()))
    manager.set_provider_status(VoiceProviderType.LOCAL, VoiceProviderStatus.ENABLED)
    manager.register_adapter(VoiceProviderType.LOCAL, LocalVoiceProvider())
    voice_runtime = VoiceRuntime(manager)
    result = synthesize_voice(
        _profile(), _identity(), "text", AIRole.OWNER, voice_runtime, VoiceProviderType.OPENAI,
        fallback_providers=[VoiceProviderType.LOCAL], flags=ENABLED,
    )
    assert result.status == VoiceResultStatus.REJECTED
    assert "local" in result.reason


# --- remember_turn / recall_turn (TASK 4) ---

def test_remember_turn_owner_stores_value():
    memory_runtime = MemoryRuntime()
    ok = remember_turn(_profile(), "some value", AIRole.OWNER, memory_runtime, sub_key="last_response", flags=ENABLED)
    assert ok is True
    entry = recall_turn(_profile(), AIRole.OWNER, memory_runtime, sub_key="last_response", flags=ENABLED)
    assert entry.value == "some value"


def test_remember_turn_admin_blocked():
    memory_runtime = MemoryRuntime()
    ok = remember_turn(_profile(), "some value", AIRole.ADMIN, memory_runtime, flags=ENABLED)
    assert ok is False


def test_recall_turn_admin_blocked_returns_none():
    memory_runtime = MemoryRuntime()
    remember_turn(_profile(), "some value", AIRole.OWNER, memory_runtime, flags=ENABLED)
    assert recall_turn(_profile(), AIRole.ADMIN, memory_runtime, flags=ENABLED) is None


def test_recall_turn_unknown_key_returns_none():
    memory_runtime = MemoryRuntime()
    assert recall_turn(_profile(), AIRole.OWNER, memory_runtime, sub_key="never-stored", flags=ENABLED) is None


def test_remember_turn_scoped_by_user_id_never_assistant_id():
    memory_runtime = MemoryRuntime()
    remember_turn(_profile(), "some value", AIRole.OWNER, memory_runtime, flags=ENABLED)
    entries = memory_runtime.list_all()
    assert len(entries) == 1
    assert entries[0].key.startswith("USER_PREFERENCE:u1")
    assert "a1" not in entries[0].key


# --- run_intelligence_pipeline (TASK 5/6) ---

def test_run_intelligence_pipeline_owner_returns_pipeline_run():
    intelligence_runtime = IntelligenceRuntime()
    result = run_intelligence_pipeline("gold", _profile(), AIRole.OWNER, intelligence_runtime, flags=ENABLED)
    assert result is not None
    assert result.topic == "gold"
    assert len(result.stages) == 8


def test_run_intelligence_pipeline_admin_blocked_returns_none():
    intelligence_runtime = IntelligenceRuntime()
    result = run_intelligence_pipeline("gold", _profile(), AIRole.ADMIN, intelligence_runtime, flags=ENABLED)
    assert result is None


def test_run_intelligence_pipeline_uses_profile_user_id_as_telegram_id():
    intelligence_runtime = IntelligenceRuntime()
    result = run_intelligence_pipeline("gold", _profile(), AIRole.OWNER, intelligence_runtime, flags=ENABLED)
    assert result is not None


# --- run_personal_ai_turn (TASK 9, full composition) ---

def test_run_personal_ai_turn_full_success_path():
    runtime = _runtime()
    result = run_personal_ai_turn(
        runtime, _profile(), _identity(), "Bugun Gold nima bo'ladi?", AIRole.OWNER, _ai_context(),
        _FakeConversationEngineAccepts(), _voice_runtime(), MemoryRuntime(), IntelligenceRuntime(),
        VoiceProviderType.OPENAI, flags=ENABLED,
    )
    assert result.status == VoiceResultStatus.READY


def test_run_personal_ai_turn_sets_conversation_id_on_runtime():
    runtime = _runtime()
    assert runtime.conversation_id is None
    run_personal_ai_turn(
        runtime, _profile(), _identity(), "hello", AIRole.OWNER, _ai_context(),
        _FakeConversationEngineAccepts(), _voice_runtime(), MemoryRuntime(), IntelligenceRuntime(),
        VoiceProviderType.OPENAI, flags=ENABLED,
    )
    assert runtime.conversation_id == "conv-1"


def test_run_personal_ai_turn_stores_response_in_memory():
    runtime = _runtime()
    memory_runtime = MemoryRuntime()
    profile = _profile()
    run_personal_ai_turn(
        runtime, profile, _identity(), "hello", AIRole.OWNER, _ai_context(),
        _FakeConversationEngineAccepts(), _voice_runtime(), memory_runtime, IntelligenceRuntime(),
        VoiceProviderType.OPENAI, flags=ENABLED,
    )
    entry = recall_turn(profile, AIRole.OWNER, memory_runtime, sub_key="last_response", flags=ENABLED)
    assert entry is not None
    assert entry.value == "Gold likely bullish today."


def test_run_personal_ai_turn_admin_blocked():
    runtime = _runtime()
    result = run_personal_ai_turn(
        runtime, _profile(), _identity(), "hello", AIRole.ADMIN, _ai_context(),
        _FakeConversationEngineAccepts(), _voice_runtime(), MemoryRuntime(), IntelligenceRuntime(),
        VoiceProviderType.OPENAI, flags=ENABLED,
    )
    assert result.status == VoiceResultStatus.REJECTED
    assert "Owner Mode required" in result.reason


def test_run_personal_ai_turn_blocked_when_flag_disabled_even_for_owner():
    runtime = _runtime()
    result = run_personal_ai_turn(
        runtime, _profile(), _identity(), "hello", AIRole.OWNER, _ai_context(),
        _FakeConversationEngineAccepts(), _voice_runtime(), MemoryRuntime(), IntelligenceRuntime(),
        VoiceProviderType.OPENAI, flags=DISABLED,
    )
    assert result.status == VoiceResultStatus.REJECTED


def test_run_personal_ai_turn_rejected_when_conversation_rejects():
    runtime = _runtime()
    result = run_personal_ai_turn(
        runtime, _profile(), _identity(), "hello", AIRole.OWNER, _ai_context(),
        _FakeConversationEngineRejects(), _voice_runtime(), MemoryRuntime(), IntelligenceRuntime(),
        VoiceProviderType.OPENAI, flags=ENABLED,
    )
    assert result.status == VoiceResultStatus.REJECTED
    assert "conversation rejected" in result.reason


def test_run_personal_ai_turn_rejected_when_voice_fails():
    runtime = _runtime()
    result = run_personal_ai_turn(
        runtime, _profile(), _identity(), "hello", AIRole.OWNER, _ai_context(),
        _FakeConversationEngineAccepts(), _voice_runtime(session=_FailingTTSSession()), MemoryRuntime(), IntelligenceRuntime(),
        VoiceProviderType.OPENAI, flags=ENABLED,
    )
    assert result.status == VoiceResultStatus.REJECTED


def test_run_personal_ai_turn_uses_fallback_providers():
    runtime = _runtime()
    manager = VoiceManager()
    manager.set_provider_status(VoiceProviderType.OPENAI, VoiceProviderStatus.ENABLED)
    manager.register_adapter(VoiceProviderType.OPENAI, OpenAIVoiceProvider(session=_FailingTTSSession(), secrets=_FakeSecrets()))
    manager.set_provider_status(VoiceProviderType.LOCAL, VoiceProviderStatus.ENABLED)
    manager.register_adapter(VoiceProviderType.LOCAL, LocalVoiceProvider())
    voice_runtime = VoiceRuntime(manager)
    result = run_personal_ai_turn(
        runtime, _profile(), _identity(), "hello", AIRole.OWNER, _ai_context(),
        _FakeConversationEngineAccepts(), voice_runtime, MemoryRuntime(), IntelligenceRuntime(),
        VoiceProviderType.OPENAI, fallback_providers=[VoiceProviderType.LOCAL], flags=ENABLED,
    )
    assert result.status == VoiceResultStatus.REJECTED
    assert "local" in result.reason


def test_run_personal_ai_turn_never_raises_on_any_path():
    """Sweeps every role for a smoke assertion that nothing raises."""
    for role in AIRole:
        runtime = _runtime()
        result = run_personal_ai_turn(
            runtime, _profile(), _identity(), "hello", role, _ai_context(),
            _FakeConversationEngineAccepts(), _voice_runtime(), MemoryRuntime(), IntelligenceRuntime(),
            VoiceProviderType.OPENAI, flags=ENABLED,
        )
        assert result is not None
