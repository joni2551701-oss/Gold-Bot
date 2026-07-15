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
every module's own documentation follows. For the Director-requested
full-project re-audit taken after Phase 59.9 (redundant/parallel
modules, duplicate-logic check, dependency-direction re-verification,
a consolidated wiring plan, and the Phase 60 roadmap), see
`docs/PHASE59_ARCHITECTURE_FREEZE.md` — it supersedes nothing (the
Phase A1 `docs/ARCHITECTURE_AUDIT.md`/`DEPENDENCY_MAP.md` remain valid
snapshots of that earlier state) but is the current, Phase-59-era
freeze audit. For the formal Phase 60.0 six-part audit that followed
it (module dependency graph, dead code, duplicate logic, database
audit, owner audit, pipeline audit — including two real duplicate
findings the freeze audit didn't surface), see
`docs/PHASE60_ARCHITECTURE_AUDIT.md`.

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
      |     |
      v     |
Market Phase (context/market_phase.py)  -- ACCUMULATION/MANIPULATION/
      |     |                       DISTRIBUTION/MARKUP/MARKDOWN/UNKNOWN,
      |     |                       classified from already-computed
      |     |                       Wyckoff/AMD/Market Regime (Pre-Phase
      |     |                       59 Architecture Readiness Review,
      |     |                       AC-02; advisory only, logged, see
      |     |                       below)
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
Signal History (core/pipeline.py)  -- links every SignalSchema to the
      |                             cycle's ContextSnapshotSchema via
      |                             context_id/snapshot_id, plus a
      |                             fresh decision_id per TradeDecision
      |                             (Pre-Phase 59 Architecture Readiness
      |                             Review, AC-03; advisory record-
      |                             building only, see below)
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
was **not** shown in the diagram above through Phase A19 — but as of
the Pre-Phase 59 Architecture Readiness Review (AC-03), `core/pipeline.py`
now calls `from_signal_candidate()` once per candidate in the new
**Signal History** stage (see the diagram above and its own section
below) to build the historical link record. `Signal Generation
(signals/)` itself is unchanged — it still produces `SignalCandidate`s
exactly as before; `SignalSchema` is built downstream, after Risk, from
already-computed values only.

Context Snapshot (`context/snapshot.py`, Phase A16) was likewise
**not** shown in the diagram above through Phase A19 — but as of the
same Pre-Phase 59 Architecture Readiness Review (AC-03),
`core/pipeline.py` now calls `from_context_snapshot()` once per cycle,
also in the new **Signal History** stage, to obtain the
`snapshot_id` every `SignalSchema` in that cycle links back to via
`context_id`. The `Context Engine (context/)` node above is unchanged —
it still produces the real, internal `ContextSnapshot` exactly as
before, and every existing consumer (Strategies, Signal Quality Score,
Explainability, Feature Engineering, and now Market Phase) keeps
reading it directly, unaffected. See "Signal History Foundation
(Pre-Phase 59 Architecture Readiness Review, AC-03)" below for the
full linkage.

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

### Phase 59.2 — Market Data Intelligence Layer

Hardens the Phase 59.1 provider foundation before adding new
providers — full detail: `docs/MARKET_DATA_ARCHITECTURE.md`,
`docs/PROVIDER_CONTRACTS.md`, `docs/TRADINGVIEW_PROVIDER.md`,
`docs/OWNER_COMMANDS.md`. `data/providers/base_provider.py`'s
`MarketDataProvider` was split from a new, more general
`DataProvider` root (`get_provider_name()`, `get_market_status()`),
so a non-candle provider (macro/economic data) can share the same
registry without being force-fit into a candle shape.
`MarketDataProvider` gained `get_supported_timeframes()`; a third
candidate method, `get_symbol_info()`, was audited and deliberately
**not** added (no concrete consumer yet — see
`docs/PROVIDER_CONTRACTS.md`'s audit table).

Two new provider stubs, same inert-by-design posture as
`mt5_provider.py`: `binance_provider.py`'s `BinanceProvider` (v0.9
Multi Asset foundation; validates `BTCUSDT`/`ETHUSDT` symbols before
raising `NotImplementedError`) and a new, separate hierarchy —
`fundamental_base.py`'s `FundamentalDataProvider` (`get_macro_indicator()`,
`get_interest_rate()`, `get_inflation_data()`, `FundamentalDataPoint`,
`FundamentalSnapshot`) — and `fred_provider.py`'s `FredProvider`
(verified real FRED series IDs `FEDFUNDS`/`CPIAUCSL`/`DTWEXBGS`, no
live connection). TradingView was researched, not coded —
`docs/TRADINGVIEW_PROVIDER.md` concluded TradingView's own Terms of
Service forbid the commercial/automated use a `MarketDataProvider`
implementation would require, so no `tradingview_provider.py` exists.

`data/providers/registry.py`'s `ProviderRegistry`
(`register()`/`get()`/`available()`/`all_names()`) is a new, broader
catalog — explicitly not a replacement for Phase 59.1's `get_provider()`
(single active choice, `Config`-driven); see `registry.py`'s own
docstring for the exact relationship. `build_default_registry()`
registers all four real/stub providers (not TradingView).

`monitoring/provider_health.py` (a new file in the pre-existing
`monitoring/` package, alongside `monitoring/performance.py`) adds
`ProviderHealthStatus` (`ONLINE`/`DEGRADED`/`OFFLINE`) and
`check_provider_health()`/`check_registry_health()`, timing each
provider's own always-safe `get_market_status()` call — a third,
distinct kind of "performance" from `performance/` (Phase A19, system
timing) and `analytics/` (Phase 59 Preparation, trading outcome).

`docs/OWNER_COMMANDS.md` is a new, dedicated contract-only document
(migrated and expanded from Phase 59.1's own "Owner Mode" section,
which now just points here) — five owner-only Telegram commands
(`/provider`, `/providers`, `/provider_status`, `/enable_provider`,
`/disable_provider`), none implemented.

None of `data/market_data.py`, `core/pipeline.py`, `context/`,
`strategies/`, `signals/` (candidate generation),
`decision/decision_engine.py`, `risk/risk_manager.py`, `ai/`,
`execution/`, or any Telegram file changed in this phase — see
`docs/MARKET_DATA_ARCHITECTURE.md`'s "As implemented today" section
for the explicit, disclosed gap between this diagram and what
`data/market_data.py` actually calls.

### Phase 59.3 — Data Intelligence Foundation

Hardens the provider layer further, per the Director's own priority
after reviewing Phase 59.2: normalize, persist, cache-verify,
health-extend, owner-command-foundation, fundamental-context-connect —
no new provider added (TradingView/Bitget explicitly deferred). Full
detail: `docs/PROVIDER_CONTRACTS.md`, `docs/MARKET_DATA_ARCHITECTURE.md`.

**TASK 1 (Provider Normalization)** — audit found `MarketCandle`
already carried the caller's canonical symbol/timeframe; the real gap
was a missing `provider` field (added, additive;
`TwelveDataProvider.get_candles()` now stamps it) and no centralized
per-provider format table. New `data/normalization/` package:
`symbol_mapper.py`/`timeframe_mapper.py` (canonical ⟷ provider wire
format, TwelveData/Binance), `candle_normalizer.py`
(`stamp_provider()`). No new candle type.

**TASK 2 (Raw Market Storage)** — the first real database migration
added by any Phase A/AC/Phase-59 module; every prior one deliberately
stayed in-memory-only. Two new, fully isolated tables (`raw_candles`,
`market_snapshots` — see `docs/DATABASE.md`), following the exact
established idempotent `CREATE TABLE IF NOT EXISTS` pattern, never
touching `signals`/`users`/etc. `database/raw_candle_models.py`/
`raw_candle_repository.py`, `database/market_snapshot_models.py`/
`market_snapshot_repository.py` (the latter's `from_market_data_snapshot()`
bridges Phase 59 Preparation's own in-memory `MarketDataSnapshot` to a
real row). Not called from `core/pipeline.py`.

**TASK 3 (Market Data Cache)** — "Already implemented — verified":
`data/data_cache.py`'s pre-existing `SmartDataCache` already provides
exactly this task's two goals (duplicate-API-call reduction,
rate-limit protection), but had zero test coverage and is unwired
anywhere. No competing `data/cache/market_cache.py` was built;
`tests/data/test_data_cache.py` closes the real, disclosed gap
(coverage only).

**TASK 4 (Provider Health Integration)** — `monitoring/provider_health.py`'s
`ProviderHealthReport` gained `checked_at` (additive, the brief's own
"Last Update" example), stamped by `check_provider_health()`.

**TASK 5 (Owner Command Foundation)** — new `telegram/owner/` package
(`provider_commands.py`, `system_commands.py`, `feature_commands.py`)
with real, tested functions reusing `data/providers/registry.py` and
`monitoring/provider_health.py` — a scope shift from Phase 59.2's own
"contract only" instruction for the same idea. **Not** registered into
`telegram/commands.py`'s `OWNER_COMMANDS`/`ADMIN_COMMANDS`, **not**
called from `telegram/command_router.py`/`telegram/handlers.py` — the
live bot's command surface is unaffected. `enable_provider()`/
`disable_provider()` honestly report `success=False`: no runtime
override mechanism exists for `config.py`'s import-time-read
`ENABLE_*` flags.

**TASK 6 (Fundamental Context Contract)** — `context/fundamental_context.py`'s
`compute_fundamental_context()` connects `data/providers/fred_provider.py`
(Phase 59.2, never previously read by `context/`) to a new
`FundamentalContextSnapshot` (`fed_rate`, `inflation`,
`dollar_strength`, `risk_level`) — deliberately not named
`FundamentalSnapshot` (a different, existing provider-layer type, see
the module's own naming note). Pure adapter over already-supplied
`FundamentalDataPoint` values; does not call `FredProvider` itself
(always raises `NotImplementedError` today). `dollar_strength`/
`risk_level` stay honest `None` hooks — no classification threshold is
fabricated. Generates no signal, makes no decision.

None of `data/market_data.py`, `core/pipeline.py`, `strategies/`,
`signals/` (candidate generation), `decision/decision_engine.py`,
`risk/risk_manager.py`, `ai/`, `execution/`, `telegram/handlers.py`,
`telegram/command_router.py`, or `telegram/commands.py` changed in
this phase.

### Phase 59.5 — Historical Data Collection & Validation Foundation

Audit found no historical collector, incremental sync, integrity
validator, gap/dataset report, provider comparison, or dataset owner
command anywhere in the repo — every module below is genuinely new,
built additively on the Phase 59.1-59.3/Real Market Validation
Foundation layers rather than replacing any of them. Full detail:
`docs/DATASET_COLLECTION.md`, `docs/DATA_VALIDATION.md`,
`docs/HISTORICAL_SYNC.md`.

**TASK 1 (Historical Data Collector)** — new `data/historical_data_collector.py`.
`collect_historical_candles(provider, symbol, timeframe, start, end)`
fetches via an existing `data/providers/` `MarketDataProvider` and
saves via `database/raw_candle_repository.py`'s
`save_market_candles()` — no new fetch/storage logic, only composition
of the two. Disclosed gap: neither `TwelveDataClient.fetch_candles()`
nor `MarketDataProvider.get_candles()` accepts a real date range (both
are "most recent N" calls only), so this function requests the
largest single window a provider call can serve (capped at
`MAX_FETCH_LIMIT = 5000`) and filters client-side —
`CollectionResult.actual_start`/`actual_end` let a caller detect a
partial result rather than silently trusting a complete one.

**TASK 2 (Incremental Sync)** — new, fully isolated `sync_state` table
(`database/sync_state_models.py`/`sync_state_repository.py`, one row
per `(provider, symbol, timeframe)`, no foreign key to any other
table) plus `historical_data_collector.py`'s `sync_historical_candles()`,
which resumes from the stored `last_timestamp` instead of re-fetching
a wide window every call.

**TASK 3 (Data Integrity Validator)** — new `data/historical_validator.py`.
`validate_historical_candles()` checks a persisted
`List[RawCandle]` for missing/duplicate/out-of-order/future-timestamp/
timezone-naive/invalid-OHLC/provider-mismatch conditions, producing a
`ValidationReport`. Reuses `data.data_quality.INTERVAL_DELTAS` (a
public, same-package constant); independently re-implements the
OHLC/gap checks themselves rather than depending on
`data_quality.py`'s different-shaped, different-purpose
`assess_data_quality()` — the same disclosed-duplication precedent
that module's own docstring already established for `market_data.py`.

**TASK 4 (Gap Detector)** — new `analytics/gap_report.py`.
`build_gap_report()` enumerates every individual missing/duplicated
timestamp (capped at `MAX_GAP_ENTRIES = 1000`), where TASK 3's
validator only counts gap *events*. `format_gap_report()` renders the
brief's own worked `SYMBOL / TIMEFRAME / DATE / "HH:MM missing"` shape.

**TASK 5 (Dataset Statistics)** — new `analytics/dataset_report.py`.
`build_dataset_report()` groups a mixed `List[RawCandle]` by
`(symbol, timeframe)`, reuses TASK 3's validator per group for
duplicate/missing/invalid counts (summed across groups, not
reimplemented), and computes `coverage_pct` as an unweighted mean
across groups — disclosed, not hidden.

**TASK 6 (Multi Provider Validation)** — new `data/provider_comparison.py`.
`compare_providers()` matches two providers' candle lists by
timestamp and reports close/high/low/spread differences. Foundation
only: never merges, corrects, or picks a "winning" provider.

**TASK 7 (Owner Service Foundation)** — new
`telegram/owner/dataset_commands.py` (`get_dataset_status()`,
`get_history_status()`, `get_sync_status()`, `get_provider_compare()`).
Unlike `report_commands.py`/`validation_commands.py` (Phase 59.4/Real
Market Validation Foundation, which take caller-supplied data since
nothing persists signal/performance history yet), these four query the
real `RawCandleRepository`/`SyncStateRepository` directly — the same
"query the real backing store" posture `provider_commands.py`'s
`list_providers()` already uses. **Not** registered into
`telegram/commands.py`/`command_router.py`/`handlers.py` — the live
bot's command surface is unaffected.

None of `core/pipeline.py`, `decision/`, `execution/`, `risk/`,
`strategies/`, `context/`, `signals/`, any Telegram handler, paper
trading (`lifecycle/`), any pre-existing `analytics/` module
(`signal_performance.py`/`strategy_report.py`/`context_report.py`/
`validation_report.py`), or the pipeline's own stage order changed in
this phase.

### Phase 59.6 — Audit & Observability Foundation

The last "observe only" layer the Director's own roadmap names before
Runtime Feature Toggle (Phase 59.7), Owner Dashboard (Phase 59.8), and
Emergency Layer (Phase 59.9 — the first phase where `SystemState`/
`/panic`/`/maintenance` will actually control `Pipeline`/`Decision`/
`Execution`). Full detail: `docs/AUDIT_SYSTEM.md`,
`docs/OWNER_PERMISSIONS.md`, `docs/FEATURE_REGISTRY.md`,
`docs/CONFIG_SNAPSHOT.md`.

**TASK 1 (System State Manager)** — new `core/system_state.py`.
`SystemState` enum (`RUNNING`/`VALIDATION`/`MAINTENANCE`/`PANIC`/
`READ_ONLY`) + `SystemStateRecord` (one immutable transition record) +
`create_system_state_record()`. Pure model — no mutable "current
state" holder, nothing in `core/pipeline.py` reads it.

**TASK 2 (Audit Log)** — new, isolated, append-only `audit_log` table
(`database/audit_log_models.py`/`audit_log_repository.py`).
`log_action(actor, action, target, result, details)` records one
entry; no update/delete method exists. Nothing calls it automatically
yet — no owner command is wired to log itself.

**TASK 3 (Owner Permission System)** — new
`telegram/owner/owner_roles.py`. `OwnerRole` (`OWNER`/`SUPER_ADMIN`/
`ADMIN`/`VIEWER`) + `resolve_owner_role()`, reusing the existing
`admins.role` column (previously only a label, now classified) and
`telegram.permissions.is_owner()`. Deliberately separate from and
never touching `telegram.permissions.PermissionLevel` — that enum is
live-wired into `telegram/command_router.py`'s real permission gating
today; `OwnerRole` is a foundation-only, not-yet-checked hierarchy for
a future Owner Dashboard.

**TASK 4 (Feature Registry)** — new `configuration/feature_registry.py`.
`build_feature_registry()` unifies `config.Config`'s real
`ENABLE_MT5`/`ENABLE_TWELVEDATA`/`VALIDATION_MODE` and
`configuration.feature_flags.FeatureFlags`' 5 reserved fields with 13
declared-only names from the brief (`ENABLE_EXECUTION`, `ENABLE_NEWS`,
etc.) that have no real backing — always `enabled=False`,
`implemented=False`, `source="declared"`. Not runtime: gates nothing.

**TASK 5 (Feature Dependency Validator)** — new
`configuration/feature_dependency_validator.py`. `DEPENDENCY_RULES`
(`ENABLE_EXECUTION` requires `ENABLE_RISK`/`ENABLE_DECISION`) +
`validate_feature_dependencies()`. Since all three names are
declared-only today, no real configuration can violate this rule yet —
the contract exists for whichever future phase makes one of these
names real.

**TASK 6 (Configuration Snapshot)** — new, isolated, append-only
`config_snapshots` table (`database/config_snapshot_models.py`/
`config_snapshot_repository.py`). `create_config_snapshot(registry)`
serializes a feature registry's `{name: enabled}` state to JSON;
`save_snapshot()`/`get_latest()`/`get_all()` persist and read it back.
No apply/restore function exists — capture and read only.

None of `core/pipeline.py`, `decision/`, `execution/`, `risk/`,
`strategies/`, `context/`, `signals/`, any Telegram handler,
`telegram.permissions.PermissionLevel`, `telegram/command_router.py`,
or any pre-existing `analytics/`/`configuration/` module's behavior
changed in this phase.

### Phase 59.7 — Runtime Feature Toggle Center

Turns the Phase 59.6 static feature registry into an actual runtime
controller. Per the Director's own brief: *"Bu phase hali pipeline'ni
o'zgartirmaydi. Faqat Runtime Controller quriladi."* Full detail:
`docs/RUNTIME_FEATURE_CONTROL.md`, `docs/FEATURE_REGISTRY.md`'s own
"Runtime lifecycle" section.

**TASK 1-4 (Runtime Feature Manager, State Model, Persistent Storage,
Feature Loader)** — new `configuration/runtime_state.py`
(`FeatureRuntimeState` + `RuntimeStateCache`, in-memory only), new
isolated `runtime_features` table
(`database/runtime_feature_models.py`/`runtime_feature_repository.py`,
one row per feature name, `created_at` preserved across every later
upsert), and new `configuration/runtime_feature_manager.py`'s
`RuntimeFeatureManager` — `load()`/`reload()` seed the in-memory cache
from `build_feature_registry()`'s static defaults
(`source="default"`) then overlay any persisted row
(`source="runtime"`), auto-invoked from `__init__` so a fresh manager
is immediately queryable. `status()`/`get_feature_state()` (a
`{"feature","state","source","updated_at"}` dict view),
`list_features()`.

**TASK 5/6 (Dependency Safety, Dry Run)** — `enable()`/`disable()`/
`toggle()` (+ `enable_feature()`/`disable_feature()` aliases) all run
a dry-run `validate_feature_dependencies()` check (Phase 59.6, reused
unmodified) against the hypothetical post-toggle state before applying
anything. Symmetric: enabling a feature whose dependency isn't enabled
is rejected, and — the task's own worked example — disabling a feature
an already-enabled dependent still needs is *also* rejected ("Cannot
disable ENABLE_RISK. Dependent features active: ENABLE_EXECUTION"),
never silently applied or cascaded onto the dependent.

**TASK 7/8 (Audit Integration, Snapshot Integration)** — every
successful toggle writes an `AuditLogRepository.log_action()` entry
(`FEATURE_ENABLED`/`FEATURE_DISABLED`) and a
`ConfigSnapshotRepository.save_snapshot()` of the full runtime state
(both Phase 59.6, reused unmodified); a rejected toggle still writes
one `REJECTED` audit entry but no snapshot and no persisted change.

**TASK 9 (Public API)** — new `configuration/runtime_api.py`
(`enable_feature()`/`disable_feature()`/`feature_status()`/
`list_runtime_features()`, each returning a `RuntimeApiResult`). No
`telegram/` import — the existing one-directional `telegram/` →
`configuration/` dependency stays intact, never reversed.

None of `core/pipeline.py`, `decision/`, `risk/`, `execution/`,
`strategies/`, `signals/`, `context/`, `ai/`, any Telegram handler, or
`telegram/command_router.py` changed in this phase, and none of them
import anything from `configuration/` — a runtime toggle changes only
what `RuntimeFeatureManager`/`runtime_api.py` themselves report.

### Phase 59.8 — Owner Control Center

Consolidates `telegram/owner/`'s five prior modules (Phase 59.3-59.5's
`provider_commands.py`/`system_commands.py`/`feature_commands.py`/
`dataset_commands.py`, Phase 59.4's `report_commands.py`, Phase 59.6's
`owner_roles.py`, Phase 59.7's `configuration/runtime_api.py`) into a
control-center surface — still, per the Director's own roadmap,
**not** registered into `telegram/commands.py`/`command_router.py`/
`handlers.py`. Full detail: `docs/OWNER_COMMANDS.md`'s "Phase 59.8
update" section.

**`status_commands.py`** — new `get_system_status()`, composing
`AdminService.get_system_status()`, `data.providers.registry`,
`config.Config.MARKET_DATA_PROVIDER`/`VALIDATION_MODE`,
`core.system_state.SystemState` (display label only — no instance
held), and `SignalRepository.get_latest_signal()`. No new health-check
logic — pure composition.

**`control_commands.py`** — new `get_feature_states()`/
`enable_feature()`/`disable_feature()`, thin wrappers over
`configuration/runtime_api.py` (Phase 59.7). Deliberately not named
`list_features()` — `feature_commands.py`'s existing function of that
name reports the older *static* Config/FeatureFlags view; this reports
the newer *runtime* view. Both now coexist, disclosed explicitly in
`docs/OWNER_COMMANDS.md` since a future `/features` wiring step must
pick exactly one.

**`report_commands.py`** gained `get_validation_summary()` (additive,
existing `format_daily_stats()`/`pick_best_strategy()` untouched) —
reuses `build_strategy_report()`/`compute_win_rate()` for the
`Signals`/`Win`/`Loss`/`Accuracy`/`Best Strategy` shape.

**`security.py`** — new `require_role()` (ranks `owner_roles.OwnerRole`
against a minimum) and `log_owner_action()` (a convenience
`AuditLogRepository.log_action()` call-through). Foundation only: no
command in this package calls either yet.

**`dashboard.py`** — new `get_dashboard()`, one consolidated overview
composing `status_commands`/`control_commands`/`provider_commands`'
own functions. No new status/health/provider logic.

The `/enable_provider`/`/disable_provider` gap `docs/OWNER_COMMANDS.md`
already disclosed (Phase 59.1) remains open: `config.Config.ENABLE_MT5`/
`ENABLE_TWELVEDATA` are still process-start, `os.getenv()`-read
constants; Phase 59.7's runtime registry tracks a *separate* value
under the same name, not a mutation of `Config` itself.

None of `core/pipeline.py`, `decision/`, `risk/`, `execution/`,
`strategies/`, `signals/`, `context/`, `ai/`, `telegram/handlers.py`,
`telegram/command_router.py`, or `telegram/commands.py` changed in
this phase.

### Phase 59.9 — Emergency Safety Layer Foundation

New `core/emergency/` package — a finer-grained state vocabulary and
runtime controller for the bot's emergency posture, still, per the
Director's own roadmap, **not** wired into `core/pipeline.py`,
`decision/`, `risk/risk_manager.py`, `execution/`, or any Telegram
routing surface. Full detail: `docs/EMERGENCY_SYSTEM.md`.

**`emergency_state.py`** — `EmergencyState` enum
(`NORMAL`/`WARNING`/`PAUSED`/`KILLED`/`MAINTENANCE`) + immutable
`EmergencyStateRecord`. Deliberately separate from
`core.system_state.SystemState` (Phase 59.6) — same "two hierarchies
for two granularities" precedent as `OwnerRole` vs `PermissionLevel` —
because `SystemState` has no `WARNING`/`PAUSED` equivalent that
`circuit_breaker.py` needs. `core/system_state.py` is unchanged.

**`emergency_manager.py`** — `EmergencyManager`:
`activate_pause()`/`activate_kill()`/`activate_maintenance()`/
`restore_normal()`/`get_status()`. Every transition is persisted via
`database.emergency_repository.EmergencyRepository` (append-only —
history is never overwritten, unlike `runtime_features`' one-row-per-
name upsert) and audited via `database.audit_log_repository.AuditLogRepository`
(`KILL_ACTIVATED`/`PAUSE_ACTIVATED`/`MAINTENANCE_ENABLED`/
`SYSTEM_RESTORED`) — the same one-directional `core/` → `database/`
dependency `configuration/runtime_feature_manager.py` already
established for `configuration/` → `database/` (Phase 59.7).

**`circuit_breaker.py`** — pure, stateless `evaluate_circuit()`:
`CircuitBreakerInput` (`loss_count`/`daily_drawdown`/`api_status`/
`execution_error`) → `CircuitDecision` (`ALLOW`/`BLOCK`/`WARNING`) +
reason. No database, no side effects, never called from
`core/pipeline.py` or any pipeline stage in this phase — it returns a
decision, it does not act on one.

**`maintenance.py`** — `MaintenanceMode` (`enabled`/`reason`/
`started_at`/`owner`), a finer-grained detail record for
`EmergencyState.MAINTENANCE`, same "enum value vs. detail record"
split as `FeatureDescriptor` vs `FeatureRuntimeState`.

**`database/emergency_models.py`/`emergency_repository.py`** — new
`emergency_states` table, append-only (mirrors `audit_log`'s own
posture, not `runtime_features`' upsert). `EmergencyRepository.get_current_state()`
derives "current" from the most recent row; `get_history()` returns
the full, never-lost sequence.

**`telegram/owner/emergency_commands.py`** — `kill_system()`/
`pause_system()`/`maintenance_on()`/`restore_system()`/
`get_emergency_status()`, thin wrappers over `EmergencyManager`. Not
registered into `telegram/commands.py`/`command_router.py`/
`handlers.py`, same posture as every Owner Mode module before it.

None of `core/pipeline.py`, `decision/`, `risk/risk_manager.py`,
`execution/`, `strategies/`, `signals/`, `context/`, `ai/`,
`telegram/handlers.py`, `telegram/command_router.py`, or
`telegram/commands.py` changed in this phase. No real order or signal
is blocked by any module in this phase.

### Phase 60.0 — Architecture Audit (no code)

A six-part audit (module dependency graph, dead code, duplicate
logic, database audit, owner audit, pipeline audit) run before any
Phase 60.1+ code, per the Director's explicit "stop coding, audit
first" instruction. Design/documentation only. Full detail:
`docs/PHASE60_ARCHITECTURE_AUDIT.md`. Found and the Director resolved
two real duplicates (`telegram/owner/validation_commands.py`'s
`get_validation_report()` vs `report_commands.py`'s
`get_validation_summary()`; `status_commands.get_system_status()` vs
`system_commands.get_system_health()`) — both decisions recorded, not
yet implemented (a future, separately-approved consolidation phase).
Added the mandatory Module Reuse Principle to `CLAUDE.md` itself.

### Phase 60.1 — Historical Replay Engine

New `backtesting/` package — deliberately not a new `market/`
top-level package (the Director's own Module-Reuse-Principle-guided
decision): Replay is a service over existing Historical Data
(`database.raw_candle_repository.RawCandleRepository`, Phase
59.3/59.5), not a new business domain. Still, per the Director's own
explicit rule, **not** wired into `core/pipeline.py`, `strategies/`,
`signals/`, `decision/`, `risk/`, or `execution/` — Replay replaces
only the data source, never the trading algorithms. Full detail:
`docs/REPLAY_ENGINE.md`.

**`replay_models.py`** — `ReplayState` enum
(`PENDING`/`RUNNING`/`PAUSED`/`STOPPED`/`FINISHED`), frozen
`ReplayConfig`/`ReplayResult`, and `format_replay_report()` (folds
TASK 7 into this file rather than a 7th module — the Module Reuse
Principle applied at the package's own internal scope).

**`replay_session.py`** — `ReplaySession`: one replay run's identity
and progress bookkeeping only, no candle traversal or timing logic of
its own (that's `replay_feed.py`'s/`replay_clock.py`'s job).

**`replay_clock.py`** — `ReplayClock`: a pure play/pause/resume/stop/
speed/seek state machine over an integer position, no candle-data
knowledge. Position starts at `-1` (matching `ReplayFeed.cursor`'s own
convention) so `replay_engine.py` can keep the two in lockstep without
an off-by-one.

**`replay_feed.py`** — `ReplayFeed`: cursor-based `next`/`previous`/
`jump`/`window`/`current` access over an already-loaded candle list.
Hands out `data.twelve_data_client.Candle` — the exact type
`data.market_data.MarketDataNormalizer.get_candles()` already returns
to the live pipeline, so a future Strategy consumer needs no shape
change to accept replayed data instead of live data.

**`replay_engine.py`** — `ReplayEngine`: composes
`RawCandleRepository` (loads the configured window once, via this
phase's own additive `get_candles_range()`), `ReplayClock`, and
`ReplayFeed`. `step()` advances both together and returns the new
current `Candle`; never calls `strategies/`/`signals/`/`decision/`/
`risk/`.

**`replay_controller.py`** — `ReplayController`: the public
session-management API (`start()`/`pause()`/`resume()`/`stop()`/
`restart()`/`step()`/`get_status()`), one process-local
`{session_id: (ReplaySession, ReplayEngine)}` map — no database table,
same "in-memory holder" convention as
`configuration.runtime_state.RuntimeStateCache`.

**`telegram/owner/replay_commands.py`** — `replay_start()`/
`replay_pause()`/`replay_stop()`/`replay_status()`, thin wrappers over
`ReplayController`. Not registered into `telegram/commands.py`/
`command_router.py`/`handlers.py`, same posture as every Owner Mode
module before it.

**`database/raw_candle_repository.py`** gained one additive method,
`get_candles_range(symbol, timeframe, start, end, provider=None)` —
TASK 1's own reuse-audit finding: the existing `get_candles()` only
supports "most recent N rows," no date bound, which a fixed
historical replay window needs. `get_candles()` itself is unchanged.

None of `core/pipeline.py`, `decision/`, `risk/risk_manager.py`,
`execution/`, `strategies/`, `signals/`, `context/`, `ai/`,
`telegram/handlers.py`, `telegram/command_router.py`, or
`telegram/commands.py` changed in this phase.

### Phase 60.2 — Backtesting Engine

The full Replay → Strategy → Signal → Decision → Risk → Paper Trade →
Analytics chain, built entirely by composing already-existing,
unmodified functions — no Strategy/Signal/Decision/Risk logic is
reimplemented anywhere. Still, per the Director's own explicit rule,
**not** wired into `core/pipeline.py` or any live routing surface.
Full detail: `docs/BACKTESTING_ENGINE.md`.

**`backtesting/data_feed.py`** — `IDataFeed` (ABC) + `LiveDataFeed`/
`ReplayDataFeed`. Per the Director's own rule ("no `if backtest: ...
else: ...`"): TASK 1's reuse audit found `strategies/`/
`signals/signal_engine.py` were already source-agnostic (they consume
`ContextSnapshot`, never a candle source directly) — the real seam is
one level up, between the live `market_data` stage
(`MarketDataNormalizer.get_candles()`) and Phase 60.1's `ReplayFeed`.
`IDataFeed` unifies exactly those two.

**`backtesting/backtest_engine.py`** — `BacktestEngine`: composes
`ReplayEngine` (Phase 60.1), `build_context_snapshot()`,
`compute_market_phase()`, `SignalEngine().generate_signals()`,
`compute_signal_quality()`, `AIAnalyzer().analyze()`,
`DecisionEngine().evaluate()`, `RiskManager().evaluate()`,
`from_signal_candidate()`, `create_paper_trade()`/`open_paper_trade()`,
`check_paper_trade_against_candles()`, and
`compute_signal_performance()` — every one read directly from source
this phase and left unmodified. The APPROVE+risk-approved gate for
opening a `PaperTrade` was copied verbatim from `core/pipeline.py`'s
own `run()`. Two documented, deliberate differences from live (not
trading-logic changes): every approved+risk-approved candidate opens a
trade (not just the single highest-confidence one per cycle, since
live's "one Telegram message per cycle" constraint doesn't apply to
measuring strategy performance), and HTF Bias defaults to a neutral
fallback (`compute_htf_bias(MarketSnapshot(symbol=...))`, the same
degrade path `core/pipeline.py` itself already uses on a live HTF
fetch failure) since true multi-timeframe HTF replay is out of scope
for this phase.

**`backtesting/backtest_result.py`** — `BacktestResult` + `build_backtest_result()`
(wraps `analytics.strategy_report.build_strategy_report()`, unmodified)
+ `format_backtest_report()`.

**`telegram/owner/backtest_commands.py`** — `backtest_run()`, a thin
wrapper running a full `BacktestEngine` pass synchronously. Not
registered into `telegram/commands.py`/`command_router.py`/
`handlers.py`.

**A genuine Phase 60.1 bug found and fixed during this phase's own
validation**: `ReplayEngine.is_finished`'s `self.feed.is_exhausted and
self.feed.cursor >= 0` condition infinite-looped for a zero-candle
dataset — `ReplayFeed.jump()` always clamps the cursor back to `-1`
when there are no candles at all, so the `cursor >= 0` half could
never become `True`. Fixed to just `self.feed.is_exhausted` (already
correct for every case on its own); a regression test now covers the
empty-dataset edge case, bounded so a future regression fails fast
instead of hanging CI. See `docs/BACKTESTING_ENGINE.md`'s own section
on this for the full root-cause writeup.

None of `core/pipeline.py`, `decision/`, `risk/risk_manager.py`,
`execution/`, `strategies/`, `signals/`, `context/`, `ai/`,
`telegram/handlers.py`, `telegram/command_router.py`, or
`telegram/commands.py` changed in this phase.

### Phase 60.3 — Execution Simulator Foundation

New `execution/simulator/` subpackage — deliberately inside the
*existing* `execution/` top-level package, not a new `simulation/`
package. TASK 1's reuse audit read `execution/execution_engine.py`/
`execution/signal_lifecycle.py` directly: both are still deliberately
inert stubs, nothing to reuse, and extending either would blur the
"intentionally inert, needs separate approval" line `CLAUDE.md` draws
around live execution — so this phase leaves both files completely
untouched. Full detail: `docs/EXECUTION_SIMULATOR.md`.

**`models.py`** — `SimulatedOrder`/`SimulatedFill`/
`ExecutionSimulationResult`. Deliberately not named `ExecutionResult`
(that name already belongs to `execution_engine.py`'s own, unrelated,
still-inert dispatch stub).

**`slippage.py`**/**`spread.py`**/**`latency.py`** — deterministic
(not stochastic) `SlippageConfig`/`SpreadConfig`/`LatencyConfig` +
pure functions, matching the Director's own worked examples (BUY
2350.00 → fill 2350.15; London 0.15 / NY news 0.80 spread; 2000ms
latency). Deterministic so a `backtesting/` run stays reproducible.

**`simulator_engine.py`** — `ExecutionSimulator.simulate(paper_trade,
risk_result, session=None, signal_time=None)`: reads an already-OPEN
`PaperTrade` + its `RiskResult` (Decision already APPROVEd, Risk
already approved — this module re-checks neither), computes
`fill_price = apply_slippage(requested_price, direction,
slippage_points + spread_points)`, and rejects (no fill) when the
session's spread is at or above the configured maximum. Never mutates
the `PaperTrade` it reads; never calls `execution_engine.py`,
`decision/`, or `risk/`.

**`analytics/execution_report.py`** (TASK 8) — `ExecutionAnalyticsRecord`/
`ExecutionAnalyticsSummary` + `build_execution_record()`/
`summarize_execution_records()`/`format_execution_record()`. Packages
an already-computed `ExecutionSimulationResult` (requested price, fill
price, slippage, spread, latency, rejection reason) for later
comparison against real MT5 fills, per the Director's own brief. No
new execution logic.

### Phase 60.4 — Performance Validation Foundation

Three new `analytics/` modules, all in-memory-only (no new database
table — TASK 6's own decision, matching every prior analytics module).
Full detail: `docs/PERFORMANCE_VALIDATION.md`.

**`performance_metrics.py`** — `PerformanceMetrics` +
`compute_performance_metrics(performances, equity_curve=None)`.
Portfolio-wide expectancy/profit-factor/risk-adjusted-return, all
R-based (no PnL model exists anywhere in this codebase). Max
Drawdown/Recovery Factor stay `None` unless an already-built equity
curve is supplied.

**`equity_curve.py`** — `EquityCurveConfig`/`EquityPoint` +
`build_equity_curve()`/`max_drawdown()`. One disclosed,
visualization-only assumption (`unit_risk_amount`, a configurable
dollar-per-1R) bridges the "no PnL model exists" gap to match the
Director's own worked example (`1000$ -> +30 -> 1030$`).
`risk/risk_manager.py` is untouched.

**`benchmark.py`** — `BenchmarkComparison` +
`compute_benchmark_comparison(equity_curve, benchmark_start_price,
benchmark_end_price)`, matching the Director's own worked example
(`Gold +5%, Strategy +18% -> Alpha: +13%`). Does not read candles
itself — the caller supplies both benchmark prices.

**`telegram/owner/performance_commands.py`** (TASK 7) —
`get_performance_report()`/`get_equity_curve_report()`/
`get_backtest_performance_report()`, thin wrappers over the three
modules above. Not wired into the live bot.

**TASK 5 (Validation Report duplicate)** — re-audited, not touched:
`docs/PHASE60_ARCHITECTURE_AUDIT.md`'s own finding 1 / Director
decision 1 already recorded the resolution (`get_validation_summary()`
kept, `get_validation_report()` deprecated) as a future,
separately-approved step, not an instruction to refactor
`telegram/owner/` in this pass — this phase confirms the finding still
holds and leaves both functions unchanged.

**`telegram/owner/execution_commands.py`** — `execution_status()`/
`slippage_status()`/`set_simulation_mode()`, thin wrappers reporting
already-computed config. `set_simulation_mode()` selects a named
session preset (`DEFAULT`/`LONDON`/`NY_NEWS`) in an in-memory-only
holder — not persisted, not wired into `telegram/commands.py`/
`command_router.py`/`handlers.py`.

None of `core/pipeline.py`, `decision/`, `risk/risk_manager.py`,
`execution/execution_engine.py`, `execution/signal_lifecycle.py`,
`strategies/`, `signals/`, `context/`, `ai/`, `lifecycle/paper_trade.py`,
`telegram/handlers.py`, `telegram/command_router.py`, or
`telegram/commands.py` changed in this phase.

### Phase 60.5 — Fundamental Intelligence Foundation

A **Macro Context Engine**, not a signal generator, per the Director's
own hard rule: this layer never returns "BUY"/"SELL" and never opens a
trade — only a macro bias (`BULLISH GOLD`/`BEARISH GOLD`/`NEUTRAL`), a
confidence, and reasons. `decision/decision_engine.py` is unchanged;
this phase adds no connection to it. Full detail:
`docs/FUNDAMENTAL_INTELLIGENCE.md`.

TASK 1's reuse audit found two of the Director's own brief's suggested
new paths already had a better home and were not created: a new
`context/fundamental/` subpackage (this phase extends the existing
`context/fundamental_context.py` instead, plus two flat sibling files
— `context/` has no subpackages today, and Module Reuse Principle
counsels against introducing the first one for this alone) and a new
`ai/fundamental_prompt.py` (this phase adds one method to the existing
`ai/prompts/prompt_manager.py`'s `PromptManager` instead).

**`context/fundamental_context.py` extensions (TASK 2/6)** —
`FundamentalContextSnapshot` gained eight new `Optional` fields
(`dxy_bias`/`rates_bias`/`inflation_bias`/`fed_expectation`/
`risk_sentiment`/`gold_bias`/`confidence`/`macro_score`, all default
`None`) plus `merge_fundamental_score()`. `compute_fundamental_context()`
itself is unchanged. New `EnrichedContextSnapshot` +
`attach_fundamental_context()` pair a real `ContextSnapshot` with a
`FundamentalContextSnapshot` by composition — `ContextSnapshot` itself
was deliberately not touched, since its own docstring states "no
defaults by design," a stable contract every existing caller
(`core/pipeline.py`, `backtesting/backtest_engine.py`) depends on.

**`data/providers/fred_provider.py` extension (TASK 3)** —
`FredProvider.collect_snapshot()`, a new method (not a new file)
composing the three fetch methods into one `FundamentalSnapshot`,
catching each `NotImplementedError` individually. Still no real
`api.stlouisfed.org` connection — that needs an API key and is a
separate, explicitly-approvable future step.

**`context/economic_events.py`** (TASK 4) — `EventImpact` +
`EconomicEvent` (`name`/`date`/`impact`/`currency`/`expected`/`actual`
+ a computed `surprise` property). Data model only, no provider yet.

**`context/fundamental_scoring.py`** (TASK 5) —
`FundamentalScoreWeights`/`FundamentalScoreResult` +
`compute_fundamental_score()`/`explain_fundamental_score()`/
`format_fundamental_score()`. Aggregates already-classified
per-indicator biases (supplied by a future analyst/AI layer, not
computed here — no threshold/calibration model exists) into one
`gold_bias`/`confidence`/`macro_score`, matching the Director's own
"Macro Bias / Confidence / Reasons" worked example shape. The
Director's own illustrative numbers (`DXY: -20, Rates: -15,
Inflation: +10, Risk: +15 -> Gold Score: +70`) do not arithmetically
sum to +70, so this module reproduces the shape, not the literal
numbers.

**`ai/prompts/prompt_manager.py` extension (TASK 7)** —
`PromptManager.get_fundamental_analysis_prompt()`, one new method
combining technical + fundamental context into an explanation-only
template. No LLM call, no network access, same posture as every other
method on this class.

**`telegram/owner/fundamental_commands.py`** (TASK 8) —
`get_macro_status()`/`get_fundamental_score_report()`/`get_fed_status()`,
thin wrappers over the modules above. Not wired into the live bot.

No new database table (TASK 9's own decision, matching every prior
foundation phase). None of `core/pipeline.py`, `decision/`, `risk/`,
`execution/`, `strategies/`, `signals/`, `telegram/handlers.py`,
`telegram/command_router.py`, or `telegram/commands.py` changed in
this phase.

### Phase 60.6 — Learning Loop Foundation

A learning *foundation*, not an autonomous learner, per the
Director's own hard rule: `observe -> analyze -> report`, never
`observe -> mutate`. Nothing in this phase reads a `LearningRecord`/
`PatternInsight` back into `strategies/`, `decision/`, or `risk/` to
change behavior, and nothing here changes a strategy parameter,
confidence threshold, or risk value. Full detail:
`docs/LEARNING_LOOP.md` (architecture diagram, safety rules, future
AI training plan) and `docs/LEARNING_LOOP_AUDIT.md` (TASK 1's reuse
findings).

New top-level `learning/` package — TASK 1's reuse audit found no
existing pattern-detection or persisted-learning-memory module
anywhere in this codebase; `analytics/signal_performance.py`'s
`SignalPerformance` shares 7 of `LearningRecord`'s 11 fields but is an
in-memory, computed-on-demand analytics type with no persistence
story, a different lifecycle from an append-only learning memory.

**`learning/models.py`** (TASK 2) — `LearningRecord` (`record_id`,
`trade_id`, `signal_id`, `strategy_name`, `market_phase`, `session`,
`timeframe`, `result`, `r_multiple`, `failure_type`,
`success_pattern`, `created_at`). `id` deliberately excluded — same
convention `AuditLogEntry` already established.

**`learning/outcome_analyzer.py`** (TASK 3) — `TradeAnalysis` +
`analyze_trade_result(paper_trade, context=None, performance=None,
htf_bias=None)`. Purely observational: reads only already-detected
structural facts (BOS/CHoCH/liquidity sweep/order block/FVG presence,
HTF-direction alignment) — no new detection logic anywhere.

**`learning/pattern_detector.py`** (TASK 4) — `PatternInsight` +
`detect_patterns()`/`filter_high_failure_patterns()`/
`filter_high_success_patterns()`/`format_pattern_insight()`. Groups by
`(strategy_name, session, market_phase)`, reusing
`analytics.strategy_report.compute_win_rate()` directly. Does not
parse `failure_type`/`success_pattern` free text into structured
sub-conditions — a most-common-string example only, never a
generalized rule.

**`database/learning_models.py` + `learning_repository.py`** (TASK 5)
— `LearningRecordRow` + `LearningRepository`, mirroring
`database/audit_log_repository.py`'s structure exactly. Append-only:
**no `update()`/`delete()` method exists**. New `learning_records`
table (`init_learning_schema()` in `database/models.py`).

**`analytics/learning_report.py`** (TASK 6) — `LearningReport` +
`build_learning_report()`/`format_learning_report()`, reusing
`detect_patterns()` directly to pick the best/worst condition —
matches the Director's own "Last 100 trades / Best condition / Worst
condition" worked example shape.

**`ai/learning_context.py`** (TASK 7) — `LearningContext` +
`build_learning_context()`, matching the Director's own
`{recent_failures, successful_patterns, strategy_stats}` JSON shape.
Generates no explanation/recommendation text itself — left to a
future AI consumer, still bound by `AIAnalyzerInterface`'s
advisory-only contract.

**`telegram/owner/learning_commands.py`** (TASK 8) —
`get_learning_status()`/`get_patterns_report()`/`get_failures_report()`/
`get_best_conditions_report()`, thin wrappers over the modules above.
Not wired into the live bot.

No wiring exists yet from a real closed `PaperTrade` to
`LearningRepository.record()` — a separate, future, explicitly-
approvable step, same "foundation, not observed yet" gap every module
in this phase discloses. None of `core/pipeline.py`, `decision/`,
`risk/`, `execution/`, `strategies/`, `signals/`, `telegram/handlers.py`,
`telegram/command_router.py`, or `telegram/commands.py` changed in
this phase.

### Phase 60.7 — Adaptive Intelligence Layer Foundation

Closes Phase 60.6's own disclosed gap and extends every module built
there — still `observe -> analyze -> report`, never
`observe -> mutate`. Full detail: `docs/LEARNING_LOOP.md`'s Phase 60.7
section, `docs/ADAPTIVE_INTELLIGENCE_AUDIT.md`.

**A genuine Phase 60.2 bug found and fixed during TASK 1's own
audit** — `backtesting/backtest_engine.py`'s `_process_candidate()`
never captured `open_paper_trade()`/`check_paper_trade_against_candles()`'s
returned trade (both pure, frozen-dataclass functions), so every
backtest's `PaperTrade` stayed `CREATED` forever and
`SignalPerformance.result` was silently `None` for every trade since
Phase 60.2 shipped. Fixed (three lines, confined to that one file);
see `backtest_engine.py`'s own module docstring for the full writeup.

**`learning/trade_event_bridge.py`** (TASK 2) —
`build_learning_record_from_trade()`/`bridge_closed_trade()`, the
first real caller of `LearningRepository.record()`. This package's one
disclosed exception to "does not persist anything itself"
(dependency-injected `LearningRepository`, same posture
`telegram/*_service.py` already uses).

**Enhanced Learning Schema** (TASK 3) — `LearningRecord`/
`LearningRecordRow`/`learning_records` all gained six additive fields
(`htf_bias`/`volatility_state`/`fundamental_bias`/`confidence_score`/
`engine_version`/`sample_size`), migrated via a `PRAGMA table_info()`-
guarded `ALTER TABLE`, same pattern `signals`/`users` already
established. Every Phase 60.6 caller/test keeps working unmodified.

**Advanced Pattern Detector** (TASK 4) — `detect_patterns()`'s
grouping key extended to a 5-tuple (`+ htf_bias, volatility_state`) —
additive, identical groups for any pre-existing record set. New
`MIN_PATTERN_SAMPLE = 20` constant (consumed by TASK 5, not by
`detect_patterns()`'s own unchanged `min_occurrences=3` exclusion
gate). Grouping logic extracted into a reusable
`group_records_for_patterns()` helper (behavior-preserving refactor).

**`learning/confidence.py`** (TASK 5) — `PatternConfidence` +
`compute_pattern_confidence()`: LOW/MEDIUM/HIGH from four 0.0-1.0
sub-scores, with sample size as a **multiplicative gate**
(`sample_size_score * mean(consistency, recency, performance)`) rather
than a fourth additive term — a plain average would let a tiny,
perfect-looking pattern reach HIGH, contradicting the Director's own
worked example directly (caught by the worked-example test itself
during this phase).

**AI Memory Adapter** (TASK 6) — `ai/learning_context.py`'s
`LearningContext` gained `patterns`/`failures`/`regimes`/`confidence`
alongside the unchanged Phase 60.6 three. `regimes` is a
caller-supplied `Sequence[str]`, not an import of
`learning.regime_memory` — loose coupling between TASK 6 and TASK 7.

**`learning/regime_memory.py`** (TASK 7) — `RegimeMemory` +
`record_from_context()` + `format_regime_summary()`, an in-memory,
per-process log of the Director's own five named regimes. Four map
onto `context.market_regime.MarketRegime` directly; `NEWS_EVENT` has
no detector anywhere in this codebase and is only recorded when a
caller supplies it explicitly.

Nothing in this phase calls `bridge_closed_trade()` from
`backtesting/backtest_engine.py`'s own loop — the bridge exists and is
tested end-to-end, but wiring it into a real run is a separate, future
step. None of `core/pipeline.py`, `decision/`, `risk/`, `execution/`,
`strategies/`, `signals/`, `telegram/handlers.py`,
`telegram/command_router.py`, or `telegram/commands.py` changed in
this phase.

### Pre-Phase 59 Architecture Readiness Review (AC-01–AC-07)

A Director-requested audit run after Phase A19, before Phase 59 Real
Market Validation, checked nine previously-built foundation modules
(HTF Bias, Wyckoff/AMD, Signal+Context linkage, Asset Abstraction,
Strategy Lifecycle, Performance Analytics, Session Intelligence, Data
Quality, Explainability) against the roadmap's original request. Full
detail, including file:line evidence for every item: see
`docs/ARCHITECTURE_READINESS_REVIEW.md`. Two outcomes:

**Six items were already complete and correctly wired** (AC-01 HTF
Bias, AC-04 Asset Abstraction, AC-05 Strategy Lifecycle, AC-06
Performance Analytics being correctly kept distinct from A19, plus
Session Intelligence and Explainability) — verified, not rebuilt, per
this codebase's "No duplicate logic" rule. **Three items had a real,
narrow gap**, closed in this review:

**Market Phase Foundation (AC-02)** — `context/market_phase.py` adds
`MarketPhase` (`ACCUMULATION`/`MANIPULATION`/`DISTRIBUTION`/`MARKUP`/
`MARKDOWN`/`UNKNOWN`) and `compute_market_phase(context)`, extending
the pre-existing 2-state `WyckoffPhase` into the Director's requested
5-state model (plus `UNKNOWN`, a safe fallback added by direct analogy
to every other classification enum in this codebase — e.g. `HTFBias`,
`MarketRegime` — not one of the Director's own 5 listed values,
disclosed explicitly). Priority order, mirroring
`context/market_regime.py`'s own established pattern: most recent
Wyckoff Spring/Upthrust event (most specific) → most recent AMD event
→ confirmed `TRENDING` `MarketRegime` direction → `UNKNOWN`. Computes
nothing new — reads only `context.wyckoff_events`, `context.amd_events`,
and `context.market_regime`, all already fields on `ContextSnapshot`
today. New `core/pipeline.py` stage immediately after `context`;
`"market_phase"` is a new key in `run()`'s result dict, advisory only
(not consumed by Decision Engine, Risk Manager, or any strategy).

**Signal History Foundation (AC-03)** — the review's highest-priority
item. `core/pipeline.py`'s new `signal_history` stage (immediately
after `risk`, before candidate selection) is the first place in this
codebase that connects `signals/schema.py` (Phase A15) and
`context/snapshot.py` (Phase A16) — both previously built with "zero
pipeline wiring" — into a live record. Per cycle: one
`ContextSnapshotSchema` is built via `from_context_snapshot()`; then,
per candidate, one `SignalSchema` is built via `from_signal_candidate()`
with `context_id=context_snapshot.snapshot_id` (the two sides of the
same link) and a freshly generated `decision_id=str(uuid.uuid4())`
(mirroring `database/signal_record.py`'s own `signal_id` generation
convention — `decision.models.TradeDecision`, a Trading-Safety-protected
file, is deliberately left with no id field of its own). `strategy_id`
needed no new field: `SignalSchema.strategy_name` (Phase A15) already
carries the same value as `StrategyDefinition.id` (Phase A11, e.g.
`"LIQUIDITY_SWEEP_STRATEGY"`). `SignalSchema` gained one genuinely new
field, `decision_id: Optional[str] = None` (now 20 fields total).
`"context_snapshot"` and `"signal_history"` (a `List[SignalSchema]`)
are new keys in `run()`'s result dict — this review does **not** add a
database table or migration; "written to history" is satisfied by
these now-linked, `to_json()`-serializable records being available for
a future persistence step, not by persisting them today (see
`docs/ARCHITECTURE_READINESS_REVIEW.md`'s AC-03 section for the full
scope decision).

**API Error Classification (AC-07, part of Data Quality)** —
`data/api_error_classifier.py` adds `classify_api_error(exception,
module)`, mapping an already-caught data-fetch exception to a
`core.errors.exceptions.ExternalAPIError` (Phase A18) — `API_001` for
a timeout/connection failure, `API_002` for anything else (rate limit,
malformed response, unrecognized type). Never raises; used for
structured logging only. `data/market_data.py`'s `get_candles()`
gained exactly one additional `logger.error(...)` call inside its
pre-existing `except Exception as e:` block — the graceful
degrade-to-`[]` return and all control flow are unchanged, verified by
dedicated tests. `data/twelve_data_client.py`'s retry/backoff logic and
raise behavior are untouched.

Neither `strategies/`, `signals/` (candidate generation), `risk/`, nor
`decision/decision_engine.py` changed in this review — every item
above is either read-only verification or an additive, advisory record
built from already-computed values.

### Phase 59 Preparation (TASK 1-6)

Audit before Phase 59 Real Market Validation, closing the same kind of
narrow, verified gaps as the Architecture Readiness Review above — no
new trading logic, and none of `strategies/`, `signals/` (candidate
generation), `decision/decision_engine.py`, `risk/risk_manager.py`, or
`ai/` changed. Full detail: `docs/PHASE59_VALIDATION.md`.

**Architecture Final Verification (TASK 6)**: the live pipeline stage
order in `core/pipeline.py` is unchanged by this phase and confirmed
to still exactly match the Data Flow diagram and stage-by-stage prose
above (`market_data` → `data_quality` → `htf_bias` → `context` →
`market_phase` → `signal` → `signal_quality` → `explainability` →
`features` → `ai` → `decision` → `risk` → `signal_history` →
`telegram_format` → `telegram_delivery` → `database`). Every module's
Input/Output/Dependency contract is already documented in
`contracts/*.md` (Phase A17) — verified current, not rewritten. Three
new, standalone foundation packages were added; none is part of the
pipeline sequence above:

- **`data/market_data_snapshot.py`** (TASK 1) — `MarketDataSnapshot`,
  a lightweight window-identity/fingerprint record (`symbol`,
  `timeframe`, `candle_count`, `first_timestamp`, `last_timestamp`,
  `candles_reference`), closing the audit finding that the `signals`
  database table stores no candle data and its own `symbol` column is
  never actually populated (`database/signal_repository.py`'s
  `save_signal_record()` hardcodes `data["symbol"] = ""`) — so market
  state at signal time could not be reconstructed before this phase.
  Deliberately not a full candle store (no database migration, per
  this task's own boundary) — `candles_reference` is a content
  fingerprint for future re-fetch/verification, not a foreign key.
  Distinct from the pre-existing `data.market_data.MarketSnapshot`
  (live, multi-timeframe, never persisted) — see the module's own
  naming note.
- **`lifecycle/`** (TASK 2 + TASK 4, new top-level package) —
  `paper_trade.py` (`PaperTrade`, `TradeState` CREATED/OPEN/CLOSED/
  CANCELLED, and pure `create_`/`open_`/`close_`/`cancel_paper_trade()`
  transition functions) simulates the `Signal → Decision APPROVED →
  Paper Trade OPEN → Monitor → CLOSE → Result` flow with zero broker
  calls, zero real orders, and zero risk-sizing change.
  `signal_state.py` (`SignalLifecycleState` CREATED/QUALITY_CHECKED/
  EXPLAINED/APPROVED/REJECTED/PAPER_OPEN/CLOSED, `transition_signal_state()`,
  `derive_signal_lifecycle_state()`) names a signal's own progress
  through the analysis pipeline for the first time. Not the same
  concept as `strategies/lifecycle/` (per-strategy metadata, Phase
  A11) or `execution/signal_lifecycle.py` (a pre-existing, still-inert
  Telegram-delivery state machine, untouched — its own `SignalState`
  enum is deliberately not reused, to avoid a same-name collision with
  this module's differently-scoped `SignalLifecycleState`). No
  database persistence, no pipeline wiring.
- **`analytics/`** (TASK 3, new top-level package) —
  `signal_performance.py` (`SignalPerformance`,
  `compute_signal_performance()`) and `strategy_report.py`
  (`StrategyPerformanceReport`, `build_strategy_report()`) — **trading**
  performance (win/loss/R-multiple by strategy/session/market phase),
  never to be confused with `performance/` (Phase A19, **system**
  timing) — the exact distinction this task's own brief required.
  Deliberately does not duplicate `monitoring/performance.py`'s
  pre-existing `PerformanceTracker` (a real, working, database-driven
  strategy win-rate calculator) — `strategy_report.py` reuses its
  exact `WIN / (WIN + LOSS)` formula by convention, disclosed, not
  hidden, rather than inventing a competing definition of "win rate."
  `profit_loss` stays an honest `None` hook — no PnL/lot-value
  computation exists anywhere in this codebase, and building one is
  out of this task's "Risk o'zgarmaydi" boundary.

**TASK 5** (`docs/PHASE59_VALIDATION.md`) is documentation only — no
module. It fixes the 7-day validation report's exact metric
definitions in advance, and honestly discloses which are computable
today (Signal totals, per-strategy identifiers, Market Context) versus
which need a still-unbuilt persistence/monitor step (Result, Risk) —
see that document's own "Known gaps" section.

None of `data/market_data_snapshot.py`, `lifecycle/`, or `analytics/`
is imported by `core/pipeline.py`, `execution/`, or `database/` in
this phase — each is a standalone, tested foundation, the same
"foundation, not a rewrite" posture every Phase A/AC module has used,
ready for a future, separately-approved wiring/persistence step.

### Phase 59.1 — Market Data Provider Abstraction & TwelveData Integration Foundation

GoldBot needs to run without an always-on MT5 terminal (no owner PC
available today). Full detail: `docs/MARKET_PROVIDER.md`. New,
standalone package `data/providers/` (`base_provider.py`'s
`MarketDataProvider` abstract contract + `MarketCandle`/`ProviderStatus`,
`twelve_data_provider.py`'s `TwelveDataProvider` wrapping the existing,
untouched `data.twelve_data_client.TwelveDataClient`,
`mt5_provider.py`'s deliberately inert `MT5Provider` stub,
`__init__.py`'s `get_provider()` factory) — not imported by
`core/pipeline.py` or `data/market_data.py` in this phase; the live
pipeline's data path is unaffected. A provider never generates a
signal, never knows about a strategy or a decision — data only.

`config.py` gained `MARKET_DATA_PROVIDER`/`ENABLE_MT5`/
`ENABLE_TWELVEDATA` (additive, `Config.DEBUG`'s existing `os.getenv()`
convention). `core/errors/codes.py`'s registry gained `API_003`
(invalid symbol) and `API_004` (empty response); `data/api_error_classifier.py`
gained `classify_empty_response()` and a disclosed message-heuristic
for `API_003`. `data/market_data_snapshot.py`'s `MarketDataSnapshot`
(Phase 59 Preparation) gained two optional, additive fields
(`provider`, `data_quality`), both defaulting `None`. None of
`strategies/`, `signals/` (candidate generation), `decision/decision_engine.py`,
`risk/risk_manager.py`, or `ai/` changed.

## Module Responsibilities (summary — full detail in `docs/code_structure.md`)

| Module | Responsibility |
|---|---|
| `core/` | Cross-cutting infrastructure: pipeline orchestration, logging, secrets, and (Phase A18) the `GoldBotError` exception hierarchy (`core/errors/`) — implemented, not yet wired into any existing raise site. Phase 59.6 added `system_state.py` — `SystemState`/`SystemStateRecord`, a pure model with no mutable "current state" holder and no pipeline wiring. Phase 59.9 added `emergency/` — `EmergencyState`/`EmergencyManager` (a runtime controller, persisted append-only via `database.emergency_repository`, audited via `AuditLogRepository`) and stateless `circuit_breaker.evaluate_circuit()`; still gates nothing in `core/pipeline.py`/`decision/`/`risk/`/`execution/`. |
| `backtesting/` | New in Phase 60.1 (Historical Replay Engine) — `replay_models.py`/`replay_session.py`/`replay_clock.py`/`replay_feed.py`/`replay_engine.py`/`replay_controller.py`. A service over existing Historical Data (`database.raw_candle_repository.RawCandleRepository`), not a new business domain — deliberately not a `market/` top-level package, per the Module Reuse Principle. `ReplayFeed` hands out `data.twelve_data_client.Candle`, the same type the live pipeline already uses, so a future Strategy consumer needs no shape change. Phase 60.2 (Backtesting Engine) added `data_feed.py` (`IDataFeed`/`LiveDataFeed`/`ReplayDataFeed`), `backtest_engine.py` (`BacktestEngine`, composing `strategies/`/`signals/`/`ai/`/`decision/`/`risk/`/`lifecycle/`/`analytics/` unmodified), and `backtest_result.py`. Still never *modifies* `strategies/`/`signals/`/`decision/`/`risk/`; nothing in `core/pipeline.py` constructs anything here. |
| `configuration/` | Configuration & Feature Flags foundation (Phase A13) — `Environment`/`ApplicationSettings`/`FeatureFlags`, additive to `config.py` (untouched). Every feature flag defaults `False`; no pipeline wiring. Phase 59.6 added `feature_registry.py` (`FeatureDescriptor`/`build_feature_registry()`, unifying real + declared-only flag names) and `feature_dependency_validator.py` (`validate_feature_dependencies()`) — still not runtime, gates nothing. Phase 59.7 added the first genuinely *runtime* control in this package — `runtime_state.py`/`runtime_feature_manager.py`/`runtime_api.py` (`RuntimeFeatureManager`: validated, persisted, audited, snapshotted enable/disable) — still gates nothing in `core/pipeline.py`/`decision/`/`risk/`/`execution/`, none of which import `configuration/`. |
| `assets/` | Asset Intelligence foundation (Phase A12) — `AssetDefinition`/`AssetRegistry`, one metadata record per tradable asset (symbol, type, market, currency, plus seven not-yet-implemented `None` hooks). Registers only `GOLD_ASSET` (XAUUSD) today; no market data, no execution, no pipeline wiring. |
| `data/` | Market data fetch and normalization, plus Data Quality assessment (`data_quality.py`, Phase A8) — observational scoring, not filtering — API error classification (`api_error_classifier.py`, AC-07/Phase 59.1 TASK 5) — maps a caught fetch exception (or a known empty-response condition) to a structured `ExternalAPIError` for logging only, never changes control flow — Market Data Snapshot (`market_data_snapshot.py`, Phase 59 Preparation/59.1) — a lightweight, unwired window-identity/fingerprint record for a future replay/backtesting step; not a full candle store — and Market Provider Abstraction (`providers/`, Phase 59.1) — `DataProvider`/`MarketDataProvider`/`FundamentalDataProvider`, `TwelveDataProvider`/`MT5Provider`/`BinanceProvider`/`FredProvider`, `ProviderRegistry`, data-only, not wired into the live pipeline — plus Provider Normalization (`normalization/`, Phase 59.3) — `symbol_mapper.py`/`timeframe_mapper.py`/`candle_normalizer.py`, centralized per-provider format tables, no new candle type. |
| `context/` | Pure SMC market-structure detection functions (structure, BOS/CHoCH, liquidity, OB, FVG, AMD, Wyckoff Spring/Upthrust — Phase A5, Session classification — Phase A6, and Market Regime — Phase A7, all part of `ContextSnapshot`), plus HTF Bias (`htf_bias.py`, Phase A2) — a market-context-only Daily/H4/H1 classification, not itself part of `ContextSnapshot`. `snapshot.py` (Phase A16) additionally standardizes a `ContextSnapshot` into a flat, JSON-serializable `ContextSnapshotSchema`, now wired into `core/pipeline.py`'s `signal_history` stage (AC-03) — a distinct type, not a replacement. `market_phase.py` (AC-02) adds a wired, advisory 5-state (+`UNKNOWN`) `MarketPhase` classification reusing already-detected Wyckoff/AMD/Market Regime data. `fundamental_context.py` (Phase 59.3) adds `compute_fundamental_context()` — a pure adapter connecting `data/providers/fred_provider.py` (Phase 59.2) into a new `FundamentalContextSnapshot`; not called by anything in this phase. |
| `strategies/` | Independent signal-candidate generation per SMC methodology, plus a Strategy Lifecycle metadata layer (`lifecycle/`, Phase A11) — `StrategyDefinition`/`StrategyRegistry`, storing status/version/supported-assets metadata only, never running a strategy or generating a signal. |
| `signals/` | The `SignalCandidate` data contract, strategy aggregation, Signal Quality Score (`signal_quality.py`, Phase A4) — a per-candidate, advisory-only A+/A/B/C grade — Explainability (`explainability.py`, Phase A9) — human-readable reasons, reusing Signal Quality's criteria — and Signal Schema (`schema.py`/`adapter.py`, Phase A15) — one standard, JSON-serializable cross-module signal contract, computing nothing itself, now wired into `core/pipeline.py`'s `signal_history` stage (AC-03) with a new `decision_id` field. |
| `features/` | Feature Engineering foundation (Phase A10) — `MarketFeatures`, one standard snapshot per candidate for a future AI/backtester/ML/Failure-Analysis consumer. A standardization layer: relays `context/` and `signals/` (Signal Quality + Explainability) results as-is, computes nothing new. |
| `ai/` | Advisory-only AI evaluation layer (Phase 55: foundation for a future provider; production analyzer is still a heuristic stub). |
| `decision/` | Blends signal confidence, HTF bias, (inverted) AI risk score, and AI confidence — weighted, Phase A3 — into APPROVE/REJECT/NO_TRADE. |
| `risk/` | SL/TP geometry and stop-loss-distance validation; sizing suggestion only. |
| `execution/` | Inert scaffolding for future MT5 integration — not reachable from any runtime path today. |
| `monitoring/` | Historical trade-outcome statistics (win rate, strategy breakdown — `performance.py`'s `PerformanceTracker`), not wired into any live command yet. Distinct from `performance/` (Phase A19) — see that row. Also `provider_health.py` (Phase 59.2) — `ProviderHealthStatus`/`check_provider_health()`, a third, distinct kind of “performance” (a provider's own live availability/latency), not wired into any live command yet either. |
| `performance/` | Performance Metrics foundation (Phase A19) — `PerformanceMetric`/`PerformanceCollector`/`PerformanceTimer`, a standalone code-timing foundation. Not wired into `core/pipeline.py`; not the same concept as `monitoring/performance.py`'s trade-outcome statistics. |
| `database/` | SQLite persistence — the only place SQL is written. Phase 59.3 added the first tables from any Phase A/AC/Phase-59 foundation module (`raw_candles`, `market_snapshots` — `raw_candle_models.py`/`raw_candle_repository.py`, `market_snapshot_models.py`/`market_snapshot_repository.py`), fully isolated, not wired into `core/pipeline.py`. Phase 59.5 added `sync_state` (`sync_state_models.py`/`sync_state_repository.py`) — one row per `(provider, symbol, timeframe)`, the historical collector's own incremental resume watermark. Phase 59.6 added `audit_log`/`config_snapshots` (`audit_log_models.py`/`audit_log_repository.py`, `config_snapshot_models.py`/`config_snapshot_repository.py`) — both append-only. Phase 59.7 added `runtime_features` (`runtime_feature_models.py`/`runtime_feature_repository.py`) — one row per feature name, `configuration.runtime_feature_manager.RuntimeFeatureManager`'s persistence layer; `audit_log`/`config_snapshots` are now actually written to on every successful runtime toggle, no longer purely a manual/future-command capture. Phase 59.9 added `emergency_states` (`emergency_models.py`/`emergency_repository.py`) — append-only (like `audit_log`, unlike `runtime_features`' upsert), `core.emergency.emergency_manager.EmergencyManager`'s persistence layer; every transition is also written to `audit_log`. |
| `telegram/` | The Telegram product layer: routing, permissions, handlers, services. `owner/` (Phase 59.3-59.5) — real, tested owner-command service functions (`provider_commands.py`/`system_commands.py`/`feature_commands.py`/`report_commands.py`/`validation_commands.py`/`dataset_commands.py`), not registered into `commands.py`/`command_router.py`/`handlers.py` — the live bot's command surface is unaffected. |
| `lifecycle/` | Phase 59 Preparation foundation — `PaperTrade`/`TradeState` (simulated, broker-free trade state machine) and `SignalLifecycleState` (a signal's own progress through the analysis pipeline). In-memory only: no database persistence, no pipeline wiring. Not the same as `strategies/lifecycle/` (per-strategy metadata) or `execution/signal_lifecycle.py` (a pre-existing, inert, Telegram-delivery state machine). |
| `analytics/` | Phase 59 Preparation foundation — `SignalPerformance`/`StrategyPerformanceReport`, **trading** performance (win/loss/R-multiple by strategy). Not wired into `core/pipeline.py`; not the same concept as `performance/` (Phase A19, system timing) or a replacement for `monitoring/performance.py`'s pre-existing, database-driven `PerformanceTracker`. |

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
  string, not an `assets/` import (see `docs/SIGNAL_SCHEMA.md`). As of
  AC-03, `core/pipeline.py` imports and calls
  `signals.adapter.from_signal_candidate()` at runtime — allowed,
  since `core/pipeline.py` is the one file permitted to import from
  every layer (see its own rule below); `signals/schema.py`'s and
  `signals/adapter.py`'s own import lists above are otherwise
  unchanged by this.
- `context/snapshot.py` (Phase A16) imports only the standard library
  plus `context.context_orchestrator` and `context.market_structure`
  (same package) — no dependency on `strategies/`, `signals/`, `ai/`,
  `decision/`, `risk/`, `database/`, `telegram/`, or `assets/`.
  Deliberately does not import `signals.schema.ValidationResult`
  despite the identical shape — `context/` must never depend on
  `signals/` (see `docs/ARCHITECTURE_RULES.md`'s Context Engine rule)
  — `context/snapshot.py` declares its own, independent
  `ValidationResult` instead (see `docs/CONTEXT_SNAPSHOT.md`). As of
  AC-03, `core/pipeline.py` imports and calls
  `context.snapshot.from_context_snapshot()` at runtime, same allowed
  pattern as `signals/adapter.py` above.
- `context/market_phase.py` (AC-02) imports `context.amd`,
  `context.market_regime`, and `context.wyckoff` (same package,
  standard library `enum`/`dataclasses` otherwise) plus, `TYPE_CHECKING`-
  only, `context.context_orchestrator.ContextSnapshot` — no dependency
  on `strategies/`, `signals/`, `ai/`, `decision/`, `risk/`,
  `database/`, or `telegram/`. Called by `core/pipeline.py` as a new
  stage immediately after `context`.
- `data/api_error_classifier.py` (AC-07) imports `requests` and
  `core.errors` (cross-cutting) only — no dependency on `context/`,
  `strategies/`, `signals/`, `ai/`, `decision/`, `risk/`, `database/`,
  or `telegram/`. Called by `data/market_data.py`'s `get_candles()`
  inside its existing `except` block, for logging only.
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
- `data/normalization/` (Phase 59.3) imports
  `data.providers.base_provider.MarketCandle` (`candle_normalizer.py`
  only) — `symbol_mapper.py`/`timeframe_mapper.py` import only the
  standard library. No dependency on `context/`, `strategies/`,
  `signals/`, `ai/`, `decision/`, `risk/`, `execution/`, `database/`,
  or `telegram/`. Not imported by `core/pipeline.py` or
  `data/market_data.py`.
- `database/raw_candle_models.py`/`raw_candle_repository.py` and
  `database/market_snapshot_models.py`/`market_snapshot_repository.py`
  (Phase 59.3) follow the exact same dependency shape as every other
  `database/*_repository.py` — `database/database.py` and
  `database/models.py` only, plus (for `market_snapshot_models.py`'s
  `from_market_data_snapshot()`)
  `data.market_data_snapshot.MarketDataSnapshot`, `TYPE_CHECKING`-only.
  No dependency on `telegram/`, `ai/`, `decision/`, `risk/`,
  `context/`, or `strategies/`.
- `context/fundamental_context.py` (Phase 59.3) imports only the
  standard library plus, `TYPE_CHECKING`-only,
  `data.providers.fundamental_base.FundamentalDataPoint` — no runtime
  dependency on `data/providers/` (inputs are supplied by the caller,
  never fetched). No dependency on `signals/`, `ai/`, `decision/`,
  `risk/`, `database/`, or `telegram/`. Not imported by
  `core/pipeline.py`, `ai/`, or `decision/` in this phase.
- `telegram/owner/` (Phase 59.3) imports `data.providers.registry`,
  `monitoring.provider_health`, `telegram.admin_service.AdminService`,
  `config.Config`, and `configuration.feature_flags.DEFAULT_FLAGS` —
  no dependency on `telegram.handlers`, `telegram.command_router`, or
  `telegram.commands`. Not imported by any of those three, or by
  `core/pipeline.py`, in this phase.
- `data/market_data_snapshot.py` (Phase 59 Preparation TASK 1) imports
  only the standard library plus `data.twelve_data_client.Candle`
  (same package) — no dependency on `context/`, `strategies/`,
  `signals/`, `ai/`, `decision/`, `risk/`, `database/`, or `telegram/`.
  Not called by `data/market_data.py` or any other existing module in
  this phase.
- `lifecycle/` (Phase 59 Preparation TASK 2 + TASK 4) imports
  `signals.schema.SignalSchema` (`TYPE_CHECKING`-only, in both
  `paper_trade.py` and `signal_state.py`) and, within the package,
  `lifecycle.trade_state`/`lifecycle.paper_trade` — no dependency on
  `context/`, `strategies/`, `ai/`, `decision/`, `risk/`, `execution/`,
  `database/`, or `telegram/`. Deliberately does **not** import
  `execution/` — `lifecycle/`'s `PaperTrade` never calls a broker, and
  does not make `execution/`'s own inert stubs any less inert (see
  `lifecycle/README.md`'s "Not the same as `execution/`" section). Not
  imported by `core/pipeline.py` or `execution/` in this phase.
- `data/providers/` (Phase 59.1) imports `data.twelve_data_client.TwelveDataClient`
  and `data.api_error_classifier` (same top-level `data/` package)
  plus `config.Config` (cross-cutting, in `__init__.py`'s
  `get_provider()` only) — no dependency on `context/`, `strategies/`,
  `signals/`, `ai/`, `decision/`, `risk/`, `execution/`, `database/`,
  or `telegram/`. `mt5_provider.py` imports only `base_provider.py`
  (same package) — no `MetaTrader5` package dependency. Not imported
  by `core/pipeline.py`, `data/market_data.py`, or any other existing
  module in this phase. Extended by Phase 59.2:
  `binance_provider.py`/`fred_provider.py`/`fundamental_base.py`/
  `registry.py` all import only other files within `data/providers/`
  — no new external dependency (no exchange or FRED API package).
  `monitoring/provider_health.py` (Phase 59.2) imports
  `data.providers.base_provider`/`data.providers.registry` — a new,
  one-directional `monitoring/` → `data/providers/` dependency, never
  reversed.
- `analytics/` (Phase 59 Preparation TASK 3) imports
  `lifecycle.paper_trade.PaperTrade` and `signals.schema.SignalSchema`
  (`TYPE_CHECKING`-only) plus, within the package,
  `analytics.signal_performance` — no dependency on `context/`,
  `strategies/`, `ai/`, `decision/`, `risk/`, `execution/`,
  `database/`, or `telegram/`. Does not import
  `monitoring/performance.py` or `database/signal_repository.py` —
  its input is an in-memory `List[SignalPerformance]`, not a database
  read. Not imported by `core/pipeline.py` or `monitoring/` in this
  phase.
- `data/historical_data_collector.py`/`historical_validator.py`/
  `provider_comparison.py` (Phase 59.5) import `data.providers.base_provider`,
  `data.data_quality.INTERVAL_DELTAS` (same top-level `data/` package),
  `database.raw_candle_repository`/`database.sync_state_repository`
  (a new, one-directional `data/` → `database/` dependency — the first
  time anything in `data/` has depended on `database/`, since a
  collector's whole job is persisting what it fetches; never reversed,
  and no other `data/` module gained this dependency). No dependency on
  `context/`, `strategies/`, `signals/`, `ai/`, `decision/`, `risk/`,
  `execution/`, or `telegram/`. `analytics/gap_report.py`/
  `dataset_report.py` (Phase 59.5) import `data.data_quality.INTERVAL_DELTAS`
  and, within `analytics/`, `dataset_report.py` imports
  `data.historical_validator` — no dependency on `context/`,
  `strategies/`, `ai/`, `decision/`, `risk/`, `execution/`, or
  `telegram/`. `telegram/owner/dataset_commands.py` (Phase 59.5)
  imports `analytics.dataset_report`, `data.provider_comparison`,
  `database.raw_candle_repository`, `database.sync_state_repository`,
  and `provider_commands.ProviderCommandResult` (same package) — not
  imported by `telegram/handlers.py`, `telegram/command_router.py`, or
  `telegram/commands.py`. None of the six new modules are imported by
  `core/pipeline.py`.
- `core/system_state.py` (Phase 59.6) imports only the standard
  library (`dataclasses`, `datetime`, `enum`) — no dependency on any
  other package, not imported by `core/pipeline.py`.
  `database/audit_log_models.py`/`audit_log_repository.py` and
  `database/config_snapshot_models.py`/`config_snapshot_repository.py`
  (Phase 59.6) follow the exact same shape as every other
  `database/*_repository.py` pair — `config_snapshot_models.py`
  additionally imports `configuration.feature_registry.FeatureDescriptor`
  (`TYPE_CHECKING`-only), a new, one-directional `database/` →
  `configuration/` dependency, never reversed.
  `telegram/owner/owner_roles.py` (Phase 59.6) imports
  `telegram.permissions.is_owner` and, lazily inside
  `resolve_owner_role()` (not at module import time),
  `database.admin_repository.AdminRepository` — never imports or
  modifies `telegram.permissions.PermissionLevel` itself.
  `configuration/feature_registry.py`/`feature_dependency_validator.py`
  (Phase 59.6) import `config.Config` and
  `configuration.feature_flags.DEFAULT_FLAGS` (same package) only — no
  dependency on `database/`, `telegram/`, or any pipeline layer. None
  of these six new modules are imported by `core/pipeline.py`,
  `decision/`, `risk/`, `execution/`, `strategies/`, `context/`,
  `signals/`, or `telegram/command_router.py`.
- `configuration/runtime_state.py` (Phase 59.7) imports only the
  standard library. `configuration/runtime_feature_manager.py` (Phase
  59.7) imports `database.runtime_feature_repository`,
  `database.audit_log_repository`,
  `database.config_snapshot_repository`/`config_snapshot_models` — the
  first *runtime* (not `TYPE_CHECKING`-only) `configuration/` →
  `database/` dependency in this codebase. Combined with Phase 59.6's
  `database/config_snapshot_models.py`'s own `TYPE_CHECKING`-only
  `configuration.feature_registry.FeatureDescriptor` import, the two
  packages now reference each other from different files — never a
  circular import in practice (Python resolves each module
  independently; the import sweep in every phase's own validation
  pass confirms this), but worth naming explicitly so a future change
  to either file checks both directions before adding a third.
  `configuration/runtime_api.py` (Phase 59.7) imports only
  `configuration.runtime_feature_manager` — no `telegram/` dependency,
  keeping the existing one-directional `telegram/` → `configuration/`
  relationship intact. None of the four new Phase 59.7 modules are
  imported by `core/pipeline.py`, `decision/`, `risk/`, `execution/`,
  `strategies/`, `signals/`, `context/`, `ai/`, any Telegram handler,
  or `telegram/command_router.py`.
- `core/emergency/emergency_state.py`/`circuit_breaker.py`/
  `maintenance.py` (Phase 59.9) import only the standard library.
  `core/emergency/emergency_manager.py` (Phase 59.9) imports
  `database.emergency_repository`, `database.audit_log_repository` —
  a new, one-directional `core/` → `database/` dependency, the same
  shape `configuration/runtime_feature_manager.py` already established
  for `configuration/` → `database/` (Phase 59.7); never reversed,
  `database/` does not import `core/emergency/`.
  `telegram/owner/emergency_commands.py` (Phase 59.9) imports
  `core.emergency.emergency_manager`/`emergency_state` and
  `provider_commands.ProviderCommandResult` (same package) — not
  imported by `telegram/handlers.py`, `telegram/command_router.py`, or
  `telegram/commands.py`. None of the six new Phase 59.9 modules are
  imported by `core/pipeline.py`, `decision/`, `risk/`, `execution/`,
  `strategies/`, `signals/`, `context/`, `ai/`, any Telegram handler,
  or `telegram/command_router.py`.

If a change requires violating one of these rules, that is a signal
to stop and reconsider the design, not to add the import and move on
— see `CLAUDE.md`'s "Architecture Rules" for the same point stated as
a working rule rather than a description.
