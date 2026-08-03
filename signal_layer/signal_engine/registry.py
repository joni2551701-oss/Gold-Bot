"""
Signals — Signal Kind registry (TASK-CORE-008 / STEP-08).

Names the *kinds* of canonical signal a consumer can receive. This is a
transport/routing vocabulary — "what is this signal telling the consumer to
show" — deliberately distinct from signals.models.SignalType (BUY/SELL/NONE),
which is the FROZEN live-pipeline strategy-output direction and is left
untouched.

SignalKind is a superset that adds lifecycle-style kinds (CLOSE/CANCEL/UPDATE)
and a WATCHLIST kind, none of which SignalType carries. A directional
SignalType maps onto a SignalKind via kind_for_direction(); the extra kinds
have no SignalType equivalent (they describe an action on an already-emitted
signal, not a fresh directional read).

No trading here — the registry only enumerates and looks up names.
"""

from enum import Enum
from typing import Dict, Optional


class SignalKind(str, Enum):
    """The canonical signal kinds a consumer platform can render."""
    BUY = "BUY"
    SELL = "SELL"
    CLOSE = "CLOSE"
    CANCEL = "CANCEL"
    UPDATE = "UPDATE"
    WATCHLIST = "WATCHLIST"


# Directional SignalType.value / SignalSchema direction -> SignalKind.
# "NONE" has no actionable kind; a caller gets None back and treats the
# signal as a non-directional watch (kind_for_direction documents this).
_DIRECTION_TO_KIND: Dict[str, SignalKind] = {
    "BUY": SignalKind.BUY,
    "SELL": SignalKind.SELL,
}


def kind_for_direction(direction: Optional[str]) -> Optional[SignalKind]:
    """
    Map a canonical direction string ("BUY"/"SELL"/"NONE"/None) to its
    SignalKind, or None when the direction is non-actionable. Pure lookup —
    never raises, never decides.
    """
    if not direction:
        return None
    return _DIRECTION_TO_KIND.get(direction.upper())


def is_registered(kind: str) -> bool:
    """True when `kind` is a known SignalKind value."""
    return kind in SignalKind._value2member_map_


def all_kinds() -> tuple:
    """Every registered SignalKind, stable order."""
    return tuple(SignalKind)
