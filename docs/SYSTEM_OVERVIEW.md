# GoldBot System Overview (Phase A14)

Part of GoldBot's Documentation Architecture Foundation (Phase A14).
Written for a new developer or agent's first read — a map of what
GoldBot is and where to go next, not a detailed reference.
`docs/ARCHITECTURE.md` is the detailed reference; `docs/ARCHITECTURE_RULES.md`
and `docs/DECISION_PRINCIPLES.md` are the rule statements; this
document is the entry point that orients a reader before either.

## What is GoldBot?

GoldBot is a semi-automatic XAUUSD (Gold) trading-signal bot. It
analyzes price action using Smart Money Concepts (market structure,
liquidity, order blocks, fair value gaps, AMD cycles), evaluates
candidate setups through an advisory AI layer, blends everything into
one decision, validates that decision against risk rules, and
delivers approved signals to a trader over Telegram. **It does not
place trades automatically** — execution remains manual, performed by
the trader in their own MT5 terminal (see `docs/DECISION_PRINCIPLES.md`'s
Principle 4 for why `execution/` staying inert is a deliberate,
enforced boundary, not a missing feature).

## Purpose

Give a discretionary trader a disciplined, explainable second opinion
on XAUUSD setups — never an autonomous trading system. Every signal
that reaches a user has passed through Signal Quality grading,
Explainability, an advisory AI read, a weighted Decision Engine
blend, and Risk Manager validation, in that order, with no shortcut
path (`CLAUDE.md`: "Never bypass Risk Manager").

## Architecture

Two independent OS processes share one SQLite database:

1. **Trading pipeline** (`main.py`, scheduled every 5 minutes during
   trading hours) — one run per invocation: fetch data, analyze it,
   and (if a signal clears every gate) send one Telegram notification
   and persist the result.
2. **Telegram product layer** (`telegram/polling.py`, long-lived) —
   user registration, settings, subscriptions, admin panel, feedback.
   Reads/writes the same database, entirely independent of when the
   pipeline last ran.

See `docs/ARCHITECTURE.md`'s System Overview section for the full
detail, and `docs/ARCHITECTURE_RULES.md` for the module-boundary rules
that keep the two processes independent.

## Data flow

The governance-level flow (see `docs/ARCHITECTURE_RULES.md` section
1.1 for the full diagram and its caveats):

```
Market Data -> Context Engine -> Strategy Engine -> Signal Quality ->
Explainability -> Feature Engineering -> AI Layer -> Decision Engine ->
Risk Manager -> Execution -> Analytics -> Telegram
```

The exact, implementation-accurate `core/pipeline.py` stage order
(including Data Quality and HTF Bias, both folded into "Market Data"/
"Context Engine" above for readability) is documented in
`docs/ARCHITECTURE.md`'s Data Flow diagram, kept current every phase.

## Version roadmap

| Version | Theme |
|---|---|
| v0.1 | Trading Engine — the original SMC strategy/signal/AI/decision/risk pipeline. |
| v0.2 | Telegram Product — user registration, subscriptions, admin panel, feedback, built on top of v0.1's pipeline output. |
| v0.3 | Foundation Hardening & Optimization — a professionalization pass over v0.2, no new user-facing feature. |
| v0.3.5 | Architecture Completion — foundation layers for future AI/Research/Multi-Asset work: HTF Bias, Decision Engine v2, Signal Quality Score, Wyckoff, Session Intelligence, Market Regime, Data Quality, Explainability, Feature Engineering, Strategy Lifecycle, Asset Intelligence, Configuration & Feature Flags, and this Documentation Architecture (Phases A1 through A14, this document's own phase). |
| v0.4 | AI Assistant — a real AI provider replacing `ai/ai_analyzer.py`'s current heuristic stub; not started. |

Every v0.3.5 phase followed the same rule: foundation only, no signal
logic, no AI behavior, no decision-threshold change, unless a task
explicitly asked for one and the Trading Safety rules in `CLAUDE.md`
were followed. See each phase's own `docs/*.md` (`docs/HTF_BIAS.md`
through `docs/CONFIGURATION_MANAGEMENT.md`) for what was built and
why.

## Where to go next

- Changing code? Start with `docs/DEVELOPMENT_GUIDE.md`.
- Understanding a module boundary? `docs/ARCHITECTURE_RULES.md`.
- Understanding who owns a decision? `docs/DECISION_PRINCIPLES.md`.
- Writing a new module's documentation? `docs/DOCUMENTATION_STANDARD.md`.
- Full technical detail? `docs/ARCHITECTURE.md`.
