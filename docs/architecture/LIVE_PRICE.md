# Live Price — User-Facing Capabilities & Live Price Service

**Purpose:** describes what GoldBot presents to users about live prices,
and the **Live Price Service** layer that delivers it. This is the
*presentation* side; the *collection* side is the Price Stream
(`PRICE_STREAM.md`).

## Related — Market Data Service (candles, not ticks)

`data_layer/live_data/market_data_service.py`'s `MarketDataService` is a sibling
service, not part of this document's Price Stream/Live Price chain:
it answers `TradingPipeline`'s need for multi-candle OHLC history
(`get_candles()`/`get_snapshot()`/historical series), which a
single-latest-tick `PriceStreamService` cannot supply. The two never
depend on each other:

```
TradingPipeline        -> MarketDataService    (candles/snapshot/history)
CurrentPriceProvider,      -> PriceStreamService (single latest tick)
Telegram, Dashboard,
future UI
```

`MarketDataService` is a thin, uncached facade over the existing
`MarketDataNormalizer` in this phase (TASK-DATA-001 Phase 2) — see its
own module docstring for why, and `PRICE_STREAM.md` for the
`PriceStreamService` side of this split.

## Architecture — responsibility separation

```
Price Stream          collects prices (provider-agnostic)
      │
      ▼
MarketMemory          single in-RAM source of truth (Memory-First)
      │
      ▼
Live Price Service    presents prices to consumers (reads MemoryReader)
      ├── Telegram
      ├── Web Dashboard
      ├── Mobile App
      └── REST API
```

- **Price Stream** only *collects* prices → CandleBuilder → MarketMemory.
- **Live Price Service** only *presents* prices: it reads through
  `MemoryReader` / the snapshot + event surfaces (never calls a provider,
  never touches a vendor SDK) and serves each consumer.
- Adding a new consumer (Telegram, Web, mobile, REST) is a **new adapter
  on the Live Price Service** — the Core (stream + memory) does not
  change. This is the extensibility guarantee.

The Live Price Service is a **future layer** (its consumers arrive on the
roadmap below); this document records the architecture requirement now so
later work slots in without a Core rewrite. It will be formally recorded
as a Director Decision in the next governance batch.

## Capability roadmap

### Now — v1.1
- Gold · Forex · Crypto
- Current Price
- Bid · Ask · Spread
- Last Update
- Market Status
- Data Source

### v1.2
- Daily High · Daily Low
- Session Open
- Daily Change · Daily %
- Daily Range

### v1.3
- Trend per timeframe (M1, M5, M15, H1, H4, D1)

### v1.4
- Session · Volatility · Liquidity
- Premium/Discount
- BOS · CHoCH · FVG · Order Block

### v2.0
- AI Bias · AI Confidence · AI Probability · AI Summary

### v3.0
- Telegram · Web Dashboard · Mobile App · REST API · WebSocket Broadcast

## Principles
- **Memory-First:** the Live Price Service reads only from Memory
  (`MemoryReader` / snapshot / events), never from a provider.
- **Consumer-agnostic Core:** stream + memory never change when a
  consumer is added; only a Live Price Service adapter is added.
- **Trading Safety:** presentation carries no signal/risk/decision
  authority; higher-value fields (v1.4/v2.0) are read-outs, not trade
  actions.

## References
- `docs/architecture/PRICE_STREAM.md` — the collection side.
- `docs/architecture/MARKET_DATA_FOUNDATION.md` — the canonical
  architecture (MemoryReader §7, snapshot §8, future API server §19).
