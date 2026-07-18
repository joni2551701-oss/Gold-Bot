"""
AI Layer — Intelligence Runtime (Phase 64.0: AI Intelligence
Integration Layer).

The one composition root for the Official Intelligence Pipeline
(`docs/roadmap/AI_EVOLUTION.md`): `Knowledge -> Memory -> Reasoning ->
Conversation -> Explanation -> Content -> Media -> Broadcast`. Per
`docs/PHASE64_0_AUDIT.md`'s own finding, no orchestrator existed
anywhere in the codebase before this phase -- `docs/architecture/AI_FLOW.md`
and `docs/ai/AI_PIPELINE.md` only describe the composition order in
prose. `IntelligenceRuntime` adds zero new business logic to any
layer: every stage below calls that layer's own existing, LOCKed
deterministic entry point (never a `generate()`/`ask()`/LLM-calling
path) and, where one already exists, that layer's own cross-layer
adapter function -- see the audit's per-layer table for the exact
method used from each.

This is deliberately a **stub**: `run()` demonstrates that all eight
layers compose in the correct dependency order using only primitive
values and dataclasses as inputs/outputs between stages (Rule 4 — no
`DecisionResult`/`RiskResult`/`TradeContext` ever crosses a stage
boundary here, and none of these types are even importable from this
module's own dependency set). It performs no real content generation
of its own -- Knowledge lookup, deterministic Memory/Reasoning
storage, a deterministic Conversation turn, template-based Explanation,
and deterministic Content/Media/Broadcast asset creation, nothing more.

`IntelligenceRuntime` is the one narrow, explicit exception to "a
layer only imports its own upstream layers" (see the audit's own
"why this one file may import every layer" section) -- the same
composition-root role `core/pipeline.py` already plays for the Trading
layer. Every individual layer's own isolation is otherwise unchanged
and still independently tested.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

from ai.content.content_adapter import ContentEngine
from ai.content.content_types import ContentType
from ai.conversation.conversation_engine import ConversationEngine
from ai.explanation.explanation_builder import ExplanationBuilder
from ai.explanation.explanation_input import ExplanationInput, ExplanationMode
from ai.memory.memory_runtime import MemoryRuntime
from ai.memory.models import MemoryEntry, MemoryScope, MemoryType
from ai.reasoning.reasoning_adapters import (
    reasoning_result_to_explanation_fields,
    step_from_knowledge_entry,
)
from ai.reasoning.reasoning_runtime import ReasoningRuntime
from ai.reasoning.models import ReasoningMode, ReasoningResult, ReasoningType
from broadcast.broadcast_adapter import broadcast_asset_from_content_and_media
from broadcast.broadcast_manager import BroadcastManager
from knowledge.knowledge_manager import KnowledgeManager
from media.media_manager import MediaManager
from media.media_pipeline import prepare_media_from_content
from media.media_types import MediaType


class PipelineStage(Enum):
    KNOWLEDGE = "KNOWLEDGE"
    MEMORY = "MEMORY"
    REASONING = "REASONING"
    CONVERSATION = "CONVERSATION"
    EXPLANATION = "EXPLANATION"
    CONTENT = "CONTENT"
    MEDIA = "MEDIA"
    BROADCAST = "BROADCAST"


@dataclass(frozen=True)
class PipelineStageResult:
    """`detail` is a short, human-readable primitive string -- never the stage's own dataclass object, so a caller of run() never receives another layer's internal shape."""
    stage: PipelineStage
    ok: bool
    detail: str = ""


@dataclass(frozen=True)
class PipelineRun:
    topic: str
    stages: List[PipelineStageResult] = field(default_factory=list)


class IntelligenceRuntime:
    """Every dependency is injectable, same convention as every other Phase 61.x/62.x/63.x manager."""

    def __init__(
        self,
        knowledge_manager: Optional[KnowledgeManager] = None,
        memory_runtime: Optional[MemoryRuntime] = None,
        reasoning_runtime: Optional[ReasoningRuntime] = None,
        conversation_engine: Optional[ConversationEngine] = None,
        explanation_builder: Optional[ExplanationBuilder] = None,
        content_engine: Optional[ContentEngine] = None,
        media_manager: Optional[MediaManager] = None,
        broadcast_manager: Optional[BroadcastManager] = None,
    ) -> None:
        self._knowledge = knowledge_manager or KnowledgeManager()
        self._memory = memory_runtime or MemoryRuntime()
        self._reasoning = reasoning_runtime or ReasoningRuntime()
        self._conversation = conversation_engine or ConversationEngine()
        self._explanation = explanation_builder or ExplanationBuilder()
        self._content = content_engine or ContentEngine()
        self._media = media_manager or MediaManager()
        self._broadcast = broadcast_manager or BroadcastManager()

    def run(self, topic: str, telegram_id: str = "intelligence-runtime") -> PipelineRun:
        """Never raises: every stage below is deterministic and each already-existing manager's own methods never raise for the inputs this method supplies. Walks all eight layers in Official Intelligence Pipeline order, stopping early (recording a not-ok stage) only if an upstream stage produced nothing usable for the next one."""
        stages: List[PipelineStageResult] = []

        # --- KNOWLEDGE ---
        entries = self._knowledge.search(topic)
        knowledge_summary = entries[0].summary if entries else ""
        stages.append(PipelineStageResult(
            PipelineStage.KNOWLEDGE, ok=bool(entries),
            detail=f"{len(entries)} entr{'y' if len(entries) == 1 else 'ies'} matched" if entries else "no knowledge entry matched",
        ))

        # --- MEMORY ---
        memory_key = f"intelligence:{topic}"
        self._memory.store(MemoryEntry(
            key=memory_key, scope=MemoryScope.KNOWLEDGE_REFERENCE,
            memory_type=MemoryType.SHORT_TERM, value=knowledge_summary,
        ))
        recalled = self._memory.recall(memory_key)
        stages.append(PipelineStageResult(
            PipelineStage.MEMORY, ok=recalled is not None, detail=f"stored under key {memory_key}",
        ))

        # --- REASONING ---
        steps = (step_from_knowledge_entry(entries[0]),) if entries else ()
        reasoning_result = self._reasoning.reason(ReasoningResult(
            key=memory_key, mode=ReasoningMode.EDUCATION, reasoning_type=ReasoningType.SUMMARY,
            conclusion=knowledge_summary or f"No knowledge found for '{topic}'.",
            steps=steps, confidence=1.0 if entries else 0.0,
        ))
        stages.append(PipelineStageResult(
            PipelineStage.REASONING, ok=True, detail=reasoning_result.conclusion,
        ))

        # --- CONVERSATION ---
        session = self._conversation.start_session(telegram_id)
        appended = self._conversation.append(session.session_id, "system", reasoning_result.conclusion)
        stages.append(PipelineStageResult(
            PipelineStage.CONVERSATION, ok=appended, detail=f"session {session.session_id}",
        ))

        # --- EXPLANATION ---
        explanation_fields = reasoning_result_to_explanation_fields(reasoning_result)
        explanation_output = self._explanation.build(ExplanationInput(
            mode=ExplanationMode.EDUCATION, symbol=topic, concept=topic,
            lesson=reasoning_result.conclusion, technical_reason=explanation_fields["technical_reason"],
            confidence=explanation_fields["confidence"],
        ))
        stages.append(PipelineStageResult(
            PipelineStage.EXPLANATION, ok=True, detail=explanation_output.title,
        ))

        # --- CONTENT ---
        content_result = self._content.create(
            ContentType.EDUCATION, title=explanation_output.title, body=explanation_output.body,
        )
        stages.append(PipelineStageResult(
            PipelineStage.CONTENT, ok=content_result.accepted, detail=content_result.title,
        ))

        # --- MEDIA ---
        media_asset = prepare_media_from_content(content_result, self._media, media_type=MediaType.TEXT)
        stages.append(PipelineStageResult(
            PipelineStage.MEDIA, ok=media_asset is not None,
            detail=media_asset.status.value if media_asset else "no media asset produced",
        ))

        # --- BROADCAST ---
        broadcast_asset = None
        if media_asset is not None:
            broadcast_asset = broadcast_asset_from_content_and_media(
                content_result, media_asset, self._broadcast, broadcast_type=ContentType.EDUCATION,
            )
            if broadcast_asset is not None:
                broadcast_asset = self._broadcast.prepare_broadcast(broadcast_asset)
        stages.append(PipelineStageResult(
            PipelineStage.BROADCAST, ok=broadcast_asset is not None,
            detail=broadcast_asset.status.value if broadcast_asset else "no broadcast asset produced",
        ))

        return PipelineRun(topic=topic, stages=stages)
