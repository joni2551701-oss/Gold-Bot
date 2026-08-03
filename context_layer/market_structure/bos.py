from dataclasses import dataclass
from enum import Enum
from typing import List, Sequence
from datetime import datetime
from data_layer.providers.twelve_data_client import Candle
from context_layer.market_structure.market_structure import StructurePoint, StructureType
from core_layer.logger.logger import setup_logger

logger = setup_logger("BOSEngine")

class BosDirection(Enum):
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"

@dataclass(frozen=True)
class BosEvent:
    index: int
    timestamp: datetime
    direction: BosDirection
    broken_structure: StructurePoint

def detect_bos(candles: Sequence[Candle], structures: Sequence[StructurePoint]) -> List[BosEvent]:
    """
    Detects confirmed Break of Structure (BOS) events.
    BOS is confirmed only when price closes beyond a trend-aligned 
    structural pivot (HH for Bullish, LL for Bearish).
    """
    bos_events: List[BosEvent] = []
    
    if len(structures) < 1:
        return bos_events

    last_bullish_bos_index = -1
    last_bearish_bos_index = -1

    for struct in structures:
        # Bullish BOS: Structural continuation from Higher High
        if struct.structure == StructureType.HIGHER_HIGH:
            for j in range(struct.swing.index + 1, len(candles)):
                if j <= last_bullish_bos_index:
                    continue

                if candles[j].close > struct.swing.price:
                    bos_events.append(BosEvent(
                        index=j,
                        timestamp=candles[j].timestamp,
                        direction=BosDirection.BULLISH,
                        broken_structure=struct
                    ))
                    last_bullish_bos_index = j
                    break

        # Bearish BOS: Structural continuation from Lower Low
        elif struct.structure == StructureType.LOWER_LOW:
            for j in range(struct.swing.index + 1, len(candles)):
                if j <= last_bearish_bos_index:
                    continue

                if candles[j].close < struct.swing.price:
                    bos_events.append(BosEvent(
                        index=j,
                        timestamp=candles[j].timestamp,
                        direction=BosDirection.BEARISH,
                        broken_structure=struct
                    ))
                    last_bearish_bos_index = j
                    break
                
    return bos_events
