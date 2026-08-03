"""
AI Layer — Routing Result (Phase 61.0: AI Infrastructure Foundation,
TASK 4).
"""

from dataclasses import dataclass
from typing import Optional

from ai.capabilities.capability import Capability


@dataclass(frozen=True)
class RoutingResult:
    """
    provider_name: None when no available provider was found for
        `capability` -- a router caller must check this before using
        the result, same "structured result, never raise" convention
        `signal_layer/signal_builder/schema.py`'s `ValidationResult` uses.
    reason: a short, human-readable explanation of the outcome (which
        rule matched, or why nothing did).
    """
    capability: Capability
    provider_name: Optional[str]
    reason: str
