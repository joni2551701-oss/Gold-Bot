# data_layer / live_data / stream

**Module**

## Purpose

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

## Files

- `__init__.py` -- Stream Layer — real-time market data flow (TASK-CORE-004).
- `current_price.py` -- Stream Layer — Current Price (TASK-CORE-004).
- `price_stream.py` -- Stream Layer — Price Stream (TASK-CORE-004).
- `stream_event.py` -- Stream Layer — Stream Event model (TASK-CORE-004).
- `stream_mode.py` -- Stream Layer — Stream Mode (TASK-CORE-004).
- `stream_router.py` -- Stream Layer — Stream Router (TASK-CORE-004).
- `stream_state.py` -- Stream Layer — Stream State (TASK-CORE-004).
- `stream_subscriber.py` -- Stream Layer — Stream Subscriber (TASK-CORE-004).
- `stream_validator.py` -- Stream Layer — Stream Validator (TASK-CORE-004).

## Responsibilities

See `CONTRACTS.md` and `MODULE_MAP.md` in this directory.

## Dependencies

See `CONTRACTS.md` in this directory for cross-layer dependencies (mechanically derived from actual imports).

## Public API

- `current_price.py`: class `PricePoint`
- `current_price.py`: class `CurrentPrice`
- `price_stream.py`: class `IngestResult`
- `price_stream.py`: class `PriceStream`
- `stream_event.py`: class `StreamEvent`
- `stream_mode.py`: class `StreamMode`
- `stream_mode.py`: function `is_weekend()`
- `stream_mode.py`: function `is_market_open()`
- `stream_mode.py`: function `resolve_mode()`
- `stream_router.py`: class `RouteResult`
- `stream_router.py`: class `StreamRouter`
- `stream_state.py`: class `StreamState`
- `stream_subscriber.py`: class `StreamSubscriber`
- `stream_subscriber.py`: class `CallbackSubscriber`
- `stream_validator.py`: class `ValidationResult`
- `stream_validator.py`: class `StreamValidator`

---
*Generated 2026-08-03 by GoldBot Engineering Standard v1.0 rollout (Director Order No. 012/013). Documentation standardization only -- content mechanically derived from existing code, not authored from scratch.*
