# GoldBot Architecture Overview

System-level overview and dependency rules. For the detailed
per-module responsibility map, see `docs/code_structure.md`; for the
database-specific schema/relationship map, see
`docs/DATABASE.md`; for the Telegram-specific
service/permission map, see `docs/telegram_layer.md`. This document
is the entry point that ties them together and states the dependency
rules explicitly, which none of the earlier docs did as their primary
focus.

This document is the **detailed, implementation-accurate** technical
reference, kept current every phase. For the short, stable rule
statements built on top of it (Phase A14's Documentation Architecture
Foundation), see `docs/ARCHITECTURE_RULES.md` (module boundaries),
`docs/DECISION_PRINCIPLES.md` (decision ownership), and
`docs/SYSTEM_OVERVIEW.md` (a first-read map for a new developer or
agent). `docs/DEVELOPMENT_GUIDE.md` states the workflow for changing
this codebase; `docs/DOCUMENTATION_STANDARD.md` states the format
every module's own documentation follows.

## System Overview

GoldBot is two independent OS processes sharing one SQLite database
file (`database/goldbot.db`):

1. **Trading pipeline** (`main.py`, scheduled by
   `.github/workflows/trading_bot.yml` every 5 minutes during trading
   hours) — one run per invocation, exits when done. Fetches market
   data, analyzes it, and (if a signal clears every gate) sends one
   Telegram notification and persists the result.
2. **Telegram product layer** (`telegram/polling.py`, run as a
   long-lived process) — user registration, settings, subscriptions,
   admin panel, feedback. Reads/writes the same database, entirely
   independent of when the pipeline last ran.

They are never invoked from one another and share no in-memory state
— only the database file connects them.

## Data Flow

```
Market Data (data/)
      |
      v
Data Quality (data/data_quality.py)  -- observational only, Phase A8
      |                                  (never filters/blocks, see
      |                                  docs/DATA_QUALITY.md)
      v
HTF Bias (context/htf_bias.py)   -- Daily/H4/H1 market-context only
      |     |                       (Phase A2; never itself a trade
      |     |                       decision, see docs/HTF_BIAS.md)
      v     |
Context Engine (context/)        |  -- SMC structure detection:
      |     |                       structure, BOS/CHoCH, liquidity,
      |     |                       OB, FVG, AMD, Wyckoff (Phase A5),
      |     |                       Session (Phase A6), Market Regime
      |     |                       (Phase A7, reads htf_bias too --
      |     |                       see below) -- see below
      v     |
Strategies (strategies/)         |  -- 3 independent SMC methodologies
      |     |
      v     |
Signal Generation (signals/)     |  -- aggregates strategy output
      |     |     |
      |     |     '-- Signal Quality Score (signals/signal_quality.py)
      |     |          -- per-candidate A+/A/B/C grade (Phase A4;
      |     |          advisory only, see docs/SIGNAL_QUALITY.md;
      |     |          not consumed below in this phase)
      |     |     |
      |     |     '-- Explainability (signals/explainability.py)
      |     |          -- reasons list from Signal Quality's
      |     |          criteria_met + Wyckoff/Session/Regime
      |     |          (Phase A9; advisory only, see
      |     |          docs/EXPLAINABILITY.md)
      |     |     |
      |     |     '-- Feature Engineering (features/feature_engine.py)
      |     |          -- standardizes Context + Signal Quality's
      |     |          grade + Explainability's confidence into one
      |     |          MarketFeatures object per candidate (Phase
      |     |          A10; a normalization layer, not analysis, see
      |     |          docs/FEATURE_ENGINEERING.md; not consumed
      |     |          below in this phase)
      v     |
AI Layer (ai/)                   |  -- advisory input only (currently a stub)
      |     |
      v     v
Decision Engine (decision/)      -- weighted signal+HTF+risk+AI blend
      |                             -> APPROVE / REJECT / NO_TRADE
      |                             (Phase A3: "Decision Engine v2",
      |                             see below)
      v
Risk Manager (risk/)             -- geometry + stop-loss validation
      |
      v
Telegram Notification Filter     -- (inside core/pipeline.py)
      |                             APPROVE + risk-approved only,
      |                             highest-confidence candidate,
      |                             max 1 message per cycle
      v
Database (database/) <---------> Telegram Product Layer (telegram/)
```

HTF Bias feeds two consumers of the same computed result: it is
returned in `TradingPipeline.run()`'s result dict unconditionally
(the vertical arrow through Context/Strategies/Signal/AI above is a
diagram simplification — HTF Bias does not literally pass through
those stages, it is computed once, in parallel, right after Market
Data), and, as of Phase A3, it is also passed directly into
`DecisionEngine.evaluate()` as one of four weighted inputs.

Strategy Lifecycle (`strategies/lifecycle/`, Phase A11) is
deliberately **not** shown in the diagram above: unlike every other
Phase A module, it is not wired into `core/pipeline.py` at all in
this phase — `TradingPipeline.run()` never constructs or reads a
`StrategyRegistry`. It exists alongside the `Strategies (strategies/)`
node as a separate, standalone metadata layer over the same three
strategies, for a future consumer (Phase 59, Analytics, AI Assistant)
to query directly — see its own section below.

Asset Intelligence (`assets/`, Phase A12) is likewise **not** shown in
the diagram above, for the same reason: `core/pipeline.py` never
constructs, reads, or imports `AssetRegistry`/`AssetDefinition` in
this phase. It exists as a standalone metadata layer alongside
`Market Data (data/)` and `Strategies (strategies/)`, unconnected to
either today — see its own section below.

Configuration & Feature Flags (`configuration/`, Phase A13) is
likewise **not** shown in the diagram above: it sits *above*
`config.py` (a cross-cutting dependency every layer may already read,
same as `core/`), not inside the Data→...→Database flow, and
`core/pipeline.py` does not construct, read, or import
`Environment`/`ApplicationSettings`/`FeatureFlags` in this phase —
see its own section below.

Signal Schema (`signals/schema.py`/`signals/adapter.py`, Phase A15)
is likewise **not** shown in the diagram above: `core/pipeline.py`
does not call `from_signal_candidate()` anywhere in this phase — the
`Signal Generation (signals/)` node above still produces
`SignalCandidate`s exactly as before. `SignalSchema` exists as a
standardization layer any of `Signal Generation`'s existing consumers
(Decision, Risk, Telegram, Analytics, AI) could adopt in a future,
separately-approved phase — see its own section below.

Context Snapshot (`context/snapshot.py`, Phase A16) is likewise
**not** shown in the diagram above: `core/pipeline.py` does not call
`from_context_snapshot()` anywhere in this phase — the
`Context Engine (context/)` node above still produces the real,
internal `ContextSnapshot` exactly as before, and every existing
consumer (Strategies, Signal Quality Score, Explainability, Feature
Engineering) keeps reading it directly, unaffected.
`ContextSnapshotSchema` exists as a standardization layer for a
future AI/Analytics/Replay/Education consumer — see its own section
below.

### Decision Engine v2 (Phase A3)

`decision/decision_engine.py`'s `DecisionEngine.evaluate()` no longer
computes a flat `(signal.confidence + ai_analysis.confidence) / 2`
average (the pre-A3 formula). It now blends four weighted components,
all on the existing 0.0–1.0 confidence scale:

```
final_confidence = 0.40 * signal_score   (SignalCandidate.confidence)
                  + 0.25 * htf_score      (HTFBiasResult.bias, quality-dampened)
                  + 0.20 * risk_score     (1.0 - AIAnalysisResult.risk_score)
                  + 0.15 * ai_score       (AIAnalysisResult.confidence)
```

The AI-approval hard gate (`if not ai_analysis.approved: REJECT`,
checked before any threshold) and the `min_confidence`/
`approve_confidence` three-branch threshold logic are unchanged —
only what feeds into `final_confidence` changed. `TradeDecision` now
also exposes each component individually
(`signal_score`/`htf_score`/`risk_score`/`ai_score`/`final_score`) for
explainability. Weights (`DecisionWeights`) and the `HTFBias`→score
mapping (`HTF_BIAS_SCORE_MAP`) are named module-level constants, never
hardcoded inline in `evaluate()`. Full detail, including the exact
HTF-bias mapping table and the quality-dampening formula:
`decision/README.md`.

`risk.risk_manager.RiskResult` is **not** one of the four inputs —
Risk Manager runs *after* Decision Engine in the pipeline (see the
diagram above) and cannot supply an input to a decision that precedes
it. The "Risk" component instead reads `AIAnalysisResult.risk_score`
(already computed by the AI layer, before Decision Engine runs),
inverted so higher always means better, consistent with the other
three inputs. `risk/risk_manager.py` itself is entirely unmodified by
Phase A3.

### Signal Quality Score (Phase A4)

`signals/signal_quality.py`'s `compute_signal_quality(signal, context,
htf_bias)` grades each signal candidate's alignment with existing
context into a letter grade — a **checklist model**, not a weighted
average like Decision Engine v2's, since it answers a different
question ("how clean is this setup?" vs. "how strong is this
signal?"):

```
score = (criteria_met_count / 5) * 100
5-4 met -> A+   3 met -> A   2 met -> B   0-1 met -> C
```

The 5 criteria (`HTF_ALIGNED`, `STRUCTURE_ALIGNED`, `LIQUIDITY_SWEPT`,
`ORDER_BLOCK_ALIGNED`, `FVG_ALIGNED`) are each direction-specific
booleans reusing already-detected context — no new detection logic.
Full criteria definitions and the grading table: `docs/SIGNAL_QUALITY.md`.

**Not included in this phase**: Session and Volume, both named in the
original roadmap sketch. Session Intelligence doesn't exist yet
(a later phase); this codebase has no volume data source at all. Both
are documented, explicit future-extension points, not faked with a
placeholder score — see `docs/SIGNAL_QUALITY.md`'s "Deliberately not
included" section.

**Not consumed downstream in this phase** — `SignalQualityResult` is
returned in `run()`'s result dict (`"quality_results"`) only, the same
"compute now, connect later" posture HTF Bias had between Phase A2 and
Phase A3. `AIAnalyzer`, `DecisionEngine`, and `RiskManager` are all
unmodified by Phase A4.

One shared extraction, zero behavior change: `context/htf_bias.py`'s
per-timeframe "most recent structure direction" walk (previously
inline) was factored out to `context.market_structure.most_recent_bias()`
so both `htf_bias.py` and `signal_quality.py` use the same definition
instead of two copies of the same six lines — `context/htf_bias.py`'s
own 9 tests were re-run after the extraction and confirmed unchanged.

### Wyckoff Engine (Phase A5)

`context/wyckoff.py`'s `detect_wyckoff_events()` correlates already-
detected liquidity sweeps with the nearest subsequent same-direction
structural break into Spring (`SSL` sweep -> bullish break,
`phase=ACCUMULATION`) and Upthrust (`BSL` sweep -> bearish break,
`phase=DISTRIBUTION`) events — the "test of support/resistance"
patterns Wyckoff theory is most identified by. Unlike HTF Bias and
Signal Quality Score, this required **no `core/pipeline.py` change**:
it is a sixth `ContextEngine.build()` detector, following `amd_events`'s
exact pattern, so its output (`wyckoff_events`) is simply a new field
on `ContextSnapshot` (now 10 fields; every pre-existing field's name
and meaning is unchanged).

Deliberately does not reuse `context/amd.py`'s
`detect_amd_events()` despite the vocabulary overlap (both correlate a
sweep with a break) — `amd.py` already feeds a live, tested strategy,
and sharing code with a brand-new, unwired module was judged higher
risk than a small, independently-implemented, documented duplication
(see `docs/WYCKOFF.md`'s "Relationship to AMD" section). "Manipulation"
is not a third event type — it is each event's `sweep` field.

Includes a volume-confirmation hook (`_volume_confirms()`) that always
returns `None` — this codebase has no volume data source at all
(`data/twelve_data_client.py`'s `Candle` is OHLC-only), so the hook
never fabricates a `True`/`False` confirmation. Not consumed by any
`strategies/*.py` file in this phase.

### Session Intelligence (Phase A6)

`context/session.py`'s `classify_session(timestamp)` classifies a
candle's UTC hour into `ASIA` / `LONDON` /
`LONDON_NEW_YORK_OVERLAP` / `NEW_YORK` / `OFF_HOURS`. Like Wyckoff,
this needed no `core/pipeline.py` change — an 8th `ContextEngine.build()`
detector, so `session_events` (sparse transitions) is simply an 11th
field on `ContextSnapshot`.

Two real, data-backed statistics — not fabricated — are also exposed
as standalone functions (not `ContextSnapshot` fields, since their
`Dict[Session, ...]` shape doesn't match the event-list convention):
`compute_session_volatility()` (average `high - low` range per
session) and `compute_session_liquidity_activity()` (count of
already-detected `LiquiditySweepEvent`s per session, reused, not
re-detected). "Liquidity probability" and "setup quality" per session
were both named in the roadmap and both deliberately **not**
fabricated this phase — see `docs/SESSION_INTELLIGENCE.md`'s "What was
asked but is NOT included" section for why each needs a different,
separate future step (historical aggregation for the former; a
`SESSION_ALIGNED` criterion in `signals/signal_quality.py`, Phase A4's
already-documented extension point, for the latter — neither wired in
this phase).

Distinct from `data/session_filter.py`'s `is_trading_time()` (a
wall-clock, Tashkent-time, binary trading-hours gate for a different
purpose) — not read, called, or duplicated by this module.

### Market Regime Engine (Phase A7)

`context/market_regime.py`'s `compute_market_regime()` classifies
overall market character (`TRENDING`/`RANGE`/`ACCUMULATION`/
`DISTRIBUTION`/`HIGH_VOLATILITY`/`LOW_VOLATILITY`/`UNKNOWN`) from
already-computed structure, Wyckoff events, session volatility, and
(if available) HTF Bias — no new indicator. Priority order when
multiple signals could apply: a recent Wyckoff Spring/Upthrust first
(most specific) → confirmed HTF+structure trend → a volatility extreme
→ `RANGE` (default with data) → `UNKNOWN` (no data at all). Full
detection rule and confidence table: `docs/MARKET_REGIME.md`.

**The one field that needed a signature change**: unlike Wyckoff/
Session, Market Regime needs `HTFBiasResult`, which is computed
*outside* `ContextEngine.build()` (a separate multi-timeframe fetch).
Since `core/pipeline.py` already computes `htf_bias` before building
`context`, `build_context_snapshot()`/`ContextEngine.build()` gained
an optional `htf_bias=None` parameter — backward compatible with
every pre-Phase-A7 call site (both real code and every existing
test), verified by re-running the full suite after the change.
`context.market_regime` is `ContextSnapshot`'s 12th field, and the
only one that is a single `MarketRegimeResult` rather than a
`Sequence[...]` — a regime is a state of the whole window, not a
sparse event list.

Not consumed by any strategy, `AIAnalyzer`, `DecisionEngine`, or
`RiskManager` in this phase — see `docs/MARKET_REGIME.md`'s
"Significance for AI" section for why this is nonetheless a natural,
already-available input for a future real AI provider.

### Data Quality Engine (Phase A8)

`data/data_quality.py`'s `assess_data_quality(candles, interval)`
assesses the candle list `get_candles()` already returned — missing
candles, duplicate timestamps, invalid OHLC, timeframe consistency —
into a scored, structured `DataQualityResult`. Purely observational:
never filters, blocks, or alters what `context/` receives, even when
`valid` is `False`. New `core/pipeline.py` stage immediately after
`market_data`; `"data_quality"` is the only new key in `run()`'s
result dict.

Deliberately does not reuse or modify `data/market_data.py`'s
existing `_validate_and_clean()`/`_detect_missing_candles()` (private
methods on a class that already feeds the live M15 pipeline path) —
same reasoning as Wyckoff's relationship to `amd.py`
(`docs/WYCKOFF.md`). Independently implements its own checks instead;
full detail and the exact penalty table: `docs/DATA_QUALITY.md`.

### Explainability Layer (Phase A9)

`signals/explainability.py`'s `explain_signal(signal, context,
quality)` produces a `SignalExplanation` (`direction`, `reasons`,
`quality`, `confidence`) — human-readable reasons for a signal, with
zero new detection logic. Its primary reason source is Signal Quality
Score's already-computed `criteria_met` (Phase A4), translated into
direction-aware phrases (`"HTF bullish bias"`, `"HH/HL structure"`,
etc.) — no alignment check is re-derived. Three additional reasons,
each included only when directionally relevant, come from Wyckoff
(Phase A5), Session (Phase A6), and Market Regime (Phase A7) — all
already computed, none re-detected.

New stage immediately after `signal_quality`; `"explanations"` is the
only new key in `run()`'s result dict. `confidence` is
`SignalCandidate.confidence * 100`, relayed exactly as generated —
never recomputed, since Explainability runs before
`DecisionEngine.evaluate()` and no blended/final confidence exists
yet to report. Not consumed by `AIAnalyzer`, `DecisionEngine`,
`RiskManager`, or `telegram/signal_formatter.py` in this phase — see
`docs/EXPLAINABILITY.md`'s "How AI will use this in the future"
section.

### Feature Engineering Foundation (Phase A10)

`features/feature_engine.py`'s `compute_market_features(context,
explanation, asset, timeframe, htf_bias)` builds one `MarketFeatures`
snapshot per candidate (`asset`, `timeframe`, `htf_bias`,
`market_regime`, `session`, `signal_quality`, `confidence`,
`volatility`, `trend_strength`, `liquidity_distance`, `volume`,
`atr`) — a standard, flat shape for a future AI Analyzer, backtester,
ML dataset exporter, or Failure Analysis module. **A standardization
layer, not an analysis layer**: it does not detect or grade anything
itself. `volatility`/`trend_strength`/`market_regime` are direct
reads of Market Regime's own classification (Phase A7), `session`
reuses the latest `SessionEvent` (Phase A6), `liquidity_distance` is
computed from already-detected `liquidity_zones`, and
`signal_quality`/`confidence` are relayed directly from
Explainability's already-computed `SignalExplanation` (Phase A9,
itself built from Signal Quality Score, Phase A4) — no new detection,
no new grading, no new confidence calculation. `volume` and `atr` are
always `None`: this codebase has no volume data source, and a real
ATR would be a new technical indicator, out of scope for a
standardization-only phase — both are explicit, honest hooks, never
fabricated values, matching Wyckoff's (Phase A5) own
`_volume_confirms()` hook.

New stage at the **end** of the per-candidate analysis chain,
immediately after `explainability` (not between `context` and
`signal` — an earlier version of this phase placed it there and was
corrected, since a pre-Strategy Feature Engineering module would
eventually be pulled into reimplementing strategy logic just to
describe a candidate). Computed once per candidate, same list shape
as `quality_results`/`explanations` (not the once-per-cycle shape
`htf_bias`/`market_regime` use, since `signal_quality`/`confidence`
only exist per candidate); `"features"` is the only new key in
`run()`'s result dict. Not consumed by any `strategies/*.py` file,
`signals/signal_quality.py`'s scoring, `signals/explainability.py`,
`AIAnalyzer`, `DecisionEngine`, or `RiskManager` in this phase — see
`docs/FEATURE_ENGINEERING.md`'s "Significance for AI" section for why
this is nonetheless a natural, already-available input for a future
real AI provider.

### Strategy Lifecycle Management Foundation (Phase A11)

`strategies/lifecycle/` adds `StrategyDefinition` (`id`, `name`,
`version`, `status`, `supported_assets`, `supported_styles`,
`supported_timeframes`, plus `performance`/`win_rate`/
`last_validation` hooks), `StrategyStatus` (`TESTING`/`ACTIVE`/
`DISABLED`/`DEPRECATED`), and `StrategyRegistry`
(`register()`/`get()`/`list()`/`active()`) — a metadata layer, not a
signal-generation layer. `build_default_registry()` registers the
three strategies `strategies/strategy_manager.py`'s `StrategyManager`
already runs (`LIQUIDITY_SWEEP_STRATEGY`/`FVG_STRATEGY`/
`AMD_STRATEGY`, matched by their real `SignalCandidate.strategy_name`
string literals) — no new strategy is introduced, and no existing
`strategies/*.py` file is modified.

Deliberately has **zero pipeline wiring** in this phase: unlike every
other Phase A module, `core/pipeline.py` never constructs or reads a
`StrategyRegistry`, and `strategies/lifecycle/` itself never imports
`strategy_manager.py` or any strategy class — `StrategyStatus` does
not gate which strategies actually run. `performance`/`win_rate`/
`last_validation` are always `None`: this codebase computes no
per-strategy performance or win rate anywhere today (unrelated to
`monitoring/performance.py`'s database-driven, already-existing
per-strategy aggregation) — explicit, honest hooks for Phase 59
Validation to populate, never fabricated values. See
`docs/STRATEGY_LIFECYCLE.md` for the full contract.

### Asset Intelligence Foundation (Phase A12)

`assets/` adds `AssetDefinition` (`symbol`, `name`, `asset_type`,
`market`, `base_currency`, `quote_currency`, plus seven `None` hooks
— `trading_session`/`volatility_class`/`news_sensitivity`/
`fundamental_profile`/`session_profile`/`risk_profile`/
`news_profile`), `AssetType` (`GOLD`/`FOREX`/`CRYPTO`/`INDEX`/
`STOCK`/`UNKNOWN`), and `AssetRegistry` (`register()`/`get()`/
`list()`/`by_type()`) — a metadata layer, not a market integration.
`build_default_registry()` registers `GOLD_ASSET`
(`assets/profiles/gold.py`), the one asset this codebase actually
trades today — no Forex/Crypto/Index/Stock data provider, API, or
profile is added; those `AssetType` values are reserved, not
implemented.

Deliberately has **zero pipeline wiring** in this phase, same posture
as Strategy Lifecycle: `core/pipeline.py` never constructs, reads, or
imports `AssetRegistry`/`AssetDefinition`. `assets/` itself imports
nothing outside itself (not even `data/`, `strategies/`, or
`strategies/lifecycle/` — the Strategy↔Asset relationship is
documentation-only in this phase, see `docs/ASSET_INTELLIGENCE.md`).
`GOLD_ASSET.base_currency="XAU"`/`quote_currency="USD"` deliberately
differs from the Director brief's own illustrative
`base_currency="USD"` example — `data/twelve_data_client.py`'s
`_format_symbol()` already splits `"XAUUSD"` into `"XAU/USD"`, so
`"XAU"`/`"USD"` is the value already real in this codebase, not a new
invention (the same kind of correction Phase A11 made for
`supported_assets=["XAUUSD"]` over the brief's `["GOLD"]`). All seven
`None` hooks stay `None`: no session/volatility/news/fundamental
intelligence is computed for any asset anywhere in this codebase
today — explicit, honest placeholders, never fabricated values. See
`docs/ASSET_INTELLIGENCE.md` for the full contract.

### Configuration & Feature Flags Foundation (Phase A13)

`configuration/` adds `Environment` (`DEVELOPMENT`/`TESTING`/
`PRODUCTION`, plus `resolve_environment()`, a safe adapter that
degrades a missing/unrecognized value to `DEVELOPMENT` rather than
raising), `ApplicationSettings` (`environment`, `symbol`,
`default_timeframe`, `timezone`, plus `build_settings_from_config()`,
the minimal adapter from the existing `config.Config`), and
`FeatureFlags` (`enable_ai`/`enable_crypto`/`enable_swing`/
`enable_ai_memory`/`enable_replay`, every default `False`) — a
foundation layer, not a rewrite of `config.py`.

`config.py` is entirely untouched: `Config.APP_ENV`/`Config.TIMEZONE`
are read (never written) by `build_settings_from_config()`;
`Config.DB_PATH`/`Config.TIMEFRAME_HISTORY`/`Config.DEBUG`/
`Config.BASE_DIR` are not read by `configuration/` at all. `symbol`/
`default_timeframe` reuse the exact `"XAUUSD"`/`"M15"` literals
`main.py`'s `TradingPipeline(...)` already uses (`config.py` has no
constant of its own for either) — the same real-value-reuse pattern
Phase A11/A12 followed. Every `FeatureFlags` default is `False`: none
of the five reserved flags (AI, Crypto, Swing, AI Memory, Replay) is
wired to an actual feature — `ai/ai_analyzer.py` stays a stub, no
Crypto/swing capability exists, regardless of flag value.

Deliberately has **zero pipeline wiring** in this phase, same posture
as Strategy Lifecycle and Asset Intelligence: `core/pipeline.py` never
constructs, reads, or imports `Environment`/`ApplicationSettings`/
`FeatureFlags`. `configuration/` imports only `config.Config` — no
dependency on `data/`, `context/`, `strategies/`, `signals/`, `ai/`,
`decision/`, `risk/`, `assets/`, `database/`, or `telegram/`. See
`docs/CONFIGURATION_MANAGEMENT.md` for the full contract.

### Signal Schema Standard Foundation (Phase A15)

`signals/schema.py` adds `SignalSchema` — one standard, cross-module
signal contract (identity, market info, direction, price, a
`context_id` reference, strategy info, quality info, an
`explanation_id` reference, decision info, a `risk_id` reference) —
and `validate_signal()`/`generate_signal_id()`.
`signals/adapter.py` adds `from_signal_candidate()`, the one
backward-compatibility bridge from an existing `SignalCandidate` to a
`SignalSchema`. A standardization layer, not a new signal source:
computes nothing, relays already-computed values
(`SignalQualityResult`/`TradeDecision`, when supplied) or leaves an
honest `None` reference (`context_id`/`explanation_id`/`risk_id`,
none of which has a real id source anywhere in this codebase today).

Distinct from `database/signal_record.py`'s pre-existing
`SignalRecord` (untouched by this phase): `SignalRecord` is a
persistence wrapper requiring a full `(SignalCandidate, TradeDecision,
RiskResult)` triple; `SignalSchema` can exist earlier — right after
Strategy Engine, before Decision Engine or Risk Manager have run
(`decision` defaults `"PENDING"`) — and is never itself written to
the database in this phase. Both independently reuse
`database/signal_record.py`'s own `str(uuid.uuid4())`/
`datetime.now(timezone.utc)` convention for identity/timestamp
generation — not a new scheme.

`SignalSchema.decision`'s vocabulary (`APPROVED`/`REJECTED`/
`PENDING`) is deliberately distinct from `decision.models.DecisionAction`'s
real values (`APPROVE`/`REJECT`/`NO_TRADE`) — `SignalSchema` can exist
before a `TradeDecision` does at all, so `"PENDING"` is a real third
state `DecisionAction` has no equivalent for.
`signals/adapter.py`'s `_DECISION_ACTION_TO_STATUS` maps
`APPROVE`→`"APPROVED"`, `REJECT`→`"REJECTED"`,
`NO_TRADE`→`"REJECTED"` (collapsed — both mean no signal reaches the
user) — the one place that translation happens.

Deliberately has **zero pipeline wiring** in this phase, same posture
as every other Phase A foundation module: `core/pipeline.py` never
calls `from_signal_candidate()`. `signals/adapter.py` does not import
`assets/` for its `asset_type` default either — `"GOLD"` is a literal
matching `assets.asset_type.AssetType.GOLD.value`, documented, not a
new cross-package dependency (Strategy Lifecycle, Asset Intelligence,
and Configuration have each stayed similarly unwired from one another
in their own phase). See `docs/SIGNAL_SCHEMA.md` for the full
contract.

### Context Snapshot Foundation (Phase A16)

`context/snapshot.py` adds `ContextSnapshotSchema` — one standard,
flat, JSON-serializable summary of market context (identity, market
info, nested `structure`/`liquidity`/`zones`/`session` groups,
`regime`, `metadata`) — plus `validate_snapshot()`,
`generate_snapshot_id()`, and `from_context_snapshot()`, the one
adapter from an existing, already-built
`context.context_orchestrator.ContextSnapshot`. A standardization
layer, not a new analysis: computes nothing, relays already-detected
presence/values (`most_recent_bias()`, `StructureType`/`LiquidityType`/
`Session`/`MarketRegime` values) or leaves an honest `None`/`False`
default (`zones.premium_discount` — no detector for this exists
anywhere in this codebase today).

**Deliberately named `ContextSnapshotSchema`, not `ContextSnapshot`**:
`context.context_orchestrator` already defines the real, internal,
12-field `ContextSnapshot` every strategy/Signal Quality Score/
Explainability/Feature Engineering module already consumes —
untouched by this phase. A second class with the identical name in
the same package would be a serious, ongoing ambiguity for any future
reader or agent; `ContextSnapshotSchema` mirrors
`signals/schema.py`'s own `SignalSchema` naming (Phase A15, distinct
from `signals/models.py`'s real `SignalCandidate`) for the same
reason. See `docs/CONTEXT_SNAPSHOT.md`'s "A critical naming note" for
the full comparison table between the two types.

`regime` relays the real 7-value `MarketRegime` vocabulary
(`TRENDING`/`RANGE`/`ACCUMULATION`/`DISTRIBUTION`/`HIGH_VOLATILITY`/
`LOW_VOLATILITY`/`UNKNOWN`) directly, not the roadmap's own
illustrative 5-value list — collapsing the real 7 down to 5 would
require inventing a new mapping rule, itself a form of new analysis
logic this phase's scope forbids. `structure.swing_state` reads a
single already-classified `StructureType` label rather than computing
a new combined "last-high + last-low" pair the roadmap's own example
showed — both deviations are disclosed in
`docs/CONTEXT_SNAPSHOT.md`, the same real-value/simplification-
disclosure pattern Phase A10-A15 each followed.

Deliberately has **zero pipeline wiring** in this phase, same posture
as every other Phase A foundation module: `core/pipeline.py` never
calls `from_context_snapshot()`. `context/snapshot.py` does not import
`signals/` for its own `ValidationResult` either — `context/` must
never depend on `signals/` (see `docs/ARCHITECTURE_RULES.md`'s
Context Engine rule), so a separate, independently-declared,
identically-shaped `ValidationResult` exists instead of an import.
`context/market_structure.py`, `context/liquidity.py`,
`context/order_block.py`, `context/fvg.py`, and
`context/context_orchestrator.py` are all read-only inputs to this
phase — none is modified. See `docs/CONTEXT_SNAPSHOT.md` for the full
contract.

### Error Classification Foundation (Phase A18)

`core/errors/` adds `GoldBotError` (`base.py`) — a base exception
carrying `code`/`message`/`module`/`timestamp`/`details` and a
`to_dict()` — plus nine category subclasses (`exceptions.py`:
`ConfigurationError`, `ValidationError`, `DataError`,
`ExternalAPIError`, `DatabaseError`, `PermissionError`,
`StrategyError`, `DecisionError`, `ExecutionError`) and a standard
error-code registry (`codes.py`: `CODE_REGISTRY`, `CODE_PATTERN`,
e.g. `"DATA_001"`). Implements the hierarchy
`contracts/error_contract.md` (Phase A17) specified but explicitly
deferred as a future phase's job — this is that phase. Cross-cutting,
like `core/logger.py`/`core/secrets.py`: every layer may import from
it without creating a new architecture boundary.

**A foundation, not a retrofit**: no existing raise site is migrated
in this phase. `core/secrets.py`'s existing bare `ValueError`,
`assets.asset_registry.DuplicateAssetSymbolError`, and
`strategies.lifecycle.strategy_registry.DuplicateStrategyIdError` are
all untouched — migrating them is a named, explicitly deferred future
step (`docs/ERROR_HANDLING.md`'s "What this phase does NOT do").
Existing "expected, data-driven" error reporting
(`ValidationResult`/`RiskResult`/`TradeDecision`, never a raised
exception) is unchanged — `GoldBotError` is for genuine programmer/
integrity errors, not a replacement for that pattern.

`PermissionError` (the class name) shadows Python's built-in
`PermissionError` within any module that imports it directly —
deliberate (it is Phase A17's own contract naming and this phase's
own brief's exact hierarchy), documented in
`core/errors/exceptions.py`'s own docstring, and safe (no code in
this codebase relies on catching the built-in `PermissionError`
anywhere near an import of this one).

`core/errors/codes.py` adds three code prefixes
(`STRATEGY_001`/`DECISION_001`/`EXECUTION_001`) the brief's own error-
code section didn't name, despite naming all nine exception classes
in its hierarchy — filling a real gap between the hierarchy and the
code registry, disclosed in `docs/ERROR_HANDLING.md`'s "A completed
gap" section, not left silent.

Deliberately has **zero pipeline wiring** in this phase, same posture
as every other Phase A foundation module: no existing `core/`,
`data/`, `strategies/`, `signals/`, `ai/`, `decision/`, `risk/`,
`telegram/`, or `database/` file raises a `GoldBotError` subclass
yet. See `docs/ERROR_HANDLING.md` for the full contract.

### Performance Metrics Foundation (Phase A19)

`performance/` adds `PerformanceMetric` (`metrics.py`: `name`/
`module`/`duration_ms` required, `metric_id`/`timestamp`/`status`/
`metadata`/`error_code` defaulted — matching this phase's own brief's
three-argument construction example), `PerformanceCollector`
(`collector.py`: `record()`/`get_metrics()`/`get_by_module()`/
`clear()`, not a singleton), and `PerformanceTimer`/
`measure_performance()` (`timer.py`: a context manager and its
decorator form, both using `time.perf_counter()` — the same primitive
`core/pipeline.py`'s own `_log_stage()` already uses). Measures
duration; computes nothing else, decides nothing, generates no
signal.

**Not what it sounds like**: `monitoring/performance.py`'s
pre-existing `PerformanceTracker`/`PerformanceResult` compute
historical *trade outcome* statistics (win rate, strategy breakdown)
from the database — an unrelated question from "how long did this
code take to run." `core/pipeline.py`'s own `_log_stage()` already
logs each pipeline stage's duration today — `performance/` does not
replace, wrap, or read from it. `docs/PERFORMANCE.md` (Phase 53) is a
one-time benchmark *report*; `docs/PERFORMANCE_METRICS.md` (this
phase) is the ongoing measurement *infrastructure*. All three
distinctions are spelled out in `docs/PERFORMANCE_METRICS.md`'s own
"Not what it sounds like" section.

**Phase A18 integration** (the one explicit cross-wiring this phase's
own brief requested): `PerformanceTimer.__exit__` does a real
`isinstance(exc_val, GoldBotError)` check — if the exception raised
inside a measured block is a `core.errors.base.GoldBotError`, its
`.code` is captured as the metric's `error_code`; any other exception
type leaves `error_code=None`, never guessed.

Deliberately has **zero pipeline wiring** otherwise, same posture as
every other Phase A foundation module: `core/pipeline.py` is entirely
unmodified — no existing stage constructs a `PerformanceTimer` or
`PerformanceCollector` in this phase. See
`docs/PERFORMANCE_METRICS.md` for the full contract.

`core/pipeline.py`'s `TradingPipeline` is the only place that wires
every layer above together end to end — see its own docstring and
`docs/AUDIT_REPORT.md` for why the notification-eligibility filter
exists in exactly the shape it does.

## Module Responsibilities (summary — full detail in `docs/code_structure.md`)

| Module | Responsibility |
|---|---|
| `core/` | Cross-cutting infrastructure: pipeline orchestration, logging, secrets, and (Phase A18) the `GoldBotError` exception hierarchy (`core/errors/`) — implemented, not yet wired into any existing raise site. |
| `configuration/` | Configuration & Feature Flags foundation (Phase A13) — `Environment`/`ApplicationSettings`/`FeatureFlags`, additive to `config.py` (untouched). Every feature flag defaults `False`; no pipeline wiring. |
| `assets/` | Asset Intelligence foundation (Phase A12) — `AssetDefinition`/`AssetRegistry`, one metadata record per tradable asset (symbol, type, market, currency, plus seven not-yet-implemented `None` hooks). Registers only `GOLD_ASSET` (XAUUSD) today; no market data, no execution, no pipeline wiring. |
| `data/` | Market data fetch and normalization, plus Data Quality assessment (`data_quality.py`, Phase A8) — observational scoring, not filtering. |
| `context/` | Pure SMC market-structure detection functions (structure, BOS/CHoCH, liquidity, OB, FVG, AMD, Wyckoff Spring/Upthrust — Phase A5, Session classification — Phase A6, and Market Regime — Phase A7, all part of `ContextSnapshot`), plus HTF Bias (`htf_bias.py`, Phase A2) — a market-context-only Daily/H4/H1 classification, not itself part of `ContextSnapshot`. `snapshot.py` (Phase A16) additionally standardizes a `ContextSnapshot` into a flat, JSON-serializable `ContextSnapshotSchema` — a distinct type, not a replacement. |
| `strategies/` | Independent signal-candidate generation per SMC methodology, plus a Strategy Lifecycle metadata layer (`lifecycle/`, Phase A11) — `StrategyDefinition`/`StrategyRegistry`, storing status/version/supported-assets metadata only, never running a strategy or generating a signal. |
| `signals/` | The `SignalCandidate` data contract, strategy aggregation, Signal Quality Score (`signal_quality.py`, Phase A4) — a per-candidate, advisory-only A+/A/B/C grade — Explainability (`explainability.py`, Phase A9) — human-readable reasons, reusing Signal Quality's criteria — and Signal Schema (`schema.py`/`adapter.py`, Phase A15) — one standard, JSON-serializable cross-module signal contract, computing nothing itself. |
| `features/` | Feature Engineering foundation (Phase A10) — `MarketFeatures`, one standard snapshot per candidate for a future AI/backtester/ML/Failure-Analysis consumer. A standardization layer: relays `context/` and `signals/` (Signal Quality + Explainability) results as-is, computes nothing new. |
| `ai/` | Advisory-only AI evaluation layer (Phase 55: foundation for a future provider; production analyzer is still a heuristic stub). |
| `decision/` | Blends signal confidence, HTF bias, (inverted) AI risk score, and AI confidence — weighted, Phase A3 — into APPROVE/REJECT/NO_TRADE. |
| `risk/` | SL/TP geometry and stop-loss-distance validation; sizing suggestion only. |
| `execution/` | Inert scaffolding for future MT5 integration — not reachable from any runtime path today. |
| `monitoring/` | Historical trade-outcome statistics (win rate, strategy breakdown — `performance.py`'s `PerformanceTracker`), not wired into any live command yet. Distinct from `performance/` (Phase A19) — see that row. |
| `performance/` | Performance Metrics foundation (Phase A19) — `PerformanceMetric`/`PerformanceCollector`/`PerformanceTimer`, a standalone code-timing foundation. Not wired into `core/pipeline.py`; not the same concept as `monitoring/performance.py`'s trade-outcome statistics. |
| `database/` | SQLite persistence — the only place SQL is written. |
| `telegram/` | The Telegram product layer: routing, permissions, handlers, services. |

## Dependency Rules

A layer may depend on the layer(s) below it in the data-flow diagram
above, and on `core/`/`config.py` (cross-cutting). It must never
depend upward or sideways into an unrelated layer. Concretely, as
implemented and enforced today (verified by the Phase 48 audit's
circular-import check and re-verified every phase since via the CI
import sweep):

- `core/errors/` (Phase A18) imports only the standard library
  (`datetime`, `typing`, `re`) — no dependency on `strategies/`,
  `signals/`, `ai/`, `decision/`, `risk/`, `telegram/`, or
  `database/`. Every layer may import from `core/errors/` (same
  cross-cutting status as `core/logger.py`/`core/secrets.py`), but
  none does yet in this phase — see `docs/ERROR_HANDLING.md`.
- `performance/` (Phase A19) imports `core/errors/` (for the optional
  `GoldBotError` integration in `timer.py`) and `core/logger.py` (for
  the `PERFORMANCE` log line) — both cross-cutting. No dependency on
  `context/`, `strategies/`, `signals/`, `ai/`, `decision/`, `risk/`,
  `execution/`, `telegram/`, `database/`, `assets/`, or
  `configuration/`. Not imported by `core/pipeline.py` or any other
  existing module in this phase.
- `context/`, `strategies/`, `signals/` never import `telegram/`,
  `database/`, or `ai/`.
- `signals/schema.py` (Phase A15) imports only the standard library —
  no dependency on any other GoldBot package. `signals/adapter.py`
  imports `signals.schema` (same package) plus, `TYPE_CHECKING`-only,
  `signals.models`/`signals.signal_quality`/`decision.models` — this
  is not a runtime `signals/` → `decision/` dependency (which would
  invert `decision/`'s own existing `signals/` import below and
  create a cycle); it exists purely for type hints, same pattern
  `decision/`'s own `TYPE_CHECKING`-only imports already use. Neither
  file imports `ai/`, `risk/`, `database/`, `telegram/`, `execution/`,
  or `assets/` — `adapter.py`'s `asset_type` default is a literal
  string, not an `assets/` import (see `docs/SIGNAL_SCHEMA.md`).
- `context/snapshot.py` (Phase A16) imports only the standard library
  plus `context.context_orchestrator` and `context.market_structure`
  (same package) — no dependency on `strategies/`, `signals/`, `ai/`,
  `decision/`, `risk/`, `database/`, `telegram/`, or `assets/`.
  Deliberately does not import `signals.schema.ValidationResult`
  despite the identical shape — `context/` must never depend on
  `signals/` (see `docs/ARCHITECTURE_RULES.md`'s Context Engine rule)
  — `context/snapshot.py` declares its own, independent
  `ValidationResult` instead (see `docs/CONTEXT_SNAPSHOT.md`).
- `configuration/` (Phase A13) imports only the root `config.Config`
  (cross-cutting, same as every layer's pre-existing `config.py`
  access) — no dependency on `data/`, `context/`, `strategies/`,
  `signals/`, `ai/`, `decision/`, `risk/`, `assets/`, `database/`, or
  `telegram/`. `config.py` itself has zero dependency on
  `configuration/` — a one-directional relationship, never circular.
- `assets/` (Phase A12) imports nothing outside itself — no
  dependency on `data/`, `context/`, `strategies/` (including
  `strategies/lifecycle/`), `signals/`, `ai/`, `decision/`, `risk/`,
  `execution/`, `database/`, or `telegram/`. `asset_registry.py`
  imports `assets.profiles.gold` (same package) only.
- `features/` imports `context/` (`context.market_regime`) and
  `signals/` (for `SignalExplanation`, `TYPE_CHECKING`-only) plus its
  own `features.feature_model` — never `strategies/`, `ai/`,
  `decision/`, `risk/`, `database/`, or `telegram/`. `features/`
  sitting downstream of both `context/` and `signals/` mirrors
  `decision/`'s own pre-existing pattern of depending on two adjacent
  below-layers at once (see the `decision/` rule below).
- `strategies/lifecycle/` (Phase A11) imports nothing outside itself
  — no dependency on `context/`, `signals/`, `ai/`, `decision/`,
  `risk/`, `database/`, or `telegram/`, and, deliberately, no
  dependency on `strategy_manager.py` or any `strategies/*.py`
  strategy class either: `StrategyDefinition.id` matches each
  strategy's real `SignalCandidate.strategy_name` string literal by
  value, not by importing the strategy class itself, so the registry
  never instantiates or runs a strategy.
- `ai/` never imports `database/` or `telegram/`.
- `decision/` imports `ai/` (for `AIAnalysisResult`), `signals/` (for
  `SignalCandidate`), and, as of Phase A3, `context/` (for `HTFBias` —
  a real runtime import, since it's used as a dict key; `HTFBiasResult`
  itself stays `TYPE_CHECKING`-only, same as `SignalCandidate`/
  `AIAnalysisResult`). Still never `database/`, `telegram/`, or
  `risk/`. `context/` appearing here is not a new kind of dependency —
  `context/` is upstream of `decision/` in the Data Flow diagram above,
  same direction as the pre-existing `ai/`/`signals/` dependencies.
- `risk/` imports `decision/` and `signals/`, never `database/` or
  `telegram/`.
- `telegram/handlers.py` never imports `database/*` or
  `core/pipeline.py` directly — only `telegram/*_service.py` (see
  `telegram/handlers.py`'s own module docstring, which states this
  rule explicitly).
- `database/*_repository.py` never imports `telegram/` — a repository
  knows nothing about Telegram, permissions, or commands.
- `core/pipeline.py` is the one file allowed to import from every
  layer — it is the orchestrator, not a layer itself.

If a change requires violating one of these rules, that is a signal
to stop and reconsider the design, not to add the import and move on
— see `CLAUDE.md`'s "Architecture Rules" for the same point stated as
a working rule rather than a description.
