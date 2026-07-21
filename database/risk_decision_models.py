"""
Database Layer — Risk Decision persistence model (Phase V1.0.1: Risk
Management Hardening Patch, TASK 8). Mirrors
database/emergency_models.py's own shape/naming split: the DB-row
model gets its own name (RiskDecisionEntry), distinct from the domain
model (risk.risk_manager.RiskResult) -- same "two names for two
layers" precedent as database.emergency_models.EmergencyStateEntry vs
core.emergency.emergency_state.EmergencyStateRecord.

Append-only by design (see database/risk_decision_repository.py):
every RiskManager.evaluate() call is a new row, never an UPDATE, so
the full risk-decision history is never lost -- same posture as
EmergencyStateEntry.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional


@dataclass(frozen=True)
class RiskDecisionEntry:
    """
    Mirrors the 'risk_decisions' table row shape. `id` is intentionally
    excluded -- repository-internal detail, same convention as every
    other Phase 59.x/60.x/B.0 model in this codebase.

    symbol: the traded symbol, or "UNKNOWN" when RiskManager.evaluate()
        was called without one (the existing core/pipeline.py and
        backtesting/backtest_engine.py call sites, both untouched this
        phase, never supply symbol -- see
        docs/PHASE_V1_0_1_RISK_AUDIT.md section 2).
    direction: the SignalType value name ("BUY"/"SELL"), or None when
        no signal was available (e.g. decision.action != APPROVE).
    decision: "APPROVE" or "REJECT" -- the RiskResult.approved outcome
        as a stored string.
    reject_category: a short machine-readable code for *why* a REJECT
        happened (e.g. "RISK_LIMIT", "RR_BELOW_MIN", "DRAWDOWN",
        "DAILY_LOSS", "DUPLICATE", "EMERGENCY_PAUSED", "GEOMETRY",
        "INVALID_INPUT", "DECISION_NOT_APPROVE"), None for an APPROVE.
        Powers monitoring.risk_monitor's read-only aggregation without
        parsing the free-text `reason` string.
    """
    symbol: str
    strategy_name: Optional[str] = None
    direction: Optional[str] = None
    risk_percent: Optional[float] = None
    risk_reward: Optional[float] = None
    drawdown_percent: Optional[float] = None
    decision: str = "REJECT"
    reason: str = ""
    reject_category: Optional[str] = None
    created_at: Optional[datetime] = None


def create_risk_decision_entry(
    symbol: str,
    decision: str,
    reason: str,
    strategy_name: Optional[str] = None,
    direction: Optional[str] = None,
    risk_percent: Optional[float] = None,
    risk_reward: Optional[float] = None,
    drawdown_percent: Optional[float] = None,
    reject_category: Optional[str] = None,
) -> RiskDecisionEntry:
    """Pure, deterministic factory -- stamps created_at to 'now', same convention as create_emergency_state_entry()."""
    return RiskDecisionEntry(
        symbol=symbol,
        strategy_name=strategy_name,
        direction=direction,
        risk_percent=risk_percent,
        risk_reward=risk_reward,
        drawdown_percent=drawdown_percent,
        decision=decision,
        reason=reason,
        reject_category=reject_category,
        created_at=datetime.now(timezone.utc),
    )
