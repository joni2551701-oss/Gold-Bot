"""
Signals — Canonical Signal strength (TASK-CORE-008 / STEP-08).

Grades an assembled signal's *strength* into a coarse, platform-facing label
(STRONG / GOOD / NORMAL / WEAK / INVALID). This is a presentation label, not
a trade decision and not a risk figure — nothing here sizes a position or
sets a stop.

Reuse, not a second grader: signals/signal_quality.py already computes a
detailed A+/A/B/C QualityGrade over a live SignalCandidate (SMC-criteria
based). When a caller already has that grade, map_grade() projects it onto
the coarser SignalStrength label rather than re-deriving anything. When a
caller only has a setup-layer StrategyResult (no A+/A/B/C grade yet),
assess() derives the label from the setup's own already-computed confidence
and reward/risk geometry — again, only reading values computed upstream.
"""

from enum import Enum
from typing import Optional


class SignalStrength(str, Enum):
    """Coarse, platform-facing strength label. INVALID = the signal is unusable."""
    STRONG = "STRONG"
    GOOD = "GOOD"
    NORMAL = "NORMAL"
    WEAK = "WEAK"
    INVALID = "INVALID"


# A+/A/B/C (signals.signal_quality.QualityGrade.value) -> coarse label.
_GRADE_TO_STRENGTH = {
    "A+": SignalStrength.STRONG,
    "A": SignalStrength.GOOD,
    "B": SignalStrength.NORMAL,
    "C": SignalStrength.WEAK,
}


def map_grade(grade_value: Optional[str]) -> SignalStrength:
    """Project an existing A+/A/B/C grade string onto SignalStrength. Unknown/None -> INVALID."""
    if not grade_value:
        return SignalStrength.INVALID
    return _GRADE_TO_STRENGTH.get(grade_value, SignalStrength.INVALID)


def assess(
    confidence: Optional[float],
    rr: Optional[float] = None,
    *,
    has_setup: bool = True,
) -> SignalStrength:
    """
    Derive a SignalStrength from a setup's already-computed confidence
    (0.0-1.0) and optional reward/risk geometry. Pure and defensive: a
    missing/no-setup input yields INVALID, never a raise.

    Bands (confidence): >=0.8 STRONG, >=0.6 GOOD, >=0.4 NORMAL, >0 WEAK.
    A present rr < 1.0 (reward below risk) caps the label one step down —
    a purely descriptive read of the setup's own geometry, not a risk rule.
    """
    if not has_setup or confidence is None or confidence <= 0:
        return SignalStrength.INVALID

    if confidence >= 0.8:
        strength = SignalStrength.STRONG
    elif confidence >= 0.6:
        strength = SignalStrength.GOOD
    elif confidence >= 0.4:
        strength = SignalStrength.NORMAL
    else:
        strength = SignalStrength.WEAK

    if rr is not None and rr < 1.0:
        strength = _step_down(strength)
    return strength


_ORDER = (
    SignalStrength.INVALID,
    SignalStrength.WEAK,
    SignalStrength.NORMAL,
    SignalStrength.GOOD,
    SignalStrength.STRONG,
)


def _step_down(strength: SignalStrength) -> SignalStrength:
    """One coarse level weaker, floored at WEAK (never silently INVALID from a geometry cap)."""
    idx = _ORDER.index(strength)
    return _ORDER[max(1, idx - 1)]
