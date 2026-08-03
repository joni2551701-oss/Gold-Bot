"""
Signals — Canonical Signal router (TASK-CORE-008 / STEP-08).

Decides WHICH consumers a canonical signal is relevant to and returns that
as route metadata. It sends nothing — no Telegram call, no push, no HTTP.
A consumer (decision/, telegram/, a platform app, monitoring/) reads the
route list and decides for itself whether to pull the signal; signals/ never
reaches into a platform.

Routing is a pure function of the signal's own already-set fields
(direction, decision status) — no analysis, no risk, no decision is made
here; a REJECTED signal is still *routed* to monitoring/AI for the record,
it just isn't routed to the user-facing platforms.
"""

from enum import Enum
from typing import List

from signal_layer.signal_builder.schema import SignalSchema


class SignalConsumer(str, Enum):
    """The layers/platforms that can consume a canonical signal."""
    DECISION = "DECISION"
    TELEGRAM = "TELEGRAM"
    MOBILE = "MOBILE"
    MINI_APP = "MINI_APP"
    DESKTOP = "DESKTOP"
    MONITORING = "MONITORING"
    AI = "AI"


# Consumers that always receive every signal for the record, regardless of
# direction or decision — observability/decisioning, never user delivery.
_ALWAYS = (SignalConsumer.DECISION, SignalConsumer.MONITORING, SignalConsumer.AI)

# User-facing delivery platforms — reached only for an actionable
# (BUY/SELL) signal that has not been REJECTED.
_USER_FACING = (
    SignalConsumer.TELEGRAM,
    SignalConsumer.MOBILE,
    SignalConsumer.MINI_APP,
    SignalConsumer.DESKTOP,
)


def route(signal: SignalSchema) -> List[SignalConsumer]:
    """
    Return the consumers this signal should be offered to. Pure metadata —
    dispatches nothing. DECISION/MONITORING/AI always included; the
    user-facing platforms are included only for a BUY/SELL that is not
    REJECTED.
    """
    consumers: List[SignalConsumer] = list(_ALWAYS)
    actionable = signal.direction in ("BUY", "SELL")
    not_rejected = signal.decision != "REJECTED"
    if actionable and not_rejected:
        consumers.extend(_USER_FACING)
    return consumers


def route_values(signal: SignalSchema) -> List[str]:
    """route() as plain strings, for serialization."""
    return [c.value for c in route(signal)]
