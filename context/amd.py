from dataclasses import dataclass
from enum import Enum
from typing import List, Sequence, Protocol
from datetime import datetime

from data.twelve_data_client import Candle
from context.liquidity import LiquiditySweepEvent
from context.bos import BosEvent
from context.choch import ChochEvent
from context.order_block import OrderBlock
from context.fvg import FairValueGap

class AmdEventType(Enum):
    MANIPULATION = "MANIPULATION"
    DISTRIBUTION = "DISTRIBUTION"

class ContextConfig:
    OB_CORRELATION_WINDOW: int = 5

class DirectionalEvent(Protocol):
    is_bullish: bool
    index: int
    timestamp: datetime

@dataclass(frozen=True)
class AmdEvent:
    type: AmdEventType
    index: int
    timestamp: datetime
    is_bullish: bool

def detect_amd_events(
    candles: Sequence[Candle],
    sweeps: Sequence[LiquiditySweepEvent],
    bos_events: Sequence[BosEvent],
    choch_events: Sequence[ChochEvent],
    order_blocks: Sequence[OrderBlock],
    fvgs: Sequence[FairValueGap]
) -> List[AmdEvent]:
    """
    Stateless, frozen, and strictly typed AMD detection.
    Final production-ready iteration.
    """
    amd_events: List[AmdEvent] = []
    
    if not candles:
        return amd_events

    timeline = []
    for e in sweeps: timeline.append((e.index, 'sweep', e))
    for e in bos_events: timeline.append((e.index, 'break', e))
    for e in choch_events: timeline.append((e.index, 'break', e))
    for e in order_blocks: timeline.append((e.index, 'ob', e))
    for e in fvgs: timeline.append((e.index, 'fvg', e))
    
    timeline.sort(key=lambda x: x[0])

    last_bullish_sweep, last_bearish_sweep = None, None
    bullish_fvgs, bearish_fvgs = [], []
    bullish_obs, bearish_obs = [], []

    for idx, etype, event in timeline:
        is_bull = event.is_bullish
        
        if etype == 'sweep':
            if is_bull: 
                last_bullish_sweep = event
                bullish_fvgs.clear()
            else: 
                last_bearish_sweep = event
                bearish_fvgs.clear()
                
        elif etype == 'fvg':
            if is_bull and last_bullish_sweep and idx >= last_bullish_sweep.index: bullish_fvgs.append(event)
            elif not is_bull and last_bearish_sweep and idx >= last_bearish_sweep.index: bearish_fvgs.append(event)
                
        elif etype == 'ob':
            if is_bull: bullish_obs.append(event)
            else: bearish_obs.append(event)

        elif etype == 'break':
            relevant_sweep = last_bullish_sweep if is_bull else last_bearish_sweep
            if not relevant_sweep: continue
            
            has_support = (bullish_fvgs if is_bull else bearish_fvgs)
            if not has_support:
                for ob in (bullish_obs if is_bull else bearish_obs):
                    if abs(ob.index - relevant_sweep.index) <= ContextConfig.OB_CORRELATION_WINDOW or \
                       (relevant_sweep.index <= ob.index <= idx):
                        has_support = True
                        break

            if has_support:
                amd_events.append(AmdEvent(AmdEventType.DISTRIBUTION, idx, event.timestamp, is_bull))
                if is_bull: last_bullish_sweep = None
                else: last_bearish_sweep = None
        
        # Add Manipulation event to output timeline
        if etype == 'sweep':
            amd_events.append(AmdEvent(AmdEventType.MANIPULATION, idx, event.timestamp, is_bull))

    return sorted(amd_events, key=lambda x: x.index)
