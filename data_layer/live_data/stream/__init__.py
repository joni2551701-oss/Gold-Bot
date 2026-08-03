"""
Stream Layer — real-time market data flow (TASK-CORE-004).

═══════════════════════════════════════════════════════════════════════
DEPRECATED — Owner decision, TASK-ARCH-101 PART-03.

The canonical live-stream layer is `data_layer/live_data/`. Every capability this
`stream/` package provided now has a canonical equivalent, so the Owner
has flipped `stream/` to DEPRECATED:
  - `data_layer/live_data/stream/price_stream.py`/`stream_event.py`/`stream_state.py`/
    `stream_router.py`/`stream_subscriber.py` -> `data_layer/live_data/`
    (`PriceStream`/`StreamManager`/`PriceStreamService`) + `data_layer/event_system/`
    `EventBus` (fan-out).
  - `data_layer/live_data/stream/current_price.py` -> `data_layer/live_data/current_price_provider.py`.
  - `data_layer/live_data/stream/stream_validator.py` -> `data_layer/live_data/stream_validator.py`
    (TASK-ARCH-101 Part 1; OHLC-candle validation stays at its canonical
    layer, `data_layer/data_validation/data_quality.py`).
  - `data_layer/live_data/stream/stream_mode.py` (Forex 24x5 clock) ->
    `data_layer/live_data/market_calendar.py` `ForexMarketCalendar` +
    `is_weekend()`/`is_market_open()` (TASK-ARCH-101 Part 2).

DEPRECATED here means: build NO new code on this package; use the
canonical equivalents above. Per the Owner's explicit rule, this
package is **NOT deleted, no code is removed, and no feature is lost** —
its tests (`tests/stream/`) still pass and its behavior is unchanged.

Migration complete (TASK-ARCH-101 PART-03): `market/` has been
re-pointed off `stream/`, so this package now has **zero non-test
importers** — nothing outside `stream/` and its own `tests/stream/`
imports it. It is therefore eligible for the later, separate,
Owner-authorized DELETE phase (not performed here). Status and mapping:
`TASK-ARCH-100.md`/`TASK-ARCH-101.md`.
═══════════════════════════════════════════════════════════════════════

stream/ sits between the FROZEN data_layer/providers/ layer and every
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

from data_layer.live_data.stream.current_price import CurrentPrice, PricePoint
from data_layer.live_data.stream.price_stream import IngestResult, PriceStream
from data_layer.live_data.stream.stream_event import StreamEvent
from data_layer.live_data.stream.stream_mode import (
    StreamMode,
    is_market_open,
    is_weekend,
    resolve_mode,
)
from data_layer.live_data.stream.stream_router import RouteResult, StreamRouter
from data_layer.live_data.stream.stream_state import StreamState
from data_layer.live_data.stream.stream_subscriber import CallbackSubscriber, StreamSubscriber
from data_layer.live_data.stream.stream_validator import StreamValidator, ValidationResult

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
