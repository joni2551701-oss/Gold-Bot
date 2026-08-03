# data_layer/providers/

## Purpose
Phase 59.1 foundation (Market Data Provider Abstraction &
TwelveData Integration Foundation), hardened in Phase 59.2 (Market
Data Intelligence Layer) before more providers are added. GoldBot
needs to run without an always-on MT5 terminal (owner has no PC
available today) — this package is the abstraction that lets
TwelveData be the live provider now while making a future MT5/
Binance/FRED provider a drop-in addition, not a rewrite. See
`docs/MARKET_DATA_ARCHITECTURE.md` and `docs/PROVIDER_CONTRACTS.md`
for the full architecture and per-provider contract.

A provider is data-only:

    A provider NEVER generates a signal.
    A provider NEVER knows about a strategy.
    A provider NEVER knows about a decision.
    A provider only returns data.

## Modules

### `base_provider.py`
`MarketCandle` (`symbol`, `timeframe`, `open`, `high`, `low`, `close`,
`timestamp`, `volume` — always `None`, never fabricated),
`ProviderStatus` (`available`, `reason` — always safe to call, never
raises), the abstract `DataProvider` (`get_provider_name()`,
`get_market_status()` — Phase 59.2's universal root), and
`MarketDataProvider(DataProvider)` (`get_candles()`,
`get_latest_price()`, `get_supported_timeframes()` — Phase 59.2 added
the latter; `get_symbol_info()` was audited and deliberately not
added, see `docs/PROVIDER_CONTRACTS.md`).

### `fundamental_base.py` (Phase 59.2)
`FundamentalDataPoint`, `FundamentalSnapshot`, and the abstract
`FundamentalDataProvider(DataProvider)` (`get_macro_indicator()`,
`get_interest_rate()`, `get_inflation_data()`) — a separate hierarchy
from `MarketDataProvider`, since macro/economic data isn't
candle-shaped. See the module's own docstring for the full rationale.

### `twelve_data_provider.py`
`TwelveDataProvider` — wraps the existing, completely untouched
`data_layer.providers.twelve_data_client.TwelveDataClient`. No retry/backoff/symbol-
formatting logic is reimplemented; `TwelveDataClient` was **not**
moved into this package (see the module's own docstring for why —
moving it was conditional in this task's brief and was judged
unnecessary and risky for a live, tested, imported-elsewhere file).
`SUPPORTED_SYMBOLS` documents the five symbols this task's brief names
(`XAUUSD`/`EURUSD`/`GBPUSD`/`BTCUSD`/`ETHUSD`) — not a hard whitelist;
`_format_symbol()`'s existing generic 6-character split already
handles all five without new logic. `get_supported_timeframes()`
relays `TwelveDataClient.INTERVAL_MAP`'s own live keys.

### `mt5_provider.py`
`MT5Provider` — a deliberate, inert stub. `get_market_status()` always
returns `available=False` and never raises (this is how a caller
detects "MT5 is absent" safely). `get_candles()`/`get_latest_price()`
raise `NotImplementedError` if called directly, rather than returning
a silently-empty/wrong result. `get_supported_timeframes()` always
returns `()`.

### `binance_provider.py` (Phase 59.2, TASK 3)
`BinanceProvider` — a deliberate, inert stub, v0.9 Multi Asset
foundation only. `SUPPORTED_SYMBOLS = ("BTCUSDT", "ETHUSDT")` —
Binance's own format, deliberately different from TwelveData's. Unlike
`MT5Provider`, validates the requested symbol first (`ValueError` for
an unsupported one) before raising `NotImplementedError` for a
supported-but-unimplemented one — a genuine, testable distinction.

### `fred_provider.py` (Phase 59.2, TASK 4; extended Phase 60.5, TASK 3)
`FredProvider` — a deliberate, inert stub for Gold's macro drivers
(interest rates, inflation, dollar index). Verified real FRED series
IDs (`FEDFUNDS`, `CPIAUCSL`, `DTWEXBGS` — the closest free public
proxy for "DXY", not identical to it, disclosed in the module's own
docstring), no live `api.stlouisfed.org` connection. Phase 60.5 added
`collect_snapshot()` — composes the three fetch methods into one
`FundamentalSnapshot`, catching each `NotImplementedError`
individually so it returns a real (today, all-empty) snapshot rather
than raising. See `docs/FUNDAMENTAL_INTELLIGENCE.md`.

### `registry.py` (Phase 59.2, TASK 5)
`ProviderRegistry` (`register()`/`get()`/`available()`/`all_names()`)
and `build_default_registry()` (registers all four
real/stub providers above — not TradingView, no class exists). A
broader catalog than `__init__.py`'s `get_provider()` — see
`registry.py`'s own docstring for the exact relationship (not a
replacement).

### `__init__.py`
`get_provider(name=None)` — a factory reading `config.Config.MARKET_DATA_PROVIDER`
(default `"twelvedata"`) when `name` is omitted. Raises `ValueError`
for an unknown provider, or for `"mt5"` without `ENABLE_MT5=True` —
never silently substitutes a different provider than the one
requested. Deliberately does not include `"binance"`/`"fred"` in its
selectable set — both always raise `NotImplementedError` for every
real call, so making either the one "active" `MarketDataProvider`
would be actively harmful, not just incomplete.

## What this package does NOT do
- Does not change `data_layer/live_data/market_data.py`, `data_layer/providers/twelve_data_client.py`,
  or `core/pipeline.py` — the live pipeline's data path is completely
  unaffected; this is a new, parallel, unwired abstraction.
- Does not fabricate volume — every `MarketCandle.volume` is `None`
  from every provider in this phase.
- Does not generate a signal, know about a strategy, or know about a
  decision — see this file's own "Purpose" section.
- Does not implement MT5, Binance, or FRED — each stub is honest, not
  a partial or fake integration.
- Does not include a TradingView provider — `docs/TRADINGVIEW_PROVIDER.md`
  concluded a `MarketDataProvider` implementation would violate
  TradingView's own Terms of Service for a commercial/automated
  product; no code was written.

## Dependencies
`base_provider.py`/`fundamental_base.py` import only the standard
library (`fundamental_base.py` additionally imports `DataProvider`
from `base_provider.py`, same package).
`twelve_data_provider.py` imports `data_layer.providers.twelve_data_client.TwelveDataClient`
(same top-level package) and `data_layer.providers.api_error_classifier` (AC-07/Phase
59.1 TASK 5). `mt5_provider.py`/`binance_provider.py`/`fred_provider.py`
import only `base_provider.py`/`fundamental_base.py` (same package) —
no `MetaTrader5`/exchange/FRED API package dependency of any kind.
`registry.py` imports the four concrete provider classes (same
package). `__init__.py` imports `config.Config` plus every module in
this package. None imports `context/`, `strategies/`, `signals/`,
`ai/`, `decision/`, `risk/`, `execution/`, `database/`, or `telegram/`.
Not imported by `core/pipeline.py`, `data_layer/live_data/market_data.py`, or any
other existing module in this phase. `core_layer/health_monitor/provider_health.py`
(Phase 59.2) imports this package — a new, one-directional dependency,
never reversed.

## Future Roadmap
A real MT5/Binance/FRED implementation (each a genuine,
separately-approved future phase — CLAUDE.md's Trading Safety rules
require explicit approval before wiring `execution/`, and a live MT5
connection is a prerequisite for that), `core/pipeline.py`/
`data_layer/live_data/market_data.py` wiring to actually call `get_provider()`/
`ProviderRegistry` instead of constructing `TwelveDataClient` directly
(see `docs/MARKET_DATA_ARCHITECTURE.md`'s "As implemented today"
section), a `Fundamental Context` consumer for `FundamentalDataProvider`
output (named `Phase 59.3 — Fundamental Intelligence Layer` in the
roadmap), and the Owner Mode commands (contract only, see
`docs/OWNER_COMMANDS.md`) all remain unimplemented.
