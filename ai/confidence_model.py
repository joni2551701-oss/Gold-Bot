from dataclasses import dataclass
from typing import List, Optional
from context.context_orchestrator import ContextSnapshot
from signals.models import SignalCandidate

@dataclass(frozen=True)
class ScoringConfig:
    WEIGHT_STRUCTURE: float = 20.0
    WEIGHT_LIQUIDITY: float = 20.0
    WEIGHT_FOOTPRINT: float = 20.0
    WEIGHT_BOS: float = 15.0
    WEIGHT_CHOCH: float = 15.0
    WEIGHT_AMD: float = 10.0
    MAX_SIGNAL_AGE: int = 50

@dataclass(frozen=True)
class ConfidenceResult:
    technical_score: float
    confidence: float
    warnings: List[str]
    reasons: List[str]

def evaluate_confidence(signal: SignalCandidate, context: ContextSnapshot) -> ConfidenceResult:
    """
    Deterministic scoring engine utilizing cached context references 
    from SignalCandidate.context_refs.
    """
    score = 0.0
    reasons = []
    warnings = []
    refs = signal.context_refs

    # 1. Structural/BOS/CHoCH Confluence
    if refs.bos_index is not None:
        score += ScoringConfig.WEIGHT_BOS
        reasons.append("BOS structural confluence validated.")
    if refs.choch_index is not None:
        score += ScoringConfig.WEIGHT_CHOCH
        reasons.append("CHoCH reversal confluence validated.")

    # 2. Footprint Confluence (OB/FVG)
    if refs.ob_index is not None or refs.fvg_index is not None:
        score += ScoringConfig.WEIGHT_FOOTPRINT
        reasons.append("Institutional footprint (OB/FVG) confirmed.")

    # 3. AMD Confluence
    if refs.amd_index is not None:
        score += ScoringConfig.WEIGHT_AMD
        reasons.append("AMD cycle alignment confirmed.")

    # 4. Latency Check
    current_index = context.candles[-1].index
    if (current_index - refs.entry_index) > ScoringConfig.MAX_SIGNAL_AGE:
        warnings.append("Stale signal: Setup index aged beyond threshold.")
        score -= ScoringConfig.PENALTY_LATENCY

    final_score = max(0.0, min(100.0, score))
    return ConfidenceResult(
        technical_score=final_score,
        confidence=final_score / 100.0,
        warnings=warnings,
        reasons=reasons
    )
