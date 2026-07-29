"""
Decision — STEP-09 business rules (TASK-CORE-009).

Pure business rules that turn a canonical signal + its base status (mapped
from the FROZEN engine's verdict) into a final DecisionStatus. These are
DECISION rules — "should this signal proceed, hold, or expire" — not risk
rules: no lot size, no stop distance, no exposure, no account maths lives
here (that is STEP-10 risk/).

Each rule is a pure function `(signal, base_status, ctx) -> Optional[(status,
reason)]`; returning None means "this rule doesn't apply." apply_rules()
evaluates them in priority order and the first override wins. Rules read the
signal duck-typed (getattr) so a partial/None signal never raises.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List, Optional, Tuple

from decision.decision_status import DecisionStatus

# Decision-layer business thresholds (NOT risk parameters).
DEFAULT_MIN_CONFIDENCE = 0.5      # below this an APPROVE is downgraded to HOLD
DEFAULT_MAX_AGE_SECONDS = 900     # older than this a signal EXPIREs (15 min)


@dataclass(frozen=True)
class RuleContext:
    now: datetime
    min_confidence: float = DEFAULT_MIN_CONFIDENCE
    max_age_seconds: int = DEFAULT_MAX_AGE_SECONDS


def _direction(signal) -> Optional[str]:
    return getattr(signal, "direction", None)


def _has_prices(signal) -> bool:
    return all(
        getattr(signal, f, None) is not None
        for f in ("entry_price", "stop_loss", "take_profit")
    )


def rule_reject_invalid(signal, base_status, ctx) -> Optional[Tuple[DecisionStatus, str]]:
    """A non-actionable or price-incomplete signal is a hard REJECT."""
    direction = _direction(signal)
    if direction not in ("BUY", "SELL"):
        return DecisionStatus.REJECT, f"non-actionable direction {direction!r}"
    if not _has_prices(signal):
        return DecisionStatus.REJECT, "missing entry/stop_loss/take_profit"
    return None


def rule_expire_stale(signal, base_status, ctx) -> Optional[Tuple[DecisionStatus, str]]:
    """A signal older than the max age EXPIREs — the engine's verdict is stale."""
    created = getattr(signal, "created_at", None)
    if created is None:
        return None
    now = ctx.now
    if created.tzinfo is None:
        created = created.replace(tzinfo=timezone.utc)
    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)
    age = (now - created).total_seconds()
    if age > ctx.max_age_seconds:
        return DecisionStatus.EXPIRE, f"signal age {int(age)}s > {ctx.max_age_seconds}s"
    return None


def rule_hold_low_confidence(signal, base_status, ctx) -> Optional[Tuple[DecisionStatus, str]]:
    """An otherwise-APPROVE signal with low confidence is HELD, not sent on."""
    if base_status != DecisionStatus.APPROVE:
        return None
    confidence = getattr(signal, "confidence_score", None)
    if confidence is not None and confidence < ctx.min_confidence:
        return DecisionStatus.HOLD, f"confidence {confidence} < {ctx.min_confidence}"
    return None


# Priority order — first override wins.
DEFAULT_RULES = (
    ("reject_invalid", rule_reject_invalid),
    ("expire_stale", rule_expire_stale),
    ("hold_low_confidence", rule_hold_low_confidence),
)


def apply_rules(signal, base_status: DecisionStatus, ctx: RuleContext):
    """
    Evaluate DEFAULT_RULES in priority order. Returns
    (final_status, reasons, rules_applied). The first rule that overrides
    wins and stops evaluation; if none override, base_status passes through.
    Never raises.
    """
    reasons: List[str] = []
    applied: List[str] = []
    for name, rule in DEFAULT_RULES:
        result = rule(signal, base_status, ctx)
        if result is not None:
            status, reason = result
            reasons.append(reason)
            applied.append(name)
            return status, reasons, applied
    return base_status, [f"passthrough base status {base_status.value}"], ["passthrough"]
