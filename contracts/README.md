# contracts/

## Purpose
Interface & Module Contracts Foundation (Phase A17) — a precise,
per-module specification of what each layer accepts, returns, may
depend on, must never depend on, and how it reports failure. No new
business logic, no refactor, no import change: this directory writes
down boundaries `docs/ARCHITECTURE_RULES.md` and `docs/ARCHITECTURE.md`
already established, at a finer, module-by-module grain, so a future
worker or AI agent can check a specific module's contract without
re-reading the whole architecture doc set.

## Files
| File | Module |
|---|---|
| `context_contract.md` | `context/` |
| `strategy_contract.md` | `strategies/` |
| `signal_contract.md` | `signals/` |
| `ai_contract.md` | `ai/` |
| `decision_contract.md` | `decision/` |
| `risk_contract.md` | `risk/` |
| `execution_contract.md` | `execution/` |
| `telegram_contract.md` | `telegram/` |
| `database_contract.md` | `database/` |
| `error_contract.md` | Cross-cutting — the proposed `GoldBotError` hierarchy every other contract's own Error Contract section references. |

## Format
Every module contract follows the same eight-section shape:

```markdown
# Module Name
## Responsibility
## Input
## Output
## Allowed Dependencies
## Forbidden Dependencies
## Error Contract
## Future Extension
```

## Relationship to other governance docs
- `docs/ARCHITECTURE_RULES.md` (Phase A14) states module boundaries at
  the "constitution" level — short, stable, rarely-changing.
- `docs/ARCHITECTURE.md` is the detailed, implementation-accurate
  technical reference, updated every phase.
- `docs/DECISION_PRINCIPLES.md` (Phase A14) states *who owns which
  decision* — every `contracts/*.md` file's Responsibility section
  points back to the relevant principle.
- `contracts/*.md` (this directory, Phase A17) is the most granular
  tier: one file per module, with exact real input/output types
  (not illustrative pseudocode), exact allowed/forbidden imports, and
  an error-handling contract.
- `docs/MODULE_CONTRACTS.md` is the entry point tying all of the
  above together — the architecture map and the dependency-rule
  summary table.

Together with `configuration/` (A13), `docs/ARCHITECTURE_RULES.md`
(A14), `signals/schema.py` (A15), and `context/snapshot.py` (A16),
this directory completes what `docs/MODULE_CONTRACTS.md` calls
GoldBot's "platform constitution" — see that document's own closing
note.

## What this is NOT
- Not a refactor — no class moved, no import changed, no pipeline
  behavior changed. Every claim in every `contracts/*.md` file
  describes code that already exists and already behaves this way.
- Not enforced by a linter or test beyond
  `tests/contracts/test_contracts_exist.py`, which checks that every
  contract file exists and is well-formed markdown containing its
  required sections — it does not (and cannot) verify that the real
  code still matches the contract. Keeping them in sync is a
  documentation-update step in `docs/DEVELOPMENT_GUIDE.md`'s own
  code-change workflow (step 6), not a separate CI gate.
- Not a new error-handling implementation —
  `contracts/error_contract.md`'s `GoldBotError` hierarchy is a
  specification for a future, separately-approved phase to implement,
  not a new `core/errors.py` file added by this phase.
