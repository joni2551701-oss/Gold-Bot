"""
Strategies — StrategyResult contract (TASK-CORE-007, setup layer).

StrategyResult is the OUTPUT of the strategies/ setup-detection layer:
"is there a setup, and if so what does it look like." It is NOT a
signal (see signals/models.py's SignalCandidate for the live signal
contract) and NOT a trade decision. This layer runs alongside the
existing live SignalCandidate path (strategies/strategy_manager.py),
which is unchanged and frozen; the new setup layer produces
StrategyResult and is not wired into core/pipeline.py.

Every strategy returns a StrategyResult even when no setup exists
(status=NO_SETUP) — a defined shape, never a random one. No signal,
decision, risk, execution, provider, or secret access here.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Tuple


class StrategyDirection(str, Enum):
    """Directional read of a setup. NEUTRAL when the setup carries no side (or none was found)."""
    LONG = "long"
    SHORT = "short"
    NEUTRAL = "neutral"


class SetupStatus(str, Enum):
    """SETUP_FOUND = a real setup; NO_SETUP = evaluated, nothing there; INVALID = context unusable."""
    SETUP_FOUND = "setup_found"
    NO_SETUP = "no_setup"
    INVALID = "invalid"


def compute_rr(entry: float, invalidation: float, target: float) -> Optional[float]:
    """
    Descriptive risk-reward *geometry* of a setup (reward distance /
    risk distance) — NOT risk management (no lot size, no account risk,
    no exposure). Returns None when the stop distance is zero/degenerate.
    """
    risk = abs(entry - invalidation)
    reward = abs(target - entry)
    if risk <= 0:
        return None
    return round(reward / risk, 2)


@dataclass(frozen=True)
class StrategyResult:
    """
    strategy_name: the producing strategy's name().
    direction: LONG / SHORT / NEUTRAL.
    confidence: 0.0–1.0 (setup quality, not a decision threshold).
    entry_zone: (low, high) price band, or None.
    invalidation: the price that voids the setup, or None.
    rr: descriptive reward/risk geometry, or None.
    reasons: human-readable why-strings (explainability only).
    status: SETUP_FOUND / NO_SETUP / INVALID.
    metadata: free-form extra detail (indices, regime, session, …).
    """
    strategy_name: str
    direction: StrategyDirection = StrategyDirection.NEUTRAL
    confidence: float = 0.0
    entry_zone: Optional[Tuple[float, float]] = None
    invalidation: Optional[float] = None
    rr: Optional[float] = None
    reasons: List[str] = field(default_factory=list)
    status: SetupStatus = SetupStatus.NO_SETUP
    metadata: dict = field(default_factory=dict)

    @property
    def has_setup(self) -> bool:
        return self.status == SetupStatus.SETUP_FOUND

    @classmethod
    def none(cls, strategy_name: str, reason: Optional[str] = None, **metadata) -> "StrategyResult":
        """The standard 'no setup' result — always returned instead of an empty/None."""
        return cls(
            strategy_name=strategy_name,
            reasons=[reason] if reason else [],
            status=SetupStatus.NO_SETUP,
            metadata=metadata,
        )

    @classmethod
    def invalid(cls, strategy_name: str, reason: str) -> "StrategyResult":
        """Context was missing/unusable — a defined shape, never a raise."""
        return cls(strategy_name=strategy_name, reasons=[reason], status=SetupStatus.INVALID)

    @classmethod
    def from_signal_candidate(cls, candidate, strategy_name: Optional[str] = None) -> "StrategyResult":
        """
        Adapt a live signals.models.SignalCandidate into a setup-layer
        StrategyResult (duck-typed — no import of signals/, so result.py
        stays signal-free). Used by the setup-layer wrappers over the
        three existing live strategies to REUSE their frozen detection
        instead of duplicating it. entry becomes a point entry_zone,
        stop_loss the invalidation, and rr the descriptive geometry.
        """
        side = getattr(getattr(candidate, "signal_type", None), "name", "")
        direction = (
            StrategyDirection.LONG if side == "BUY"
            else StrategyDirection.SHORT if side == "SELL"
            else StrategyDirection.NEUTRAL
        )
        entry = getattr(candidate, "entry", None)
        stop = getattr(candidate, "stop_loss", None)
        target = getattr(candidate, "take_profit", None)
        rr = compute_rr(entry, stop, target) if None not in (entry, stop, target) else None
        return cls(
            strategy_name=strategy_name or getattr(candidate, "strategy_name", "UNKNOWN"),
            direction=direction,
            confidence=float(getattr(candidate, "confidence", 0.0) or 0.0),
            entry_zone=(entry, entry) if entry is not None else None,
            invalidation=stop,
            rr=rr,
            reasons=list(getattr(candidate, "reasons", []) or []),
            status=SetupStatus.SETUP_FOUND,
            metadata={"adapted_from": "SignalCandidate", "take_profit": target},
        )

    def to_dict(self) -> dict:
        """JSON-safe view (enums rendered as their .value)."""
        return {
            "strategy_name": self.strategy_name,
            "direction": self.direction.value,
            "confidence": self.confidence,
            "entry_zone": list(self.entry_zone) if self.entry_zone else None,
            "invalidation": self.invalidation,
            "rr": self.rr,
            "reasons": list(self.reasons),
            "status": self.status.value,
            "metadata": dict(self.metadata),
        }
