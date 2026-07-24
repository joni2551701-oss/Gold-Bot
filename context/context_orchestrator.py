from dataclasses import dataclass
from typing import List, Optional, Sequence, TYPE_CHECKING

from data.twelve_data_client import Candle

from context.context_config import ContextConfig
from context.market_structure import (
    detect_swing_points,
    classify_structure,
    SwingPoint,
    StructurePoint,
)
from context.bos import detect_bos, BosEvent
from context.choch import detect_choch, ChochEvent
from context.liquidity import (
    detect_equal_levels,
    detect_sweeps,
    LiquidityZone,
    LiquiditySweepEvent,
)
from context.order_block import detect_order_blocks, OrderBlock
from context.fvg import detect_fvg, FairValueGap
from context.amd import detect_amd_events, AmdEvent
from context.wyckoff import detect_wyckoff_events, WyckoffEvent
from context.session import detect_session_events, SessionEvent
from context.market_regime import compute_market_regime, MarketRegimeResult
from core.logger import setup_logger

if TYPE_CHECKING:
    from context.htf_bias import HTFBiasResult

logger = setup_logger("ContextEngine")


@dataclass(frozen=True)
class ContextSnapshot:
    """
    Immutable, fully-resolved market context for a single symbol at a
    single point in time.

    Consumed by the Strategy Layer, AI Layer, and any downstream
    engine that requires a complete Smart Money Concepts view of the
    market. Field names and their semantic meaning are a stable
    contract; downstream consumers depend on them remaining unchanged
    -- Phase A5 added wyckoff_events, Phase A6 added session_events,
    and Phase A7 adds market_regime, but none renames, removes, or
    changes the meaning of any earlier field.

    All fields are required (no defaults) by design -- every caller
    must supply every field explicitly, even as an empty sequence, so
    a caller can never silently construct a snapshot with an
    unintentionally-missing detector's output. See
    tests/test_generate_signals.py's docstring for this convention
    stated as an explicit contract. market_regime is the one
    exception to "empty sequence" (it is a single MarketRegimeResult,
    not a list) -- see context/market_regime.py; a caller with no
    real data still supplies a real MarketRegimeResult(regime=UNKNOWN, ...),
    never None, keeping the same "always supplied, never silently
    missing" spirit.
    """
    candles: Sequence[Candle]
    structure: Sequence[StructurePoint]
    bos_events: Sequence[BosEvent]
    choch_events: Sequence[ChochEvent]
    liquidity_zones: Sequence[LiquidityZone]
    liquidity_sweeps: Sequence[LiquiditySweepEvent]
    order_blocks: Sequence[OrderBlock]
    fair_value_gaps: Sequence[FairValueGap]
    amd_events: Sequence[AmdEvent]
    wyckoff_events: Sequence[WyckoffEvent]
    session_events: Sequence[SessionEvent]
    market_regime: MarketRegimeResult


class ContextEngine:
    """
    Orchestrates the full Context Layer detection pipeline.

    Pipeline stages:
        Candles
          -> SwingPoints            (_build_structure)
          -> StructurePoints        (_build_structure)
          -> BOS / CHoCH            (_build_breaks)
          -> Liquidity Zones        (_build_liquidity)
          -> Liquidity Sweeps       (_build_liquidity)
          -> Order Blocks           (_build_footprints)
          -> Fair Value Gaps        (_build_footprints)
          -> AMD Events             (_build_amd)
          -> Wyckoff Events         (_build_wyckoff, Phase A5)
          -> Session Events         (_build_session, Phase A6)
          -> Market Regime          (_build_market_regime, Phase A7)
          -> ContextSnapshot        (build)

    The engine holds no mutable state between calls to build(): each
    invocation is independent and deterministic for a given candle
    series and configuration, which keeps it safe for repeated or
    concurrent use in future phases (e.g. multi-symbol scanning).
    """

    def __init__(self, config: ContextConfig = None):
        """
        Initializes the engine with the provided configuration, or
        falls back to default detection parameters if none is given.
        """
        self.config = config or ContextConfig()

    def build(self, candles: Sequence[Candle], htf_bias: Optional['HTFBiasResult'] = None) -> ContextSnapshot:
        """
        Runs the full detection pipeline against the provided candle
        series and returns an immutable ContextSnapshot.

        htf_bias (Phase A7, optional, default None) is the only input
        to this method that isn't derived from `candles` -- Market
        Regime reads it, everything else ignores it. Passing None
        (any pre-Phase-A7 caller) simply means Market Regime classifies
        without HTF confirmation available, never an error -- see
        context/market_regime.py.
        """
        self._validate_candle_order(candles)

        swings, structure = self._build_structure(candles)
        bos, choch = self._build_breaks(candles, structure)
        liquidity_zones, liquidity_sweeps = self._build_liquidity(candles, swings)
        order_blocks, fair_value_gaps = self._build_footprints(
            candles, liquidity_sweeps, bos, choch
        )
        amd_events = self._build_amd(
            candles, liquidity_sweeps, bos, choch, order_blocks, fair_value_gaps
        )
        wyckoff_events = self._build_wyckoff(candles, liquidity_sweeps, bos, choch)
        session_events = self._build_session(candles)
        market_regime = self._build_market_regime(candles, structure, wyckoff_events, htf_bias)

        return ContextSnapshot(
            candles=candles,
            structure=structure,
            bos_events=bos,
            choch_events=choch,
            liquidity_zones=liquidity_zones,
            liquidity_sweeps=liquidity_sweeps,
            order_blocks=order_blocks,
            fair_value_gaps=fair_value_gaps,
            amd_events=amd_events,
            wyckoff_events=wyckoff_events,
            session_events=session_events,
            market_regime=market_regime,
        )

    def _validate_candle_order(self, candles: Sequence[Candle]) -> None:
        """
        Logs (never raises, never filters/reorders) if the incoming
        candle series is not strictly ascending by timestamp. Every
        detector below indexes candles positionally and assumes
        chronological order; production candles are already
        deduplicated/sorted by MarketDataNormalizer._validate_and_clean(),
        so this is a diagnostic safety net for any other caller
        (tests, a future data source) that hands build() unsorted or
        duplicate-timestamp candles, not a behavior change.
        """
        for prev, curr in zip(candles, candles[1:]):
            if curr.timestamp <= prev.timestamp:
                logger.warning(
                    "Candle series is not strictly ascending by timestamp "
                    f"({prev.timestamp} -> {curr.timestamp}); detection "
                    "results may be unreliable."
                )
                return

    def _build_structure(
        self, candles: Sequence[Candle]
    ) -> "tuple[List[SwingPoint], List[StructurePoint]]":
        """
        Stage 1: Detects raw swing points (fractals) using the
        configured left/right strength, then classifies them into
        structural points (HH / HL / LH / LL).
        """
        swings: List[SwingPoint] = detect_swing_points(
            candles,
            self.config.swing_left_strength,
            self.config.swing_right_strength,
        )
        structure: List[StructurePoint] = classify_structure(swings)
        return swings, structure

    def _build_breaks(
        self, candles: Sequence[Candle], structure: Sequence[StructurePoint]
    ) -> "tuple[List[BosEvent], List[ChochEvent]]":
        """
        Stage 2: Detects confirmed trend-continuation breaks (BOS) and
        counter-trend reversals (CHoCH) from classified structure.
        """
        bos: List[BosEvent] = detect_bos(candles, structure)
        choch: List[ChochEvent] = detect_choch(candles, structure)
        return bos, choch

    def _build_liquidity(
        self, candles: Sequence[Candle], swings: Sequence[SwingPoint]
    ) -> "tuple[List[LiquidityZone], List[LiquiditySweepEvent]]":
        """
        Stage 3: Detects equal-level liquidity zones (EQH/EQL) from
        swing points using the configured tolerance, then detects
        sweeps of those zones on the candle series.
        """
        zones: List[LiquidityZone] = detect_equal_levels(
            swings,
            self.config.liquidity_equal_level_tolerance,
        )
        sweeps: List[LiquiditySweepEvent] = detect_sweeps(candles, zones)
        return zones, sweeps

    def _build_footprints(
        self,
        candles: Sequence[Candle],
        sweeps: Sequence[LiquiditySweepEvent],
        bos: Sequence[BosEvent],
        choch: Sequence[ChochEvent],
    ) -> "tuple[List[OrderBlock], List[FairValueGap]]":
        """
        Stage 4: Detects institutional footprints — Order Blocks
        (sweep-and-structural-break confirmed) and Fair Value Gaps
        (three-candle structural imbalances).
        """
        order_blocks: List[OrderBlock] = detect_order_blocks(
            candles, sweeps, bos, choch
        )
        fair_value_gaps: List[FairValueGap] = detect_fvg(candles)
        return order_blocks, fair_value_gaps

    def _build_amd(
        self,
        candles: Sequence[Candle],
        sweeps: Sequence[LiquiditySweepEvent],
        bos: Sequence[BosEvent],
        choch: Sequence[ChochEvent],
        order_blocks: Sequence[OrderBlock],
        fair_value_gaps: Sequence[FairValueGap],
    ) -> List[AmdEvent]:
        """
        Stage 5: Correlates liquidity sweeps, structural breaks, and
        footprints into Accumulation-Manipulation-Distribution cycles.
        """
        return detect_amd_events(
            candles, sweeps, bos, choch, order_blocks, fair_value_gaps
        )

    def _build_wyckoff(
        self,
        candles: Sequence[Candle],
        sweeps: Sequence[LiquiditySweepEvent],
        bos: Sequence[BosEvent],
        choch: Sequence[ChochEvent],
    ) -> List[WyckoffEvent]:
        """
        Stage 6 (Phase A5): correlates liquidity sweeps with the
        nearest subsequent same-direction structural break into Spring
        (Accumulation) / Upthrust (Distribution) events. Foundation
        only -- not consumed by any strategy. See context/wyckoff.py
        and docs/WYCKOFF.md.
        """
        return detect_wyckoff_events(candles, sweeps, bos, choch)

    def _build_session(self, candles: Sequence[Candle]) -> List[SessionEvent]:
        """
        Stage 7 (Phase A6): classifies each candle's UTC hour into a
        trading session (Asia/London/New York/Overlap/Off-hours),
        emitting one SessionEvent per transition. Foundation only --
        not consumed by any strategy. See context/session.py and
        docs/SESSION_INTELLIGENCE.md.
        """
        return detect_session_events(candles)

    def _build_market_regime(
        self,
        candles: Sequence[Candle],
        structure: Sequence[StructurePoint],
        wyckoff_events: Sequence[WyckoffEvent],
        htf_bias: Optional['HTFBiasResult'],
    ) -> MarketRegimeResult:
        """
        Stage 8 (Phase A7): classifies overall market character from
        already-computed structure, Wyckoff events, session/volatility
        data, and (if available) HTF Bias -- no new indicator. Not
        consumed by any strategy. See context/market_regime.py and
        docs/MARKET_REGIME.md.
        """
        return compute_market_regime(candles, structure, wyckoff_events, htf_bias)


def build_context_snapshot(candles: Sequence[Candle], htf_bias: Optional['HTFBiasResult'] = None) -> ContextSnapshot:
    """
    Backward-compatible functional entry point.

    Delegates to ContextEngine with default configuration. Retained
    so any existing caller using the original function-based API
    continues to work unchanged. htf_bias (Phase A7, optional) is
    passed straight through to ContextEngine.build() -- see that
    method's docstring.
    """
    return ContextEngine(ContextConfig()).build(candles, htf_bias)
