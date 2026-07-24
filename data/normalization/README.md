# data/normalization/

## Purpose
Phase 59.3 foundation (TASK 1: Provider Normalization). Centralizes
per-provider symbol/timeframe format tables and the `MarketCandle`
provider-stamping helper — see `docs/PROVIDER_CONTRACTS.md`'s TASK 1
section for the full audit finding this closes.

**Audit finding**: `data/providers/base_provider.py`'s `MarketCandle`
already carries the caller's canonical symbol/timeframe (each
provider's own adapter sets it, e.g. `TwelveDataProvider.get_candles()`)
— there is no cross-provider candle-SHAPE mismatch to fix, since
Binance is still a full stub and never produces a real candle to
normalize. What was missing: (1) a `provider` field on `MarketCandle`
(added this phase, additive), and (2) a single, centralized place for
each provider's own symbol/timeframe wire-format table, instead of one
hardcoded inline per provider file. This package is that
centralization — no new candle type, no provider file's own logic
duplicated wholesale (each provider still owns its own real request-
building; these tables are for lookup/documentation and reuse by a
future real Binance/Bitget/etc. implementation).

## Modules

### `symbol_mapper.py`
`to_provider_symbol()`/`from_provider_symbol()`/`is_known_symbol()` —
GoldBot canonical (`"XAUUSD"`) ⟷ provider wire format (`"XAU/USD"`
TwelveData, `"BTCUSDT"` Binance). Falls back to the input unchanged
for an unmapped pair — never raises.

### `timeframe_mapper.py`
Same shape, for timeframes (`"M15"` ⟷ `"15min"` TwelveData, `"15m"`
Binance). The TwelveData table is cross-checked against the real
`TwelveDataClient.INTERVAL_MAP` in tests — must never drift.

### `candle_normalizer.py`
`stamp_provider(candle, provider_name)` — returns a copy of a
`MarketCandle` with `provider` set (frozen dataclass, `dataclasses.replace()`).
`normalize_candle_list()` — the same, batched.
`TwelveDataProvider.get_candles()` (Phase 59.1/59.2) now calls this
implicitly by setting `provider=self.get_provider_name()` directly.

## What this package does NOT do
- Does not introduce a competing candle type — `MarketCandle` remains
  the one standard shape.
- Does not change `data/twelve_data_client.py`'s own
  `_format_symbol()`/`INTERVAL_MAP`, or `data/providers/binance_provider.py`'s
  own `SUPPORTED_SYMBOLS`/`SUPPORTED_TIMEFRAMES` — each provider still
  owns its own real translation for its own real request-building;
  this package's tables are a separate, disclosed, small duplication
  for lookup/documentation, the same "small documented duplication"
  precedent Wyckoff-vs-AMD and Data Quality-vs-market_data.py already
  established.
- Does not wire into `core/pipeline.py` or `data/market_data.py`.

## Dependencies
`symbol_mapper.py`/`timeframe_mapper.py` import only the standard
library. `candle_normalizer.py` imports
`data.providers.base_provider.MarketCandle`. None imports `context/`,
`strategies/`, `signals/`, `ai/`, `decision/`, `risk/`, `execution/`,
`database/`, or `telegram/`.
