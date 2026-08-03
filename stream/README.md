# stream/

> **DEPRECATED — Owner decision, TASK-ARCH-101 PART-03.** The canonical
> live-stream layer is `data_layer/live_data/`; every capability here now has a
> canonical equivalent (validator → `data_layer/live_data/stream_validator.py`,
> Forex clock → `data_layer/live_data/market_calendar.py`, everything else →
> `data_layer/live_data/` + `data_layer/event_system/` + `data_layer/live_data/current_price_provider.py`).
> Build no new code on this package. **NOT deleted, no code removed, no
> feature lost** — its tests still pass. DELETE is a separate later
> Owner-authorized phase, only after `market/` (its last importer) is
> migrated off it. See `docs/governance/collaboration/TASK-ARCH-101.md`.

## Purpose
`stream/` (TASK-CORE-004) is GoldBot's real-time market **data-flow**
layer. It sits between the **FROZEN** `data_layer/providers/` layer and every
real-time consumer:

```
config.py
   ↓
data_layer/providers/     (FROZEN — provider adapters + ProviderManager)
   ↓
stream/             (this layer — real-time flow)
   ↓
consumers: Telegram · future chart · market · context · monitoring · platform
```

A stream is **data-only**. It NEVER computes a signal, strategy,
decision, risk rule, trade, Telegram/UI, or chart rendering. It only
receives data, standardises it, checks it, tracks current state, and
hands it to subscribers.

## Flow (enforced by `price_stream.py`)
```
raw MarketCandle (from a frozen provider)
   → StreamEvent            (stream_event.py — never route raw data)
   → StreamValidator        (stream_validator.py — drop invalid)
   → StreamState + CurrentPrice   (runtime state, not history)
   → StreamMode gate        (route only when ACTIVE)
   → StreamRouter → StreamSubscriber(s)
```

## Modules
- **`stream_event.py`** — `StreamEvent` (symbol, timeframe, timestamp,
  OHLC, volume, `source`, `provider`) + `from_candle()` adapter from a
  frozen `MarketCandle`. The one transport shape; raw provider output
  never reaches a consumer.
- **`stream_validator.py`** — `StreamValidator.validate()` → a
  `ValidationResult` (never raises). Checks empty / symbol / OHLC
  integrity / future timestamp / duplicate / out-of-sequence.
- **`stream_state.py`** — `StreamState`: last price/event/timestamp/
  provider/mode. Volatile runtime state, **not** history.
- **`current_price.py`** — `CurrentPrice`: the fast single-value
  latest-price read point every later layer anchors on. Current value
  only, no history, no signal.
- **`stream_mode.py`** — `StreamMode` (ACTIVE / PAUSED / WEEKEND_WAIT /
  MARKET_CLOSED / MANUAL_HOLD) + `resolve_mode()` / `is_weekend()` /
  `is_market_open()`. Forex 24×5 clock (opens Sun 22:00 UTC, closes Fri
  22:00 UTC) — a coarse default, not a holiday calendar.
- **`stream_router.py`** — `StreamRouter`: fan-out to subscribers with
  per-subscriber fault isolation (one bad consumer can't stop the
  others). Splits/dispatches only — no business logic.
- **`stream_subscriber.py`** — `StreamSubscriber` ABC (`name`,
  `on_event`) + `CallbackSubscriber`. The single contract every
  consumer connects through.
- **`price_stream.py`** — `PriceStream`: composition root.
  `ingest_event()` / `ingest_candle()` run the full flow; `poll()` is an
  optional pull from a `ProviderManager`'s active provider.

## Weekend / pause
When `resolve_mode()` returns a non-ACTIVE mode (weekend, closed,
paused, manual hold), `PriceStream` records the mode in state but does
**not** route data events — the stream waits without crashing. It
resumes automatically when the mode returns to ACTIVE.

## Chart readiness
Chart code is **not** written here. `stream/` only prepares
chart-ready data: `CurrentPrice` (live price), `StreamEvent`
(candle/live update in a history-ready shape), and the subscriber
contract a future chart module attaches to. A future `chart/` phase is
a separate module — `stream/` writes no chart logic.

## WebSocket / live-transport readiness
The `source` field on `StreamEvent` (`"provider"`/`"poll"`/`"replay"`/
future `"live"`) and the subscriber/router split are transport-neutral,
so a later WebSocket/live feed becomes a new ingest source, not a
rewrite. No websocket server or UI is written in this phase.

## Security
No `.env` is read here (only `config.py` reads `.env`). No API key or
secret is read, logged, printed, or placed in a repr — the stream layer
deals in candles/prices, not credentials.

## Status
Foundation only — nothing here is wired into `core/pipeline.py` yet,
matching the other foundation layers' zero-pipeline-wiring posture.
