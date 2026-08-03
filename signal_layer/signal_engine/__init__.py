"""
signals/ — GoldBot's Canonical Signal Layer (TASK-CORE-008 / STEP-08).

Takes a setup-layer StrategyResult and turns it into ONE canonical signal
every consumer (decision/, telegram/, mobile/, mini app/, desktop/, ai/,
monitoring/) can read — validated, strength-labelled, enriched, formatted,
serialized. It computes no market analysis, chooses no strategy, sizes no
risk, makes no decision, and touches no platform API.

Canonical model = signals.schema.SignalSchema (Phase A15), re-exported as
CanonicalSignal — NOT a duplicate model (STEP-08 reuse-first decision). The
FROZEN live path (signal_layer.signal_engine.signal_engine.SignalEngine -> SignalCandidate,
consumed by core/pipeline.py + decision/) is untouched and still importable
from its own modules.

Entry point: signals.manager.SignalManager.
"""

from signal_layer.signal_builder.signal import CanonicalSignal, generate_signal_id, validate_signal
from signal_layer.signal_service.manager import SignalManager, CanonicalSignalResult
from signal_layer.signal_scoring.quality import SignalStrength
from signal_layer.signal_engine.registry import SignalKind
from signal_layer.signal_service.router import SignalConsumer
from signal_layer.signal_engine.lifecycle.state import CanonicalSignalStatus

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

# Canonical documentation: 06_Signal_Layer/SignalEngine/README.md
