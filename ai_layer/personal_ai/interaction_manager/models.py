"""
AI Layer — Conversation Model (Phase 63.5, TASK 2).

`ConversationMode` and `ConversationContext` are the two genuine gaps
this phase's Foundation Reuse Audit found (`docs/PHASE63_5_AUDIT.md`).
`ConversationContext`'s own fields are primitive, enum, or the
already-existing, already-primitive `ai_layer.ai_service.session.conversation_state.ConversationTurn`
-- no `DecisionResult`, `RiskResult`, `Trade`, `Position`, or `Order`
anywhere. No parallel `ConversationMessage`/`ConversationSession`
class is created here -- those concepts are already covered by the
existing `ConversationTurn`/`ConversationState` (Phase 61.0), and no
`ConversationResult` is created either -- see the audit's own naming
resolution for why.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Sequence

from ai_layer.ai_service.session.conversation_state import ConversationTurn


class ConversationMode(Enum):
    GENERAL = "GENERAL"
    MARKET = "MARKET"
    EDUCATION = "EDUCATION"


@dataclass(frozen=True)
class ConversationContext:
    """
    `knowledge_keys`/`memory_keys`/`reasoning_keys` are free-text
    pointer strings (produced by `conversation_adapters.py`), never an
    embedded `KnowledgeEntry`/`MemoryEntry`/`ReasoningResult` object --
    `ConversationContext` never carries another package's object
    graph, the same posture `ai/reasoning/models.py`'s `ReasoningStep.source`
    already established in Phase 63.4.
    """
    session_id: str
    telegram_id: str
    mode: ConversationMode
    recent_messages: Sequence[ConversationTurn] = field(default_factory=tuple)
    knowledge_keys: Sequence[str] = field(default_factory=tuple)
    memory_keys: Sequence[str] = field(default_factory=tuple)
    reasoning_keys: Sequence[str] = field(default_factory=tuple)
