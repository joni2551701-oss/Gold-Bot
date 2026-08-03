"""
AI Layer — Coaching Model (Phase 66.4: AI Coaching Intelligence
Foundation, TASK 2).

`CoachingRecommendation` follows the same Article 3 resolution
`ai/trading_analyst/models.py`, `ai/chart_intelligence/models.py`,
`ai/trade_journal/models.py`, and `ai/ai_layer/knowledge_ai/learning_loop/models.py` all already
established: every field is a primitive (`str`/`float`/`Mapping[str,
str]`) or an enum defined in this same file -- never a
`decision_layer.decision_engine.models.TradeDecision`, `risk_layer.risk_engine.risk_manager.RiskResult`, or any
other Trading Core object reference. `ai/coaching/` never imports
`decision/`, `risk/`, `execution/`, `strategies/`, `signals/`,
`context/`, `telegram/`, `database/`, `voice/`, `assistant/`, `media/`,
`broadcast/`, `academy/`, `performance/`, `portfolio/`, `research/`, or
`core.` (TASK 8's own isolation list).

Per `docs/PHASE66_4_AUDIT.md`'s conclusion, no naming collision exists
this phase -- `CoachingRecommendation`, `CoachingTopic`,
`CoachingPriority`, `CoachingType`, and `CoachingStatus` are all new
names with no pre-existing bare-class-name namesake anywhere in the
codebase (unlike `TradeJournalEntry` in Phase 66.2 or `LearningRecord`
in Phase 66.3).

`message`/`recommendation` are always caller-supplied and relayed
as-is -- this module never generates coaching text itself (TASK 3: "LLM
yo'q, Reasoning yo'q, Inference yo'q"). `topic`/`priority`/`type` are
likewise caller-supplied classifications, never computed or graded
here (mirrors `ai/ai_layer/knowledge_ai/learning_loop/models.py`'s own `level` field posture).
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Mapping, Optional
from uuid import uuid4


class CoachingTopic(Enum):
    """
    TASK 2's own vocabulary -- caller-supplied, never inferred by this
    package. Mirrors `ai_layer.knowledge_ai.learning_engine.models.LearningTopic`'s own value
    set for coherence across the Learning -> Coaching pipeline stage,
    but is a separate, local enum (not imported from `ai_layer.knowledge_ai.learning_engine`) --
    `models.py` stays free of any upstream package import, the same
    "adapter-confined import" discipline every prior `66.x` phase
    already established.
    """

    DISCIPLINE = "DISCIPLINE"
    ENTRY = "ENTRY"
    EXIT = "EXIT"
    RISK = "RISK"
    PATIENCE = "PATIENCE"
    STRUCTURE = "STRUCTURE"
    FVG = "FVG"
    OB = "OB"
    LIQUIDITY = "LIQUIDITY"
    TREND = "TREND"
    SESSION = "SESSION"
    PSYCHOLOGY = "PSYCHOLOGY"


class CoachingPriority(Enum):
    """TASK 2's own vocabulary -- a caller-supplied urgency classification, never computed by this package."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class CoachingType(Enum):
    """
    TASK 2's own vocabulary -- what kind of coaching message this
    record carries. Deliberately does not include Daily/Weekly/Monthly
    plan types (Director Notes 3/4) -- those belong to a future,
    separately-briefed phase; this Foundation only classifies the
    message itself.
    """

    FEEDBACK = "FEEDBACK"
    RECOMMENDATION = "RECOMMENDATION"
    WARNING = "WARNING"
    MOTIVATION = "MOTIVATION"
    REMINDER = "REMINDER"


class CoachingStatus(Enum):
    """
    TASK 2's own vocabulary -- this record's own lifecycle state.
    `PENDING` (just created) -> `ACTIVE` (delivered/current) ->
    `ACKNOWLEDGED` (user has seen it) are reachable via
    `CoachingRuntime.update_status()`; `ARCHIVED` is reachable only via
    `CoachingRuntime.archive()` (mirrors
    `ai_layer.knowledge_ai.learning_engine.learning_runtime.LearningRuntime.archive()`'s own
    "archive is a dedicated, one-way action" convention).
    """

    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    ARCHIVED = "ARCHIVED"


@dataclass(frozen=True)
class CoachingRecommendation:
    """
    TASK 2's own exact field list: `coach_id`, `user_id`,
    `learning_id`, `journal_id`, `topic`, `priority`, `type`,
    `message`, `recommendation`, `status`, `created_at`, `metadata`.
    Reordered only as required for dataclass validity (required fields
    first) -- the same reordering convention
    `ai_layer.knowledge_ai.knowledge_base.trade_journal.models.TradeJournalEntry` already used.

    coach_id: this record's own generated identity
        (`generate_coach_id()`).
    user_id: the trader this recommendation is for -- a plain string
        reference, never a live `User`/`TelegramUser` object
        (Constitution Article 3 -- `database/` is off-limits).
    topic: which skill area this recommendation concerns -- relayed,
        never inferred.
    message: the coaching text itself -- always caller-supplied; this
        module never generates it (Rule: no LLM/Reasoning/Inference).
    learning_id: an optional reference to the originating
        `ai_layer.knowledge_ai.learning_engine.models.LearningRecord.id`, when this
        recommendation traces back to a Learning record (TASK 4) --
        a plain string pointer, never a `LearningRecord` object
        reference.
    journal_id: an optional reference to the originating
        `ai_layer.knowledge_ai.knowledge_base.trade_journal.models.TradeJournalEntry.journal_id`, when
        this recommendation traces back to a Trade Journal entry
        (TASK 5) -- a plain string pointer, never a `TradeJournalEntry`
        object reference.
    priority: caller-supplied urgency classification.
    type: caller-supplied message classification.
    recommendation: an optional, short free-text suggested action --
        distinct from `message` (the coaching text) the same way
        `ai_layer.knowledge_ai.knowledge_base.trade_journal.models.TradeJournalEntry.reason` and
        `.lesson` stay two distinct free-text fields.
    status: this record's own lifecycle state, mutated only via
        `CoachingRuntime.update_status()`/`.archive()`.
    created_at: ISO-8601 timestamp string, stamped by
        `CoachingRuntime.create()`.
    metadata: an optional, flat `str` -> `str` mapping for any
        additional caller-supplied context -- primitive values only,
        never a nested object or a Trading Core reference.
    """

    coach_id: str
    user_id: str
    topic: CoachingTopic
    message: str
    learning_id: Optional[str] = None
    journal_id: Optional[str] = None
    priority: CoachingPriority = CoachingPriority.MEDIUM
    type: CoachingType = CoachingType.RECOMMENDATION
    recommendation: Optional[str] = None
    status: CoachingStatus = CoachingStatus.PENDING
    created_at: str = ""
    metadata: Mapping[str, str] = field(default_factory=dict)


def generate_coach_id() -> str:
    """Same stateless uuid4 convention as every other generate_X_id() in this codebase (e.g. ai.learning.models.generate_learning_id())."""
    return str(uuid4())
