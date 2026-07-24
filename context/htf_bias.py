"""
Context Layer — Higher Timeframe (HTF) Bias (Phase A2).

Describes the higher-timeframe market state (Daily/H4/H1). It does
NOT make a trading decision, does NOT generate a BUY/SELL signal, and
is NOT itself a strategy -- see docs/HTF_BIAS.md for the full
contract and context/README.md for what it does not do.

Reuses existing detection logic rather than duplicating it:
- data.market_data.MarketDataNormalizer.get_snapshot() supplies the
  multi-timeframe candles AND the per-timeframe data-quality flags
  ("OK"/"WARNING_GAP"/"ERROR_NO_DATA") this module reads -- no new
  fetch, validation, or gap-detection logic is added here.
- context.market_structure.detect_swing_points()/classify_structure()
  supplies the HH/HL/LH/LL classification this module's per-timeframe
  bias is derived from -- the same functions context_orchestrator.py
  already uses for the execution timeframe.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Sequence, Tuple

from data.market_data import MarketSnapshot
from data.twelve_data_client import Candle
from context.context_config import ContextConfig
from context.market_structure import (
    detect_swing_points,
    classify_structure,
    most_recent_bias,
)
from core.logger import setup_logger

logger = setup_logger("HTFBiasEngine")

# Task 3: Daily/H4/H1 only. The execution timeframe (M15) is untouched
# -- no M1/M5 logic here.
SUPPORTED_HTF_TIMEFRAMES: Tuple[str, ...] = ("Daily", "H4", "H1")


class HTFBias(Enum):
    """Market-context-only classification -- never a trade action."""
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    NEUTRAL = "NEUTRAL"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class HTFBiasResult:
    """
    Immutable Higher-Timeframe bias snapshot.

    bias: overall HTF direction (BULLISH/BEARISH/NEUTRAL/UNKNOWN).
    confidence: 0-100, how much of SUPPORTED_HTF_TIMEFRAMES agreed on
        the winning direction (not a trade confidence -- see
        docs/HTF_BIAS.md's "Confidence meaning" section).
    timeframes: which of SUPPORTED_HTF_TIMEFRAMES had usable candle
        data this call (may be fewer than all three).
    quality_score: 0.0-1.0, the fraction of SUPPORTED_HTF_TIMEFRAMES
        MarketSnapshot.quality marked "OK" -- reused directly from
        MarketDataNormalizer.get_snapshot(), not recomputed here.
    """
    bias: HTFBias
    confidence: float
    timeframes: Sequence[str]
    quality_score: float


def _classify_timeframe(candles: Sequence[Candle], config: ContextConfig) -> HTFBias:
    """
    Derives one timeframe's bias from its most recent classified
    structure point via context.market_structure.most_recent_bias()
    (Phase A4: extracted from this function's own former inline walk,
    now shared with signals/signal_quality.py -- behavior unchanged).
    UNKNOWN if there isn't yet enough data to confirm any structure.
    """
    swings = detect_swing_points(
        candles, config.swing_left_strength, config.swing_right_strength
    )
    structure = classify_structure(swings)

    bias = most_recent_bias(structure)
    if bias == "BULLISH":
        return HTFBias.BULLISH
    if bias == "BEARISH":
        return HTFBias.BEARISH
    return HTFBias.UNKNOWN


def compute_htf_bias(
    snapshot: MarketSnapshot,
    config: ContextConfig = None,
) -> HTFBiasResult:
    """
    Derives an overall HTF bias from a multi-timeframe MarketSnapshot
    (data.market_data.MarketDataNormalizer.get_snapshot()).

    Never raises: missing/empty candle data for a timeframe is treated
    as that timeframe being UNKNOWN, not an error -- if every
    requested timeframe is UNKNOWN, the overall result is UNKNOWN with
    confidence 0.0.
    """
    config = config or ContextConfig()

    per_timeframe: Dict[str, HTFBias] = {}
    usable_timeframes = []

    for timeframe in SUPPORTED_HTF_TIMEFRAMES:
        candles = snapshot.candles.get(timeframe, [])
        if not candles:
            per_timeframe[timeframe] = HTFBias.UNKNOWN
            continue
        per_timeframe[timeframe] = _classify_timeframe(candles, config)
        usable_timeframes.append(timeframe)

    bullish_count = sum(1 for b in per_timeframe.values() if b == HTFBias.BULLISH)
    bearish_count = sum(1 for b in per_timeframe.values() if b == HTFBias.BEARISH)
    known_count = bullish_count + bearish_count

    if known_count == 0:
        bias = HTFBias.UNKNOWN
        confidence = 0.0
    elif bullish_count == bearish_count:
        bias = HTFBias.NEUTRAL
        confidence = 50.0
    elif bullish_count > bearish_count:
        bias = HTFBias.BULLISH
        confidence = round((bullish_count / len(SUPPORTED_HTF_TIMEFRAMES)) * 100, 2)
    else:
        bias = HTFBias.BEARISH
        confidence = round((bearish_count / len(SUPPORTED_HTF_TIMEFRAMES)) * 100, 2)

    ok_count = sum(
        1 for tf in SUPPORTED_HTF_TIMEFRAMES if snapshot.quality.get(tf) == "OK"
    )
    quality_score = round(ok_count / len(SUPPORTED_HTF_TIMEFRAMES), 2)

    logger.info(
        f"HTF bias computed: bias={bias.value} confidence={confidence:.2f} "
        f"quality_score={quality_score:.2f} timeframes={usable_timeframes}"
    )

    return HTFBiasResult(
        bias=bias,
        confidence=confidence,
        timeframes=tuple(usable_timeframes),
        quality_score=quality_score,
    )
