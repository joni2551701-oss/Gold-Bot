"""
Context Layer — Market Phase classification (Pre-Phase 59 Architecture
Readiness Review, AC-02).

MarketPhase is a standard 5-state (+ UNKNOWN) classification of "what
point in the Accumulation-Manipulation-Distribution-Markup-Markdown
cycle is the market in right now" -- built entirely from already-
computed data (Wyckoff Spring/Upthrust events, AMD events, Market
Regime). No new detection logic; context/wyckoff.py and context/amd.py
are both untouched.

Extends context/wyckoff.py's own 2-state WyckoffPhase
(ACCUMULATION/DISTRIBUTION, tied strictly to Spring/Upthrust) to the
5-state model named in the Director's Architecture Readiness Review
(Accumulation/Manipulation/Distribution/Markup/Markdown) -- see
docs/ARCHITECTURE_READINESS_REVIEW.md's AC-02 section for the full
rationale.

Priority order mirrors context/market_regime.py's own established
pattern (most specific signal first, a safe UNKNOWN fallback last):
1. Most recent Wyckoff Spring/Upthrust (the narrowest, most specific
   signal -- see context/wyckoff.py's own docstring on why Spring/
   Upthrust is narrower than AMD's general sweep-then-break
   detection) -> ACCUMULATION/DISTRIBUTION.
2. Else, most recent AMD event -> MANIPULATION/DISTRIBUTION.
3. Else, a confirmed TRENDING Market Regime -> MARKUP (bullish) or
   MARKDOWN (bearish).
4. Else -> UNKNOWN (RANGE/HIGH_VOLATILITY/LOW_VOLATILITY/UNKNOWN
   regimes, or no data at all) -- never fabricated.
"""

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING

from context.amd import AmdEventType
from context.market_regime import MarketRegime, RegimeDirection
from context.wyckoff import WyckoffPhase

if TYPE_CHECKING:
    from context.context_orchestrator import ContextSnapshot


class MarketPhase(Enum):
    ACCUMULATION = "ACCUMULATION"
    MANIPULATION = "MANIPULATION"
    DISTRIBUTION = "DISTRIBUTION"
    MARKUP = "MARKUP"
    MARKDOWN = "MARKDOWN"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class MarketPhaseResult:
    """
    phase: one of the six MarketPhase values.
    reason: a short, human-readable explanation of which rule fired --
        explainability, not consumed by the classification logic
        itself (same convention as context.market_regime.MarketRegimeResult.reasons).
    """
    phase: MarketPhase
    reason: str


def compute_market_phase(context: 'ContextSnapshot') -> MarketPhaseResult:
    """
    Reads context.wyckoff_events, context.amd_events, and
    context.market_regime directly -- all three already exist on
    ContextSnapshot (Phase A5/AMD pre-existing/Phase A7), so this
    function needs no new field on ContextSnapshot and no change to
    context/context_orchestrator.py. Never raises: an empty context
    (no Wyckoff/AMD events, MarketRegime.UNKNOWN) produces
    MarketPhase.UNKNOWN, not an error.
    """
    if context.wyckoff_events:
        latest = context.wyckoff_events[-1]
        phase = (
            MarketPhase.ACCUMULATION
            if latest.phase == WyckoffPhase.ACCUMULATION
            else MarketPhase.DISTRIBUTION
        )
        return MarketPhaseResult(
            phase=phase,
            reason=f"Most recent Wyckoff event: {latest.type.value}",
        )

    if context.amd_events:
        latest = context.amd_events[-1]
        phase = (
            MarketPhase.MANIPULATION
            if latest.type == AmdEventType.MANIPULATION
            else MarketPhase.DISTRIBUTION
        )
        return MarketPhaseResult(
            phase=phase,
            reason=f"Most recent AMD event: {latest.type.value}",
        )

    regime_result = context.market_regime
    if regime_result.regime == MarketRegime.TRENDING:
        if regime_result.direction == RegimeDirection.BULLISH:
            return MarketPhaseResult(phase=MarketPhase.MARKUP, reason="Market Regime: TRENDING (BULLISH)")
        if regime_result.direction == RegimeDirection.BEARISH:
            return MarketPhaseResult(phase=MarketPhase.MARKDOWN, reason="Market Regime: TRENDING (BEARISH)")

    return MarketPhaseResult(
        phase=MarketPhase.UNKNOWN,
        reason="No Wyckoff/AMD event and no confirmed trending regime",
    )
