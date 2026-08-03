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
