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
2. **Telegram product layer** (`platform_layer/telegram/polling.py`, long-lived) —
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

**Foundation (complete as of Phase 60.10 — see `docs/FOUNDATION_FREEZE_v0.4.md`):**

| Version | Theme |
|---|---|
| v0.1 | Trading Engine — the original SMC strategy/signal/AI/decision/risk pipeline. |
| v0.2 | Telegram Product — user registration, subscriptions, admin panel, feedback, built on top of v0.1's pipeline output. |
| v0.3 | Foundation Hardening & Optimization — a professionalization pass over v0.2, no new user-facing feature. |
| v0.3.5 | Architecture Completion — foundation layers for future AI/Research/Multi-Asset work: HTF Bias, Decision Engine v2, Signal Quality Score, Wyckoff, Session Intelligence, Market Regime, Data Quality, Explainability, Feature Engineering, Strategy Lifecycle, Asset Intelligence, Configuration & Feature Flags, and this Documentation Architecture (Phases A1 through A14). |
| **v0.4 Foundation** | Real-market validation, provider abstraction, replay/backtesting, execution simulation, performance validation, fundamental intelligence, the Learning Loop, Adaptive Intelligence, and Safe Integration (Pipeline Guard + Emergency Manager wiring, Runtime Registry separation) — Phases 59.0 through 60.9. **Frozen** as of Phase 60.10: no further foundation work is planned before v0.4 AI begins. |

**Future:**

| Version | Theme |
|---|---|
| v0.4 AI | A real AI provider replacing `ai_layer/ai_engine/ai_analyzer.py`'s current heuristic stub — not started. |
| v0.5 MT5 | Live MT5 broker integration — `execution_layer/execution_engine/execution_engine.py` (currently, deliberately, inert) gets wired to a real order path. |
| v0.6 Portfolio | Multi-position/portfolio-level risk and performance tracking. |
| v0.7 Cloud | Cloud-hosted deployment and scaling. |
| v0.8 Mini App | Telegram Mini App interface. |
| v0.9 Multi-Broker | Additional providers beyond MT5 — Bitget, BingX, MEXC (optional) — plus an Admin Panel with live Telegram commands (today's `platform_layer/telegram/owner/*.py` modules registered into `command_router.py`). |
| v1.0 Senior AI Trading Ecosystem | AI Avatar Layer, Voice Interface, Hologram Display Layer — a new Presentation Layer only; GoldBot Core stays unchanged underneath (see `docs/FOUNDATION_FREEZE_v0.4.md`'s Foundation Principles for why this is architecturally safe to plan for now). |

Every v0.3.5-v0.4 Foundation phase followed the same rule: foundation
only, no signal logic, no AI behavior, no decision-threshold change,
unless a task explicitly asked for one and the Trading Safety rules in
`CLAUDE.md` were followed. See each phase's own `docs/*.md`
(`docs/HTF_BIAS.md` through `docs/PIPELINE_GUARD.md`) for what was
built and why, and `docs/FOUNDATION_FREEZE_v0.4.md` for the complete
list.

## Where to go next

- Changing code? Start with `docs/DEVELOPMENT_GUIDE.md`.
- Understanding a module boundary? `docs/ARCHITECTURE_RULES.md`.
- Understanding who owns a decision? `docs/DECISION_PRINCIPLES.md`.
- Writing a new module's documentation? `docs/DOCUMENTATION_STANDARD.md`.
- Full technical detail? `docs/ARCHITECTURE.md`.
