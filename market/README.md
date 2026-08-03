# market/

> **CANONICAL PROJECTION — Application-Services tier (Owner ruling,
> TASK-ARCH-101 PART-03, L1 migration EXECUTED).** `market/` is the
> single Canonical Market Projection: an upper-layer read-only projection
> that consumes exactly two canonical inputs — `data_layer.market_memory.MemoryReader`
> (Data Layer market data) and `context.snapshot.ContextSnapshotSchema`
> (GoldBot Core context) — and nothing else. Its coupling to the
> now-DEPRECATED `stream/` is completely removed (zero `stream` imports).
> Not a Data Layer member, not Core; dependency flows strictly downward.
> The projection snapshot is `MarketStateSnapshot` (with a `MarketSnapshot`
> compat alias); the canonical `MarketSnapshot` class is
> `data_layer.live_data.market_data.MarketSnapshot`. See
> `docs/governance/collaboration/TASK-ARCH-101.md` PART-03.

## Purpose
`market/` (TASK-CORE-005) is GoldBot's **read-only market Facade
Layer** (Director decision). It gives every future consumer — chart/,
ai/, platform/, telegram/, monitoring/ — one place to read the current
market view, without each of them reaching into `stream/` or `context/`
themselves.

```
config.py
   ↓
data_layer/providers/     (FROZEN)
   ↓
stream/             (real-time flow, current price)
   ↓
[ context/ computes structure/BOS/CHoCH/liquidity/OB/FVG/regime/session ]
   ↓
market/             (this facade — READ-ONLY projection)
   ↓
consumers: context-users · strategies · signals · telegram · monitoring · future chart/AI
```

## Critical rule — no structure math here
`market/` does **not** implement any market-structure calculation. All
the real detection (swing points, HH/HL/LH/LL, BOS, CHoCH, order
blocks, FVGs, liquidity, regime, session) already lives in `context/`
(`market_structure.py`, `bos.py`, `choch.py`, `order_block.py`,
`fvg.py`, `liquidity.py`, `market_regime.py`, `session.py`, …), is
**FROZEN** for this task, and is **untouched**. Every state in `market/`
is a **projection** of the already-built
`context.snapshot.ContextSnapshotSchema` (produced by
`context.snapshot.from_context_snapshot`) plus `stream/`'s current
price. Duplicate logic is strictly forbidden.

## Public-contract binding (Director constraint)
`market/` binds to context/'s **public contract only** — the
documented, JSON-serializable `context.snapshot.ContextSnapshotSchema`
(see `docs/CONTEXT_SNAPSHOT.md`). It never touches context/'s internal
implementation (`context.context_orchestrator.ContextSnapshot` or any
detector module). Each state module reads the contract's public fields
by attribute (`structure.trend`, `zones.order_block`,
`liquidity.liquidity_type`, `session.current_session`, `regime`, …), so
the façade depends on the contract's *shape*, not on how context/
computes it. `tests/market/test_market_public_contract.py` proves the
façade consumes a genuine `ContextSnapshotSchema`; the other suites use
fakes to prove the façade reaches into no context internal. That public
contract already exists, so no change to `context/` was required.

## Input → the facade reads, never computes
`MarketManager.build_market_data(context_schema, …)` takes:
- a `context.snapshot.ContextSnapshotSchema` (already computed by `context/`), and
- the latest price (a `MarketPrice`, or read from a
  `stream.current_price.CurrentPrice` by symbol), plus optional recent candles.

## Modules
- **`market_manager.py`** — `MarketManager` (the facade entry point) +
  `MarketState` (latest data + snapshot). `build_market_data()` /
  `build_snapshot()` / `update()` / `current()` / `current_snapshot()`.
- **`market_data.py`** — `MarketData` (the aggregated container) +
  `MarketSnapshot` (immutable serializable point-in-time summary).
- **`market_structure.py`** — `MarketStructureView`: projects context
  structure + zones (trend/bos/choch/swing_state/order_block/fvg). A
  projection, **not** a detector.
- **`trend_state.py`** — `TrendState` (bullish/bearish/neutral/mixed/
  unknown) from context structure trend.
- **`liquidity_state.py`** — `LiquidityState` from context liquidity.
- **`session_state.py`** — `SessionState` from context session +
  `stream.stream_mode.is_weekend` (agrees with the stream weekend clock).
- **`volatility_state.py`** — `VolatilityLevel` projected from context's
  regime (context has no separate volatility label; HIGH/LOW_VOLATILITY
  live inside the regime enum). No new volatility math.
- **`regime_state.py`** — `RegimeState` from context regime. Advisory
  context, **not** a strategy choice.
- **`candle.py`** — `Candle` read model + adapters from a
  `stream.StreamEvent` / frozen `data_layer.providers.MarketCandle`.
- **`ticker.py`** — `Ticker` fast price/ticker read.
- **`orderbook.py`** — `OrderBook` normalisation target (optional; no
  provider supplies depth yet).
- **`current_price.py`** — `MarketPrice` + `read_current_price()` that
  reads from an existing `stream.CurrentPrice` (reuse, not a re-implementation).

## Standard output
`MarketData` / `MarketSnapshot` carry: current price, candle state,
structure state, trend, liquidity, session, volatility, regime. Missing
data → `None` / default (`UNKNOWN`) / empty — never a random shape.

## Security
No `.env` read (only `config.py` reads `.env`). No API key or secret is
read, logged, or held — `market/` deals in prices and already-computed
context views, not credentials.

## Status
Foundation only — not wired into `core/pipeline.py`. `context/` remains
the live structure engine feeding the trading pipeline; `market/` is the
read facade the next layers (chart/AI/platform) build on.
