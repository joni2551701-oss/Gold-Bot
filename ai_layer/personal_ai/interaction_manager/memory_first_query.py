"""Personal AI Core — Memory-First Query Orchestrator (FLOW-017 Production Wiring).

Composition root ONLY. This module writes zero new AI/LLM/prompt/memory
business logic — it composes the EXISTING, unmodified public methods of:

    ConversationEngine.start_session() / .ask()   (the External-AI entry;
        already composes AIService/providers internally)
    MemoryRuntime.recall() / .store()             (the memory store)
    is_personal_ai_enabled_for(role, flags)       (the Owner-Mode gate)

Director FLOW-017 rule: no new LLM, no new Prompt System, no new AI
Engine, no new AI Service, no new Memory System — reuse only.

Memory-first flow (Director order — API is called ONLY on a memory miss):

    User question
      → STEP-1  Memory Search      (MemoryRuntime.recall)
      → STEP-2  hit  → Memory answer, NO API call
      → STEP-3  miss → ConversationEngine.ask  (External AI API)
      → STEP-4  API answer received
      → STEP-5  answer written to Memory  (MemoryRuntime.store)
      → STEP-6  answer returned to the caller (Telegram)

The stored value is a MemoryAnswer (the Director's Memory Contract:
Question / Answer / Topic / Tags / Timestamp / Source / Confidence /
Version). Senior and Seniorita share this exact orchestration —
persona differs only in presentation, never in Knowledge/Memory/API.
"""
from __future__ import annotations

import hashlib
import re
import time
from dataclasses import dataclass, field
from typing import Optional, Sequence

from ai_layer.ai_engine.context.context_snapshot import AIContext
from ai_layer.ai_service.access.permissions import AIRole
from ai_layer.ai_service.assistant.access import is_personal_ai_enabled_for
from ai_layer.knowledge_ai.memory_manager.memory_runtime import MemoryRuntime
from ai_layer.knowledge_ai.memory_manager.models import (
    MemoryEntry,
    MemoryScope,
    MemoryType,
)
from ai_layer.personal_ai.interaction_manager.conversation_engine import ConversationEngine
from core_layer.configuration.feature_flags import DEFAULT_FLAGS, FeatureFlags

MEMORY_KEY_PREFIX = "personal_ai:qa:"
CONTRACT_VERSION = "1.0"
_DEFAULT_SESSION = "personal-ai"


# --- Memory Contract ------------------------------------------------------
@dataclass(frozen=True)
class MemoryAnswer:
    """The Director's Memory Contract — the value stored in MemoryRuntime
    for one answered question. Reuses MemoryRuntime for storage; this is
    only the value shape, not a new memory system."""

    question: str
    answer: str
    topic: str
    tags: Sequence[str] = field(default_factory=tuple)
    timestamp: float = field(default_factory=time.time)
    source: str = "api"
    confidence: float = 0.7
    version: str = CONTRACT_VERSION


@dataclass(frozen=True)
class PersonalAIResult:
    """What the Telegram consumer receives. `source` is one of
    memory / api / denied / failed."""

    answer: str
    source: str
    from_memory: bool
    accepted: bool
    reason: str = ""


def personal_ai_memory_key(question: str) -> str:
    """Deterministic key: normalized question → sha256. The same
    question (case/whitespace-insensitive) always maps to the same key,
    so a repeat question is a memory hit."""
    normalized = re.sub(r"\s+", " ", (question or "").strip().lower())
    digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
    return MEMORY_KEY_PREFIX + digest


def _derive_topic(question: str) -> str:
    q = re.sub(r"\s+", " ", (question or "").strip())
    return (q[:48] or "general")


def _derive_tags(question: str) -> tuple:
    words = re.findall(r"[a-z0-9]{3,}", (question or "").lower())
    seen: list = []
    for w in words:
        if w not in seen:
            seen.append(w)
        if len(seen) >= 5:
            break
    return tuple(seen)


# --- Shared process singletons (composition root owns them) ---------------
_SHARED_MEMORY: Optional[MemoryRuntime] = None
_SHARED_ENGINE: Optional[ConversationEngine] = None


def get_shared_memory_runtime() -> MemoryRuntime:
    """One MemoryRuntime per process, so an answer stored for one
    question is reused on the next identical question."""
    global _SHARED_MEMORY
    if _SHARED_MEMORY is None:
        _SHARED_MEMORY = MemoryRuntime()
    return _SHARED_MEMORY


def get_shared_conversation_engine() -> ConversationEngine:
    global _SHARED_ENGINE
    if _SHARED_ENGINE is None:
        _SHARED_ENGINE = ConversationEngine()
    return _SHARED_ENGINE


def answer_question(
    question: str,
    role: AIRole,
    ai_context: Optional[AIContext] = None,
    *,
    conversation_engine: Optional[ConversationEngine] = None,
    memory_runtime: Optional[MemoryRuntime] = None,
    telegram_id: Optional[str] = None,
    flags: FeatureFlags = DEFAULT_FLAGS,
    session_id: str = _DEFAULT_SESSION,
) -> PersonalAIResult:
    """Memory-first Personal AI answer. Never raises.

    Owner-Mode gate first, then Memory Search; the External AI API is
    reached ONLY when Memory has no stored answer for this question.
    """
    text = (question or "").strip()
    if not text:
        return PersonalAIResult(answer="", source="failed", from_memory=False,
                                accepted=False, reason="empty question")

    # Owner-Mode gate (unmodified reuse) — API/Memory are never touched
    # for a role that is not entitled.
    if not is_personal_ai_enabled_for(role, flags):
        return PersonalAIResult(answer="", source="denied", from_memory=False,
                                accepted=False, reason="personal ai disabled or role not owner")

    memory = memory_runtime or get_shared_memory_runtime()
    key = personal_ai_memory_key(text)

    # STEP-1 / STEP-2 — Memory Search. On a hit the API is NOT called.
    entry = memory.recall(key)
    if entry is not None and isinstance(entry.value, MemoryAnswer):
        return PersonalAIResult(answer=entry.value.answer, source="memory",
                                from_memory=True, accepted=True, reason="memory hit")

    # STEP-3 / STEP-4 — memory miss → External AI API.
    engine = conversation_engine or get_shared_conversation_engine()
    context = ai_context or AIContext()
    try:
        state = engine.start_session(telegram_id or _DEFAULT_SESSION)
        result = engine.ask(session_id=state.session_id, message=text,
                            ai_context=context, role=role, telegram_id=telegram_id)
    except Exception as exc:  # noqa: BLE001 - never raise into the Telegram consumer
        return PersonalAIResult(answer="", source="failed", from_memory=False,
                                accepted=False, reason=f"ai error: {exc}")

    response = getattr(result, "response", None)
    if response is None or not response.accepted or not response.content:
        reason = response.reason if response is not None else "no response"
        return PersonalAIResult(answer="", source="failed", from_memory=False,
                                accepted=False, reason=reason)

    # STEP-5 — write the answer to Memory for future reuse.
    confidence = 0.7
    try:
        confidence = float(response.metadata.get("confidence", 0.7))
    except (TypeError, ValueError, AttributeError):
        confidence = 0.7
    stored = MemoryAnswer(
        question=text, answer=response.content, topic=_derive_topic(text),
        tags=_derive_tags(text), timestamp=time.time(),
        source="api", confidence=confidence, version=CONTRACT_VERSION,
    )
    memory.store(MemoryEntry(key=key, scope=MemoryScope.KNOWLEDGE_REFERENCE,
                             memory_type=MemoryType.LONG_TERM, value=stored))

    # STEP-6 — return.
    return PersonalAIResult(answer=response.content, source="api",
                            from_memory=False, accepted=True, reason="api")
