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

### Director Order No. 017 — GoldBot Development Standard (GDS)

Establishes the single Development Standard governing how code is
written, tested, refactored, and evolved: GDS-001 Coding Standard
through GDS-011 Code Review Standard, plus Definition of Done (DoD),
Development Workflow (Read → Understand → Design → Implement → Unit
Test → Integration Test → Refactor → Documentation → Validation →
Commit → Push → Review), Risk Assessment (Low/Medium/High/Critical,
High/Critical requiring Director Review), Rollback Strategy (Failure →
Rollback → Restore → Revalidate → Retest → Continue), Module Health
Score (Architecture/Contracts/Documentation/Testing/Performance/
Maintainability/Dependency/Security), Technical Debt Standard (housed
in each module's ROADMAP.md), Dependency Graph Standard (housed in
each module's CONTRACTS.md/MODULE_MAP.md), Module Status Lifecycle
(Blueprint → In Development → Implemented → Testing → Stable →
Deprecated), and an AI Knowledge Base / Lessons Learned standard
(housed in each module's WORK_LOG.md, reusing ARCA's Problem → Root
Cause → Permanent Solution → Lessons Learned structure). GDS
operationalizes existing rules (CLAUDE.md's Commit Protocol and
Trading Safety, GEL-001's doc set, ARCHITECTURE.md's Layer Direction)
into a day-to-day workflow — it does not override any of them.

Full order text and every GDS-NNN section live in
`GOLDBOT_DEVELOPMENT_STANDARD.md`.

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

### Director Order No. 021 — Deployment Authority — Worker as Deployment/DevOps Engineer

Establishes the Worker's deployment authority in two phases. Phase 1
(recommended, in effect now) is semi-autonomous: the Worker may
connect to the VPS, clone/pull the repo, create a virtualenv, install
dependencies, verify (never change) `.env`, run migrations, run tests
and a smoke test, create/update the systemd service, configure Nginx
if needed, check logs, start monitoring, fix errors, and prepare a
deployment report — but must not change production API keys, change
DNS, change firewall rules, or enable production trading. Phase 2
(fully autonomous, production-level — not yet in effect, Development
must complete first) adds CI/CD-driven deploy, Blue/Green deployment,
rollback, health check, auto-restart, monitoring, hotfix deploy, and
release deploy. Regardless of phase, replacing a Production API Key,
replacing the server, changing the VPS provider, a database reset,
changing firewall policy, replacing an SSL certificate,
enabling/disabling Live Trading, and deleting production data always
require Director Approval. The Director's own framing: the Worker is
not a VPS Administrator — the Worker performs the role of Deployment
Engineer / DevOps Engineer. The future-state target pipeline is Git
Push → Worker → CI/CD → VPS → Deploy → Health Check → Monitoring →
Report.

### Director Decision — DD-003 (Append-Only Journal Discipline)

Approved. `DIRECTOR_DECISIONS.md` is an append-only log — a missing
entry (Order No. 017's, caught and backfilled above) must never be
deferred to "next time"; it is corrected immediately as its own
append, never by editing or reordering existing entries.

**Governance Rule — Append-Only Discipline.** No entry is ever skipped
in any of the repository's append-only journals: `DIRECTOR_DECISIONS.md`,
a module's `WORK_LOG.md`, a module's `CHANGELOG.md`, an RFC record
under `rfcs/`, or an ADR record under `adrs/`. Every completed Director
Order, RFC, ADR, or significant Sprint must update its corresponding
journal immediately, in the same work pass — not deferred. This closes
the "when was this decision actually made?" question permanently by
keeping Governance History continuous.

Full order text recorded in `CLAUDE.md`'s "Deployment Authority —
Director Order No. 021" section; `docs/DEPLOYMENT.md` and
`docs/deployment/PRODUCTION_DEPLOYMENT.md` cross-reference it rather
than duplicating it.

### Director Decision — DD-004 (superseded by DD-005 below)

Recorded here for the first time, per DD-003's Append-Only Discipline
(a ratified decision must never remain only in chat history): DD-004
proposed a "flat `.py` facade" pattern for select GEL-001 modules —
keeping a canonical module as a top-level `.py` file re-exporting from
elsewhere, to preserve compatibility with code that resolves it by a
literal file path. **Status: superseded.** Empirical verification (see
DD-005) showed CPython's import system does not support this pattern
the way DD-004 assumed — see DD-005 for the corrected mechanism.

### Director Decision — DD-005 (GEL-001 Compatibility Exception)

**Approved.** The Worker's empirical finding is ratified: in CPython,
if both `system_monitor.py` and `system_monitor/` exist as siblings,
`import system_monitor` always resolves to the **package**, never the
flat file — there is no way to make a flat `.py` act as a stable
facade next to a same-named package. DD-004's flat-facade diagram is
therefore **revoked**; DD-005 replaces it.

**Canonical Decision.** GEL-001's goal remains *One Canonical Module =
One Package*, with one exception class:

**Compatibility Exception.** A module is exempted from automatic
packaging — and classified `Compatibility Exception`, not
`Violation` — if it is physically path-bound to any of: an
architecture/isolation test, an AST parser, a monkeypatch target, or
an external Public API. Converting such a module to a package would
break the very thing depending on its literal file path.

**Metrics (superseding any prior GEL-001 count):**

| Category | Count |
|---|---|
| Canonical Packages | 274 |
| Compatibility Exceptions | 11 |
| Violations | 0 |

`Exception ≠ Violation` — an exception is a deliberate, documented,
Worker-classified state; a violation is unaddressed non-compliance.

**Worker Authority.** The Worker may self-classify any module as
`Compatible → Package` or `AST Coupled → Compatibility Exception`
without Director Review — report only, per Director Order No. 016.

**Future path.** In v2, once the coupled AST tests are themselves
refactored to stop depending on the literal file path, the exception
is removed and the module is packaged normally.

**New standing rule — Empirical Verification for Foundation Rules.**
For any Foundation Rule, the Worker decides from empirical
verification, not theoretical assumption. If the real platform
(Python, the OS, Git, etc.) constrains what a rule can require, the
Worker documents the constraint and raises a Director Review to adapt
the rule — as happened here (GEL-001's flat-facade assumption in DD-004
did not hold empirically, so GEL-001 itself was adapted via DD-005
rather than forcing an unworkable rule on real code).

### DD-005 Compliance Audit — Result (commit `d9e0a84`)

A full DD-005 compliance audit (`DD005_COMPLIANCE_REPORT.md`, Uzbek,
per GLS-001 below) checked all 146 top-level canonical modules across
all 17 Layers against the seven DD-005 audit questions. Result: 146/146
`Compatible`, 0 `Potential Violations`. **One item raised for Director
Review** (documentation-completeness gap, not a Foundation Rule
breach): DD-005 states 274 Canonical Packages / 11 Compatibility
Exceptions, but no document itemizes those 11 exceptions by module
name — the audit's own top-level scope found 0 exceptions, meaning the
11 exist at a narrower/nested-file granularity that isn't registered
anywhere. Open question for Director: should a dedicated itemized
registry (e.g. `GEL001_EXCEPTIONS.md`) be created to name all 11, so
this count is independently verifiable rather than only asserted.

### Director Order — GLS-001 (GoldBot Engineering Language Standard)

**Approved.** All documents, audits, reports, and engineering records
in the GoldBot repository are written in Uzbek. Exceptions, kept in
their original form: programming languages, code elements (class/
function/file names, import statements, code blocks), API names,
library/framework names, standard protocols, and international
technical terms (the Director's own list: API, REST API, WebSocket,
Event Bus, Cache, Queue, Pipeline, Layer, Module, Package, Interface,
Dependency, Import, Export, Commit, Branch, Merge, Pull Request,
CI/CD, Docker, Kubernetes, PostgreSQL, Redis, Logger, Metrics, Health
Check, Benchmark, Performance, Rollback, Refactor, Compatibility,
Regression, Unit Test, Integration Test, Mock, Fixture — extensible,
not exhaustive). Report section headers use Uzbek terms, not copied
English templates (`Muammo`/`Sabab`/`Tavsiya`, not `Problem`/`Cause`/
`Recommendation`). Standard technical values (YES/NO, PASS/FAIL) are
exempt.

**Scope decision (Director-selected option): phased via RFC, not
immediate retroactive translation.** GLS-001 applies from this
decision onward to every newly created document, audit, and report —
already demonstrated by `DD005_COMPLIANCE_REPORT.md`, written fully
in Uzbek per this rule. The repository's existing English-language
documents (`CLAUDE.md`, `README.md`, `ARCHITECTURE.md`,
`GOLDBOT_DEVELOPMENT_STANDARD.md`, `RFC_STANDARD.md`, `ADR_STANDARD.md`,
`RELEASE_MANAGEMENT_STANDARD.md`, `DIRECTOR_DECISIONS.md` itself, and
others) are **not** retroactively translated by this decision. Full
retroactive translation — a large, risk-bearing effort, especially for
Trading Safety/Risk Logic text where a translation slip could shift
meaning — is deferred to its own dedicated RFC (per `RFC_STANDARD.md`,
since it is a Development/Engineering Standard-affecting change),
carrying its own Impact Analysis and Rollback Plan, to be scheduled as
a future Sprint rather than executed under this order.

Full order text recorded here (`DIRECTOR_DECISIONS.md`); no new
top-level file created for GLS-001 itself, per the Module Reuse
Principle — this entry is its canonical record.
