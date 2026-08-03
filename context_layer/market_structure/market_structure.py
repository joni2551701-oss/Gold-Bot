from dataclasses import dataclass
from enum import Enum
from typing import List, Sequence, Optional
from datetime import datetime
from data_layer.providers.twelve_data_client import Candle
from core_layer.logger.logger import setup_logger

logger = setup_logger("MarketStructureEngine")

class SwingType(Enum):
    HIGH = "HIGH"
    LOW = "LOW"

class StructureType(Enum):
    HIGHER_HIGH = "HH"
    HIGHER_LOW = "HL"
    LOWER_HIGH = "LH"
    LOWER_LOW = "LL"
    UNKNOWN = "UNKNOWN"

@dataclass(frozen=True)
class SwingPoint:
    index: int
    price: float
    timestamp: datetime
    type: SwingType

@dataclass(frozen=True)
class StructurePoint:
    swing: SwingPoint
    structure: StructureType

def detect_swing_points(candles: Sequence[Candle], left_strength: int, right_strength: int) -> List[SwingPoint]:
    """
    Identifies confirmed swing points (fractals) in a candle series.
    Returns an empty list and logs a warning if parameters are invalid.
    """
    if left_strength <= 0 or right_strength <= 0:
        logger.warning(f"Invalid strength parameters: left={left_strength}, right={right_strength}. Swing detection aborted.")
        return []
        
    swings: List[SwingPoint] = []
    
    if len(candles) < (left_strength + right_strength + 1):
        return swings

    for i in range(left_strength, len(candles) - right_strength):
        current = candles[i]
        
        # Check for Swing High
        is_swing_high = all(candles[i-j].high < current.high for j in range(1, left_strength + 1)) and \
                        all(candles[i+j].high < current.high for j in range(1, right_strength + 1))
        
        if is_swing_high:
            swings.append(SwingPoint(i, current.high, current.timestamp, SwingType.HIGH))
            continue
            
        # Check for Swing Low
        is_swing_low = all(candles[i-j].low > current.low for j in range(1, left_strength + 1)) and \
                       all(candles[i+j].low > current.low for j in range(1, right_strength + 1))
        
        if is_swing_low:
            swings.append(SwingPoint(i, current.low, current.timestamp, SwingType.LOW))
            
    return swings

def most_recent_bias(structure: Sequence[StructurePoint]) -> Optional[str]:
    """
    Walks backward through already-classified structure points
    (classify_structure()'s output) for the most recent confirmed
    directional read: "BULLISH" for HH/HL, "BEARISH" for LH/LL. None
    if no point has been classified yet (e.g. too few swings to
    confirm any structure -- every point is still StructureType.UNKNOWN).

    Extracted (Phase A4) from context_layer/trend/htf_bias.py's per-timeframe
    classification, which had this exact walk-backward logic inline --
    now the single, shared definition of "what does this structure
    sequence's most recent point say about direction," reused by both
    HTF Bias and Signal Quality Score (signals/signal_quality.py).
    Behavior is unchanged from the pre-extraction inline version.
    """
    for point in reversed(structure):
        if point.structure in (StructureType.HIGHER_HIGH, StructureType.HIGHER_LOW):
            return "BULLISH"
        if point.structure in (StructureType.LOWER_HIGH, StructureType.LOWER_LOW):
            return "BEARISH"
    return None


def classify_structure(swings: Sequence[SwingPoint]) -> List[StructurePoint]:
    """
    Classifies swings as HH, HL, LH, LL based on previous swing of the same type.
    UNKNOWN is returned for the first occurrence of HIGH or LOW types.
    Complexity: O(n)
    """
    classified: List[StructurePoint] = []
    
    last_high: Optional[SwingPoint] = None
    last_low: Optional[SwingPoint] = None
    
    for swing in swings:
        structure = StructureType.UNKNOWN
        
        if swing.type == SwingType.HIGH:
            if last_high:
                if swing.price > last_high.price:
                    structure = StructureType.HIGHER_HIGH
                else:
                    structure = StructureType.LOWER_HIGH
            last_high = swing
            
        elif swing.type == SwingType.LOW:
            if last_low:
                if swing.price > last_low.price:
                    structure = StructureType.HIGHER_LOW
                else:
                    structure = StructureType.LOWER_LOW
            last_low = swing
            
        classified.append(StructurePoint(swing, structure))
        
    return classified
