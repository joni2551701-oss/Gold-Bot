"""
AI Layer — Provider Failover (Phase 61.1: AI Provider Reliability
Foundation, TASK 2).

One pure function: given an already-ordered candidate list (from
`ai/router/routing_rules.py`, filtered through TASK 3's capability
matrix), walk it and return the first provider `ProviderHealthTracker`
reports as available. Owns only the "pick the first healthy one"
algorithm -- building the candidate list stays `ai/router/router.py`'s
job (TASK 4), so this function has no knowledge of capabilities or
routing rules.
"""

from typing import Optional, Sequence

from ai_layer.ai_engine.providers.provider_health import ProviderHealthTracker


def select_available(candidates: Sequence[str], health_tracker: ProviderHealthTracker) -> Optional[str]:
    """Never raises: an empty `candidates` sequence, or one where nothing is available, returns None."""
    for name in candidates:
        if health_tracker.is_available(name):
            return name
    return None
