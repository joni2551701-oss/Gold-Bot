# Price Stream — GoldBot v1.1 Phase 1 (Module 4)

**Status:** implemented (`data_layer/live_data/`, PR #8), built to the frozen
Market Data Foundation architecture (DD-039) and amendments DD-046…DD-052.

**Single responsibility:** the Price Stream **collects and relays prices**
— nothing else. It ingests from a provider, runs the market lifecycle,
and forwards ordered `StreamEvent`s to the CandleBuilder (which writes
`MarketMemory`). It does **not** present data to users; that is the
**Live Price Service** (see `LIVE_PRICE.md`). It contains **no
business/signal logic** (Trading Safety).

```
Price Stream ──▶ CandleBuilder ──▶ MarketMemory
 (collect)         (aggregate)       (store)
```

## Now — v1.1 (implemented)

| Capability | Where |
|---|---|
| **Provider Interface** | `data_layer/live_data/provider.py` `PriceProvider` (DD-048) |
| **Connection Manager** | `data_layer/live_data/price_stream.py` `PriceStream` |
| **Lifecycle State Machine** | INITIALIZING→CONNECTING→STREAMING→{WAITING\|RECONNECTING}→SHUTDOWN (DD-046) |
| **Waiting Mode** | market-closed idle, no polling, auto-resume; crypto-exempt (DD-047) |
| **Reconnect Strategy** | capped exponential backoff; exhaustion → shutdown |
| **Health Monitoring** | `PriceStream.health()` / stats |
| **Provider Capability** | `ProviderCapabilities` (DD-049) — stream reads, never guesses |
| **Stream Event** | `data_layer/live_data/stream_event.py` `StreamEvent` (frozen) |
| **Event Ordering** | strict per-asset timestamp order; older dropped + flagged (DD-052) |
| **Current Price Update** | latest price folds into the forming candle via CandleBuilder |
| **CandleBuilder Integration** | stream forwards events to the module-3 sink (single-writer) |
| **Multi Asset** | `data_layer/live_data/stream_manager.py` `StreamManager` (DD-030) |
| **Multi Provider** | any `PriceProvider` adapter (`TwelveDataProvider` today) |
| **Graceful Shutdown** | flush → disconnect → health snapshot → memory preserved (DD-050) |
| **Error Recovery** | provider isolation (DD-051) → standardized state/health |

## Future (not in v1.1)

- **WebSocket** transport provider
- **REST Fallback** when a streaming provider drops
- **Failover** across providers
- **Tick Buffer** / **Tick Compression**
- **Provider Priority** ordering
- **Latency Monitor**
- **Data Quality Score** on the stream
- **Duplicate Tick Filter**
- **Outlier Detection**
- **Load Balancing** across providers

Each is a provider-side or ingestion-side enhancement; none change the
`PriceProvider` contract or anything above the stream (that is the point
of DD-048 provider abstraction).

## TASK-DATA-001 — Price Stream Service (latest-tick API)

A second, independent sink on top of the same `PriceStream`/
`StreamManager` (no changes to either): `data_layer/live_data/price_stream_service.py`'s
`PriceStreamService` registers a `_PriceTickSink` per asset that converts
each forwarded `StreamEvent` into a unified `PriceTick`
(`data_layer/live_data/price_tick.py` — symbol/price/bid/ask/volume/timestamp/
provider), stores the latest one per symbol in `data_layer/live_data/price_cache.py`'s
`PriceCache`, and publishes `EventType.PRICE_UPDATED` on the existing
`data_layer/event_system/event_bus.py` `EventBus`. This is the **one sanctioned read
API** for a live price:

```
price_stream.get_price("XAUUSD")
price_stream.get_price("BTCUSDT")
```

Sources registered by `build_default_price_stream_service()`:
`TwelveDataProvider` (XAUUSD, already existed) and
`data_layer/live_data/bitget_price_source.py`'s `BitgetPriceSource` (BTCUSDT — an
adapter over the existing, still-inert `data_layer/providers/bitget_provider.py`
stub; starts working with no interface change once that stub gets a real
exchange connection). A future Binance/CoinGecko/OANDA/Polygon source is
one more `PriceProvider` adapter registered the same way — no
architecture change (DD-048).

Not wired into `core/pipeline.py`, `telegram/`, or any consumer in this
phase — foundation only, same posture as `data_cache.py`/
`session_filter.py` before it. Consumers must go through
`PriceStreamService.get_price()`, never a provider directly (task
requirement) — mirrors `current_price_provider.py`'s existing
Telegram-facing seam.

### TASK-DATA-004 — MarketMemory write path (opt-in)

Rather than build a new "market memory" (the Owner-approved reuse
decision), `PriceStreamService` optionally writes into the **existing**,
Director-accepted `MarketMemory` (MA-001, `data_layer/market_memory/`). When a
`MarketMemoryRegistry` is passed to the service (or its factory),
`register_source()` builds one `data_layer/live_data/candle_builder.py` `CandleBuilder`
per asset over that asset's `MarketMemory`, and the sink forwards each
`StreamEvent` to it. So live ticks fold into MarketMemory through its
documented **single writer** (CandleBuilder) — not a second, parallel
write path — preserving the frozen single-writer discipline. The
`PriceCache` + `PRICE.UPDATED` path is untouched and runs alongside;
the memory write is fully fail-safe. With no registry (the default, and
what the Phase 3 `CurrentPriceProvider` path uses), no memory objects
are constructed and behavior is unchanged. `MarketDataService` gains a
symmetric opt-in write path — it `hydrate()`s the matching
`TimeframeMemory` with fetched closed candles. Passing **one shared
registry** to both factories makes MarketMemory the single source of
truth. Still foundation only: no consumer reads memory yet, and the
`TradingPipeline`'s bare `MarketDataService()` stays memory-less and
unchanged.

## Boundaries
- Reads from a provider; **writes memory only via the CandleBuilder** (never directly).
- Vendor-agnostic (DD-048): swapping a provider changes nothing above the interface.
- Clock-injected (`tick(now)`) — deterministic, replay-safe.
- Not wired into `core/pipeline.py`.

## References
- `data_layer/live_data/` — the implementation.
- `docs/architecture/MARKET_DATA_FOUNDATION.md` — the canonical architecture.
- `docs/architecture/LIVE_PRICE.md` — the presentation layer that consumes Memory.
- `docs/governance/director/DD-046.md`…`DD-052.md` — the amendments (recorded on their module PRs).
