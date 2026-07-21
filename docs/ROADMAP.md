# GoldBot — Roadmap (Index)

This is a top-level pointer, not a duplicate roadmap. GoldBot's
roadmap-of-record lives in `docs/roadmap/`:

- `docs/roadmap/VERSIONS.md` — the authoritative, code-and-Freeze-doc
  -backed version history ("Actual Development Status" per the Phase
  62.1c ruling — never claims a version is further along than the
  real code proves).
- `docs/roadmap/AI_EVOLUTION.md` — the AI-specific stage timeline
  within the same roadmap (the `63.x`/`66.x` AI Foundation
  sub-sequences and their composition into the Official Intelligence
  Pipeline).
- `docs/VISION.md` — the longer-range destination these versions build
  toward.

## Current state (as of Phase V1.0.1)

GoldBot has completed its core trading pipeline (v0.1), database/
product layer (v0.2), Telegram Owner foundation (v0.3), AI Foundation
through the full `63.x`/`66.x` intelligence sub-sequences (v0.4.x),
and a GoldBot Core Owner Monitoring Alpha track (Phase B.0). Phase
V1.0 ("GoldBot V1 Final Audit Foundation") was a pre-freeze audit —
verification and stabilization only, no new capability — covering
Architecture, Trading Pipeline, Risk, Execution, AI, Monitoring,
Database, Configuration, Error/Logging, Test, Performance, and
Production Readiness. See `docs/V1_AUDIT.md` for the audit's summary
index and `docs/PHASE_V1_FREEZE.md` for the freeze recommendation.

Phase V1.0.1 ("Risk Management Hardening Patch") followed directly,
fixing every Risk gap V1.0's audit found that its RULE 1 permitted:
risk-per-trade bounds, risk-calculation validation, minimum
risk/reward enforcement, drawdown protection, daily-loss protection,
duplicate-trade protection, and Emergency-state correction (PAUSED/
KILLED/MAINTENANCE now block new approvals at the Risk layer itself,
not just at Telegram delivery), plus risk decision logging and a
read-only monitoring integration. Scope was confined to `risk/`,
`configuration/`, `database/`, `monitoring/`, `tests/`, `docs/` —
`core/`, `decision/`, `execution/`, `strategies/`, `signals/`,
`context/`, and `ai/` (Trading Core) were never touched, verified by
an empty diff. See `docs/PHASE_V1_0_1_RISK_AUDIT.md` and
`docs/PHASE_V1_0_1_RISK_FREEZE.md` for the full audit/freeze trail.

Per the Director's own stated sequence (see `docs/roadmap/VERSIONS.md`
and `docs/roadmap/AI_EVOLUTION.md`), a successful V1.0.1 Risk
Hardening Patch is intended to lead to: V1.0.1 PASS -> VPS Deployment
-> 24/7 Closed Beta. No new strategy, AI Foundation, or Trading Core
work is scheduled ahead of that sequence completing.
