from dataclasses import dataclass
from enum import Enum
from typing import List, Sequence
from datetime import datetime
from data.twelve_data_client import Candle
from context.market_structure import SwingPoint, SwingType

class LiquidityType(Enum):
    BSL = "BUY_SIDE_LIQUIDITY"
    SSL = "SELL_SIDE_LIQUIDITY"

@dataclass(frozen=True)
class LiquidityZone:
    price: float
    type: LiquidityType
    start_index: int
    end_index: int
    strength: int  # Number of touching points

@dataclass(frozen=True)
class LiquiditySweepEvent:
    index: int
    timestamp: datetime
    type: LiquidityType
    sweep_price: float
    zone: LiquidityZone

def detect_equal_levels(swings: Sequence[SwingPoint], tolerance: float) -> List[LiquidityZone]:
    """Identifies EQH/EQL zones by grouping swings with similar prices."""
    zones: List[LiquidityZone] = []
    highs = [s for s in swings if s.type == SwingType.HIGH]
    lows = [s for s in swings if s.type == SwingType.LOW]
    
    def find_clusters(points: List[SwingPoint], l_type: LiquidityType):
        if len(points) < 2: return
        for i in range(len(points)):
            cluster = [points[i]]
            for j in range(i + 1, len(points)):
                if abs(points[j].price - points[i].price) <= tolerance:
                    cluster.append(points[j])
                else:
                    break
            if len(cluster) >= 2:
                zones.append(LiquidityZone(
                    price=sum(s.price for s in cluster) / len(cluster),
                    type=l_type,
                    start_index=cluster[0].index,
                    end_index=cluster[-1].index,
                    strength=len(cluster)
                ))
    
    find_clusters(highs, LiquidityType.BSL)
    find_clusters(lows, LiquidityType.SSL)
    return zones

def detect_sweeps(candles: Sequence[Candle], zones: Sequence[LiquidityZone]) -> List[LiquiditySweepEvent]:
    """Detects wick penetration of liquidity zones followed by a close back inside."""
    sweeps: List[LiquiditySweepEvent] = []
    
    for zone in zones:
        for i in range(zone.end_index + 1, len(candles)):
            c = candles[i]
            if zone.type == LiquidityType.BSL:
                if c.high > zone.price and c.close < zone.price:
                    sweeps.append(LiquiditySweepEvent(i, c.timestamp, zone.type, c.high, zone))
            elif zone.type == LiquidityType.SSL:
                if c.low < zone.price and c.close > zone.price:
                    sweeps.append(LiquiditySweepEvent(i, c.timestamp, zone.type, c.low, zone))
    return sweeps
