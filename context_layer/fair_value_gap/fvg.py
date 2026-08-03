from dataclasses import dataclass
from enum import Enum
from typing import List, Sequence
from datetime import datetime
from data_layer.providers.twelve_data_client import Candle

class FvgType(Enum):
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"

@dataclass(frozen=True)
class FairValueGap:
    top: float
    bottom: float
    index: int       # Index of the 3rd candle that confirms the gap
    timestamp: datetime
    type: FvgType
    filled: bool = False  # Mitigation lifecycle managed externally by Context Orchestrator

def detect_fvg(candles: Sequence[Candle]) -> List[FairValueGap]:
    """
    Detects Fair Value Gaps (Imbalances) using a 3-candle sequence.
    Bullish FVG: Gap between Candle 1 High and Candle 3 Low.
    Bearish FVG: Gap between Candle 1 Low and Candle 3 High.
    """
    fvgs: List[FairValueGap] = []
    
    if len(candles) < 3:
        return fvgs

    for i in range(2, len(candles)):
        c1 = candles[i-2]
        c3 = candles[i]
        
        # Bullish FVG: Imbalance where C1 High is lower than C3 Low
        if c1.high < c3.low:
            fvgs.append(FairValueGap(
                top=c3.low,
                bottom=c1.high,
                index=i,
                timestamp=c3.timestamp,
                type=FvgType.BULLISH,
                filled=False
            ))
            
        # Bearish FVG: Imbalance where C1 Low is higher than C3 High
        elif c1.low > c3.high:
            fvgs.append(FairValueGap(
                top=c1.low,
                bottom=c3.high,
                index=i,
                timestamp=c3.timestamp,
                type=FvgType.BEARISH,
                filled=False
            ))
            
    return fvgs
