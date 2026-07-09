from dataclasses import dataclass
from enum import Enum
from typing import List, Sequence
from datetime import datetime
from data.twelve_data_client import Candle
from context.market_structure import SwingPoint, SwingType

class BosDirection(Enum):
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"

@dataclass(frozen=True)
class BosEvent:
    index: int
    timestamp: datetime
    direction: BosDirection
    broken_swing_price: float

def detect_bos(candles: Sequence[Candle], swings: Sequence[SwingPoint]) -> List[BosEvent]:
    """
    Detects confirmed Break of Structure events based on candle closes.
    A BOS is confirmed when a candle closes beyond a validated Swing High (Bullish)
    or Swing Low (Bearish).
    """
    bos_events: List[BosEvent] = []
    
    if len(swings) < 2:
        return bos_events

    # Iterate through confirmed swings to find structural breaks
    for i in range(1, len(swings)):
        prev_swing = swings[i-1]
        
        # Bullish BOS: Price closes above previous Swing High
        if prev_swing.type == SwingType.HIGH:
            # Look for the first candle after the swing that closes above the high
            for j in range(prev_swing.index + 1, len(candles)):
                if candles[j].close > prev_swing.price:
                    bos_events.append(BosEvent(
                        index=j,
                        timestamp=candles[j].timestamp,
                        direction=BosDirection.BULLISH,
                        broken_swing_price=prev_swing.price
                    ))
                    break
        
        # Bearish BOS: Price closes below previous Swing Low
        elif prev_swing.type == SwingType.LOW:
            for j in range(prev_swing.index + 1, len(candles)):
                if candles[j].close < prev_swing.price:
                    bos_events.append(BosEvent(
                        index=j,
                        timestamp=candles[j].timestamp,
                        direction=BosDirection.BEARISH,
                        broken_swing_price=prev_swing.price
                    ))
                    break
                
    return bos_events
