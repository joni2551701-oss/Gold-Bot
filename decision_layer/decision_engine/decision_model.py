"""
Decision — STEP-09 outcome model (TASK-CORE-009).

DecisionOutcome is the STEP-09 result: the business verdict (DecisionStatus)
over one canonical signal, plus the reasons and the rule names that produced
it. Additive-parallel to the FROZEN decision.models.TradeDecision (which the
live pipeline still produces from a SignalCandidate + AIAnalysisResult);
TradeDecision is untouched. DecisionOutcome is built from a canonical signal
(signal_layer.signal_builder.schema.SignalSchema) and is what STEP-10 risk/ and the platforms
read.

It computes nothing about the market and holds no risk figure — it records a
verdict and its justification only.
"""

import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from decision_layer.decision_engine.decision_status import DecisionStatus


@dataclass(frozen=True)
class DecisionOutcome:
    """
    signal_id/symbol/direction: identity relayed from the canonical signal.
    status: the STEP-09 verdict (APPROVE/REJECT/HOLD/EXPIRE).
    confidence: relayed from the signal (0.0-1.0), never recomputed.
    reasons: human-readable justification strings.
    rules_applied: names of the STEP-09 rules that fired.
    created_at: when this outcome was produced.
    metadata: free-form extra detail (base_status, source, ...).
    """
    signal_id: Optional[str]
    symbol: Optional[str]
    direction: Optional[str]
    status: DecisionStatus
    confidence: float = 0.0
    reasons: List[str] = field(default_factory=list)
    rules_applied: List[str] = field(default_factory=list)
    created_at: Optional[datetime] = None
    metadata: dict = field(default_factory=dict)

    @property
    def is_approved(self) -> bool:
        return self.status == DecisionStatus.APPROVE

    def to_dict(self) -> dict:
        return {
            "signal_id": self.signal_id,
            "symbol": self.symbol,
            "direction": self.direction,
            "status": self.status.value,
            "confidence": self.confidence,
            "reasons": list(self.reasons),
            "rules_applied": list(self.rules_applied),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "metadata": dict(self.metadata),
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())
