from dataclasses import dataclass
from enum import Enum
from typing import List, Sequence
from datetime import datetime

from data_layer.providers.twelve_data_client import Candle
from context.liquidity import LiquiditySweepEvent, LiquidityType
from context.bos import BosEvent, BosDirection
from context.choch import ChochEvent, ChochDirection
from context.order_block import OrderBlock, OrderBlockType
from context.fvg import FairValueGap, FvgType
from core_layer.logger.logger import setup_logger

logger = setup_logger("AMD")


class AmdEventType(Enum):
    MANIPULATION = "MANIPULATION"
    DISTRIBUTION = "DISTRIBUTION"


class AMDConfig:
    """
    AMD-specific heuristic configuration.

    Distinct from context.context_config.ContextConfig: this value
    controls the AMD correlation heuristic only, not the shared
    pipeline detection parameters used across multiple Context Layer
    modules.
    """
    OB_CORRELATION_WINDOW: int = 5


@dataclass(frozen=True)
class AmdEvent:
    """
    A single point in an Accumulation-Manipulation-Distribution cycle.
    """
    type: AmdEventType
    index: int
    timestamp: datetime
    is_bullish: bool


def _resolve_direction(etype: str, event) -> bool:
    """
    Resolves the bullish/bearish direction of a timeline event using
    that event's own confirmed contract field.

    No shared 'is_bullish' attribute exists across the five event
    types produced by the Context Layer (LiquiditySweepEvent, BosEvent,
    ChochEvent, OrderBlock, FairValueGap) — each exposes direction
    through a different, type-specific enum field. This function is
    the single point where that mapping is defined, so the timeline
    loop below remains agnostic to per-type contract differences.

    Args:
        etype: One of 'sweep', 'break', 'ob', 'fvg' — the timeline
            tag assigned when the event was added to the AMD timeline.
        event: The underlying event object matching that tag.

    Returns:
        True if the event represents bullish directional intent,
        False if bearish.

    Raises:
        ValueError: If etype is not one of the recognized tags, or if
            a 'break' event is of an unrecognized type.
    """
    if etype == 'sweep':
        return event.type == LiquidityType.SSL

    elif etype == 'break':
        if isinstance(event, BosEvent):
            return event.direction == BosDirection.BULLISH
        elif isinstance(event, ChochEvent):
            return event.direction == ChochDirection.BULLISH
        raise ValueError(f"Unrecognized 'break' event type: {type(event).__name__}")

    elif etype == 'ob':
        return event.type == OrderBlockType.BULLISH

    elif etype == 'fvg':
        return event.type == FvgType.BULLISH

    raise ValueError(f"Unrecognized timeline event tag: {etype}")


def detect_amd_events(
    candles: Sequence[Candle],
    sweeps: Sequence[LiquiditySweepEvent],
    bos_events: Sequence[BosEvent],
    choch_events: Sequence[ChochEvent],
    order_blocks: Sequence[OrderBlock],
    fvgs: Sequence[FairValueGap]
) -> List[AmdEvent]:
    """
    Detects Accumulation-Manipulation-Distribution (AMD) cycles by
    correlating liquidity sweeps (Manipulation) with subsequent
    structural breaks supported by an Order Block or FVG footprint
    (Distribution).

    State machine, timeline construction, and correlation logic are
    unchanged from the original implementation. The only change from
    the prior version is direction resolution: instead of assuming a
    shared `event.is_bullish` attribute (which does not exist on any
    of the five contributing event types), direction is resolved per
    event type via _resolve_direction(), using each type's own
    confirmed contract field.
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
        try:
            is_bull = _resolve_direction(etype, event)
        except ValueError as e:
            # Defensive only: today's timeline construction (lines above)
            # only ever tags 'sweep'/'break'/'ob'/'fvg' with matching
            # event types, so this branch is unreachable with the
            # current five event types. It exists so that a future
            # timeline addition with a missing _resolve_direction()
            # mapping degrades to "skip this event" instead of crashing
            # the whole AMD detection pass.
            logger.warning(f"Skipping unresolvable AMD timeline event at index {idx}: {e}")
            continue

        if etype == 'sweep':
            if is_bull:
                last_bullish_sweep = event
                bullish_fvgs.clear()
                bullish_obs.clear()
            else:
                last_bearish_sweep = event
                bearish_fvgs.clear()
                bearish_obs.clear()

        elif etype == 'fvg':
            if is_bull and last_bullish_sweep and idx >= last_bullish_sweep.index:
                bullish_fvgs.append(event)
            elif not is_bull and last_bearish_sweep and idx >= last_bearish_sweep.index:
                bearish_fvgs.append(event)

        elif etype == 'ob':
            if is_bull:
                bullish_obs.append(event)
            else:
                bearish_obs.append(event)

        elif etype == 'break':
            relevant_sweep = last_bullish_sweep if is_bull else last_bearish_sweep
            if not relevant_sweep:
                continue

            has_support = bool(bullish_fvgs if is_bull else bearish_fvgs)
            if not has_support:
                for ob in (bullish_obs if is_bull else bearish_obs):
                    if abs(ob.index - relevant_sweep.index) <= AMDConfig.OB_CORRELATION_WINDOW or \
                       (relevant_sweep.index <= ob.index <= idx):
                        has_support = True
                        break

            if has_support:
                amd_events.append(AmdEvent(AmdEventType.DISTRIBUTION, idx, event.timestamp, is_bull))
                if is_bull:
                    last_bullish_sweep = None
                else:
                    last_bearish_sweep = None

        # Add Manipulation event to output timeline
        if etype == 'sweep':
            amd_events.append(AmdEvent(AmdEventType.MANIPULATION, idx, event.timestamp, is_bull))

    return sorted(amd_events, key=lambda x: x.index)
