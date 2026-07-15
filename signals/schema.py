"""
Signal Layer — Signal Schema Standard (Phase A15).

SignalSchema is the standard, cross-module data contract for "how does
GoldBot store and pass a signal between modules" — one flat, documented
shape instead of every consumer (Decision, Risk, Telegram, Analytics,
a future AI provider) re-deriving its own subset from
SignalCandidate/SignalQualityResult/SignalExplanation/TradeDecision.
It does NOT compute anything -- every field is either a direct copy of
an already-computed value or an explicit None placeholder for a
reference that doesn't exist yet (explanation_id/risk_id -- see
docs/SIGNAL_SCHEMA.md). context_id and decision_id are real,
generated references as of the Pre-Phase 59 Architecture Readiness
Review's AC-03 task -- see signals/adapter.py and core/pipeline.py's
"Signal <-> Context Historical Link" stage. See signals/adapter.py for
how an existing SignalCandidate becomes a SignalSchema, and
signals/README.md/docs/SIGNAL_SCHEMA.md for the full contract.

Distinct from database/signal_record.py's SignalRecord (pre-existing,
untouched by this phase): SignalRecord is a persistence-layer wrapper,
built only once a full (SignalCandidate, TradeDecision, RiskResult)
triple already exists, immediately before a database write.
SignalSchema is a cross-module contract that can exist earlier --
right after Strategy Engine, before Decision Engine or Risk Manager
have run (decision defaults to "PENDING", risk_id stays None) -- and
is never itself written to the database in this phase.
"""

import json
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import List, Optional

# The exact vocabulary signals.models.SignalType already defines
# (BUY/SELL/NONE) -- read here as plain literals (not imported as the
# enum type) so SignalSchema's own fields stay plain, JSON-native
# primitives; see docs/SIGNAL_SCHEMA.md's "Why fields are plain
# strings, not enums" section.
ALLOWED_DIRECTIONS = ("BUY", "SELL", "NONE")

# A schema-level status vocabulary, distinct from
# decision.models.DecisionAction's real values (APPROVE/REJECT/
# NO_TRADE) -- SignalSchema can exist before Decision Engine has run
# at all, so "PENDING" is a real, necessary third state DecisionAction
# itself has no equivalent for. signals/adapter.py documents the exact
# DecisionAction -> this vocabulary mapping.
ALLOWED_DECISION_STATUSES = ("APPROVED", "REJECTED", "PENDING")


@dataclass(frozen=True)
class SignalSchema:
    """
    Identity: signal_id (a real, generated identity -- see
        generate_signal_id() below), created_at, version (schema
        version, not strategy version -- "1.0" today).
    Market: symbol, timeframe (both required -- the real values this
        codebase runs, e.g. "XAUUSD"/"M15"), asset_type, session
        (both optional -- not every caller has this context available
        yet), market_phase (Phase 59 Real Market Validation Foundation,
        TASK 2 -- context.market_phase.MarketPhaseResult.phase.value,
        e.g. "ACCUMULATION", relayed from the same cycle's
        already-computed classification; None until a caller supplies
        it -- this model never computes it).
    Direction: direction -- one of ALLOWED_DIRECTIONS, validated by
        validate_signal(), not by the dataclass itself (never raises
        at construction time -- see validate_signal()'s own docstring
        for why).
    Price: entry_price/stop_loss/take_profit -- required for a BUY/
        SELL direction (validated by validate_signal()), meaningless
        (left None) for a NONE direction.
    Context reference: context_id -- a reference only, never the
        ContextSnapshot itself. Phase A16 (Context Snapshot
        Foundation) is the named future phase that wires this up;
        None until then.
    Strategy: strategy_name (the real SignalCandidate.strategy_name
        value, e.g. "LIQUIDITY_SWEEP_STRATEGY" -- not a human label),
        strategy_version (no source exists on SignalCandidate today;
        None unless a caller supplies one explicitly).
    Quality: quality_grade/confidence_score -- relayed from an
        already-computed SignalQualityResult, never recomputed here.
    Explainability reference: explanation_id -- a reference only.
        SignalExplanation (Phase A9) has no id field of its own today,
        so this stays None until a future phase adds one.
    Decision: decision (one of ALLOWED_DECISION_STATUSES, defaults to
        "PENDING" -- decision hasn't necessarily happened yet when a
        SignalSchema is first built), decision_score, decision_id (a
        real, generated identity for the specific TradeDecision this
        record reflects -- added by the Pre-Phase 59 Architecture
        Readiness Review's AC-03 task, "Signal + Context Historical
        Link"; None until a TradeDecision actually exists, same
        posture as decision/decision_score). decision.models.TradeDecision
        itself has no id field of its own -- core/pipeline.py generates
        this id at the point it builds the historical record, not
        inside TradeDecision.
    Risk reference: risk_id -- a reference only. RiskResult has no id
        field of its own today, so this stays None until a future
        phase adds one. Risk is never computed by this model.
    """
    signal_id: str
    created_at: datetime
    symbol: str
    timeframe: str
    direction: str
    version: str = "1.0"
    asset_type: Optional[str] = None
    session: Optional[str] = None
    market_phase: Optional[str] = None
    entry_price: Optional[float] = None
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    context_id: Optional[str] = None
    strategy_name: Optional[str] = None
    strategy_version: Optional[str] = None
    quality_grade: Optional[str] = None
    confidence_score: Optional[float] = None
    explanation_id: Optional[str] = None
    decision: str = "PENDING"
    decision_score: Optional[float] = None
    decision_id: Optional[str] = None
    risk_id: Optional[str] = None

    def to_dict(self) -> dict:
        """JSON-safe dict -- created_at is rendered as an ISO-8601 string, everything else is already a primitive."""
        data = asdict(self)
        data["created_at"] = self.created_at.isoformat()
        return data

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


def generate_signal_id() -> str:
    """
    A real, collision-safe id -- the same generation convention
    database/signal_record.py's create_signal_record() already uses
    (str(uuid.uuid4())), reused here rather than inventing a new
    counter-based scheme.
    """
    return str(uuid.uuid4())


@dataclass(frozen=True)
class ValidationResult:
    """
    valid: True only if `errors` is empty.
    errors: human-readable strings, one per failed rule -- empty list
        is the valid, non-error case (same "structured result, never
        raise" convention as SignalQualityResult/DataQualityResult/
        RiskResult.approved elsewhere in this codebase).
    """
    valid: bool
    errors: List[str] = field(default_factory=list)


def validate_signal(signal: SignalSchema) -> ValidationResult:
    """
    Never raises: an invalid SignalSchema (missing required field,
    unrecognized direction, inverted BUY/SELL price ordering) produces
    ValidationResult(valid=False, errors=[...]), not an exception --
    the same fail-safe posture every other Phase A foundation module
    uses. Checks, in order: required fields present, direction is one
    of ALLOWED_DIRECTIONS, price ordering for a BUY/SELL direction
    (SL < Entry < TP for BUY, TP < Entry < SL for SELL -- a NONE
    direction has no price ordering to check), and decision (if set)
    is one of ALLOWED_DECISION_STATUSES.
    """
    errors: List[str] = []

    if not signal.signal_id:
        errors.append("signal_id is required")
    if not signal.symbol:
        errors.append("symbol is required")
    if not signal.timeframe:
        errors.append("timeframe is required")
    if not signal.direction:
        errors.append("direction is required")
    if not signal.created_at:
        errors.append("created_at is required")

    if signal.direction and signal.direction not in ALLOWED_DIRECTIONS:
        errors.append(
            f"direction must be one of {ALLOWED_DIRECTIONS}, got {signal.direction!r}"
        )

    if signal.direction in ("BUY", "SELL"):
        if signal.entry_price is None or signal.stop_loss is None or signal.take_profit is None:
            errors.append("entry_price, stop_loss, and take_profit are required for a BUY/SELL direction")
        elif signal.direction == "BUY":
            if not (signal.stop_loss < signal.entry_price < signal.take_profit):
                errors.append(
                    f"BUY requires stop_loss < entry_price < take_profit, got "
                    f"{signal.stop_loss} / {signal.entry_price} / {signal.take_profit}"
                )
        elif signal.direction == "SELL":
            if not (signal.take_profit < signal.entry_price < signal.stop_loss):
                errors.append(
                    f"SELL requires take_profit < entry_price < stop_loss, got "
                    f"{signal.take_profit} / {signal.entry_price} / {signal.stop_loss}"
                )

    if signal.decision and signal.decision not in ALLOWED_DECISION_STATUSES:
        errors.append(
            f"decision must be one of {ALLOWED_DECISION_STATUSES}, got {signal.decision!r}"
        )

    return ValidationResult(valid=len(errors) == 0, errors=errors)
