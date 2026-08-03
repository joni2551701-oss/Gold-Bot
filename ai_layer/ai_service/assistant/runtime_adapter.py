"""
Assistant Layer — Runtime Adapter (Phase 65.4: Personal AI Runtime
Integration, TASK 2/3/4/5/6/9).

The third composition-root-shaped file in this codebase (after
`ai_layer/ai_engine/intelligence_runtime.py` and `ai_layer/voice_ai/conversation_bridge.py`) --
the one file in `assistant/` permitted to import
`ai_layer.personal_ai.interaction_manager.conversation_engine`, `ai_layer.ai_engine.intelligence_runtime`,
`ai_layer.knowledge_ai.memory_manager.memory_runtime`/`ai_layer.knowledge_ai.memory_manager.models`, and
`ai_layer.voice_ai.runtime`/`ai_layer.voice_ai.models`. Every other file in this package keeps
the zero-downstream-import posture Phase 65.3 established. See
`docs/PHASE65_4_AUDIT.md` for the full reasoning.

Composes real, unmodified public methods only -- zero new business
logic of its own, the same "the composed systems do the work" posture
`ai_layer/voice_ai/conversation_bridge.py` already established:

    ConversationEngine.start_session() / .ask()                (TASK 2)
    VoiceRuntime.generate_audio() / .generate_with_fallback()   (TASK 3)
    MemoryRuntime.store() / .recall()                           (TASK 4)
    IntelligenceRuntime.run()                                   (TASK 5/6
        -- already composes Knowledge/Memory/Reasoning/Explanation/
        Content/Media/Broadcast internally; this module never calls
        ReasoningRuntime directly, only through this one method)

Every entry point requires `role: AIRole` and re-checks
`ai_layer.ai_service.assistant.access.is_personal_ai_enabled_for()` itself (defense in
depth alongside `AssistantManager.create_runtime()`'s own gate) --
Owner Mode holds even if a caller reaches this module directly.
"""

from typing import Any, List, Optional

from ai_layer.ai_service.access.permissions import AIRole
from ai_layer.ai_engine.context.context_snapshot import AIContext
from ai_layer.personal_ai.interaction_manager.conversation_engine import ConversationEngine, ConversationResult
from ai_layer.ai_engine.intelligence_runtime import IntelligenceRuntime, PipelineRun
from ai_layer.knowledge_ai.memory_manager.memory_runtime import MemoryRuntime
from ai_layer.knowledge_ai.memory_manager.models import MemoryEntry, MemoryScope, MemoryType
from ai_layer.ai_service.assistant.access import is_personal_ai_enabled_for
from ai_layer.ai_service.assistant.conversation_adapter import assistant_memory_scope_key, assistant_to_voice_session_params
from ai_layer.ai_service.assistant.identity import AssistantIdentity
from ai_layer.ai_service.assistant.models import AssistantProfile, AssistantRuntime
from core_layer.configuration.feature_flags import DEFAULT_FLAGS, FeatureFlags
from ai_layer.voice_ai.models import VoiceProviderType, VoiceResult, VoiceResultStatus, VoiceSettings
from ai_layer.voice_ai.runtime import VoiceRuntime


def advance_conversation(
    runtime: AssistantRuntime,
    profile: AssistantProfile,
    message: str,
    role: AIRole,
    ai_context: AIContext,
    conversation_engine: ConversationEngine,
    flags: FeatureFlags = DEFAULT_FLAGS,
) -> Optional[ConversationResult]:
    """
    TASK 2. Never raises: a denied role returns None before
    `ConversationEngine` is ever touched. Creates a session via
    `start_session()` the first time `runtime.conversation_id` is
    unset, and stores the pointer back onto `runtime` -- a real side
    effect, not a fabricated one, mirroring
    `ai_layer/voice_ai/conversation_bridge.py`'s own session-linking behavior.
    """
    if not is_personal_ai_enabled_for(role, flags):
        return None
    if runtime.conversation_id is None:
        state = conversation_engine.start_session(profile.user_id)
        runtime.conversation_id = state.session_id
    return conversation_engine.ask(
        session_id=runtime.conversation_id, message=message, ai_context=ai_context,
        role=role, telegram_id=profile.user_id,
    )


def synthesize_voice(
    profile: AssistantProfile,
    identity: AssistantIdentity,
    text: str,
    role: AIRole,
    voice_runtime: VoiceRuntime,
    provider_type: VoiceProviderType,
    fallback_providers: Optional[List[VoiceProviderType]] = None,
    request_id: Optional[str] = None,
    flags: FeatureFlags = DEFAULT_FLAGS,
) -> Optional[VoiceResult]:
    """TASK 3. Never raises: a denied role returns None before `VoiceRuntime` is ever touched. Voice profile/language are resolved via `assistant_to_voice_session_params()` (Phase 65.3) -- "Voice: Auto" falls back to `identity.default_voice` when `profile.selected_voice` is unset."""
    if not is_personal_ai_enabled_for(role, flags):
        return None
    params = assistant_to_voice_session_params(profile, identity)
    request = voice_runtime.build_request(
        request_id=request_id or profile.assistant_id, profile_name=params["voice_profile_name"],
        provider_type=provider_type, text=text, settings=VoiceSettings(language=params["language"]),
    )
    if fallback_providers:
        return voice_runtime.generate_with_fallback(request, fallback_providers=fallback_providers)
    return voice_runtime.generate_audio(request)


def remember_turn(
    profile: AssistantProfile,
    value: Any,
    role: AIRole,
    memory_runtime: MemoryRuntime,
    sub_key: Optional[str] = None,
    flags: FeatureFlags = DEFAULT_FLAGS,
) -> bool:
    """TASK 4. Never raises: a denied role returns False before `MemoryRuntime` is ever touched. Keyed via `assistant_memory_scope_key()` (Phase 65.3), always by `profile.user_id` -- Assistant is never the memory owner."""
    if not is_personal_ai_enabled_for(role, flags):
        return False
    key = assistant_memory_scope_key(profile, sub_key=sub_key)
    memory_runtime.store(MemoryEntry(key=key, scope=MemoryScope.USER_PREFERENCE, memory_type=MemoryType.SHORT_TERM, value=value))
    return True


def recall_turn(
    profile: AssistantProfile,
    role: AIRole,
    memory_runtime: MemoryRuntime,
    sub_key: Optional[str] = None,
    flags: FeatureFlags = DEFAULT_FLAGS,
) -> Optional[MemoryEntry]:
    """TASK 4. Never raises: a denied role or an unknown key both return None."""
    if not is_personal_ai_enabled_for(role, flags):
        return None
    key = assistant_memory_scope_key(profile, sub_key=sub_key)
    return memory_runtime.recall(key)


def run_intelligence_pipeline(
    topic: str,
    profile: AssistantProfile,
    role: AIRole,
    intelligence_runtime: IntelligenceRuntime,
    flags: FeatureFlags = DEFAULT_FLAGS,
) -> Optional[PipelineRun]:
    """TASK 5/6. Never raises: a denied role returns None. Reuses `IntelligenceRuntime.run()` exactly as-is (Phase 64.0, unmodified) -- Reasoning is reached only through this one call, which already composes `ReasoningRuntime` internally; this module never imports or calls it directly."""
    if not is_personal_ai_enabled_for(role, flags):
        return None
    return intelligence_runtime.run(topic=topic, telegram_id=profile.user_id)


def run_personal_ai_turn(
    runtime: AssistantRuntime,
    profile: AssistantProfile,
    identity: AssistantIdentity,
    message: str,
    role: AIRole,
    ai_context: AIContext,
    conversation_engine: ConversationEngine,
    voice_runtime: VoiceRuntime,
    memory_runtime: MemoryRuntime,
    intelligence_runtime: IntelligenceRuntime,
    provider_type: VoiceProviderType,
    fallback_providers: Optional[List[VoiceProviderType]] = None,
    flags: FeatureFlags = DEFAULT_FLAGS,
) -> VoiceResult:
    """
    TASK 9. The full round trip: Assistant -> Conversation -> Voice ->
    Runtime -> Media -> Broadcast (Media/Broadcast are reached inside
    `run_intelligence_pipeline()`'s own `IntelligenceRuntime.run()`
    call, not duplicated here). Never raises: every failure path
    (denied role, conversation rejection, TTS failure) returns a
    REJECTED `VoiceResult` explaining which step failed -- the same
    "never fabricate" convention `ai_layer/voice_ai/conversation_bridge.py`'s
    `handle_voice_turn()` already established.
    """
    if not is_personal_ai_enabled_for(role, flags):
        return VoiceResult(
            request_id=runtime.session_id, status=VoiceResultStatus.REJECTED,
            reason="Owner Mode required: role is not entitled to Personal AI Assistant",
        )

    run_intelligence_pipeline(message, profile, role, intelligence_runtime, flags=flags)

    conversation_result = advance_conversation(runtime, profile, message, role, ai_context, conversation_engine, flags=flags)
    if conversation_result is None or not conversation_result.response.accepted or not conversation_result.response.content:
        reason = conversation_result.response.reason if conversation_result is not None else "unknown"
        return VoiceResult(request_id=runtime.session_id, status=VoiceResultStatus.REJECTED, reason=f"conversation rejected: {reason}")

    remember_turn(profile, conversation_result.response.content, role, memory_runtime, sub_key="last_response", flags=flags)

    voice_result = synthesize_voice(
        profile, identity, conversation_result.response.content, role, voice_runtime, provider_type,
        fallback_providers=fallback_providers, request_id=runtime.session_id, flags=flags,
    )
    if voice_result is None:
        return VoiceResult(
            request_id=runtime.session_id, status=VoiceResultStatus.REJECTED,
            reason="voice synthesis blocked: role is not entitled to Personal AI Assistant",
        )
    return voice_result
