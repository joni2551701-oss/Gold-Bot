"""
Signals — Canonical Signal model (TASK-CORE-008 / STEP-08).

Director decision (STEP-08): the Canonical Signal is NOT a new dataclass.
signals.schema.SignalSchema (Phase A15) is ALREADY the cross-module,
platform-independent signal contract every consumer (decision/, telegram/,
mobile/, mini app/, desktop/, ai/, monitoring/) reads. Re-inventing it here
would be the exact duplicate this task's own Refactor Rules forbid, so this
module simply RE-EXPORTS SignalSchema under the canonical name and pulls the
already-existing identity/validation helpers into one import surface.

    from signals.signal import CanonicalSignal, generate_signal_id

`CanonicalSignal` IS `signals.schema.SignalSchema` — same frozen dataclass,
same to_dict()/to_json(), same fields. The extra task-spec fields (rr,
reason, quality label, lifecycle status, free-form metadata) are carried by
the STEP-08 pipeline's surrounding structures (signals/quality.py's
SignalStrength, signals/enricher.py's SignalEnrichment, signals/formatter.py's
SignalPresentation, signals/lifecycle/), NOT bolted onto the frozen A15
contract — see docs/PHASE_SIGNALS.md's field-mapping table.

This module computes nothing. It reads no context, runs no detector, makes
no decision, sizes no risk.
"""

from signals.schema import (  # re-export: single canonical import surface
    SignalSchema as CanonicalSignal,
    ValidationResult,
    generate_signal_id,
    validate_signal,
    ALLOWED_DIRECTIONS,
    ALLOWED_DECISION_STATUSES,
)

__all__ = [
    "CanonicalSignal",
    "ValidationResult",
    "generate_signal_id",
    "validate_signal",
    "ALLOWED_DIRECTIONS",
    "ALLOWED_DECISION_STATUSES",
]
