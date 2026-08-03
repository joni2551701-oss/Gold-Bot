# GoldBot Decision Principles (Phase A14)

Part of GoldBot's Documentation Architecture Foundation (Phase A14).
This document states GoldBot's decision philosophy: which module owns
which kind of authority, and why no module is allowed to reach past
its own boundary. `docs/ARCHITECTURE_RULES.md` states *what* each
module may and may not do; this document states *who decides what*,
end to end.

Every principle below is already enforced in the real codebase — this
document names the principle, `docs/ARCHITECTURE_RULES.md` names the
module boundary, and `docs/ARCHITECTURE.md` names the exact file and
phase that implements it.

## Principle 1 — AI is not the final decision owner

```
AI
 |
 v
Decision Engine
 |
 v
Final decision
```

`ai_layer/ai_engine/ai_analyzer.py`'s `AIAnalyzer.analyze()` produces an
`AIAnalysisResult` — advisory confidence and risk scoring, nothing
more. It is never itself an `APPROVE`/`REJECT` decision.
`decision_layer/decision_engine/decision_engine.py`'s `DecisionEngine.evaluate()` is the
only place a `TradeDecision` is produced, blending `AIAnalysisResult`
with signal confidence and HTF bias (Phase A3, "Decision Engine v2" —
see `docs/ARCHITECTURE.md`). This is a hard rule, not a style
preference: see `CLAUDE.md`'s Trading Safety section ("Never allow AI
direct execution") and `ai_layer/ai_service/interfaces.py`'s `AIAnalyzerInterface`
docstring, and `docs/AUDIT_REPORT.md` for the incident (REJECT/BLOCKED
signals reaching Telegram) that made this boundary explicit.

## Principle 2 — Strategy does not generate a signal

```
Strategy:

Market condition
      |
      v
Candidate
```

A strategy (`strategy_layer/strategy_library/liquidity_strategy.py`, `fvg_strategy.py`,
`amd_strategy.py`) produces a `SignalCandidate` — a *proposal*, not a
signal a user ever sees. A `SignalCandidate` only becomes a delivered
signal after passing Signal Quality, Explainability, AI, Decision
Engine, and Risk Manager, and only the single highest-confidence
`APPROVE`d, risk-approved candidate per cycle is ever formatted for
Telegram (see `core/pipeline.py`'s own docstring on the
notification-eligibility filter). "Candidate" is the precise word
used throughout this codebase (`signal_layer/signal_builder/models.py`'s
`SignalCandidate`) specifically to keep this distinction visible in
code, not just in this document.

## Principle 3 — Risk does not originate a trade idea

```
Risk:

Existing decision
        |
        v
Risk validation
```

`risk_layer/risk_engine/risk_manager.py`'s `RiskManager.evaluate()` takes a
`TradeDecision` that already exists — produced by Decision Engine —
and validates its geometry and stop-loss distance, and suggests a lot
size. It never searches for an entry, never proposes a trade, and
never reads `context/` or `strategies/` to look for a setup of its
own. See `docs/ARCHITECTURE_RULES.md`'s Risk Manager section for the
concrete import boundary this principle maps to.

## Principle 4 — Execution does not change the strategy

```
Execution:

Approved signal
       |
       v
Order
```

`execution/` (currently inert — see `execution/README.md`, no MT5/
broker connection exists yet) is scoped to take an already-`APPROVE`d,
risk-validated signal and place an order — nothing upstream of that.
When execution is eventually wired up (an explicitly separate,
approved phase per `CLAUDE.md`'s Trading Safety rules), it must not
gain the ability to alter a `SignalCandidate`'s entry/stop-loss/
take-profit, re-run a strategy, or override a `TradeDecision` — it
executes what Decision Engine and Risk Manager already produced,
unmodified.

## Principle 5 — Database only persists

```
Database:

❌ business logic
```

`database/*_repository.py` files contain SQL and row mapping only —
`CLAUDE.md`'s Architecture Rules state this explicitly ("Repositories
own SQL only — no business rule belongs in a
`database/*_repository.py` file"). A repository does not decide
whether a signal was good, does not compute a score, and does not
gate what gets saved based on quality — every candidate's outcome is
persisted for analytics regardless of whether it was approved,
rejected, or risk-blocked (see `core/pipeline.py`'s
`create_signal_record()` call, unconditional per candidate). The one
place that *does* have judgment about what reaches a user — the
notification-eligibility filter — lives in `core/pipeline.py`, not in
`database/`.

## Why this matters

Every principle above answers the same underlying question: **when
two modules disagree, whose read wins?** GoldBot's answer is always
"the module positioned to own that decision, and only that module" —
never the module that happens to run first, run last, or have the
most information available. This is what keeps
`docs/ARCHITECTURE_RULES.md`'s module boundaries meaningful over time:
a boundary that can be silently overridden by whichever module gets
there first is not a boundary. See `docs/DEVELOPMENT_GUIDE.md` for
what this means when adding new code.
