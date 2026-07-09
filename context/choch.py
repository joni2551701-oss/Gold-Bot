from dataclasses import dataclass
from enum import Enum
from typing import List, Sequence
from datetime import datetime
from data.twelve_data_client import Candle
from context.market_structure import StructurePoint, StructureType
from core.logger import setup_logger

logger = setup_logger("ChochEngine")

class ChochDirection(Enum):
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"

@dataclass(frozen=True)
class ChochEvent:
    index: int
    timestamp: datetime
    direction: ChochDirection
    broken_structure: StructurePoint

def detect_choch(candles: Sequence[Candle], structures: Sequence[StructurePoint]) -> List[ChochEvent]:
    """
    Detects Change of Character (CHoCH) events based on counter-trend structural breaks.
    Bullish CHoCH: Close above a Lower High (LH).
    Bearish CHoCH: Close below a Higher Low (HL).
    """
    choch_events: List[ChochEvent] = []
    
    if len(structures) < 1:
        return choch_events

    last_choch_index = -1

    for struct in structures:
        # Bullish CHoCH: Market breaks Lower High
        if struct.structure == StructureType.LOWER_HIGH:
            for j in range(struct.swing.index + 1, len(candles)):
                if j <= last_choch_index:
                    continue
                
                if candles[j].close > struct.swing.price:
                    choch_events.append(ChochEvent(
                        index=j,
                        timestamp=candles[j].timestamp,
                        direction=ChochDirection.BULLISH,
                        broken_structure=struct
                    ))
                    last_choch_index = j
                    break
        
        # Bearish CHoCH: Market breaks Higher Low
        elif struct.structure == StructureType.HIGHER_LOW:
            for j in range(struct.swing.index + 1, len(candles)):
                if j <= last_choch_index:
                    continue
                
                if candles[j].close < struct.swing.price:
                    choch_events.append(ChochEvent(
                        index=j,
                        timestamp=candles[j].timestamp,
                        direction=ChochDirection.BEARISH,
                        broken_structure=struct
                    ))
                    last_choch_index = j
                    break
                
    return choch_events
