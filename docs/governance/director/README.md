# Director Decision Records (DD)

The controlled registry of **Director Decision Records** for GoldBot
Engineering Governance v1.1. A Director Decision Record (`DD-XXX.md`)
is the durable, audit-traceable form of a ratified Director ruling at
the **architecture, governance, or repository** level.

## Why this folder exists (Director Policy, DD-004)

Per **DD-004 — Governance Records**, the standing rule from its own
introduction onward is:

> No architecture-, governance-, or repository-level Director decision
> may remain only in chat history. Once ratified it is preserved in the
> governance documents as a formal Decision Record.

This registry is where those records live, versioned with individual
identifiers (`DD-001`, `DD-002`, …) so the decision set stays coherent
and auditable as it grows. It is distinct from — and complementary to —
the existing `communication/decisions/ADR-*.md` Architecture Decision
Records: ADRs capture *architecture/engineering* decisions surfaced
during task work; DD records capture *Director-tier* rulings on
governance, canonical-source, branch status, and audit outcomes.

## Scope note (Execution Constraint, DD-004)

These records are documented on the **working branch**
(`claude/trading-ai-arch-review-tgszrz`) — **not** on `main`. Recording
a Director decision is a documentation act; it does not touch the
Recovery Git sequence, does not alter the production branch, and does
not conflict with the Migration SSOT (`docs/governance/MIGRATION_PLAN.md`).

## Registry

| ID | Title | Decision | Status |
|----|-------|----------|--------|
| [DD-001](DD-001.md) | Audit Acceptance & Flag Rulings | Repository / Structure / Validation / Migration-Plan audits ACCEPTED; FLAG 1 (QA/Release roles) REJECTED; FLAG 2 (no Migration before Recovery) ACCEPTED | Approved |
| [DD-002](DD-002.md) | Canonical Source | `claude/code-analysis-optimization-pwfo3q` (production) **= GoldBot v1**, the reference implementation | Approved |
| [DD-003](DD-003.md) | `main` Branch Status | Current `main` is a temporary holding branch, not development/production/release | Approved |
| [DD-004](DD-004.md) | Governance Records | Director decisions are persisted as controlled Decision Records; establishes this registry | Approved |
| [DD-024](DD-024.md) | Repository Consolidation & GoldBot v1.0.0 Release | Recovery SKIPPED (supersedes DD-001); Path 2 approved; `main` consolidated to v1.0.0 non-force; old branches archived; tag deferred | Approved / Executed |

> **Numbering note:** DD-024 uses the identifier the Director assigned
> directly from the decision stream; DD-005…DD-023 are reserved/unused in
> this registry. The gap is intentional, recorded here per No Silent
> Decisions rather than renumbered.

## Related

- `docs/governance/roles/Director.md` — the Director role definition
  (authority these records exercise).
- `docs/governance/MIGRATION_PLAN.md` — the Recovery + Migration SSOT
  these decisions govern the sequencing of.
- `communication/decisions/ADR-*.md` — Architecture Decision Records
  (engineering-tier; complementary, not superseded).
