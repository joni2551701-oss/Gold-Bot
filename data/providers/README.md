# data/providers/

## Purpose
Phase 59.1 foundation (Market Data Provider Abstraction &
TwelveData Integration Foundation). GoldBot needs to run without an
always-on MT5 terminal (owner has no PC available today) — this
package is the abstraction that lets TwelveData be the live provider
now while making a future MT5 provider a drop-in addition, not a
rewrite. See `docs/MARKET_PROVIDER.md` for the full architecture.

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
raises), and the abstract `MarketDataProvider` (`get_candles()`,
`get_latest_price()`, `get_market_status()`).

### `twelve_data_provider.py`
`TwelveDataProvider` — wraps the existing, completely untouched
`data.twelve_data_client.TwelveDataClient`. No retry/backoff/symbol-
formatting logic is reimplemented; `TwelveDataClient` was **not**
moved into this package (see the module's own docstring for why —
moving it was conditional in this task's brief and was judged
unnecessary and risky for a live, tested, imported-elsewhere file).
`SUPPORTED_SYMBOLS` documents the five symbols this task's brief names
(`XAUUSD`/`EURUSD`/`GBPUSD`/`BTCUSD`/`ETHUSD`) — not a hard whitelist;
`_format_symbol()`'s existing generic 6-character split already
handles all five without new logic.

### `mt5_provider.py`
`MT5Provider` — a deliberate, inert stub. `get_market_status()` always
returns `available=False` and never raises (this is how a caller
detects "MT5 is absent" safely). `get_candles()`/`get_latest_price()`
raise `NotImplementedError` if called directly, rather than returning
a silently-empty/wrong result.

### `__init__.py`
`get_provider(name=None)` — a factory reading `config.Config.MARKET_DATA_PROVIDER`
(default `"twelvedata"`) when `name` is omitted. Raises `ValueError`
for an unknown provider, or for `"mt5"` without `ENABLE_MT5=True` —
never silently substitutes a different provider than the one
requested.

## What this package does NOT do
- Does not change `data/market_data.py`, `data/twelve_data_client.py`,
  or `core/pipeline.py` — the live pipeline's data path is completely
  unaffected; this is a new, parallel, unwired abstraction.
- Does not fabricate volume — every `MarketCandle.volume` is `None`
  from every provider in this phase.
- Does not generate a signal, know about a strategy, or know about a
  decision — see this file's own "Purpose" section.
- Does not implement MT5 — `mt5_provider.py` is an honest stub, not a
  partial or fake integration.

## Dependencies
`base_provider.py` imports only the standard library.
`twelve_data_provider.py` imports `data.twelve_data_client.TwelveDataClient`
(same top-level package) and `data.api_error_classifier` (AC-07/TASK
5). `mt5_provider.py` imports only `base_provider` (same package) — no
MetaTrader5 package dependency. `__init__.py` imports `config.Config`.
None of the four imports `context/`, `strategies/`, `signals/`, `ai/`,
`decision/`, `risk/`, `execution/`, `database/`, or `telegram/`. Not
imported by `core/pipeline.py`, `data/market_data.py`, or any other
existing module in this phase.

## Future Roadmap
A real MT5 implementation (a genuine, separately-approved future
phase — CLAUDE.md's Trading Safety rules require explicit approval
before wiring `execution/`, and a live MT5 connection is a prerequisite
for that), `core/pipeline.py` wiring to actually call `get_provider()`
instead of constructing `MarketDataNormalizer` directly, and the Owner
Mode `/provider` Telegram command (contract only, see
`docs/MARKET_PROVIDER.md`'s "Owner Mode" section) all remain
unimplemented.
