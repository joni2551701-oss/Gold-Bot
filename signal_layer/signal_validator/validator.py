"""
Signals — Canonical Signal validator (TASK-CORE-008 / STEP-08).

Checks that an assembled canonical signal is well-formed and not a
duplicate. It makes NO trading decision — a valid signal is not an approved
trade; validation only answers "is this signal structurally usable and
unique."

Reuse, not a reimplementation: the field/price-ordering rules already live
in signals.schema.validate_signal() (Phase A15). This module reuses that
verbatim for structural validation and adds the two checks the STEP-08 spec
names that schema.validate_signal does not cover:
- a duplicate check (SignalDeduplicator, an in-memory identity guard), and
- a setup-input precheck (precheck_source) that confirms a StrategyResult
  actually carries a direction / entry / strategy / confidence / rr before
  the manager tries to build a signal from it.
"""

from typing import List, Optional, Set, Tuple

from signal_layer.signal_builder.schema import SignalSchema, ValidationResult, validate_signal


def validate(signal: SignalSchema) -> ValidationResult:
    """Structural validation — reuses signals.schema.validate_signal verbatim."""
    return validate_signal(signal)


def _identity_key(signal: SignalSchema) -> Tuple:
    """
    What makes two canonical signals 'the same' for dedup: same symbol,
    direction, entry, and producing strategy. signal_id/created_at are
    deliberately excluded (they are unique per build, so including them would
    defeat the check).
    """
    return (
        signal.symbol,
        signal.direction,
        signal.entry_price,
        signal.strategy_name,
    )


class SignalDeduplicator:
    """
    In-memory guard against emitting the same canonical signal twice. Holds
    only a set of identity keys — no signal payloads, no persistence. A caller
    that wants cross-run dedup persists elsewhere; this is a per-session guard.
    """

    def __init__(self) -> None:
        self._seen: Set[Tuple] = set()

    def is_duplicate(self, signal: SignalSchema) -> bool:
        """True if a signal with the same identity key has already been registered."""
        return _identity_key(signal) in self._seen

    def register(self, signal: SignalSchema) -> None:
        """Record this signal's identity so a later identical one reads as duplicate."""
        self._seen.add(_identity_key(signal))

    def reset(self) -> None:
        self._seen.clear()


def precheck_source(
    *,
    direction: Optional[str],
    entry: Optional[float],
    strategy: Optional[str],
    confidence: Optional[float],
    rr: Optional[float],
) -> ValidationResult:
    """
    Confirm a setup carries the minimum the STEP-08 spec lists before a
    signal is built from it: direction, entry, strategy, a valid confidence
    (0-1), and an rr. Never raises — returns ValidationResult(valid, errors).
    """
    errors: List[str] = []
    if not direction:
        errors.append("direction is required")
    if entry is None:
        errors.append("entry is required")
    if not strategy:
        errors.append("strategy is required")
    if confidence is None or not (0.0 <= confidence <= 1.0):
        errors.append("confidence must be within 0.0-1.0")
    if rr is None:
        errors.append("rr is required")
    return ValidationResult(valid=len(errors) == 0, errors=errors)
