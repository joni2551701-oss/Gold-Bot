# Price Stream — GoldBot v1.1 Phase 1 (Module 4)

**Status:** implemented (`data/stream/`, PR #8), built to the frozen
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
| **Provider Interface** | `data/stream/provider.py` `PriceProvider` (DD-048) |
| **Connection Manager** | `data/stream/price_stream.py` `PriceStream` |
| **Lifecycle State Machine** | INITIALIZING→CONNECTING→STREAMING→{WAITING\|RECONNECTING}→SHUTDOWN (DD-046) |
| **Waiting Mode** | market-closed idle, no polling, auto-resume; crypto-exempt (DD-047) |
| **Reconnect Strategy** | capped exponential backoff; exhaustion → shutdown |
| **Health Monitoring** | `PriceStream.health()` / stats |
| **Provider Capability** | `ProviderCapabilities` (DD-049) — stream reads, never guesses |
| **Stream Event** | `data/stream/stream_event.py` `StreamEvent` (frozen) |
| **Event Ordering** | strict per-asset timestamp order; older dropped + flagged (DD-052) |
| **Current Price Update** | latest price folds into the forming candle via CandleBuilder |
| **CandleBuilder Integration** | stream forwards events to the module-3 sink (single-writer) |
| **Multi Asset** | `data/stream/stream_manager.py` `StreamManager` (DD-030) |
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

## Boundaries
- Reads from a provider; **writes memory only via the CandleBuilder** (never directly).
- Vendor-agnostic (DD-048): swapping a provider changes nothing above the interface.
- Clock-injected (`tick(now)`) — deterministic, replay-safe.
- Not wired into `core/pipeline.py`.

## References
- `data/stream/` — the implementation.
- `docs/architecture/MARKET_DATA_FOUNDATION.md` — the canonical architecture.
- `docs/architecture/LIVE_PRICE.md` — the presentation layer that consumes Memory.
- `docs/governance/director/DD-046.md`…`DD-052.md` — the amendments (recorded on their module PRs).
