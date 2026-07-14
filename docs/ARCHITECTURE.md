# GoldBot Architecture Overview

System-level overview and dependency rules. For the detailed
per-module responsibility map, see `docs/code_structure.md`; for the
database-specific schema/relationship map, see
`docs/DATABASE.md`; for the Telegram-specific
service/permission map, see `docs/telegram_layer.md`. This document
is the entry point that ties them together and states the dependency
rules explicitly, which none of the earlier docs did as their primary
focus.

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

`core/pipeline.py`'s `TradingPipeline` is the only place that wires
every layer above together end to end — see its own docstring and
`docs/AUDIT_REPORT.md` for why the notification-eligibility filter
exists in exactly the shape it does.

## Module Responsibilities (summary — full detail in `docs/code_structure.md`)

| Module | Responsibility |
|---|---|
| `core/` | Cross-cutting infrastructure: pipeline orchestration, logging, secrets. |
| `data/` | Market data fetch and normalization, plus Data Quality assessment (`data_quality.py`, Phase A8) — observational scoring, not filtering. |
| `context/` | Pure SMC market-structure detection functions (structure, BOS/CHoCH, liquidity, OB, FVG, AMD, Wyckoff Spring/Upthrust — Phase A5, Session classification — Phase A6, and Market Regime — Phase A7, all part of `ContextSnapshot`), plus HTF Bias (`htf_bias.py`, Phase A2) — a market-context-only Daily/H4/H1 classification, not itself part of `ContextSnapshot`. |
| `strategies/` | Independent signal-candidate generation per SMC methodology, plus a Strategy Lifecycle metadata layer (`lifecycle/`, Phase A11) — `StrategyDefinition`/`StrategyRegistry`, storing status/version/supported-assets metadata only, never running a strategy or generating a signal. |
| `signals/` | The `SignalCandidate` data contract, strategy aggregation, Signal Quality Score (`signal_quality.py`, Phase A4) — a per-candidate, advisory-only A+/A/B/C grade — and Explainability (`explainability.py`, Phase A9) — human-readable reasons, reusing Signal Quality's criteria. |
| `features/` | Feature Engineering foundation (Phase A10) — `MarketFeatures`, one standard snapshot per candidate for a future AI/backtester/ML/Failure-Analysis consumer. A standardization layer: relays `context/` and `signals/` (Signal Quality + Explainability) results as-is, computes nothing new. |
| `ai/` | Advisory-only AI evaluation layer (Phase 55: foundation for a future provider; production analyzer is still a heuristic stub). |
| `decision/` | Blends signal confidence, HTF bias, (inverted) AI risk score, and AI confidence — weighted, Phase A3 — into APPROVE/REJECT/NO_TRADE. |
| `risk/` | SL/TP geometry and stop-loss-distance validation; sizing suggestion only. |
| `execution/` | Inert scaffolding for future MT5 integration — not reachable from any runtime path today. |
| `monitoring/` | Performance/statistics reading, not wired into any live command yet. |
| `database/` | SQLite persistence — the only place SQL is written. |
| `telegram/` | The Telegram product layer: routing, permissions, handlers, services. |

## Dependency Rules

A layer may depend on the layer(s) below it in the data-flow diagram
above, and on `core/`/`config.py` (cross-cutting). It must never
depend upward or sideways into an unrelated layer. Concretely, as
implemented and enforced today (verified by the Phase 48 audit's
circular-import check and re-verified every phase since via the CI
import sweep):

- `context/`, `strategies/`, `signals/` never import `telegram/`,
  `database/`, or `ai/`.
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
