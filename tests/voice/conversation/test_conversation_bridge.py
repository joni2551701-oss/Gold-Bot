"""Phase 65.2 TASK 4/6 — voice/conversation_bridge.py: handle_voice_turn(), the composition-root function."""

from dataclasses import dataclass
from datetime import datetime, timezone

from ai.access.permissions import AIRole
from ai.context.context_snapshot import AIContext
from ai.runtime.runtime_response import RuntimeResponse
from voice.conversation_bridge import handle_voice_turn
from voice.manager import VoiceManager
from voice.models import VoiceProviderStatus, VoiceProviderType, VoiceResultStatus
from voice.provider_adapters.openai import OpenAIVoiceProvider
from voice.runtime import VoiceRuntime
from voice.session.models import VoiceSession
from voice.stt.manager import STTManager
from voice.stt.providers.openai import OpenAISTTProvider


class _FakeSecrets:
    OPENAI_API_KEY = "sk-test"
    ELEVENLABS_API_KEY = None


class _FakeSTTResponse:
    status_code = 200

    def __init__(self, text="why did you take this gold trade"):
        self._text = text

    def json(self):
        return {"text": self._text}


class _FakeSTTSession:
    def __init__(self, text="why did you take this gold trade"):
        self._text = text

    def post(self, *args, **kwargs):
        return _FakeSTTResponse(self._text)


class _FakeSTTFailResponse:
    status_code = 500

    def json(self):
        return {}


class _FakeSTTFailSession:
    def post(self, *args, **kwargs):
        return _FakeSTTFailResponse()


class _FakeTTSResponse:
    status_code = 200
    content = b"AUDIO"
    headers = {"Content-Type": "audio/mpeg"}


class _FakeTTSSession:
    def post(self, *args, **kwargs):
        return _FakeTTSResponse()


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
            response=RuntimeResponse(accepted=True, content="This is why we took the trade.", provider_name="fake", reason=""),
        )


class _FakeConversationEngineRejects:
    def start_session(self, user_id):
        return _FakeConversationState(session_id="conv-1")

    def ask(self, session_id, message, ai_context, role, telegram_id=None):
        return _FakeConversationResult(
            session_id=session_id,
            response=RuntimeResponse(accepted=False, content=None, provider_name=None, reason="no provider available"),
        )


def _voice_runtime(session=None):
    manager = VoiceManager()
    manager.set_provider_status(VoiceProviderType.OPENAI, VoiceProviderStatus.ENABLED)
    manager.register_adapter(VoiceProviderType.OPENAI, OpenAIVoiceProvider(session=session or _FakeTTSSession(), secrets=_FakeSecrets()))
    return VoiceRuntime(manager)


def _stt_manager(session=None):
    manager = STTManager()
    manager.register_adapter(OpenAISTTProvider(session=session or _FakeSTTSession(), secrets=_FakeSecrets()))
    manager.set_active_provider("openai")
    return manager


def _ai_context():
    return AIContext(built_at=datetime.now(timezone.utc))


def test_handle_voice_turn_full_success_path():
    session = VoiceSession(session_id="vs1", user_id="user1", voice_profile_name="Senior", language="en")
    result = handle_voice_turn(
        voice_session=session, audio=b"FAKEAUDIO", stt_manager=_stt_manager(),
        conversation_engine=_FakeConversationEngineAccepts(), voice_runtime=_voice_runtime(),
        ai_context=_ai_context(), role=AIRole.FREE, provider_type=VoiceProviderType.OPENAI,
    )
    assert result.status == VoiceResultStatus.READY
    assert result.metadata["intent"] == "TRADE_EXPLANATION"


def test_handle_voice_turn_creates_conversation_session_when_missing():
    session = VoiceSession(session_id="vs1", user_id="user1", voice_profile_name="Senior", language="en")
    assert session.conversation_session_id is None
    handle_voice_turn(
        voice_session=session, audio=b"FAKEAUDIO", stt_manager=_stt_manager(),
        conversation_engine=_FakeConversationEngineAccepts(), voice_runtime=_voice_runtime(),
        ai_context=_ai_context(), role=AIRole.FREE, provider_type=VoiceProviderType.OPENAI,
    )
    assert session.conversation_session_id == "conv-1"


def test_handle_voice_turn_reuses_existing_conversation_session():
    session = VoiceSession(session_id="vs1", user_id="user1", voice_profile_name="Senior", language="en", conversation_session_id="existing-conv")
    engine = _FakeConversationEngineAccepts()
    handle_voice_turn(
        voice_session=session, audio=b"FAKEAUDIO", stt_manager=_stt_manager(),
        conversation_engine=engine, voice_runtime=_voice_runtime(),
        ai_context=_ai_context(), role=AIRole.FREE, provider_type=VoiceProviderType.OPENAI,
    )
    assert session.conversation_session_id == "existing-conv"
    assert engine._counter == 0


def test_handle_voice_turn_rejected_when_stt_fails():
    session = VoiceSession(session_id="vs2", user_id="user2", voice_profile_name="Senior", language="en")
    result = handle_voice_turn(
        voice_session=session, audio=b"FAKEAUDIO", stt_manager=_stt_manager(session=_FakeSTTFailSession()),
        conversation_engine=_FakeConversationEngineAccepts(), voice_runtime=_voice_runtime(),
        ai_context=_ai_context(), role=AIRole.FREE, provider_type=VoiceProviderType.OPENAI,
    )
    assert result.status == VoiceResultStatus.REJECTED
    assert "STT failed" in result.reason


def test_handle_voice_turn_rejected_when_conversation_rejects():
    session = VoiceSession(session_id="vs3", user_id="user3", voice_profile_name="Senior", language="en")
    result = handle_voice_turn(
        voice_session=session, audio=b"FAKEAUDIO", stt_manager=_stt_manager(),
        conversation_engine=_FakeConversationEngineRejects(), voice_runtime=_voice_runtime(),
        ai_context=_ai_context(), role=AIRole.FREE, provider_type=VoiceProviderType.OPENAI,
    )
    assert result.status == VoiceResultStatus.REJECTED
    assert "conversation rejected" in result.reason
    assert result.metadata["intent"] == "TRADE_EXPLANATION"


def test_handle_voice_turn_rejected_when_tts_fails():
    session = VoiceSession(session_id="vs4", user_id="user4", voice_profile_name="Senior", language="en")

    class _FailingTTSSession:
        def post(self, *args, **kwargs):
            class _R:
                status_code = 500
                content = b""
                headers = {}
            return _R()

    result = handle_voice_turn(
        voice_session=session, audio=b"FAKEAUDIO", stt_manager=_stt_manager(),
        conversation_engine=_FakeConversationEngineAccepts(), voice_runtime=_voice_runtime(session=_FailingTTSSession()),
        ai_context=_ai_context(), role=AIRole.FREE, provider_type=VoiceProviderType.OPENAI,
    )
    assert result.status == VoiceResultStatus.REJECTED


def test_handle_voice_turn_uses_fallback_providers_when_given():
    session = VoiceSession(session_id="vs5", user_id="user5", voice_profile_name="Senior", language="en")
    manager = VoiceManager()
    manager.set_provider_status(VoiceProviderType.OPENAI, VoiceProviderStatus.ENABLED)

    class _FailingSession:
        def post(self, *args, **kwargs):
            class _R:
                status_code = 500
                content = b""
                headers = {}
            return _R()

    manager.register_adapter(VoiceProviderType.OPENAI, OpenAIVoiceProvider(session=_FailingSession(), secrets=_FakeSecrets()))
    manager.set_provider_status(VoiceProviderType.LOCAL, VoiceProviderStatus.ENABLED)
    from voice.provider_adapters.local import LocalVoiceProvider
    manager.register_adapter(VoiceProviderType.LOCAL, LocalVoiceProvider())
    runtime = VoiceRuntime(manager)

    result = handle_voice_turn(
        voice_session=session, audio=b"FAKEAUDIO", stt_manager=_stt_manager(),
        conversation_engine=_FakeConversationEngineAccepts(), voice_runtime=runtime,
        ai_context=_ai_context(), role=AIRole.FREE, provider_type=VoiceProviderType.OPENAI,
        fallback_providers=[VoiceProviderType.LOCAL],
    )
    assert result.status == VoiceResultStatus.REJECTED
    assert "local" in result.reason
