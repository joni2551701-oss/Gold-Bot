"""
Context Layer — Market Regime Engine foundation (Phase A7).

Classifies the overall market character (TRENDING/RANGE/ACCUMULATION/
DISTRIBUTION/HIGH_VOLATILITY/LOW_VOLATILITY/UNKNOWN) from data already
computed by the rest of the Context Engine plus HTF Bias. It does NOT
switch strategies, does NOT change AI/Decision/Risk logic, and is NOT
itself a decision -- see docs/MARKET_REGIME.md for the full contract.

No new indicator is introduced. Every signal this module reads is
already detected elsewhere:
- context.market_structure.most_recent_bias() (Phase A4's shared
  extraction) supplies the execution-timeframe directional read.
- context.wyckoff.WyckoffEvent (Phase A5) supplies Accumulation/
  Distribution phase evidence.
- context.session.compute_session_volatility()/classify_session()
  (Phase A6) supply the volatility comparison.
- context.htf_bias.HTFBiasResult (Phase A2) supplies the higher-
  timeframe read, passed in externally since it is computed outside
  ContextEngine.build() (a separate multi-timeframe fetch, unlike
  everything else this module reads).

Priority order when more than one signal could apply (regime is a
single label, not a combination): a confirmed Wyckoff Spring/Upthrust
is the most specific, highest-information signal, checked first; a
confirmed HTF+structure trend is checked next; a volatility extreme
third; RANGE is the default when data exists but nothing above
triggered; UNKNOWN is reserved for when there is no usable data at
all. This ordering is a foundation-phase judgment call, not a claim
that (e.g.) a trending market can never also be highly volatile --
see docs/MARKET_REGIME.md for the full rationale.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Sequence, TYPE_CHECKING

from data_layer.providers.twelve_data_client import Candle
from context_layer.market_structure.market_structure import StructurePoint, most_recent_bias
from context_layer.wyckoff.wyckoff import WyckoffEvent, WyckoffPhase
from context_layer.session.session import classify_session, compute_session_volatility
from context_layer.trend.htf_bias import HTFBias

if TYPE_CHECKING:
    from context_layer.trend.htf_bias import HTFBiasResult


class MarketRegime(Enum):
    TRENDING = "TRENDING"
    RANGE = "RANGE"
    ACCUMULATION = "ACCUMULATION"
    DISTRIBUTION = "DISTRIBUTION"
    HIGH_VOLATILITY = "HIGH_VOLATILITY"
    LOW_VOLATILITY = "LOW_VOLATILITY"
    UNKNOWN = "UNKNOWN"


class RegimeDirection(Enum):
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    NEUTRAL = "NEUTRAL"


@dataclass(frozen=True)
class MarketRegimeResult:
    """
    regime: one of the 7 MarketRegime values.
    direction: BULLISH/BEARISH/NEUTRAL -- NEUTRAL for every regime
        that isn't directionally meaningful (RANGE, HIGH_VOLATILITY,
        LOW_VOLATILITY, UNKNOWN).
    confidence: 0-100 (matching HTFBiasResult's convention, not
        Decision Engine's 0.0-1.0 scale).
    reasons: human-readable strings explaining the classification --
        explainability, not consumed by the classification logic
        itself.
    """
    regime: MarketRegime
    direction: RegimeDirection
    confidence: float
    reasons: Sequence[str]


# Named confidence constants -- never hardcoded inline in
# compute_market_regime(), matching this codebase's established
# DecisionWeights/HTF_BIAS_SCORE_MAP convention.
WYCKOFF_REGIME_CONFIDENCE = 75.0
TRENDING_CONFIRMED_CONFIDENCE = 85.0    # execution-timeframe structure agrees with HTF Bias
TRENDING_UNCONFIRMED_CONFIDENCE = 55.0  # structure alone, no HTF Bias available to confirm
VOLATILITY_CONFIDENCE = 65.0
RANGE_CONFIDENCE = 50.0
UNKNOWN_CONFIDENCE = 0.0

# A session's average range at or above this multiple of the whole
# window's average range is HIGH_VOLATILITY; at or below the inverse
# multiple is LOW_VOLATILITY. Both are real ratios of real, already-
# computed data (context.session.compute_session_volatility()) -- not
# a historical/cross-window claim.
HIGH_VOLATILITY_RATIO_THRESHOLD = 1.5
LOW_VOLATILITY_RATIO_THRESHOLD = 0.5


def compute_market_regime(
    candles: Sequence[Candle],
    structure: Sequence[StructurePoint],
    wyckoff_events: Sequence[WyckoffEvent],
    htf_bias: Optional['HTFBiasResult'] = None,
) -> MarketRegimeResult:
    """
    Never raises: empty/missing inputs at any stage fall through to
    the next check, ultimately reaching UNKNOWN if no usable data
    exists at all.
    """
    if wyckoff_events:
        latest = wyckoff_events[-1]
        if latest.phase == WyckoffPhase.ACCUMULATION:
            return MarketRegimeResult(
                regime=MarketRegime.ACCUMULATION,
                direction=RegimeDirection.BULLISH,
                confidence=WYCKOFF_REGIME_CONFIDENCE,
                reasons=[f"Recent Wyckoff {latest.type.value} ({latest.phase.value})"],
            )
        if latest.phase == WyckoffPhase.DISTRIBUTION:
            return MarketRegimeResult(
                regime=MarketRegime.DISTRIBUTION,
                direction=RegimeDirection.BEARISH,
                confidence=WYCKOFF_REGIME_CONFIDENCE,
                reasons=[f"Recent Wyckoff {latest.type.value} ({latest.phase.value})"],
            )

    structure_bias = most_recent_bias(structure)
    htf_reading = htf_bias.bias if htf_bias is not None else None

    if structure_bias == "BULLISH":
        if htf_reading == HTFBias.BEARISH:
            return MarketRegimeResult(
                MarketRegime.RANGE, RegimeDirection.NEUTRAL, RANGE_CONFIDENCE,
                ["Execution-timeframe structure bullish but HTF Bias bearish -- conflicting context"],
            )
        if htf_reading == HTFBias.BULLISH:
            return MarketRegimeResult(
                MarketRegime.TRENDING, RegimeDirection.BULLISH, TRENDING_CONFIRMED_CONFIDENCE,
                ["HTF bullish bias", "HH/HL structure"],
            )
        return MarketRegimeResult(
            MarketRegime.TRENDING, RegimeDirection.BULLISH, TRENDING_UNCONFIRMED_CONFIDENCE,
            ["HH/HL structure (no HTF Bias confirmation)"],
        )

    if structure_bias == "BEARISH":
        if htf_reading == HTFBias.BULLISH:
            return MarketRegimeResult(
                MarketRegime.RANGE, RegimeDirection.NEUTRAL, RANGE_CONFIDENCE,
                ["Execution-timeframe structure bearish but HTF Bias bullish -- conflicting context"],
            )
        if htf_reading == HTFBias.BEARISH:
            return MarketRegimeResult(
                MarketRegime.TRENDING, RegimeDirection.BEARISH, TRENDING_CONFIRMED_CONFIDENCE,
                ["HTF bearish bias", "LH/LL structure"],
            )
        return MarketRegimeResult(
            MarketRegime.TRENDING, RegimeDirection.BEARISH, TRENDING_UNCONFIRMED_CONFIDENCE,
            ["LH/LL structure (no HTF Bias confirmation)"],
        )

    if candles:
        volatility = compute_session_volatility(candles)
        overall_avg_range = sum(c.high - c.low for c in candles) / len(candles)
        current_session = classify_session(candles[-1].timestamp)
        current_avg_range = volatility.get(current_session)

        if current_avg_range is not None and overall_avg_range > 0:
            ratio = current_avg_range / overall_avg_range
            if ratio >= HIGH_VOLATILITY_RATIO_THRESHOLD:
                return MarketRegimeResult(
                    MarketRegime.HIGH_VOLATILITY, RegimeDirection.NEUTRAL, VOLATILITY_CONFIDENCE,
                    [f"Current session ({current_session.value}) range is {ratio:.2f}x the window average"],
                )
            if ratio <= LOW_VOLATILITY_RATIO_THRESHOLD:
                return MarketRegimeResult(
                    MarketRegime.LOW_VOLATILITY, RegimeDirection.NEUTRAL, VOLATILITY_CONFIDENCE,
                    [f"Current session ({current_session.value}) range is {ratio:.2f}x the window average"],
                )

        return MarketRegimeResult(
            MarketRegime.RANGE, RegimeDirection.NEUTRAL, RANGE_CONFIDENCE,
            ["No clear trend, Wyckoff, or volatility-extreme signal in this window"],
        )

    return MarketRegimeResult(
        MarketRegime.UNKNOWN, RegimeDirection.NEUTRAL, UNKNOWN_CONFIDENCE,
        ["Insufficient data to classify market regime"],
    )
