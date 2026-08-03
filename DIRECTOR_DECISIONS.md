# Director Decisions — Append-Only Log

This file is the single append-only record of every Director-approved
decision that governs GoldBot's engineering process: Worker Authority
Registry entries (WAR), Worker Decision Rule entries (WDR), Migration
Isolation Rule entries (MIR), Repository Aggregation Rule entries
(RAR), GoldBot Engineering Law entries (GEL), and any other Director
Decision (DD) or numbered Director Order.

Entries are never edited or removed once appended — a superseded
decision gets a new entry that says so explicitly; the old entry stays
for history. Full text/history of most entries pre-dating this file
lives in `Architecture_Audit_Plan.md`; this file is the canonical
home for everything from Director Order No. 016 onward.

## Log

### Director Order No. 016 — Worker Authority Expansion

The Worker becomes System Owner of every module it works on —
responsible for that module's quality, consistency, extensibility and
stability, not only the task at hand. Grants the Worker autonomous
authority (no per-change Director approval needed) over: Autonomous
Bug Fix, Performance Optimization (behavior-preserving), Internal
Refactoring, Documentation Evolution, Test Evolution, Code Quality,
Dependency Cleanup, Module Expansion (Canonical Architecture
preserved), Backlog Management, Continuous Self Review (per-Sprint,
Director gets only the final Consolidated Review), Development
Planning (per-Sprint Task/Risk/Dependency/Estimate), and Autonomous
Root Cause Analysis (ARCA — Problem → Root Cause → Permanent Solution
→ Validation → Lessons Learned; temporary fixes forbidden).

Director Review remains mandatory whenever a change touches: Layer
Architecture, Pipeline, Trading Logic, AI Logic, Decision Logic, Risk
Logic, a public-API breaking change, Ownership, a Canonical Contract,
or a Foundation Rule.

Filing scheme (Director's own recommendation, mapped onto existing
files per the Module Reuse Principle): `ARCHITECTURE.md` for the
unchanging architecture, `CLAUDE.md` for Worker operating rules
(Order No. 016's full text lives there), this file
(`DIRECTOR_DECISIONS.md`) for the append-only decision log, and each
module's own `WORK_LOG.md` for that module's completed work.

Full order text recorded in `CLAUDE.md`'s "Worker Authority — Director
Order No. 016" section.

### Director Order No. 018 — RFC Standard

Establishes the RFC (Request For Change) process: large changes are
proposed, analyzed, risk-assessed, and Director-approved before any
code is written — never coded directly first. Mandates an RFC before
any change touching a new/removed Layer, the Pipeline, Ownership, a
Canonical Contract, Trading Logic, AI Logic, Risk Logic, Database
Architecture, a Public API Breaking Change, Security Architecture, the
Engineering Standard, or the Development Standard — the same boundary
already set by Order No. 016's Director Review list, now formalized
into a document process. The Worker may draft an RFC freely; the
Worker must not begin implementation until the RFC's Director Decision
reads Approved — a hard gate.

Full order text, the RFC template, and the process definition live in
`RFC_STANDARD.md`; individual RFC records live under `rfcs/`
(`rfcs/README.md` index, `rfcs/TEMPLATE.md` template).

### Director Order No. 019 — ADR Standard

Establishes the ADR (Architecture Decision Record) process: the
detailed technical record of *why* a significant architecture
decision was made, kept as permanent history — distinct from the
short WAR/WDR entries already in this file. Mandates an ADR for a new
Layer, a Layer merge, an Event Bus change, a Pipeline change, Database
Architecture, AI Architecture, Execution Flow, Security Architecture,
Performance Architecture, a Canonical Rule, an Engineering Rule, or a
Development Rule. An RFC is the proposal-and-approval gate; an ADR is
the permanent record of the resulting decision — a major change often
has both. The Worker may draft an ADR; it only becomes Approved after
Director sign-off — draft ADRs are not binding.

Full order text and the ADR template live in `ADR_STANDARD.md`;
individual ADR records live under `adrs/` (`adrs/README.md` index,
`adrs/TEMPLATE.md` template).

### Director Order No. 020 — Release Management Standard

Establishes the Release Lifecycle (Planning → Development → Internal
Testing → QA → Alpha → Beta → Release Candidate → Production →
Maintenance → Hotfix → End of Life) and the mandatory per-release
fields (Version Number, Scope, Features, Breaking Changes, Migration
Guide, Test Summary, Performance Summary, Security Review, Known
Issues, Rollback Strategy, Release Notes), plus a Release Checklist
(Architecture Validation, Engineering Validation, Development
Validation, Regression Test, Performance Test, Security Review,
Documentation Review, CHANGELOG, Director Approval) required before
any Production release. The Worker prepares Release Candidates, runs
tests, and writes Release Notes and Known Issues; Worker Authority
stops at Release Candidate — Production Release requires explicit
Director approval, full stop, no exception.

Full order text, lifecycle stage criteria, and the Version Numbering
convention (semantic versioning, MAJOR.MINOR.PATCH) live in
`RELEASE_MANAGEMENT_STANDARD.md`.

Orders No. 018, 019, and 020 together with Order No. 017 (GDS) and the
existing Architecture/Engineering standards form the full Governance
Chain, recorded in `CLAUDE.md`'s Worker Authority section.
