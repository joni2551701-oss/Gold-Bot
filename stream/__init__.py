"""
Stream Layer — real-time market data flow (TASK-CORE-004).

═══════════════════════════════════════════════════════════════════════
DEPRECATED — Owner decision, TASK-ARCH-101 PART-03.

The canonical live-stream layer is `data/stream/`. Every capability this
`stream/` package provided now has a canonical equivalent, so the Owner
has flipped `stream/` to DEPRECATED:
  - `stream/price_stream.py`/`stream_event.py`/`stream_state.py`/
    `stream_router.py`/`stream_subscriber.py` -> `data/stream/`
    (`PriceStream`/`StreamManager`/`PriceStreamService`) + `data/events/`
    `EventBus` (fan-out).
  - `stream/current_price.py` -> `data/current_price_provider.py`.
  - `stream/stream_validator.py` -> `data/stream/stream_validator.py`
    (TASK-ARCH-101 Part 1; OHLC-candle validation stays at its canonical
    layer, `data/data_quality.py`).
  - `stream/stream_mode.py` (Forex 24x5 clock) ->
    `data/stream/market_calendar.py` `ForexMarketCalendar` +
    `is_weekend()`/`is_market_open()` (TASK-ARCH-101 Part 2).

DEPRECATED here means: build NO new code on this package; use the
canonical equivalents above. Per the Owner's explicit rule, this
package is **NOT deleted, no code is removed, and no feature is lost** —
its tests (`tests/stream/`) still pass and its behavior is unchanged.
Removal (DELETE) is a separate, later, Owner-authorized phase, only
after every remaining importer (today: the LEGACY `market/`) has been
migrated off it. Status and mapping: `TASK-ARCH-100.md`/`TASK-ARCH-101.md`.
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
