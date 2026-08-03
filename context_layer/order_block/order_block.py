from dataclasses import dataclass
from enum import Enum
from typing import List, Sequence
from datetime import datetime
from data_layer.providers.twelve_data_client import Candle
from context_layer.context_engine.candle import is_bullish, is_bearish
from context_layer.liquidity.liquidity import LiquiditySweepEvent, LiquidityType
from context_layer.market_structure.bos import BosEvent, BosDirection
from context_layer.market_structure.choch import ChochEvent, ChochDirection

class OrderBlockType(Enum):
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"

@dataclass(frozen=True)
class OrderBlock:
    high: float
    low: float
    index: int
    timestamp: datetime
    type: OrderBlockType
    strength: int

def detect_order_blocks(
    candles: Sequence[Candle],
    sweeps: Sequence[LiquiditySweepEvent],
    bos_events: Sequence[BosEvent],
    choch_events: Sequence[ChochEvent]
) -> List[OrderBlock]:
    """
    Identifies Order Blocks: Last candle before a sweep-induced BOS/CHoCH.
    Bullish OB: Bearish candle before an SSL sweep followed by Bullish break.
    Bearish OB: Bullish candle before a BSL sweep followed by Bearish break.
    """
    order_blocks: List[OrderBlock] = []
    
    for sweep in sweeps:
        # Find subsequent BOS or CHoCH to validate the sweep
        break_events = [b for b in bos_events if b.index > sweep.index] + \
                       [c for c in choch_events if c.index > sweep.index]
        
        if not break_events:
            continue
            
        next_break = min(break_events, key=lambda x: x.index)
        
        # Bullish OB Identification
        if sweep.type == LiquidityType.SSL and next_break.direction in [BosDirection.BULLISH, ChochDirection.BULLISH]:
            # Look at candles preceding the sweep for the last bearish candle
            for i in range(sweep.index - 1, -1, -1):
                if is_bearish(candles[i]):
                    order_blocks.append(OrderBlock(
                        high=candles[i].high,
                        low=candles[i].low,
                        index=i,
                        timestamp=candles[i].timestamp,
                        type=OrderBlockType.BULLISH,
                        strength=1
                    ))
                    break
        
        # Bearish OB Identification
        elif sweep.type == LiquidityType.BSL and next_break.direction in [BosDirection.BEARISH, ChochDirection.BEARISH]:
            # Look at candles preceding the sweep for the last bullish candle
            for i in range(sweep.index - 1, -1, -1):
                if is_bullish(candles[i]):
                    order_blocks.append(OrderBlock(
                        high=candles[i].high,
                        low=candles[i].low,
                        index=i,
                        timestamp=candles[i].timestamp,
                        type=OrderBlockType.BEARISH,
                        strength=1
                    ))
                    break
                    
    return order_blocks
