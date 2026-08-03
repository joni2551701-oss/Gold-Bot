# Asset Intelligence Foundation (Phase A12)

## Purpose

Builds a standard metadata layer for tradable assets —
`AssetDefinition`, `AssetType`, `AssetRegistry` — entirely separate
from market data fetching, strategy execution, risk sizing, and
order execution. **This is a metadata layer, not a market
integration.** No Forex data provider, no Crypto API, no multi-asset
trading, and no execution change are introduced in this phase.

This phase exists because GoldBot is architected around a single
asset (XAUUSD/Gold) today, but a future Forex/Crypto/Index/Stock
expansion, Quant Research, or an AI Assistant reasoning about "which
assets exist, what currency are they quoted in, what type are they"
would otherwise have no standard place to ask that question — the
same "everyone re-derives its own answer" problem Strategy Lifecycle
(Phase A11) solved for strategies. `AssetRegistry` is the single,
documented answer for assets.

## Asset Intelligence nima?

A registry of `AssetDefinition` records — one per tradable symbol —
carrying only real, verifiable metadata (symbol, name, type, market,
base/quote currency) plus a set of explicit, honest `None` hooks for
future intelligence (session/volatility/news characterization) that
this codebase does not yet compute for any asset. It never fetches
live data, never trades, never sizes a position, and never generates
a signal.

## Architecture

```
Asset Registry (assets/asset_registry.py)
      |
      v
Gold Profile (assets/profiles/gold.py)   -- the only real profile today
Forex Profile   -- not implemented (reserved AssetType.FOREX)
Crypto Profile  -- not implemented (reserved AssetType.CRYPTO)
Index Profile   -- not implemented (reserved AssetType.INDEX)
Stock Profile   -- not implemented (reserved AssetType.STOCK)
```

`AssetRegistry` is a plain in-memory store (`register()`/`get()`/
`list()`/`by_type()`) — not a database table, not a singleton.
`build_default_registry()` returns a fresh registry with
`GOLD_ASSET` (the one real, currently-traded asset) registered; every
call is independent, so one caller's `register()` never leaks into
another's registry.

## Pre-implementation audit

Before writing any code, `data/`, `config.py`, `execution/`, `risk/`,
`strategies/`, and `telegram/` were searched for any existing symbol/
asset/market-type/instrument constant, to reuse rather than invent:

| Found | Location | Reused as |
|---|---|---|
| `symbol="XAUUSD"` | `main.py`'s `TradingPipeline(...)` | `GOLD_ASSET.symbol` |
| `DEFAULT_SYMBOL = "XAUUSD"` | `platform_layer/telegram/signal_service.py` | confirms `"XAUUSD"` is the canonical value across the codebase |
| `_SUPPORTED_ASSETS = ["XAUUSD"]` | `strategies/lifecycle/strategy_registry.py` (Phase A11, module-private) | confirms the same value again; not imported (private, and `assets/` deliberately has no dependency on `strategies/`) |
| `_format_symbol()`'s 6-char split (`"XAUUSD"` → `"XAU/USD"`) | `data_layer/providers/twelve_data_client.py` | confirms `XAU`/`USD` is the correct base/quote split for this ticker |

No existing asset/market-type registry, `AssetType`-equivalent enum,
or per-asset metadata model was found anywhere — `execution/` and
`risk/` have zero symbol/asset/currency references at all;
`telegram/`'s only related string is a display literal
(`"🟡 GOLD SIGNAL"` in `platform_layer/telegram/signal_formatter.py`), not a market-
type constant.

## Model

```python
@dataclass(frozen=True)
class AssetDefinition:
    symbol: str
    name: str
    asset_type: AssetType
    market: str
    base_currency: str
    quote_currency: str
    trading_session: Optional[str] = None
    volatility_class: Optional[str] = None
    news_sensitivity: Optional[str] = None
    fundamental_profile: Optional[Any] = None
    session_profile: Optional[Any] = None
    risk_profile: Optional[Any] = None
    news_profile: Optional[Any] = None
```

`symbol`/`name`/`asset_type`/`market`/`base_currency`/`quote_currency`
are required, real fields — definitional facts about what the ticker
*is*, not something computed at runtime (no more "fabricated" than a
constant like `AssetType.GOLD`'s name itself). Every other field is
an explicit `None` hook — see "Future hooks" below.

### A deliberate deviation from the brief's own example

The brief's `AssetDefinition` example used
`base_currency="USD", quote_currency="USD"` for XAUUSD. Both being
`"USD"` does not match the real, standard ticker convention this
codebase's own `data_layer/providers/twelve_data_client.py` already relies on:
`_format_symbol()` splits `"XAUUSD"` into `"XAU/USD"` — base `XAU`
(one troy ounce of gold), quote `USD`. `GOLD_ASSET` therefore uses
`base_currency="XAU"`, `quote_currency="USD"` — the real,
already-encoded-in-this-codebase convention, not the illustrative
placeholder. (`supported_assets=["XAUUSD"]` not `["GOLD"]` in Phase
A11 was the same kind of correction, for the same reason: prefer the
value already real in this codebase over an illustrative label.)

## Future hooks — never fabricated

`trading_session`, `volatility_class`, `news_sensitivity`,
`fundamental_profile`, `session_profile`, `risk_profile`, and
`news_profile` are always `None` for every `DEFAULT_ASSETS` entry,
including `GOLD_ASSET`. None of these is computed anywhere in this
codebase today:

- `context_layer/session/session.py` (Phase A6) classifies a *candle's* session,
  not a per-asset "typical session" label.
- `context_layer/trend/market_regime.py` (Phase A7) classifies volatility per
  *pipeline cycle*, not a fixed per-asset volatility class.
- No news/fundamental data source exists anywhere in `data/`.

Wiring a real value into any of these seven fields is a future,
separately-approved phase — until then, they are explicit, honest
placeholders, never a synthetic estimate.

## Strategy Lifecycle relationship (documentation only)

Phase A11 added `strategies/lifecycle/`'s `StrategyRegistry`,
independent of this phase. **They are not wired together** — neither
imports the other, and no code in this phase touches
`strategies/lifecycle/`. A future phase could add a Strategy↔Asset
compatibility check:

```
Strategy
    |
    v
Asset Compatibility   -- not implemented; a future, separately-approved phase
```

e.g. checking a `StrategyDefinition.supported_assets` entry against an
`AssetRegistry.get()` result — not implemented here.

## Pipeline integration

None. `core/pipeline.py` does not construct, read, or import
`AssetRegistry`/`AssetDefinition` anywhere in this phase — Asset
Intelligence does not generate a signal, does not affect
`DecisionEngine`, and does not affect `execution/`. If a future phase
wires this in, the rule is: metadata only, never a behavior change to
signal generation, decision, risk, or execution.

## Future

- **Gold**: FED policy, CPI, NFP sensitivity — named as Gold's
  natural fundamental drivers, not implemented.
- **Forex**: interest-rate differentials, currency strength — named
  as Forex's natural fundamental drivers, not implemented (no Forex
  `AssetDefinition` is even registered yet, only the `AssetType.FOREX`
  enum value is reserved).
- **Crypto**: funding rates, on-chain metrics — named as Crypto's
  natural fundamental drivers, not implemented (no Crypto
  `AssetDefinition` is even registered yet, only the
  `AssetType.CRYPTO` enum value is reserved).

None of the above is implemented in this phase — this section exists
to document the shape a future, separately-approved phase would fill
in, not to promise a timeline.
