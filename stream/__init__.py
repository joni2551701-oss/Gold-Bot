"""
Stream Layer — real-time market data flow (TASK-CORE-004).

═══════════════════════════════════════════════════════════════════════
LEGACY (NON-CANONICAL) — TASK-ARCH-100, Owner decisions 1 & 2.

The Owner has designated `data/` as the canonical Data Layer and
`data/stream/` as the canonical live-stream implementation. This
`stream/` package is therefore NON-CANONICAL: no new consumer should be
built on it, and future live-stream development happens in
`data/stream/`, not here.

It is NOT deleted and NOT yet marked DEPRECATED. Per the Owner's staging
rule, a legacy package moves to DEPRECATED only after its unique
capabilities are fully migrated into the canonical layer AND the Owner
approves. This package's own tests (`tests/stream/`) still pass; its
behavior is unchanged. Migration status, the feature-preservation
matrix, and the per-module canonical mapping are tracked in
`docs/governance/collaboration/TASK-ARCH-100.md`.
═══════════════════════════════════════════════════════════════════════

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
