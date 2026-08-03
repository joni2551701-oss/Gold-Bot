# Market Provider Architecture

Phase 59.1 — Market Data Provider Abstraction & TwelveData Integration
Foundation. GoldBot needs to keep running without an always-on MT5
terminal (the owner has no PC available right now); this document
covers the abstraction layer that makes TwelveData the live provider
today while keeping a future MT5 provider a drop-in addition, not a
rewrite of the data layer.

## Director's decision

> Hozir MT5 uchun vaqt sarflash kerak emas. Eng to'g'ri yo'l —
> TwelveData → Provider Layer → Paper Validation. MT5 keyinchalik
> faqat Execution va real broker ulanishi uchun qo'shiladi. Bu
> arxitekturani buzmaydi.

Concretely, this phase adds:

- ❌ No trade opening, no broker execution, no real risk impact.
- ✅ Real market data, candle history, context analysis, signal
  generation, paper validation — all unaffected, all still running on
  TwelveData exactly as before.

## Provider Architecture

```
Market Provider Layer
        |
        |
+----------------+
|                |
TwelveData       MT5 Future
(API)            Adapter
|                |
+----------------+
        |
        v
MarketData
        |
Data Quality
        |
Context
        |
Strategy
        |
Signal
        |
Paper Validation
```

`data/providers/` (this phase) implements the top of this diagram —
`MarketDataProvider` (the abstract contract), `TwelveDataProvider`
(the real, working implementation), and `MT5Provider` (an honest
stub). **Nothing below "Market Provider Layer" in the diagram changed
in this phase** — `MarketData` (`data/market_data.py`), `Data Quality`
(`data/data_quality.py`), `Context`, `Strategy`, `Signal`, and Phase
59's Paper Validation foundation (`lifecycle/paper_trade.py`) are all
untouched, and none of them imports `data/providers/` yet. The
provider layer exists in parallel, ready for a future,
separately-approved wiring step — the same "foundation, not a
rewrite" posture every phase since A11 has used.

## A provider's contract

A provider is data-only. `data/providers/base_provider.py`'s
`MarketDataProvider` states this as a hard rule:

    A provider NEVER generates a signal.
    A provider NEVER knows about a strategy.
    A provider NEVER knows about a decision.
    A provider only returns data.

Three methods: `get_candles(symbol, timeframe, limit)` →
`List[MarketCandle]`, `get_latest_price(symbol)` → `Optional[float]`,
`get_market_status()` → `ProviderStatus` (never raises — the one
method a caller can always call safely, even for a provider with no
real implementation).

### `MarketCandle` — the standard output shape

```python
MarketCandle(
    symbol="XAUUSD",
    timeframe="M15",
    open=...,
    high=...,
    low=...,
    close=...,
    volume=None,
    timestamp=...,
)
```

`volume` is **always** `None` from every provider in this phase — no
fake or synthetic volume is ever fabricated. Twelve Data's
`time_series` endpoint doesn't return volume for pairs like XAU/USD; a
future MT5 provider with a real tick-volume source may populate this
field, but nothing in this codebase does today.

**Naming note**: `data/twelve_data_client.py` already defines `Candle`
(`timestamp`/`open`/`high`/`low`/`close` only — no symbol/timeframe/
volume), the real type the entire live pipeline (`data/market_data.py`,
`context/`, `strategies/`, ...) already uses, untouched by this phase.
`MarketCandle` is a distinct, richer shape for the new provider layer
only; `TwelveDataProvider` adapts one `Candle` into one `MarketCandle`
per candle — it does not change what `TwelveDataClient.fetch_candles()`
itself returns.

## TwelveData Implementation

`data/providers/twelve_data_provider.py`'s `TwelveDataProvider` wraps
the existing, **completely untouched** `data.twelve_data_client.TwelveDataClient`
— retry/backoff (3 attempts, exponential backoff on HTTP 429), symbol
formatting, and error raising are all reused, not reimplemented.

**Audit finding**: the Director's brief refers to "`data/twelve_data.py`"
— the real file is `data/twelve_data_client.py`. The brief also asks
"agar ko'chirish kerak bo'lsa" (if it needs to be moved) to move it
into the new provider package. It was **not moved**: `TwelveDataClient`
is imported directly by `data/market_data.py` (the live pipeline's
data source) and referenced by type in multiple existing tests —
moving/renaming it would be a non-additive refactor, against this
phase's own "No unnecessary refactor" rule, for no functional gain
(wrapping achieves the same abstraction goal without the risk).

**Supported symbols**: `XAUUSD`/`EURUSD`/`GBPUSD`/`BTCUSD`/`ETHUSD` —
`SUPPORTED_SYMBOLS` in `twelve_data_provider.py`, documentation only,
not a hard whitelist. `TwelveDataClient._format_symbol()` already
generically splits any 6-character symbol into `XXX/YYY` (e.g.
`"XAUUSD"` → `"XAU/USD"`, `"BTCUSD"` → `"BTC/USD"`) — no new
per-symbol format-adapter logic was needed; all five symbols already
worked with the existing formatter. This list does **not** mean
GoldBot now trades five assets — `assets/profiles/gold.py` (Phase A12)
still registers only `GOLD_ASSET`, and no strategy/signal code reads
any symbol but `"XAUUSD"` today.

**`get_latest_price()`**: an honest, disclosed simplification. Twelve
Data's `time_series` endpoint is candle-based, not a live tick/quote
stream, so "latest price" means the most recent M5 candle's close —
never a live bid/ask. Returns `None` (never raises) on any failure.

## MT5 Future Integration

`data/providers/mt5_provider.py`'s `MT5Provider` is a deliberate,
inert stub — no `MetaTrader5` package dependency, no terminal
connection attempt, no order/execution code (execution is
`execution/`'s job in a future, separately-approved phase — CLAUDE.md's
Trading Safety rules require explicit approval before wiring it).

`get_market_status()` always returns `ProviderStatus(available=False,
reason=...)` and never raises — this is exactly how "MT5 yo'q bo'lsa
tizim yiqilmaydi" (the system doesn't crash if MT5 is absent) is
satisfied: a caller checks `get_market_status().available` before ever
calling `get_candles()`/`get_latest_price()`. Calling those two
directly raises `NotImplementedError` — an honest "this doesn't exist
yet" signal, never a silently wrong empty result.

A real implementation would need, at minimum: the `MetaTrader5`
Python package, a running MT5 terminal, a connection/login step, a
symbol-mapping layer (MT5 broker symbol names vary), and its own
error classification (a new provider-specific case in
`data/api_error_classifier.py`, following the same pattern TASK 5
below established for TwelveData). None of this exists today.

## Data Source Configuration

`config.py` (additive — `Config.APP_ENV`/`DEBUG`'s existing
`os.getenv(...)` convention, not `configuration/feature_flags.py`,
since that module's own design rule requires every flag default
`False`, which `ENABLE_TWELVEDATA`'s already-live `True` default would
violate):

```python
MARKET_DATA_PROVIDER = os.getenv("MARKET_DATA_PROVIDER", "twelvedata")
ENABLE_MT5 = os.getenv("ENABLE_MT5", "False") == "True"
ENABLE_TWELVEDATA = os.getenv("ENABLE_TWELVEDATA", "True") == "True"
```

`data/providers/get_provider(name=None)` reads `Config.MARKET_DATA_PROVIDER`
when `name` is omitted, and raises `ValueError` (never silently
substitutes a different provider) for an unknown name, or for `"mt5"`
without `ENABLE_MT5=True`, or for `"twelvedata"` without
`ENABLE_TWELVEDATA=True`.

## Raw Market Snapshot (TASK 4)

Bridges to Phase 59 Preparation's own foundation
(`data/market_data_snapshot.py`'s `MarketDataSnapshot`) rather than
inventing a second, competing snapshot type. Two new, optional,
additive fields:

```python
MarketDataSnapshot(
    market_snapshot_id=...,
    symbol=...,
    timeframe=...,
    timestamp=...,        # last_timestamp, Phase 59 prep
    candles_reference=...,  # satisfies the brief's "candles_hash" -- same concept, existing real name kept, not renamed
    provider=...,          # NEW -- which MarketDataProvider supplied the candles
    data_quality=...,      # NEW -- an already-computed quality summary, never recomputed
    created_at=...,
)
```

Both new fields default to `None` — the one existing call site
(`capture_market_data_snapshot()`) and every existing test are
unaffected unless a caller opts in by passing the new keyword-only
arguments. See `docs/PHASE59_VALIDATION.md` for why full raw-candle
persistence (vs. this lightweight fingerprint) remains a deliberately
deferred, separately-approved future step.

## API Error Handling (TASK 5)

Extends `core_layer/errors/codes.py`'s existing registry (Phase A18) and
`data/api_error_classifier.py` (AC-07):

| Brief's label | Code | How it's detected |
|---|---|---|
| `API_TIMEOUT` | `API_001` (pre-existing — reused, not duplicated) | `requests.exceptions.Timeout` / `ConnectionError` |
| `API_LIMIT` | `API_002` (pre-existing — reused, not duplicated) | Any other exception (rate-limit `ValueError`, unrecognized type) |
| `INVALID_SYMBOL` | `API_003` (new) | A best-effort message heuristic — `"symbol"` (case-insensitive) present in the exception message. Disclosed limitation: `TwelveDataClient.fetch_candles()` collapses every non-429 API error into one generic `ValueError` (left untouched by this phase), so message content is the only signal available. |
| `EMPTY_RESPONSE` | `API_004` (new) | A precise, known condition (`classify_empty_response()`) — the provider call succeeded but returned zero candles; not inferred from an exception, since `fetch_candles()` already returns `[]` rather than raising for this case. |

`classify_api_error()`'s existing behavior (control flow unchanged,
never raises, only constructed and logged) is preserved exactly;
`classify_empty_response()` is a new, separate function for the one
condition that was never an exception to classify in the first place.

## Owner Mode (TASK 6 — contract only, not implemented)

**Not implemented in this phase.** Superseded by, and now fully
specified in, `docs/OWNER_COMMANDS.md` (Phase 59.2, TASK 7) — that
document is the single source of truth for the owner-only
`/provider`/`/providers`/`/provider_status`/`/enable_provider`/
`/disable_provider` command contract, so it is not duplicated here.

## Data Flow

```
Twelve Data API
      |
      v
TwelveDataClient (data/twelve_data_client.py, untouched)
      |
      v
TwelveDataProvider (data/providers/twelve_data_provider.py, NEW)
      |  adapts Candle -> MarketCandle (symbol/timeframe/volume=None added)
      v
   [ Not wired further in this phase ]

Meanwhile, unaffected, the live pipeline still runs exactly as before:

Twelve Data API
      |
      v
TwelveDataClient
      |
      v
MarketDataNormalizer (data/market_data.py, untouched)
      |
      v
core/pipeline.py's existing Data -> ... -> Database flow (docs/ARCHITECTURE.md)
```

## What this phase does NOT do

- Does not change `core/pipeline.py`, `data/market_data.py`,
  `data/twelve_data_client.py`, `context/`, `strategies/`, `signals/`
  (candidate generation), `decision/decision_engine.py`,
  `risk/risk_manager.py`, `ai/`, or `execution/`.
- Does not open a trade, dispatch a broker order, or change any risk
  calculation.
- Does not require a database migration.
- Does not implement MT5 — `mt5_provider.py` is an honest, disclosed
  stub.
- Does not implement the Owner Mode `/provider` command — contract
  only (see above).

## Roadmap

```
Phase 59.1
Market Provider Foundation
        |
        v
Phase 59.2
Paper Trading Validation
        |
        v
Phase 59.3
7 Day Real Market Test
        |
        v
v0.4
AI Assistant
```
