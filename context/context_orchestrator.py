from dataclasses import dataclass
from typing import Sequence
from data.twelve_data_client import Candle

# Standardized imports verified against Module definitions
from context.market_structure import detect_market_structure, MarketStructure
from context.bos import detect_bos, BosEvent
from context.choch import detect_choch, ChochEvent
from context.liquidity import detect_liquidity_zones, detect_liquidity_sweeps, LiquidityZone, LiquiditySweepEvent
from context.order_block import detect_order_blocks, OrderBlock
from context.fvg import detect_fvg, FairValueGap
from context.amd import detect_amd_events, AmdEvent

@dataclass(frozen=True)
class ContextSnapshot:
    candles: Sequence[Candle]
    structure: Sequence[MarketStructure]
    bos_events: Sequence[BosEvent]
    choch_events: Sequence[ChochEvent]
    liquidity_zones: Sequence[LiquidityZone]
    liquidity_sweeps: Sequence[LiquiditySweepEvent]
    order_blocks: Sequence[OrderBlock]
    fair_value_gaps: Sequence[FairValueGap]
    amd_events: Sequence[AmdEvent]

def build_context_snapshot(candles: Sequence[Candle]) -> ContextSnapshot:
    """
    Finalized aggregation pipeline. 
    Dependencies are resolved sequentially to ensure snapshot integrity.
    """
    # 1. Structural Foundation
    structure = detect_market_structure(candles)
    bos = detect_bos(candles, structure)
    choch = detect_choch(candles, structure)
    
    # 2. Liquidity & Footprints
    l_zones = detect_liquidity_zones(candles)
    l_sweeps = detect_liquidity_sweeps(candles, l_zones)
    obs = detect_order_blocks(candles, l_sweeps, bos, choch)
    fvgs = detect_fvg(candles)
    
    # 3. Correlation Layer
    amd = detect_amd_events(candles, l_sweeps, bos, choch, obs, fvgs)
    
    return ContextSnapshot(
        candles=candles,
        structure=structure,
        bos_events=bos,
        choch_events=choch,
        liquidity_zones=l_zones,
        liquidity_sweeps=l_sweeps,
        order_blocks=obs,
        fair_value_gaps=fvgs,
        amd_events=amd
    )
