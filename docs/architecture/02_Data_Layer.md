# GoldBot Ecosystem Architecture — Data Layer

Part of the Senior Trading AI Ecosystem architecture set. Governed by
`docs/constitution/CONSTITUTION.md` (supreme) and scoped under
`01_Ecosystem_Architecture.md` (the ecosystem's high-level map — see
its "Division of authority" section). This file is the Data Layer
detail split out of that document's own former Section (TASK-GOV-004,
Owner-directed restructure, Option A: ecosystem-level summary, not a
duplicate of the Trading-Core/AI/Telegram mechanical detail already
owned by `ARCHITECTURE_MASTER.md`/`LAYER_CONTRACT.md`/
`MODULE_DEPENDENCIES.md`/`DATA_FLOW.md` where this layer overlaps them
— this file cross-references those, it does not restate them).

## Data Layer boundary (Owner ruling, TASK-ARCH-101)

**The Data Layer works ONLY with raw market data. It does not know
about Context, Strategy, or Decision objects.** It fetches, validates,
normalizes, streams, caches, and stores raw prices/candles — nothing
above that. It never imports from `context/`, `strategies/`,
`decision/`, `signals/`, or `risk/` (verified in code: zero such
imports), and nothing above it is a Data Layer member merely because it
reads market data.

In particular, **Market Projection is NOT a Data Layer component.** A
projection that reads `context/`'s `ContextSnapshotSchema` (market
structure) to build trend/liquidity/session/volatility/regime views is
an **upper-layer** component that CONSUMES Data Layer output (raw price)
and GoldBot Core output (context structure) — it belongs to the
Application Services / market-view tier (`04_Application_Services.md`),
not here. Folding such a projection into `data/` would force the Data
Layer to depend on Context, violating this boundary. (Historical note:
TASK-ARCH-100 briefly mis-classified `market/` as a "Data Layer legacy
duplicate"; the Owner corrected this in TASK-ARCH-101 Part 3 — `market/`
is an upper-layer component and is not migrated into `data/`.)

Full module-by-module detail already exists and is not restated here:
`data/README.md`, `docs/architecture/MARKET_DATA_FOUNDATION.md`,
`docs/architecture/PRICE_STREAM.md`, `docs/architecture/LIVE_PRICE.md`.
Ecosystem-level summary (What/Reads/Writes/Wired-or-foundation), from
this task's own audit:

| Module | Role | Wired into live pipeline? |
|---|---|---|
| `data/market_data.py` (`MarketDataNormalizer`) | Fetch/validate/dedupe TwelveData candles | **Yes** — the pipeline's real data source |
| `data/data_quality.py` | Scores fetched candles, observational only | **Yes** |
| `data/market_data_service.py` (`MarketDataService`, TASK-DATA-001/004) | Facade unifying candles/snapshot/history; optional MarketMemory hydrate | **Yes**, but pipeline constructs it bare (no memory registry) — memory-write path dormant |
| `data/stream/price_stream_service.py` (`PriceStreamService`, TASK-DATA-001/004) | Unified live-tick API + optional MarketMemory write via `CandleBuilder` | **No** — not imported by `core/` at all; foundation only |
| `data/memory/` (`MarketMemory`, MA-001; `MemoryReader`, MA-002) | The Single Source of Truth for candle data | Exists, Director-accepted, **not yet the pipeline's read path** |
| `data/candle_builder.py` | Single writer aggregating ticks into `MarketMemory` OHLC | Foundation only — no production driver ticks it |
| `data/events/event_bus.py` | Central pub/sub (`PRICE.UPDATED`, `MARKET.*`, `STREAM.*`, ...) | Foundation only — never constructed in `core/pipeline.py` |
| `data/providers/` | Per-vendor `MarketDataProvider` adapters (TwelveData real; MT5/Binance/Bitget/FRED stubs) | TwelveData used indirectly by historical collection, not by the live cycle |
| `data/persistence/`, `data/snapshots/`, `data/replay/`, `data/bootstrap/` | Durable storage, snapshot lifecycle, replay, historical bootstrap | All foundation only |
| `data/current_price_provider.py` | Phase-1/3 current-price read facade (now backed by `PriceStreamService`) | Used outside the pipeline (Telegram-facing), not by `core/pipeline.py` |

**Who writes, who reads (Golden Rule 6):** Providers (`data/providers/`,
`data/twelve_data_client.py`) are the only writers of raw external
data; every layer above only reads (`MarketDataNormalizer`,
`MarketMemory`, `MemoryReader`) — verified true today, no counter-
example found in this audit.

