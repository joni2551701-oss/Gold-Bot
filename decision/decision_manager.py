"""
Decision — STEP-09 orchestrator (TASK-CORE-009).

DecisionManager is the STEP-09 entry point: it takes a canonical signal
(signals.schema.SignalSchema) and produces a DecisionOutcome carrying the
business verdict APPROVE / REJECT / HOLD / EXPIRE.

Additive-parallel + reuse-first (Director decision). The live, FROZEN
decision.decision_engine.DecisionEngine.evaluate() (SignalCandidate +
AIAnalysisResult -> TradeDecision, APPROVE/REJECT/NO_TRADE) is UNTOUCHED and
lives on the live pipeline path. This orchestrator does NOT re-implement the
confidence blend — it REUSES the engine's verdict:
  - when a caller already ran the frozen engine, pass its TradeDecision and
    its action is mapped (NO_TRADE -> HOLD) as the base status;
  - otherwise the canonical signal's own decision field (APPROVED/REJECTED/
    PENDING, already set upstream) is the base status.
STEP-09's own business rules (decision_rules) then add HOLD/EXPIRE and reject
invalid/price-incomplete signals.

Named decision_manager.py (not decision_engine.py, which exists and is
frozen) — the same discipline STEP-08 used with signals/manager.py alongside
the frozen signal_engine.py.

Strict boundary — this layer does NOT: compute risk, size a position, send an
order, format a platform message, or modify the frozen engine. The signal is
read duck-typed so a None/partial signal yields a defined outcome, never a
raise.
"""

from datetime import datetime, timezone
from typing import Optional

from decision.decision_model import DecisionOutcome
from decision.decision_status import (
    from_decision_action,
    from_signal_decision,
)
from decision.decision_rules import (
    RuleContext,
    apply_rules,
    DEFAULT_MIN_CONFIDENCE,
    DEFAULT_MAX_AGE_SECONDS,
)


class DecisionManager:
    """Runs the STEP-09 business-decision pipeline over a canonical signal. Stateless."""

    def __init__(
        self,
        *,
        min_confidence: float = DEFAULT_MIN_CONFIDENCE,
        max_age_seconds: int = DEFAULT_MAX_AGE_SECONDS,
    ) -> None:
        self._min_confidence = min_confidence
        self._max_age_seconds = max_age_seconds

    def decide(
        self,
        signal,
        *,
        now: Optional[datetime] = None,
        trade_decision=None,
    ) -> DecisionOutcome:
        """
        Produce a DecisionOutcome for one canonical signal. If `trade_decision`
        (a frozen-engine TradeDecision) is supplied its verdict is REUSED as
        the base status; otherwise the signal's own decision field is used.
        Never raises.
        """
        now = now or datetime.now(timezone.utc)

        # base status = reuse of the frozen engine's verdict (or the signal's)
        if trade_decision is not None:
            base_status = from_decision_action(getattr(trade_decision, "action", None))
            source = "trade_decision"
        else:
            base_status = from_signal_decision(getattr(signal, "decision", None))
            source = "signal.decision"

        ctx = RuleContext(
            now=now,
            min_confidence=self._min_confidence,
            max_age_seconds=self._max_age_seconds,
        )
        final_status, reasons, applied = apply_rules(signal, base_status, ctx)

        return DecisionOutcome(
            signal_id=getattr(signal, "signal_id", None),
            symbol=getattr(signal, "symbol", None),
            direction=getattr(signal, "direction", None),
            status=final_status,
            confidence=float(getattr(signal, "confidence_score", 0.0) or 0.0),
            reasons=reasons,
            rules_applied=applied,
            created_at=now,
            metadata={"base_status": base_status.value, "source": source},
        )
