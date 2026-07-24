# assets/

## Purpose
Asset Intelligence foundation (Phase A12) — a standard metadata layer
for tradable assets (`AssetDefinition`, `AssetType`, `AssetRegistry`),
entirely separate from market data fetching, strategy execution, risk
sizing, and order execution. GoldBot trades exactly one asset today
(XAUUSD/Gold); this module exists so a future Forex/Crypto/Index/
Stock expansion, Quant Research, or an AI Assistant has one standard
place to ask "what assets exist, what type/currency are they" without
each re-deriving its own answer. See `docs/ASSET_INTELLIGENCE.md` for
the full contract.

## Usage
```python
from assets.asset_registry import build_default_registry

registry = build_default_registry()
gold = registry.get("XAUUSD")
# gold.asset_type == AssetType.GOLD
# gold.base_currency == "XAU", gold.quote_currency == "USD"

gold_assets = registry.by_type(AssetType.GOLD)  # [GOLD_ASSET]
```

## Module layout
- `asset_type.py` — `AssetType` enum (`GOLD`/`FOREX`/`CRYPTO`/
  `INDEX`/`STOCK`/`UNKNOWN`), no other value.
- `asset_model.py` — `AssetDefinition`, an immutable dataclass:
  `symbol`/`name`/`asset_type`/`market`/`base_currency`/
  `quote_currency` (required, real metadata) plus seven `None` hooks
  (`trading_session`, `volatility_class`, `news_sensitivity`,
  `fundamental_profile`, `session_profile`, `risk_profile`,
  `news_profile`) reserved for future, not-yet-implemented
  intelligence.
- `asset_registry.py` — `AssetRegistry` (`register()`/`get()`/
  `list()`/`by_type()`), `DuplicateAssetSymbolError`, and
  `build_default_registry()`, which registers the one real,
  currently-traded asset (`GOLD_ASSET`).
- `profiles/gold.py` — `GOLD_ASSET`, the only real profile that
  exists today. `profiles/` has no `forex.py`/`crypto.py`/etc. yet —
  those are reserved `AssetType` values, not implemented profiles.

## What this does NOT do
- Does not fetch market data, call a Forex/Crypto API, or add a new
  data provider.
- Does not generate a signal and is not read by `strategies/`,
  `signals/`, `ai/`, or `decision/decision_engine.py`.
- Does not size a position — `risk/risk_manager.py` is untouched and
  does not read `AssetDefinition.risk_profile` (a `None` hook, not a
  wired-in value).
- Does not execute an order — `execution/` is untouched.
- Does not write to the database — no schema change, no new table.
- Does not fabricate `trading_session`/`volatility_class`/
  `news_sensitivity`/`fundamental_profile`/`session_profile`/
  `risk_profile`/`news_profile` — all seven are always `None` in this
  phase.

## Dependencies
`assets/` imports nothing outside itself — no dependency on `data/`,
`context/`, `strategies/`, `signals/`, `ai/`, `decision/`, `risk/`,
`execution/`, `database/`, or `telegram/`. `asset_registry.py`
imports `assets.profiles.gold` (same package) for
`build_default_registry()`.

## Future extension
See `docs/ASSET_INTELLIGENCE.md`'s "Future" section — Gold's FED/CPI/
NFP sensitivity, Forex's interest-rate/currency-strength profile,
Crypto's funding-rate/on-chain profile, a Strategy↔Asset compatibility
check against `strategies/lifecycle/`'s `StrategyRegistry`
(documentation-only relationship in this phase, not wired), and
pipeline integration (metadata only, never a signal/decision/risk/
execution behavior change) are all named, explicit future steps, none
implemented in this phase.
