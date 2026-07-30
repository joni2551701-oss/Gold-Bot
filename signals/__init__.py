"""
signals/ — GoldBot's Canonical Signal Layer (TASK-CORE-008 / STEP-08).

Takes a setup-layer StrategyResult and turns it into ONE canonical signal
every consumer (decision/, telegram/, mobile/, mini app/, desktop/, ai/,
monitoring/) can read — validated, strength-labelled, enriched, formatted,
serialized. It computes no market analysis, chooses no strategy, sizes no
risk, makes no decision, and touches no platform API.

Canonical model = signals.schema.SignalSchema (Phase A15), re-exported as
CanonicalSignal — NOT a duplicate model (STEP-08 reuse-first decision). The
FROZEN live path (signals.signal_engine.SignalEngine -> SignalCandidate,
consumed by core/pipeline.py + decision/) is untouched and still importable
from its own modules.

Entry point: signals.manager.SignalManager.
"""

from signals.signal import CanonicalSignal, generate_signal_id, validate_signal
from signals.manager import SignalManager, CanonicalSignalResult
from signals.quality import SignalStrength
from signals.registry import SignalKind
from signals.router import SignalConsumer
from signals.lifecycle.state import CanonicalSignalStatus

__all__ = [
    "CanonicalSignal",
    "generate_signal_id",
    "validate_signal",
    "SignalManager",
    "CanonicalSignalResult",
    "SignalStrength",
    "SignalKind",
    "SignalConsumer",
    "CanonicalSignalStatus",
]
