# Module Contracts (Phase A17)

Part of GoldBot's governance documentation, alongside
`docs/ARCHITECTURE_RULES.md`, `docs/DECISION_PRINCIPLES.md`,
`docs/DEVELOPMENT_GUIDE.md`, `docs/SYSTEM_OVERVIEW.md`, and
`docs/DOCUMENTATION_STANDARD.md` (Phase A14). This document is the
entry point into `contracts/*.md` — the per-module input/output/
dependency/error specification this phase adds. It does not
introduce a new rule; every boundary named below is already enforced
today (see each `contracts/*.md` file's own citations into real code).

## Purpose

GoldBot is growing past the size where "everyone reads everyone
else's source to understand a boundary" scales. Phase A17 writes down,
per module, in one predictable format: what it accepts, what it
returns, which modules it may depend on, which it must never depend
on, and how it reports failure — so a future worker or AI agent can
answer "can module X call module Y?" by reading one short file instead
of re-deriving it from `docs/ARCHITECTURE.md`'s Dependency Rules
section and the source code both.

## Architecture map

```
Context
  |
  v
Strategy
  |
  v
Signal
  |
  v
AI
  |
  v
Decision
  |
  v
Risk
  |
  v
Execution
```

Each arrow is a real, one-directional dependency, enforced today (see
`docs/ARCHITECTURE_RULES.md` section 1.1 for the full governance
diagram including Telegram/Database, and its explicit caveats versus
`docs/ARCHITECTURE.md`'s implementation-accurate Data Flow diagram).
A module never reaches into the module two steps below it, and never
reaches upward at all — Decision Engine does not re-analyze the
market Context Engine already classified, and Context Engine does not
know Telegram exists.

## Dependency rules (summary)

| Module | May depend on | May NOT depend on |
|---|---|---|
| Context | `data/` | `strategies/`, `signals/`, `ai/`, `decision/`, `risk/`, `execution/`, `telegram/`, `database/` |
| Strategy | `context/`, `signals/` (for `SignalCandidate`) | `ai/`, `decision/`, `risk/`, `execution/`, `telegram/`, `database/` |
| Signal | `context/`, `strategies/` | `ai/`, `decision/`, `risk/`, `telegram/`, `database/` |
| AI | `signals/`, `context/` | `decision/`, `risk/`, `execution/`, `telegram/`, `database/` |
| Decision | `ai/`, `signals/`, `context/` (for `HTFBias`) | `strategies/`, `risk/`, `execution/`, `telegram/`, `database/` |
| Risk | `decision/`, `signals/` (via `TradeDecision`) | `context/`, `strategies/`, `ai/`, `execution/`, `telegram/`, `database/` |
| Execution | `risk/` | `strategies/`, `signals/`, `ai/`, `decision/`, `telegram/`, `database/` |
| Telegram | `signals/`, `ai/`, `decision/`, `risk/` (read-only, for formatting) | `strategies/`, `context/`, `execution/`; direct `database/*` (handlers must go through `telegram/*_service.py`) |
| Database | Whatever typed record each repository persists | Business logic from `strategies/`, `ai/`, `decision/`; `telegram/` |

Full detail, exact real function signatures, and the specific
deviations this document deliberately made from any earlier
illustrative example (all disclosed, not silent) live in each
module's own `contracts/*_contract.md` file — this table is a
summary, not the source of truth.

## Error handling

Every module's `contracts/*.md` "Error Contract" section names which
proposed `GoldBotError` subtype (`contracts/error_contract.md`) its
failure modes would map to, if implemented. The dominant real pattern
today — and one this phase does not change — is a structured result
object (`ValidationResult`, `RiskResult.approved`,
`TradeDecision.action`, `DataQualityResult`), not a raised exception,
for any expected/data-driven condition. A raised exception is reserved
for genuine programmer/integrity errors (see
`contracts/error_contract.md`'s "When to raise vs. return a result").

## What this phase changed

Nothing in the running system. Every file added by Phase A17 is
markdown (`contracts/*.md`, this document) plus one test file
(`tests/contracts/test_contracts_exist.py`) that checks the markdown
files exist and are well-formed — it does not import, call, or alter
any production module. See `contracts/README.md`'s own "What this is
NOT" section.

## The platform constitution

After this phase, seven foundation phases together form GoldBot's
platform constitution — the near-complete v0.3.5 Foundation:

- **A13 Configuration** (`configuration/`) — how the application is
  configured and how future features are gated.
- **A14 Architecture Rules** (`docs/ARCHITECTURE_RULES.md`,
  `docs/DECISION_PRINCIPLES.md`, `docs/DEVELOPMENT_GUIDE.md`,
  `docs/SYSTEM_OVERVIEW.md`, `docs/DOCUMENTATION_STANDARD.md`) — the
  rule statements and the workflow for changing this codebase.
- **A15 Signal Schema** (`signals/schema.py`) — the standard shape a
  signal is described in across modules.
- **A16 Context Snapshot** (`context_layer/context_engine/snapshot.py`) — the standard
  shape market context is described in across modules.
- **A17 Module Contracts** (this document, `contracts/`) — the
  precise input/output/dependency/error contract per module.
- **A18 Error Classification** (`core_layer/errors/`,
  `docs/ERROR_HANDLING.md`) — the standard exception hierarchy and
  error-code registry this document's own `contracts/error_contract.md`
  specified but deferred; implemented, not yet wired into any
  existing raise site.
- **A19 Performance Metrics** (`performance/`,
  `docs/PERFORMANCE_METRICS.md`) — the standard timing/measurement
  foundation, integrated with A18's error codes, not yet wired into
  any existing module.

After A19, v0.3.5 Foundation Completion is near its close — the next
strategic phase is **Phase 59 — Real Market Validation** (see
`docs/SYSTEM_OVERVIEW.md`'s version roadmap).

Together, they mean a future worker (human or AI agent) can pick up
almost any task in this codebase, read the relevant `docs/`/
`contracts/` files first, and implement a change without
accidentally breaking an architecture boundary nobody wrote down —
the explicit goal `docs/DEVELOPMENT_GUIDE.md`'s six-step workflow
starts with ("Check architecture" before touching any file).
