"""
Stream Layer — real-time market data flow (TASK-CORE-004).

stream/ sits between the FROZEN data/providers/ layer and every
real-time consumer (Telegram, future chart, market, context,
monitoring, platform). It receives provider output, standardises it
into StreamEvents, validates them, tracks current price + runtime
state, applies weekend/pause modes, and routes events to subscribers.

It is data-flow ONLY — no signal, strategy, decision, risk, execution,
Telegram/UI, or chart-rendering logic lives here. See stream/README.md
for the architecture and the flow diagram.

Nothing here is wired into core/pipeline.py yet — this is the
provider→stream foundation the next (chart/) phase builds on, same
zero-pipeline-wiring posture as the other foundation layers.
"""

from stream.current_price import CurrentPrice, PricePoint
from stream.price_stream import IngestResult, PriceStream
from stream.stream_event import StreamEvent
from stream.stream_mode import (
    StreamMode,
    is_market_open,
    is_weekend,
    resolve_mode,
)
from stream.stream_router import RouteResult, StreamRouter
from stream.stream_state import StreamState
from stream.stream_subscriber import CallbackSubscriber, StreamSubscriber
from stream.stream_validator import StreamValidator, ValidationResult

__all__ = [
    "StreamEvent",
    "StreamMode",
    "resolve_mode",
    "is_weekend",
    "is_market_open",
    "StreamValidator",
    "ValidationResult",
    "StreamState",
    "CurrentPrice",
    "PricePoint",
    "StreamRouter",
    "RouteResult",
    "StreamSubscriber",
    "CallbackSubscriber",
    "PriceStream",
    "IngestResult",
]
