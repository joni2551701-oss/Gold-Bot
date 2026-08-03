"""
AI Layer — Learning Model (Phase 66.3: AI Learning Intelligence
Foundation, TASK 2/7).

`LearningRecord` follows the same Article 3 resolution
`ai/trading_analyst/models.py`, `ai/chart_intelligence/models.py`, and
`ai/trade_journal/models.py` all already established: every field is a
primitive (`str`/`float`/`int`) or an enum defined in this same file —
never a `decision_layer.decision_engine.models.TradeDecision`, `risk_layer.risk_engine.risk_manager.RiskResult`,
or any other Trading Core object reference. `ai/learning/` never
imports `decision/`, `risk/`, `execution/`, `signals/`, `telegram/`,
`database/`, `monitoring/`, or `strategies/` (Rule 2).

**Naming note** (documented, not a defect — see
`docs/PHASE66_3_AUDIT.md`'s "Conclusion" section): a *different*,
DB-persisted, trade-outcome-statistics type with the same bare class
name already exists at `learning.models.LearningRecord` (Phase 60.6,
`trade_id`/`signal_id`/`failure_type`/`success_pattern`/etc., wired to
real SQLite persistence via `database_layer/journal_repository/learning_repository.py`). This
module's `ai.learning.models.LearningRecord` is a distinct,
non-colliding fully-qualified path, never imported alongside the old
one, and serves a genuinely different purpose (a per-user topic-mastery
record vs. a per-trade outcome-pattern record).

Rule 3 ("Database ishlatilmaydi") means this contract is in-memory
only — no SQLite/Postgres/Redis anywhere in this package. Rule 6/7/8/9
(no trade evaluation, no coaching, no lesson/quiz generation) mean
`level`/`confidence` are always caller-supplied and relayed as-is,
never computed, classified, or graded by this module.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional
from uuid import uuid4


class LearningTopic(Enum):
    """TASK 2's own exact vocabulary -- caller-supplied, never inferred by this package."""

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


class LearningLevel(Enum):
    """TASK 2's own exact vocabulary -- a caller-supplied classification, never graded or computed by this package (Rule 6/7)."""

    UNKNOWN = "UNKNOWN"
    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"
    MASTERED = "MASTERED"


class LearningSource(Enum):
    """TASK 7's own exact vocabulary -- where a LearningRecord originated from, caller-supplied."""

    TRADE = "TRADE"
    JOURNAL = "JOURNAL"
    CHART = "CHART"
    MANUAL = "MANUAL"
    SIMULATION = "SIMULATION"


class LearningStatus(Enum):
    """TASK 7's own exact vocabulary -- a record's own lifecycle state, mutated only via LearningRuntime.archive()."""

    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"
    PENDING = "PENDING"


@dataclass(frozen=True)
class LearningRecord:
    """
    TASK 2's own exact field list: `id`, `user_id`, `topic`, `level`,
    `confidence`, `notes`, `created_at`. Extended with `source` and
    `status` (TASK 7's own vocabulary) so every record can be traced
    to its origin and lifecycle state without a second contract.

    id: this record's own generated identity (`generate_learning_id()`).
    user_id: the trader this record tracks -- a plain string reference,
        never a live `User`/`TelegramUser` object (Constitution Article
        3 -- `database/` is off-limits).
    topic: which skill this record is about -- relayed, never inferred.
    level: the caller-supplied mastery classification -- this module
        never grades or computes it (Rule 6/7: no trade evaluation, no
        coaching).
    confidence: whatever single confidence value the caller supplies,
        relayed as-is -- no scale conversion (same "Journal never
        transforms" posture `ai/trade_journal/models.py`'s own
        `confidence` field already established for its sibling
        concern).
    notes: a short free-text note.
    source: where this record originated (TASK 7).
    status: this record's own lifecycle state (TASK 7), mutated only
        via `LearningRuntime.archive()`.
    created_at: ISO-8601 timestamp string, stamped by
        `LearningRuntime.create()`.
    """

    id: str
    user_id: str
    topic: LearningTopic
    level: LearningLevel = LearningLevel.UNKNOWN
    confidence: Optional[float] = None
    notes: Optional[str] = None
    source: LearningSource = LearningSource.MANUAL
    status: LearningStatus = LearningStatus.ACTIVE
    created_at: str = ""


def generate_learning_id() -> str:
    """Same stateless uuid4 convention as every other generate_X_id() in this codebase (e.g. ai.trade_journal.models.generate_journal_id())."""
    return str(uuid4())
