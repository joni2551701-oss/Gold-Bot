# Market Data Architecture (Phase 59.2)

The consolidated, professional-grade shape of GoldBot's market data
abstraction, per the Director's own stated goal: "GoldBot uchun yagona
market data abstraksiyasini professional qilish" (make GoldBot's
market data abstraction professional-grade). This document is the
entry point; `docs/MARKET_PROVIDER.md` (Phase 59.1) covers the
provider layer's own detail, `docs/PROVIDER_CONTRACTS.md` (this phase)
covers the exact per-provider-type contract, and
`docs/TRADINGVIEW_PROVIDER.md`/`docs/OWNER_COMMANDS.md` cover their
own narrow topics.

## Pipeline

```
Provider
    |
    v
MarketDataProvider Interface
    |
    v
MarketDataNormalizer
    |
    v
Data Quality
    |
    v
Market Snapshot
    |
    v
Context Engine
```

**As implemented today**, this diagram describes two things that are
NOT yet connected to each other:

1. **The new provider layer** (`data/providers/`, Phase 59.1 + 59.2):
   `Provider` → `MarketDataProvider Interface` exists and is real,
   tested code (`TwelveDataProvider`, `MT5Provider`,
   `BinanceProvider`, `FredProvider`, `ProviderRegistry`).
2. **The live pipeline** (`data/market_data.py` → `data/data_quality.py`
   → `data/market_data_snapshot.py` → `context/`, all pre-existing or
   from Phase 59 Preparation) already implements
   `MarketDataNormalizer` → `Data Quality` → `Market Snapshot` →
   `Context Engine` exactly as drawn, and runs live today via
   `core/pipeline.py`.

**What's missing to make this one real, connected pipeline**: nothing
in `data/market_data.py` constructs or calls a `MarketDataProvider`
today — `MarketDataNormalizer` still calls
`data.twelve_data_client.TwelveDataClient` directly, exactly as it did
before Phase 59.1. Wiring `MarketDataNormalizer` to go through
`data/providers/get_provider()` (or a `ProviderRegistry`) instead of
constructing `TwelveDataClient` directly is a real, meaningful next
step — explicitly **not done in this phase**, since it touches a live,
tested file feeding the real trading pipeline, and this phase's own
boundary is "Tegilmaydi: ... AI, Telegram logic" plus (implicitly, by
the same discipline every phase since A11 has held) no live-pipeline
rewiring without separate, explicit approval.

## Provider Layer detail

```
Provider Registry (data/providers/registry.py)
        |
        +-- DataProvider (base_provider.py)
        |     |  get_provider_name(), get_market_status()
        |     |
        |     +-- MarketDataProvider          +-- FundamentalDataProvider
        |     |     get_candles()             |     get_macro_indicator()
        |     |     get_latest_price()        |     get_interest_rate()
        |     |     get_supported_timeframes()|     get_inflation_data()
        |     |                               |
        |     +-- TwelveDataProvider ✅ REAL   +-- FredProvider (stub)
        |     +-- MT5Provider (stub)
        |     +-- BinanceProvider (stub)
        |
        +-- (TradingView: no class -- see docs/TRADINGVIEW_PROVIDER.md, design-only, ToS risk)
```

Full contract detail: `docs/PROVIDER_CONTRACTS.md`.

## FRED's distinct branch

FRED does not feed the candle pipeline above at all — its own,
separate, not-yet-built branch (per this phase's TASK 4 brief):

```
FRED
 |
 v
Fundamental Context   (does not exist yet)
 |
 v
AI Analyzer            (ai/ai_analyzer.py, still a heuristic stub)
```

`FundamentalDataProvider`/`FredProvider` (this phase) are the
foundation for the first box only — `Fundamental Context` and any
`AI Analyzer` consumption remain future, separately-approved work
(named as `Phase 59.3 — Fundamental Intelligence Layer` in this
phase's own roadmap, see below).

## What this phase does NOT do

- Does not wire `data/market_data.py`'s `MarketDataNormalizer` to use
  `data/providers/` — the live pipeline's data path is unchanged (see
  "As implemented today" above).
- Does not change `context/`, `strategies/`, `signals/` (candidate
  generation), `decision/decision_engine.py`, `risk/risk_manager.py`,
  `ai/`, `execution/`, or any Telegram code.
- Does not implement a real Binance/FRED connection, or a
  TradingView `MarketDataProvider`.
- Does not implement any Owner Mode command (`docs/OWNER_COMMANDS.md`
  — contract only).

## Roadmap

```
Phase 59.1 — Market Provider Foundation (TwelveData real, MT5 stub)
        |
        v
Phase 59.2 — Market Data Intelligence Layer (this phase: provider
              contract hardening, Binance/FRED foundations, registry,
              health monitoring, TradingView design audit)
        |
        v
Phase 59.3 — Fundamental Intelligence Layer (Economic Calendar, DXY,
              Fed Events, CPI, NFP, FOMC, News Impact Score)
        |
        v
Phase 59 Validation — 7 Day Real Market Test
        |
        v
v0.4 — AI Assistant
```
