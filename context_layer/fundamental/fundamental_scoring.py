"""
Context Layer — Fundamental Scoring Engine (Phase 60.5: Fundamental
Intelligence Foundation, TASK 5).

Combines already-classified per-indicator biases (dxy_bias/rates_bias/
inflation_bias/risk_sentiment -- each "BULLISH"/"BEARISH"/"NEUTRAL"
FOR GOLD, supplied by the caller) into one aggregate gold_bias +
macro_score + confidence. This module does not classify a raw macro
number into a bias itself -- context_layer/fundamental/fundamental_context.py's own
docstring already discloses that gap ("would need a historical
baseline/threshold model this codebase has no real data to calibrate
today"), and TASK 1's reuse audit found nothing has closed it since.
A future analyst/AI layer supplies the per-indicator biases; this
module only aggregates them, the same "adapter over already-computed
data" posture context_layer/fundamental/fundamental_context.py itself established.

The Director's own worked example ("DXY: -20, Rates: -15, Inflation:
+10, Risk: +15 -> Gold Score: +70") is illustrative of the shape only
-- those four numbers do not arithmetically sum to +70, so this module
does not attempt to literally reproduce them. Instead it uses one
disclosed, deterministic weighted formula (FundamentalScoreWeights,
below) that produces the same kind of 0-100 "Gold Score" output,
centered at 50 (neutral).

Per the Director's own hard boundary for this whole phase: this module
never returns "BUY"/"SELL", never opens a trade, and is never called
from decision/decision_engine.py or risk/risk_manager.py -- it answers
"what does the macro picture look like for gold," nothing more.
"""

from dataclasses import dataclass
from typing import List, Optional

BULLISH = "BULLISH"
BEARISH = "BEARISH"
NEUTRAL = "NEUTRAL"


@dataclass(frozen=True)
class FundamentalScoreWeights:
    """
    Magnitudes only (always positive) -- the sign of each component's
    contribution comes from its own bias ("BULLISH" -> +weight,
    "BEARISH" -> -weight, anything else -> 0), not from this config.
    Defaults roughly match the Director's own worked example's
    relative ordering (DXY weighted heaviest, then Rates/Risk, then
    Inflation) without claiming to reproduce its exact numbers -- see
    module docstring.
    """
    dxy: float = 20.0
    rates: float = 15.0
    inflation: float = 10.0
    risk: float = 15.0


@dataclass(frozen=True)
class FundamentalScoreResult:
    """
    dxy_bias/rates_bias/inflation_bias/risk_sentiment/fed_expectation:
        the caller-supplied inputs, carried through unchanged (so a
        consumer never has to re-fetch them alongside the result).
        fed_expectation is informational only, not part of the score.
    gold_bias: "BULLISH"/"BEARISH"/"NEUTRAL" -- the aggregate
        classification, thresholded off macro_score.
    macro_score: 0-100, centered at 50 (fully neutral); 100 is the
        maximum possible bullish-for-gold reading, 0 the maximum
        possible bearish one, given only the four weighted components.
    confidence: 0-100, the distance of macro_score from the neutral
        midpoint (50), scaled so a maximally one-sided reading reports
        100 and a fully neutral one reports 0.
    """
    dxy_bias: Optional[str]
    rates_bias: Optional[str]
    inflation_bias: Optional[str]
    fed_expectation: Optional[str]
    risk_sentiment: Optional[str]
    gold_bias: str
    confidence: float
    macro_score: float


def _signed_contribution(bias: Optional[str], weight: float) -> float:
    """+weight for BULLISH, -weight for BEARISH, 0.0 for NEUTRAL/None/anything else -- unknown input is never fatal."""
    if bias == BULLISH:
        return weight
    if bias == BEARISH:
        return -weight
    return 0.0


def compute_fundamental_score(
    dxy_bias: Optional[str] = None,
    rates_bias: Optional[str] = None,
    inflation_bias: Optional[str] = None,
    risk_sentiment: Optional[str] = None,
    fed_expectation: Optional[str] = None,
    weights: Optional[FundamentalScoreWeights] = None,
) -> FundamentalScoreResult:
    """
    Never raises: every argument is optional and any unrecognized bias
    string contributes 0 (treated as NEUTRAL), so a caller with no
    inputs at all gets a fully neutral FundamentalScoreResult
    (macro_score=50.0, gold_bias="NEUTRAL", confidence=0.0), not an
    exception.
    """
    weights = weights or FundamentalScoreWeights()
    max_raw = weights.dxy + weights.rates + weights.inflation + weights.risk

    raw = (
        _signed_contribution(dxy_bias, weights.dxy)
        + _signed_contribution(rates_bias, weights.rates)
        + _signed_contribution(inflation_bias, weights.inflation)
        + _signed_contribution(risk_sentiment, weights.risk)
    )

    macro_score = 50.0 + (raw / max_raw) * 50.0 if max_raw > 0 else 50.0

    if macro_score >= 60.0:
        gold_bias = BULLISH
    elif macro_score <= 40.0:
        gold_bias = BEARISH
    else:
        gold_bias = NEUTRAL

    confidence = min(abs(macro_score - 50.0) * 2.0, 100.0)

    return FundamentalScoreResult(
        dxy_bias=dxy_bias,
        rates_bias=rates_bias,
        inflation_bias=inflation_bias,
        fed_expectation=fed_expectation,
        risk_sentiment=risk_sentiment,
        gold_bias=gold_bias,
        confidence=confidence,
        macro_score=macro_score,
    )


_COMPONENT_LABELS = (
    ("dxy_bias", "DXY"),
    ("rates_bias", "Rates"),
    ("inflation_bias", "Inflation"),
    ("risk_sentiment", "Risk sentiment"),
)


def explain_fundamental_score(result: FundamentalScoreResult) -> List[str]:
    """
    One short reason string per non-neutral component that actually
    contributed to the score (e.g. "DXY: BEARISH") -- in the same
    fixed order compute_fundamental_score() weighs them. A component
    that is None or "NEUTRAL" contributed nothing (see
    _signed_contribution()) and is skipped, so this list is never
    padded with non-reasons. Never raises: a fully neutral result
    produces an empty list.
    """
    reasons = []
    for field_name, label in _COMPONENT_LABELS:
        bias = getattr(result, field_name)
        if bias in (BULLISH, BEARISH):
            reasons.append(f"{label}: {bias}")
    return reasons


def format_fundamental_score(result: FundamentalScoreResult) -> str:
    """
    Matches the Director's own worked example shape exactly:

        Macro Bias:
        BULLISH GOLD
        Confidence:
        78%
        Reasons:
        - DXY: BEARISH
        - Rates: BULLISH

    "NEUTRAL" renders without the " GOLD" suffix (there is no neutral
    direction to name). Pure formatting, no computation beyond
    explain_fundamental_score() (this module, above).
    """
    bias_line = f"{result.gold_bias} GOLD" if result.gold_bias != NEUTRAL else NEUTRAL
    reasons = explain_fundamental_score(result)

    lines = [
        "Macro Bias:",
        bias_line,
        "Confidence:",
        f"{result.confidence:.0f}%",
        "Reasons:",
    ]
    if reasons:
        lines.extend(f"- {reason}" for reason in reasons)
    else:
        lines.append("- No non-neutral indicators supplied")

    return "\n".join(lines)
