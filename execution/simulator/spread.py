"""
Execution Layer — Spread Simulation (Phase 60.3: Execution Simulator
Foundation, TASK 4).

A session-aware spread lookup -- matching the Director's own worked
example (London 0.15, NY news 0.80). `session` is a free-text key
supplied by the caller (e.g. `context.session_intelligence`'s own
session label, or a signal's `SignalSchema.session` field, Phase
59-era) -- this module does not compute or classify a session itself,
it only looks one up in a configured table.
"""

from dataclasses import dataclass, field
from typing import Dict, Optional

_DEFAULT_SESSION_SPREADS: Dict[str, float] = {
    "LONDON": 0.15,
    "NY_NEWS": 0.80,
}


@dataclass(frozen=True)
class SpreadConfig:
    default_points: float = 0.20
    max_points: float = 1.00
    session_spreads: Dict[str, float] = field(default_factory=lambda: dict(_DEFAULT_SESSION_SPREADS))


def get_spread(session: Optional[str], config: SpreadConfig = None) -> float:
    """`session` not in the configured table (including None) falls back to default_points -- never raises, never clamps silently past max_points (see is_spread_too_wide() for the reject check)."""
    config = config or SpreadConfig()
    if session is None:
        return config.default_points
    return config.session_spreads.get(session, config.default_points)


def is_spread_too_wide(spread_points: float, config: SpreadConfig = None) -> bool:
    """TASK 6's own reject condition -- a spread at or above max_points is treated as un-fillable, same posture a real broker's own max-spread guard would have."""
    config = config or SpreadConfig()
    return spread_points >= config.max_points
