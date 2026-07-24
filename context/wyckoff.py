"""
Context Layer — Wyckoff Engine foundation (Phase A5).

A knowledge layer for the Context Engine only. It does NOT generate a
BUY/SELL signal and is NOT a strategy -- see docs/WYCKOFF.md for the
full contract and context/README.md for what it does not do. No
strategies/*.py file reads WyckoffEvent; wiring one is a future,
separately-approved phase.

Scope for this phase, mapped from the Director's five-item list
(Accumulation, Manipulation, Distribution, Spring, Upthrust):
- SPRING / UPTHRUST are the two detected event types -- a Spring is a
  swept support zone (sell-side liquidity) followed by a confirming
  bullish structural break; an Upthrust is the mirror (swept
  resistance / buy-side liquidity, then a bearish break). These are
  the specific, testable "test of support/resistance" patterns
  Wyckoff theory is most identified by, beyond a generic SMC sweep.
- ACCUMULATION / DISTRIBUTION are exposed as each event's `phase` --
  a Spring's phase is always ACCUMULATION, an Upthrust's is always
  DISTRIBUTION. Not a separate detector.
- MANIPULATION is not a third, separate event type -- it is the
  `sweep` field already present on every WyckoffEvent (the liquidity
  sweep that sets up the Spring/Upthrust *is* the manipulation leg of
  that cycle). Modeling it as a third independent detector would
  re-describe the same sweep context/amd.py's AmdEventType.MANIPULATION
  already names for a related but distinct concept -- see
  docs/WYCKOFF.md's "Relationship to AMD" section for why this module
  does not import or reuse context/amd.py directly (both read the same
  underlying LiquiditySweepEvent/BosEvent/ChochEvent types, but
  Spring/Upthrust are a narrower, more specific correlation than
  AMD's general sweep-then-break detection, and context/amd.py already
  feeds a live, tested strategy -- this module does not touch it).

Reuses existing detection output rather than duplicating it:
- context.liquidity.LiquiditySweepEvent, context.bos.BosEvent,
  context.choch.ChochEvent (all unchanged) supply the sweep/break
  events this module correlates -- no new sweep or structural-break
  detection is added here, same reuse principle context/order_block.py
  already established for its own sweep-then-break correlation.
"""

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Sequence
from datetime import datetime

from data.twelve_data_client import Candle
from context.liquidity import LiquiditySweepEvent, LiquidityType
from context.bos import BosEvent, BosDirection
from context.choch import ChochEvent, ChochDirection


class WyckoffEventType(Enum):
    SPRING = "SPRING"
    UPTHRUST = "UPTHRUST"


class WyckoffPhase(Enum):
    """
    Exposed alongside `type` even though it is currently a direct
    function of it (SPRING -> ACCUMULATION, UPTHRUST -> DISTRIBUTION)
    -- kept as its own field so a caller can query "give me every
    Accumulation-phase event" without knowing the type mapping, and so
    a future phase distinguishing multiple event types per phase (e.g.
    a Wyckoff "Test" or "Sign of Strength" event) does not need a
    breaking field-shape change.
    """
    ACCUMULATION = "ACCUMULATION"
    DISTRIBUTION = "DISTRIBUTION"


@dataclass(frozen=True)
class WyckoffEvent:
    """
    A single confirmed Spring or Upthrust.

    type: SPRING or UPTHRUST.
    phase: ACCUMULATION (Spring) or DISTRIBUTION (Upthrust).
    index: the confirming break's candle index (BOS/CHoCH), not the
        sweep's own index -- matches context/order_block.py's
        convention of indexing an event by its confirmation point.
    timestamp: the confirming break's timestamp.
    sweep: the LiquiditySweepEvent that set up this Spring/Upthrust --
        this *is* the Manipulation leg of the cycle (see module
        docstring); not a separate field/event.
    confirming_break_index: same as `index`, named explicitly so a
        caller doesn't have to infer which of the two indices (sweep
        vs. break) `index` refers to.
    volume_confirmed: Optional[bool], always None today -- see
        _volume_confirms()'s docstring. Never True/False without a
        real volume data source, so no caller can mistake "not
        checked" for "confirmed" or "rejected".
    """
    type: WyckoffEventType
    phase: WyckoffPhase
    index: int
    timestamp: datetime
    sweep: LiquiditySweepEvent
    confirming_break_index: int
    volume_confirmed: Optional[bool]


def _volume_confirms(candles: Sequence[Candle], sweep_index: int, break_index: int) -> Optional[bool]:
    """
    Volume confirmation hook (Phase A5, Director-specified scope item).

    Wyckoff theory conventionally looks for climactic/declining volume
    around a Spring or Upthrust to fully confirm the test. This
    codebase has no volume data source at all -- data.twelve_data_client
    .Candle is OHLC-only (confirmed in Phase A1's architecture audit;
    re-confirmed by reading the file this phase). This hook always
    returns None ("not checked"), never True or False, so a caller can
    never mistake "no data" for a real confirmation/rejection. Wire in
    real volume confirmation here once a volume data source exists
    (see docs/WYCKOFF.md's Future Expansion section) -- no other
    function in this module needs to change; only this one's body.
    """
    return None


def _confirming_break(
    sweep: LiquiditySweepEvent,
    bos_events: Sequence[BosEvent],
    choch_events: Sequence[ChochEvent],
    wanted_bos_direction: BosDirection,
    wanted_choch_direction: ChochDirection,
):
    """Nearest BOS/CHoCH of the wanted direction strictly after the sweep -- None if none exists."""
    candidates = [
        b for b in bos_events
        if b.direction == wanted_bos_direction and b.index > sweep.index
    ] + [
        c for c in choch_events
        if c.direction == wanted_choch_direction and c.index > sweep.index
    ]
    if not candidates:
        return None
    return min(candidates, key=lambda event: event.index)


def detect_wyckoff_events(
    candles: Sequence[Candle],
    liquidity_sweeps: Sequence[LiquiditySweepEvent],
    bos_events: Sequence[BosEvent],
    choch_events: Sequence[ChochEvent],
) -> List[WyckoffEvent]:
    """
    Correlates already-detected liquidity sweeps with the nearest
    subsequent same-direction structural break to identify Spring
    (SSL sweep -> bullish break, Accumulation) and Upthrust (BSL sweep
    -> bearish break, Distribution) events. Never raises: empty inputs
    simply produce an empty result.
    """
    events: List[WyckoffEvent] = []

    for sweep in liquidity_sweeps:
        if sweep.type == LiquidityType.SSL:
            event_type = WyckoffEventType.SPRING
            phase = WyckoffPhase.ACCUMULATION
            wanted_bos = BosDirection.BULLISH
            wanted_choch = ChochDirection.BULLISH
        elif sweep.type == LiquidityType.BSL:
            event_type = WyckoffEventType.UPTHRUST
            phase = WyckoffPhase.DISTRIBUTION
            wanted_bos = BosDirection.BEARISH
            wanted_choch = ChochDirection.BEARISH
        else:
            continue

        confirming_break = _confirming_break(sweep, bos_events, choch_events, wanted_bos, wanted_choch)
        if confirming_break is None:
            continue

        events.append(WyckoffEvent(
            type=event_type,
            phase=phase,
            index=confirming_break.index,
            timestamp=confirming_break.timestamp,
            sweep=sweep,
            confirming_break_index=confirming_break.index,
            volume_confirmed=_volume_confirms(candles, sweep.index, confirming_break.index),
        ))

    return events
