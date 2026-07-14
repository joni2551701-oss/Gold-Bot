# Provider Contracts (Phase 59.2, TASK 1 audit + TASK 3/4 stubs)

The full per-provider-type contract, following the same
input/output/dependency/error-contract format `contracts/*.md`
(Phase A17) established for the rest of this codebase — this document
plays that role for `data/providers/`, kept as one file (not a
`contracts/*_provider_contract.md` per provider) since the Director's
own brief asked for a single `PROVIDER_CONTRACTS.md`.

## `DataProvider` (base_provider.py) — the universal root

| | |
|---|---|
| Kind | Abstract (`abc.ABC`) |
| Methods | `get_provider_name() -> str`, `get_market_status() -> ProviderStatus` |
| Error contract | Neither method may ever raise — `get_market_status()` is the one call a registry/health-monitor can always make safely, even on a provider with no real implementation. |
| Implemented by | Every provider in this package, directly or via `MarketDataProvider`/`FundamentalDataProvider`. |

**TASK 1 audit decision** on the brief's three candidate methods:

| Candidate | Decision | Why |
|---|---|---|
| `get_provider_name()` | **Added**, on `DataProvider` | Needed by `registry.py` (registration key) and `monitoring/provider_health.py` (report label). |
| `get_supported_timeframes()` | **Added**, on `MarketDataProvider` only | Needed by the same two consumers; not universal (no timeframe concept for `FundamentalDataProvider`). |
| `get_symbol_info()` | **Not added** | No concrete consumer in this phase. Revisit when a real multi-provider symbol-translation consumer exists. |

## `MarketDataProvider` (base_provider.py) — candle-shaped data

| | |
|---|---|
| Extends | `DataProvider` |
| Input | `get_candles(symbol: str, timeframe: str, limit: int)`, `get_latest_price(symbol: str)` |
| Output | `List[MarketCandle]` (chronologically ascending), `Optional[float]` |
| Error contract | `get_candles()`/`get_latest_price()` may raise for a genuine fetch failure (implementation-specific — see each provider below) or must return an honest empty/`None` result; never fabricate data. `get_supported_timeframes()` must never raise (empty tuple is the honest "not implemented" answer). |
| Implemented by | `TwelveDataProvider`, `MT5Provider`, `BinanceProvider` |

### `TwelveDataProvider` — ✅ REAL

| | |
|---|---|
| Wraps | `data.twelve_data_client.TwelveDataClient` (untouched, not moved — see the module's own docstring) |
| `get_candles()` | Delegates to `TwelveDataClient.fetch_candles()`; re-raises on failure (a thinner adapter than `data/market_data.py`'s own swallow-to-`[]` behavior) |
| `get_latest_price()` | Most recent M5 candle's close — a disclosed candle-based approximation, not a live tick; never raises |
| `get_supported_timeframes()` | `("M5","M15","H1","H4","Daily")` — `TwelveDataClient.INTERVAL_MAP`'s own live keys, not a separately maintained list |
| `get_market_status()` | `available=True` iff an API key is configured |
| Symbols | `SUPPORTED_SYMBOLS` (documentation only, not enforced): `XAUUSD`/`EURUSD`/`GBPUSD`/`BTCUSD`/`ETHUSD` |

### `MT5Provider` — stub

| | |
|---|---|
| Real connection | None — no `MetaTrader5` package dependency |
| `get_candles()`/`get_latest_price()` | Always raise `NotImplementedError` |
| `get_supported_timeframes()` | Always `()` |
| `get_market_status()` | Always `available=False`, never raises |

### `BinanceProvider` — stub (Phase 59.2, TASK 3)

| | |
|---|---|
| Real connection | None — no `python-binance`/`ccxt` dependency |
| `get_candles()`/`get_latest_price()` | Validate the symbol first (`ValueError` if not in `SUPPORTED_SYMBOLS`), then always raise `NotImplementedError` for a valid symbol |
| `get_supported_timeframes()` | `("M5","M15","H1","H4","Daily")` — documented intended future capability, not a live guarantee |
| `get_market_status()` | Always `available=False`, never raises |
| Symbols | `SUPPORTED_SYMBOLS = ("BTCUSDT", "ETHUSDT")` — Binance's own format (no separator), deliberately different from `TwelveDataProvider`'s `"BTCUSD"` |
| **Symbol validation** | The one real behavioral distinction from `MT5Provider`: `ValueError` (genuine input error) vs. `NotImplementedError` (recognized symbol, just not wired to a real API yet) are two different, testable outcomes. |

## `FundamentalDataProvider` (fundamental_base.py) — macro/economic data

| | |
|---|---|
| Extends | `DataProvider` |
| Input | `get_macro_indicator(series_id: str)`, `get_interest_rate()`, `get_inflation_data()` |
| Output | `Optional[FundamentalDataPoint]` (`series_id`, `value`, `unit`, `as_of`, `source`) |
| Error contract | Same posture as `MarketDataProvider` — an unrecognized `series_id` is a genuine input error (`ValueError`), an unavailable observation is `None`, never fabricated. |
| Implemented by | `FredProvider` |
| Why a separate hierarchy, not `MarketDataProvider` | A macro indicator has no open/high/low/close, and updates monthly/quarterly, not per-minute — forcing it into the candle shape would mean fabricating a fake candle for a number that isn't priced data at all. See `base_provider.py`'s own module docstring. |

### `FredProvider` — stub (Phase 59.2, TASK 4)

| | |
|---|---|
| Real connection | None — no `requests` call to `api.stlouisfed.org`, no API key read |
| Series IDs | Verified against fred.stlouisfed.org (not guessed) — see Sources below: `FEDFUNDS` (Effective Federal Funds Rate), `CPIAUCSL` (Consumer Price Index for All Urban Consumers), `DTWEXBGS` (Nominal Broad U.S. Dollar Index — FRED's closest public proxy for the popular "DXY" index, **not identical to it**, disclosed explicitly) |
| `get_macro_indicator()` | Validates `series_id` first (`ValueError` if not in `SUPPORTED_SERIES`), then always raises `NotImplementedError` |
| `get_interest_rate()`/`get_inflation_data()` | Always raise `NotImplementedError` (convenience wrappers with no series-validation step of their own, since the target series is fixed, not caller-supplied) |
| `get_market_status()` | Always `available=False`, never raises |

`FundamentalSnapshot` (`fundamental_base.py`) is the standard bundle
shape a future real implementation would return — `snapshot_id`,
`created_at`, `indicators: Dict[str, FundamentalDataPoint]` (keyed by
a short logical name like `"interest_rate"`, not the source's own
series ID) — not built/populated by anything in this phase.

## `data/providers/registry.py` — `ProviderRegistry`

| | |
|---|---|
| Methods | `register(provider)`, `get(name) -> Optional[DataProvider]`, `available() -> List[str]`, `all_names() -> List[str]` |
| Error contract | Never raises — `get()` on an unregistered name returns `None`; `available()` relies on every provider's own never-raising `get_market_status()`. |
| `build_default_registry()` | Registers `TwelveDataProvider`, `MT5Provider`, `BinanceProvider`, `FredProvider` — **not** TradingView (no class exists, see `docs/TRADINGVIEW_PROVIDER.md`). |
| Relationship to `get_provider()` (Phase 59.1) | Not a replacement — see `registry.py`'s own module docstring. `get_provider()` answers "the one active `MarketDataProvider`, per `Config.MARKET_DATA_PROVIDER`"; `ProviderRegistry` answers "the full catalog, every provider, every kind." |

## Dependency rules

`data/providers/base_provider.py` and `fundamental_base.py` import
only the standard library. `twelve_data_provider.py` imports
`data.twelve_data_client`/`data.api_error_classifier` (same top-level
`data/` package). `binance_provider.py`/`fred_provider.py` import only
`base_provider.py`/`fundamental_base.py` (same package) — no external
exchange/API package dependency of any kind. `registry.py` imports the
four concrete provider classes (same package). `__init__.py` imports
`config.Config` (cross-cutting) plus every module in this package.
None of `data/providers/*.py` imports `context/`, `strategies/`,
`signals/`, `ai/`, `decision/`, `risk/`, `execution/`, `database/`, or
`telegram/`. `monitoring/provider_health.py` imports
`data.providers.base_provider`/`data.providers.registry` — a new,
one-directional `monitoring/` → `data/providers/` dependency, not
reversed (no file in `data/providers/` imports `monitoring/`).

## Sources (FRED series verification)

- [Consumer Price Index for All Urban Consumers (CPIAUCSL) — FRED](https://fred.stlouisfed.org/series/CPIAUCSL)
- [Nominal Broad U.S. Dollar Index (DTWEXBGS) — FRED](https://fred.stlouisfed.org/series/DTWEXBGS)
