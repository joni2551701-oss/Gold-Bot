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
HTF Bias (context/htf_bias.py)   -- Daily/H4/H1 market-context only
      |     |                       (Phase A2; never itself a trade
      |     |                       decision, see docs/HTF_BIAS.md)
      v     |
Context Engine (context/)        |  -- SMC structure detection:
      |     |                       structure, BOS/CHoCH, liquidity,
      |     |                       OB, FVG, AMD, Wyckoff (Phase A5,
      |     |                       Spring/Upthrust -- see below)
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

`core/pipeline.py`'s `TradingPipeline` is the only place that wires
every layer above together end to end — see its own docstring and
`docs/AUDIT_REPORT.md` for why the notification-eligibility filter
exists in exactly the shape it does.

## Module Responsibilities (summary — full detail in `docs/code_structure.md`)

| Module | Responsibility |
|---|---|
| `core/` | Cross-cutting infrastructure: pipeline orchestration, logging, secrets. |
| `data/` | Market data fetch and normalization. |
| `context/` | Pure SMC market-structure detection functions (structure, BOS/CHoCH, liquidity, OB, FVG, AMD, and Wyckoff Spring/Upthrust — Phase A5, part of `ContextSnapshot`), plus HTF Bias (`htf_bias.py`, Phase A2) — a market-context-only Daily/H4/H1 classification, not itself part of `ContextSnapshot`. |
| `strategies/` | Independent signal-candidate generation per SMC methodology. |
| `signals/` | The `SignalCandidate` data contract, strategy aggregation, and Signal Quality Score (`signal_quality.py`, Phase A4) — a per-candidate, advisory-only A+/A/B/C grade. |
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
