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

1. **The new provider layer** (`data_layer/providers/`, Phase 59.1 + 59.2):
   `Provider` → `MarketDataProvider Interface` exists and is real,
   tested code (`TwelveDataProvider`, `MT5Provider`,
   `BinanceProvider`, `FredProvider`, `ProviderRegistry`).
2. **The live pipeline** (`data_layer/live_data/market_data.py` → `data_layer/data_validation/data_quality.py`
   → `data_layer/live_data/market_data_snapshot.py` → `context/`, all pre-existing or
   from Phase 59 Preparation) already implements
   `MarketDataNormalizer` → `Data Quality` → `Market Snapshot` →
   `Context Engine` exactly as drawn, and runs live today via
   `core/pipeline.py`.

**What's missing to make this one real, connected pipeline**: nothing
in `data_layer/live_data/market_data.py` constructs or calls a `MarketDataProvider`
today — `MarketDataNormalizer` still calls
`data_layer.providers.twelve_data_client.TwelveDataClient` directly, exactly as it did
before Phase 59.1. Wiring `MarketDataNormalizer` to go through
`data_layer/providers/get_provider()` (or a `ProviderRegistry`) instead of
constructing `TwelveDataClient` directly is a real, meaningful next
step — explicitly **not done in this phase**, since it touches a live,
tested file feeding the real trading pipeline, and this phase's own
boundary is "Tegilmaydi: ... AI, Telegram logic" plus (implicitly, by
the same discipline every phase since A11 has held) no live-pipeline
rewiring without separate, explicit approval.

## Provider Layer detail

```
Provider Registry (data_layer/providers/registry.py)
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

`FundamentalDataProvider`/`FredProvider` (Phase 59.2) were the
foundation for the first box only. Phase 59.3 (TASK 6) built the
second box — `context_layer/fundamental/fundamental_context.py`'s
`compute_fundamental_context()` — but `AI Analyzer` consumption
remains future, separately-approved work; `ai/ai_analyzer.py` reads
nothing from `FundamentalContextSnapshot` in this phase.

## What Phase 59.2/59.3 do NOT do

- Does not wire `data_layer/live_data/market_data.py`'s `MarketDataNormalizer` to use
  `data_layer/providers/` — the live pipeline's data path is unchanged (see
  "As implemented today" above).
- Does not change `strategies/`, `signals/` (candidate generation),
  `decision_layer/decision_engine/decision_engine.py`, `risk_layer/risk_engine/risk_manager.py`, `ai/`,
  `execution/`, `telegram/handlers.py`, `telegram/command_router.py`,
  or `telegram/commands.py`.
- Does not implement a real Binance/FRED connection, or a
  TradingView `MarketDataProvider`.
- Does not register any Owner Mode command into the live bot
  (`docs/OWNER_COMMANDS.md`/`telegram/owner/` — real functions as of
  Phase 59.3, still not wired into `telegram/commands.py`/
  `command_router.py`/`handlers.py`).

## Roadmap

```
Phase 59.1 — Market Provider Foundation (TwelveData real, MT5 stub)
        |
        v
Phase 59.2 — Market Data Intelligence Layer (provider contract
              hardening, Binance/FRED foundations, registry, health
              monitoring, TradingView design audit)
        |
        v
Phase 59.3 — Data Intelligence Foundation (provider normalization,
              raw market storage -- first real DB migration, cache
              verification, health checked_at, owner command
              foundation, Fundamental Context connected to FRED)
        |
        v
Phase 59.4 — Real Market Validation (7-30 day: Signal -> Paper Trade
              -> Analytics -> Strategy Report)
        |
        v
Phase 59 Validation — 7 Day Real Market Test
        |
        v
v0.4 — AI Assistant
```
