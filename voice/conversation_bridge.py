"""
Voice Layer — Voice Conversation Bridge (Phase 65.2, TASK 4/6).

The second composition-root exception in this codebase (the first is
`ai/intelligence_runtime.py`, Phase 64.0) -- see
`docs/PHASE65_2_AUDIT.md`'s own "the one new composition-root file"
section for the full justification. `handle_voice_turn()` composes,
in order: `voice/stt/`'s `STTManager.transcribe()`, `voice/intents/`'s
`detect_intent()` (metadata only, no branching), the *existing*
`ConversationEngine.ask()` (real, LLM-backed call, unmodified), and
the *existing* `VoiceRuntime.generate_audio()`/`generate_with_fallback()`
(unmodified). Zero new business logic in any of the four systems it
composes -- pure orchestration.

Unlike `ai/intelligence_runtime.py` (deliberately deterministic, never
calls `AIService.ask()`), this file's entire purpose is the real,
non-deterministic round trip the Director's own brief asks for --
so it is the one `voice/*.py` file permitted to import
`ai.conversation.conversation_engine.ConversationEngine` and call its
real `ask()` method. `tests/voice/conversation/test_voice_isolation_bridge.py`
enforces that no other `voice/*.py` file does the same.
"""

from dataclasses import replace
from typing import List, Optional

from ai.access.permissions import AIRole
from ai.context.context_snapshot import AIContext
from ai.conversation.conversation_engine import ConversationEngine
from voice.intents.detector import detect_intent
from voice.models import VoiceProviderType, VoiceRequest, VoiceResult, VoiceResultStatus, VoiceSettings
from voice.runtime import VoiceRuntime
from voice.session.models import VoiceSession
from voice.stt.manager import STTManager
from voice.stt.models import STTRequest, STTResultStatus


def handle_voice_turn(
    voice_session: VoiceSession,
    audio: bytes,
    stt_manager: STTManager,
    conversation_engine: ConversationEngine,
    voice_runtime: VoiceRuntime,
    ai_context: AIContext,
    role: AIRole,
    provider_type: VoiceProviderType,
    fallback_providers: Optional[List[VoiceProviderType]] = None,
) -> VoiceResult:
    """
    One full "user speaks -> AI understands -> AI replies by voice"
    round trip. Never raises: every failure mode (STT failure,
    conversation rejection, TTS failure) returns a REJECTED
    `VoiceResult` with a `reason` explaining which step failed --
    never a partial/fabricated result. `intent` (Rule/TASK 3) is
    attached to the final result's `metadata` for observability only;
    no branching in this function reads it this phase.
    """
    stt_request = STTRequest(id=voice_session.session_id, audio=audio, language=voice_session.language)
    stt_result = stt_manager.transcribe(stt_request)
    if stt_result.status != STTResultStatus.READY or not stt_result.text:
        return VoiceResult(
            request_id=voice_session.session_id, status=VoiceResultStatus.REJECTED,
            reason=f"STT failed: {stt_result.reason or 'empty transcription'}",
        )

    intent = detect_intent(stt_result.text)

    if voice_session.conversation_session_id is None:
        conversation_state = conversation_engine.start_session(voice_session.user_id)
        voice_session.conversation_session_id = conversation_state.session_id

    conversation_result = conversation_engine.ask(
        session_id=voice_session.conversation_session_id,
        message=stt_result.text,
        ai_context=ai_context,
        role=role,
        telegram_id=voice_session.user_id,
    )
    if not conversation_result.response.accepted or not conversation_result.response.content:
        return VoiceResult(
            request_id=voice_session.session_id, status=VoiceResultStatus.REJECTED,
            reason=f"conversation rejected: {conversation_result.response.reason}",
            metadata={"intent": intent.value},
        )

    voice_request = VoiceRequest(
        id=voice_session.session_id,
        profile_name=voice_session.voice_profile_name,
        provider_type=provider_type,
        text=conversation_result.response.content,
        settings=VoiceSettings(language=voice_session.language),
    )
    if fallback_providers:
        result = voice_runtime.generate_with_fallback(voice_request, fallback_providers=fallback_providers)
    else:
        result = voice_runtime.generate_audio(voice_request)

    return replace(result, metadata={**result.metadata, "intent": intent.value})
