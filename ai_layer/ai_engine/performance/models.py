"""
AI Layer — Performance Model (Phase 66.5: AI Performance Intelligence
Foundation, TASK 2).

`PerformanceRecord`/`PerformanceMetric`/`PerformanceCategory` follow
the same Article 3 resolution `ai/trade_journal/models.py`,
`ai/ai_layer/knowledge_ai/learning_loop/models.py`, and `ai/coaching/models.py` all already
established: every field is a primitive (`str`/`float`/`bool`) or an
enum defined in this same file -- never a `decision_layer.decision_engine.models.TradeDecision`,
`risk_layer.risk_engine.risk_manager.RiskResult`, or any other Trading Core object
reference. `ai/performance/` never imports `decision/`, `risk/`,
`execution/`, `strategies/`, `signals/`, `context/`, `telegram/`,
`database/`, `voice/`, `assistant/`, `media/`, `broadcast/`,
`academy/`, `portfolio/`, `research/`, `core.`, or `ai_layer.knowledge_ai.memory_manager`.

**Naming note** (documented, not a defect — see
`docs/PHASE66_5_AUDIT.md`'s "Conclusion" section, question 1/4): a
*different*, fixed-shape portfolio-aggregate type with a similar bare
name already exists at `backtesting_layer.statistics.performance_metrics.PerformanceMetrics`
(plural, Phase 60.4 -- `total_trades`/`win_rate`/`expectancy`/
`profit_factor`/etc., computed from `SignalPerformance.r_multiple`).
This module's `PerformanceMetric` (singular) is a distinct,
non-colliding fully-qualified path serving a genuinely different
purpose: a generic, free-form named observation
(`metric_name`/`value`/`period`), not a fixed portfolio report. Never
imported alongside the `analytics/` one.

`archived` on `PerformanceRecord` is an additive field beyond TASK 2's
own listed field set -- added because TASK 3 explicitly requires an
`archive()` method, and every sibling `66.x` runtime
(`CoachingRuntime.archive()`, `LearningRuntime.archive()`) needs a
lifecycle field to archive *onto*. Mirrors `ai_layer.knowledge_ai.learning_engine.models.LearningRecord`'s
own precedent exactly (its `source`/`status` fields were likewise
added beyond TASK 2's original field list, per that phase's own TASK
7 vocabulary need) -- documented here, not a silent scope change.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional
from uuid import uuid4


class PerformanceCategory(Enum):
    """TASK 2's own exact vocabulary -- caller-supplied, never inferred by this package."""

    ENTRY = "ENTRY"
    EXIT = "EXIT"
    RISK = "RISK"
    DISCIPLINE = "DISCIPLINE"
    TIMING = "TIMING"
    PSYCHOLOGY = "PSYCHOLOGY"
    STRATEGY = "STRATEGY"


@dataclass(frozen=True)
class PerformanceRecord:
    """
    TASK 2's own exact field list: `id`, `user_id`, `trade_id`,
    `journal_id`, `result`, `direction`, `entry_quality`,
    `exit_quality`, `discipline_score`, `risk_score`,
    `confidence_score`, `notes`, `created_at`. Extended with
    `archived` (see module docstring).

    id: this record's own generated identity
        (`generate_performance_id()`).
    user_id: the trader this record is about -- a plain string
        reference, never a live `User`/`TelegramUser` object
        (Constitution Article 3 -- `database/` is off-limits).
    trade_id: the originating trade's own identity -- caller-supplied,
        never generated here (this package does not know what a
        "trade" is beyond this string, same posture
        `ai_layer.knowledge_ai.knowledge_base.trade_journal.models.TradeJournalEntry.trade_id` already
        established).
    journal_id: an optional reference to the originating
        `ai_layer.knowledge_ai.knowledge_base.trade_journal.models.TradeJournalEntry.journal_id` -- a
        plain string pointer, never a `TradeJournalEntry` object
        reference.
    result: free-text trade outcome (e.g. "WIN"/"LOSS"/"BE"), no fixed
        taxonomy enforced here -- same "free text, no fixed taxonomy"
        posture `ai_layer.knowledge_ai.knowledge_base.trade_journal.models.TradeJournalEntry.result`
        already uses.
    direction: the already-decided direction this record concerns
        (e.g. "BUY"/"SELL") -- relayed only, never computed here.
    entry_quality/exit_quality/discipline_score/risk_score: caller-
        supplied quality scores (no fixed scale enforced) -- this
        module never computes, grades, or infers any of the four
        (TASK 3's own rule: "AI xulosa bermaydi... scoring algoritm
        yaratmaydi").
    confidence_score: whatever single confidence value the caller
        supplies, relayed as-is -- no scale conversion (same
        "Journal never transforms" posture `ai/trade_journal/models.py`'s
        own `confidence` field already established).
    notes: a short free-text note.
    archived: this record's own lifecycle flag, mutated only via
        `PerformanceRuntime.archive()` (mirrors
        `ai_layer.personal_ai.senior.models.CoachingRecommendation.status`'s own
        "archiving is a dedicated, one-way action" convention, using a
        plain bool instead of a four-state enum since this phase has
        no PENDING/ACTIVE/ACKNOWLEDGED distinction to make).
    created_at: ISO-8601 timestamp string, stamped by
        `PerformanceRuntime.create()`.
    """

    id: str
    user_id: str
    trade_id: str
    journal_id: Optional[str] = None
    result: Optional[str] = None
    direction: Optional[str] = None
    entry_quality: Optional[float] = None
    exit_quality: Optional[float] = None
    discipline_score: Optional[float] = None
    risk_score: Optional[float] = None
    confidence_score: Optional[float] = None
    notes: Optional[str] = None
    archived: bool = False
    created_at: str = ""


@dataclass(frozen=True)
class PerformanceMetric:
    """
    TASK 2's own exact field list: `metric_name`, `value`, `period`,
    `created_at`. "Faqat ma'lumot modeli" (a data model only) -- no
    `id`, no lifecycle, no owning runtime; a plain value object a
    caller constructs directly (see `ai/performance/analytics_adapter.py`).

    metric_name: free-text metric identity (e.g. "win_rate",
        "discipline_score", "fomo_incidents") -- no fixed taxonomy
        enforced here, same "free text, no fixed taxonomy" posture
        `PerformanceRecord.result` already uses. This is also how
        TASK 7's Behavior Tracking vocabulary (Discipline/Patience/
        FOMO/Revenge/Overtrading) is represented: as metric_name
        values, not a new enum -- see `ai/performance/README.md`.
    value: the metric's own numeric value -- always caller-supplied
        or reused from an existing `analytics/` computation (see
        `analytics_adapter.py`), never invented here.
    period: free-text reporting window (e.g. "daily"/"weekly"/"all")
        -- no fixed taxonomy enforced here either.
    created_at: ISO-8601 timestamp string, caller-stamped.
    """

    metric_name: str
    value: float
    period: str
    created_at: str = ""


def generate_performance_id() -> str:
    """Same stateless uuid4 convention as every other generate_X_id() in this codebase (e.g. ai.coaching.models.generate_coach_id())."""
    return str(uuid4())
