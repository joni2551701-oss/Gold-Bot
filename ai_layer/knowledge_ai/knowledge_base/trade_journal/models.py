"""
AI Layer — Trade Journal Model (Phase 66.2: AI Trade Journal
Intelligence Foundation, TASK 2/3).

`TradeJournalEntry` follows the same Article 3 resolution
`ai/trading_analyst/models.py` and `ai/chart_intelligence/models.py`
both already established: every field is a primitive
(`str`/`float`/`Sequence[str]`) — never a `decision_layer.decision_engine.models.TradeDecision`,
`risk_layer.risk_engine.risk_manager.RiskResult`, or any other Trading Core object
reference. `ai/trade_journal/` never imports `decision/`, `risk/`,
`execution/`, `strategies/`, `signals/`, `context/`, or `monitoring/`.

**Naming note** (documented, not a defect — see
`docs/PHASE66_2_AUDIT.md`'s "Conclusion" section): a *different*,
Trading-Core-coupled, Phase 55-era type with the same bare class name
already exists at `ai_layer.knowledge_ai.knowledge_base.journal.trade_journal.TradeJournalEntry`
(imports `signal_layer.signal_builder.models.SignalType`, predates Constitution Article 3).
This module's `ai_layer.knowledge_ai.knowledge_base.trade_journal.models.TradeJournalEntry` is a
distinct, non-colliding fully-qualified path, never imported alongside
the old one, and serves a genuinely different purpose (a narrative,
`chart_id`-linked journal record vs. a computed pnl/outcome record).

Rule 3 ("Journal database emas") means this contract is in-memory
only — no SQLite/Postgres/Redis anywhere in this package.
Rule 4 ("Journal ... Faqat yozadi") means no field here is computed,
scored, or classified by this module; every value is caller-supplied
and relayed as-is, including `confidence` (no 0-100 -> 0.0-1.0
conversion here, unlike `TradingAnalysisInput`/`ChartAnalysisInput` --
Journal never transforms, it only records what it is told).
"""

from dataclasses import dataclass, field
from typing import Optional, Sequence
from uuid import uuid4


@dataclass(frozen=True)
class TradeJournalEntry:
    """
    TASK 2's own exact field list: `journal_id`, `chart_id`, `trade_id`,
    `symbol`, `timeframe`, `direction`, `entry`, `sl`, `tp`, `result`,
    `confidence`, `reason`, `lesson`, `mistakes`, `created_at`.

    journal_id: this entry's own generated identity
        (`generate_journal_id()`).
    chart_id: the originating `ai_layer.vision_ai.models.ChartAnalysis.chart_id`
        -- a mandatory link (Director Note 4), relayed as a plain
        string, never a `ChartAnalysis` object reference.
    trade_id: the originating trade's own identity -- a mandatory link
        (Director Note 4), caller-supplied, never generated here (this
        package does not know what a "trade" is beyond this string).
    direction: the already-decided direction this entry narrates
        (e.g. "BUY"/"SELL") -- relayed only, never computed here (Rule
        2: Trade Journal never produces BUY/SELL/NO_TRADE).
    entry/sl/tp: the trade's own price levels, relayed only.
    result: free-text trade outcome (e.g. "WIN"/"LOSS"/"BE"), no fixed
        taxonomy enforced here -- same "free text, no fixed taxonomy"
        posture `ai_layer.knowledge_ai.knowledge_base.journal.failure_analysis.FailureAnalysisEntry.reason`
        and `ai_layer.knowledge_ai.learning_loop.models.LearningRecord.result` both already use.
    confidence: whatever single confidence value the caller supplies,
        relayed as-is -- no scale conversion (Rule 4).
    reason: a short free-text note on why the trade was taken.
    lesson: a short free-text takeaway -- read-only input for a future
        Learning/Coaching phase (Rule per TASK 8, Director Note 5).
    mistakes: short, free-text bullet points -- relayed only, never
        derived (mirrors `TradingAnalysis.strengths`/`weaknesses`'s own
        `Sequence[str]` convention).
    created_at: ISO-8601 timestamp string, stamped by
        `TradeJournalRuntime.create()`.
    """

    journal_id: str
    chart_id: str
    trade_id: str
    symbol: str
    timeframe: str
    direction: str
    entry: Optional[float] = None
    sl: Optional[float] = None
    tp: Optional[float] = None
    result: Optional[str] = None
    confidence: Optional[float] = None
    reason: Optional[str] = None
    lesson: Optional[str] = None
    mistakes: Sequence[str] = field(default_factory=tuple)
    created_at: str = ""


@dataclass(frozen=True)
class ReplayContext:
    """
    TASK 3 — Replay Foundation, metadata only. No video, no image, no
    binary payload of any kind (Director Note 3) -- the same "never the
    media itself, only a reference" posture
    `ai_layer.vision_ai.models.ChartContext.image_hash` already
    established.

    trade_id/chart_id: the same mandatory links `TradeJournalEntry`
        itself carries -- relayed, not re-derived.
    snapshot_id: an optional reference to a future replay snapshot
        (e.g. `backtesting_layer.replay_engine.replay_models.ReplayResult`'s own future
        identity) -- a plain string pointer, never a live object.
    comment: a short free-text annotation for this replay point.
    sequence: this context's own ordering position within a trade's
        replay timeline (0-based) -- caller-supplied, never computed.
    """

    trade_id: str
    chart_id: str
    snapshot_id: Optional[str] = None
    comment: Optional[str] = None
    sequence: int = 0


def generate_journal_id() -> str:
    """Same stateless uuid4 convention as every other generate_X_id() in this codebase (e.g. learning.models.generate_learning_record_id())."""
    return str(uuid4())
