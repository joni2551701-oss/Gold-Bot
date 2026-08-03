# GoldBot Architecture Rules (Phase A14)

Part of GoldBot's Documentation Architecture Foundation (Phase A14).
This document is the short, authoritative statement of module
boundaries — a "constitution," not a tutorial. For the detailed,
implementation-accurate module map (every real file, every phase's
own section, the exact `core/pipeline.py` stage order), see
`docs/ARCHITECTURE.md`. For *why* a decision-ownership boundary
exists, see `docs/DECISION_PRINCIPLES.md`. For how to work inside
these rules day to day, see `docs/DEVELOPMENT_GUIDE.md`.

This document does not introduce a new rule — every boundary stated
below is already enforced today (see `docs/ARCHITECTURE.md`'s
Dependency Rules, `CLAUDE.md`'s Architecture Rules, and the CI import
sweep referenced by both). Phase A14 writes it down explicitly, in
one place, independent of any single phase's own section.

## 1.1 System Architecture

```
Market Data
      |
      v
Context Engine
      |
      v
Strategy Engine
      |
      v
Signal Quality
      |
      v
Explainability
      |
      v
Feature Engineering
      |
      v
AI Layer
      |
      v
Decision Engine
      |
      v
Risk Manager
      |
      v
Execution
      |
      v
Analytics
      |
      v
Telegram
```

This is the **governance-level** flow — the conceptual order data and
authority move through, module by module. It is deliberately
simplified for readability, and differs from `docs/ARCHITECTURE.md`'s
Data Flow diagram in three ways every reader should know:

1. **Data Quality and HTF Bias are folded into "Market Data" /
   "Context Engine" above.** In the real pipeline
   (`core/pipeline.py`), Data Quality (Phase A8) runs immediately
   after Market Data and HTF Bias (Phase A2) runs before Context —
   both are observational/context-only and don't change this
   document's ownership rules.
2. **Execution and Analytics are drawn in their intended future
   position, not their current one.** `execution/` is inert scaffolding
   today (no MT5/broker connection — see `execution/README.md`) and
   `monitoring/` (Analytics) is not wired into any live command yet.
   Drawing them here states *where they belong once built*, per this
   document's module-boundary rules — it is not a claim that they run
   today.
3. **Database is folded into "Telegram"'s downstream side.** The real
   pipeline persists a `SignalRecord` in parallel with (not strictly
   after) Telegram delivery — see `core/pipeline.py`'s `run()`.

When this document and `docs/ARCHITECTURE.md` ever appear to
disagree on an implementation detail, `docs/ARCHITECTURE.md` is the
accurate one — this document is the stable, rarely-changing rule
statement; `docs/ARCHITECTURE.md` is updated every phase.

## 1.2 Module Responsibility Rules

Each module owns exactly what is listed under "Allowed" — nothing
under "Forbidden" is a hypothetical risk, every one of these
boundaries is already true of the real code referenced.

### Context Engine (`context/`)

**Allowed**
- ✅ Market structure analysis (swings, BOS/CHoCH — `market_structure.py`, `bos.py`, `choch.py`)
- ✅ Liquidity detection (`liquidity.py`)
- ✅ Order Blocks (`order_block.py`)
- ✅ Fair Value Gaps (`fvg.py`)
- ✅ Market state classification (Wyckoff `wyckoff.py`, Session `session.py`, Market Regime `market_regime.py`, HTF Bias `htf_bias.py`)

**Forbidden**
- ❌ Generating a signal (`context/` never constructs a `SignalCandidate`)
- ❌ Sending a Telegram message (`context/` never imports `telegram/`)
- ❌ Computing risk (`context/` never imports `risk/`)

### Strategy Engine (`strategies/`)

**Allowed**
- ✅ Finding a setup (each `strategies/*_strategy.py`'s `analyze()`)
- ✅ Producing a candidate (`SignalCandidate`, from `signal_layer/signal_builder/models.py`)

**Forbidden**
- ❌ Calling the AI layer (`strategies/` never imports `ai/`)
- ❌ Opening an order (`strategies/` never imports `execution/`)
- ❌ Talking to a user (`strategies/` never imports `telegram/`)

### AI Layer (`ai/`)

**Allowed**
- ✅ Explanation (human-readable reasoning about a candidate)
- ✅ Analysis (`AIAnalyzer.analyze()` → `AIAnalysisResult`)
- ✅ Context interpretation (advisory confidence/risk scoring)

**Forbidden**
- ❌ Producing a `BUY`/`SELL` decision itself — `ai/interfaces.py`'s
  `AIAnalyzerInterface` docstring states this contract explicitly;
  see `docs/DECISION_PRINCIPLES.md`'s Principle 1.
- ❌ Making the final call — `AIAnalysisResult` is one of four
  weighted inputs to `DecisionEngine.evaluate()` (Phase A3), never a
  decision by itself.

### Decision Engine (`decision/`)

**Allowed**
- ✅ Blending every score (signal confidence, HTF bias, AI risk/
  confidence — `decision_layer/decision_engine/decision_engine.py`'s `DecisionEngine.evaluate()`)
- ✅ Approve/Reject/No-Trade (`DecisionAction`)

**Forbidden**
- ❌ Generating a new signal (`decision/` never imports `strategies/`
  or constructs a `SignalCandidate`)
- ❌ Analyzing the market itself (`decision/` reads `context/` only
  for the `HTFBias` type — Phase A3 — never re-derives structure/
  liquidity/etc.)

### Risk Manager (`risk/`)

**Allowed**
- ✅ Risk validation (`RiskManager.evaluate()`'s geometry and
  stop-loss-distance checks)
- ✅ Sizing foundation (a lot-size *suggestion* — never an MT5 order)

**Forbidden**
- ❌ Finding an entry (`risk/` never imports `strategies/` or
  `context/` — it validates a `TradeDecision` it is given, it does
  not look for one)

### Telegram Layer (`telegram/`)

**Allowed**
- ✅ User interaction (commands, settings, subscriptions —
  `platform_layer/telegram/handlers.py` → `telegram/*_service.py`)
- ✅ Notification (`platform_layer/telegram/notifier.py`, `platform_layer/telegram/signal_formatter.py`)

**Forbidden**
- ❌ Trading logic (`telegram/` never imports `strategies/`,
  `decision/`, or `risk/` — it formats and delivers what those layers
  already decided; see `CLAUDE.md`'s "No direct database access from
  Telegram handlers" rule for the same boundary applied to `database/`)

## Enforcement

These rules are not aspirational — they are checked, every phase,
by:
- The CI import sweep (`.github/workflows/ci.yml`) and this session's
  own repeated full-module-import-sweep script, both of which would
  surface a new circular or upward import.
- `docs/ARCHITECTURE.md`'s "Dependency Rules" section, updated every
  phase a new module is added (`features/`, `strategies/lifecycle/`,
  `assets/`, `configuration/` each got their own explicit line).
- `pyflakes` and the full `pytest` suite, run before every commit.

A change that would require violating one of these rules is a signal
to stop and reconsider the design — see `CLAUDE.md`'s own Architecture
Rules section and `docs/DEVELOPMENT_GUIDE.md`'s workflow below.
