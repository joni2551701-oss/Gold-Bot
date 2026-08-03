# Director Rulings Register

**Objective:** maintain the authoritative register of all **Director Rulings (DR)**.
A Director Ruling is a recorded, authoritative governance decision under the
Constitution ([Chapter 11 — Director](chapters/Chapter11_Director.md),
[Chapter 15 — Decision Process](chapters/Chapter15_DecisionProcess.md)).

**Register fields (per ruling):** DR Number · Title · Decision · Rationale · Related
Chapters · Status · Effective Date · Superseded By (optional).

Related: [Constitution Index](chapters/README.md) · [Constitution Change Log](CONSTITUTION_CHANGELOG.md) · operative decision history in [`docs/changelog/DECISION_LOG.md`](../changelog/DECISION_LOG.md) and the ADRs under [`communication/decisions/`](../../communication/decisions/).

> **Provenance note (honesty).** DR-013 … DR-016 are transcribed **verbatim** from the
> Director's Final Review of Constitution v1.0. DR-001 … DR-012 formalize **actual,
> approved Director decisions made earlier in the engagement** (originally recorded in
> conversation as consolidation/order/design decisions); no new decision is invented —
> each is an existing approved decision placed into the standard register fields, per
> Director instruction. Because the earlier decisions were not pre-assigned DR numbers,
> the DR-001…012 numbering is a **chronological reconstruction submitted for Director
> confirmation**; effective dates reflect the v1.1 Phase 1 session (on/around
> 2026-07-24). On confirmation, this note can be removed.

---

## DR-001 — Repository Consolidation
- **Decision:** GoldBot v1.0.0 becomes the single official `main`. Legacy branches are
  archived under `archive/*` before removal; the consolidation is history-preserving
  and non-force wherever a safe alternative exists. (Recovery path skipped; Path 2
  approved.)
- **Rationale:** Establishes one authoritative line of history and a clean baseline for
  v1.1 work.
- **Related Chapters:** [10](chapters/Chapter10_ConstitutionStructure.md), [37](chapters/Chapter37_ComplianceFramework.md)
- **Status:** Active
- **Effective Date:** 2026-07-24
- **Superseded By:** —

## DR-002 — Main-Line Changes via Pull Request
- **Decision:** Every update to `main` is made through a Pull Request with green CI and
  Director review; no direct pushes to the protected line.
- **Rationale:** Guarantees review-before-merge and an auditable change trail.
- **Related Chapters:** [13](chapters/Chapter13_Reviewer.md), [14](chapters/Chapter14_QualityAssurance.md), [17](chapters/Chapter17_VersionStrategy.md)
- **Status:** Active
- **Effective Date:** 2026-07-24
- **Superseded By:** —

## DR-003 — Architecture-First Module Cadence
- **Decision:** Each module proceeds Architecture → Design Review → Documentation →
  Implementation → Testing → Integration → Merge, with a Director Final Review before
  merge and a recorded acceptance after.
- **Rationale:** Ensures design and documentation precede code and that nothing merges
  unreviewed.
- **Related Chapters:** [08](chapters/Chapter08_GovernancePhilosophy.md), [09](chapters/Chapter09_ArchitecturePhilosophy.md), [16](chapters/Chapter16_DocumentationGovernance.md)
- **Status:** Active
- **Effective Date:** 2026-07-24
- **Superseded By:** —

## DR-004 — Foundation Isolation (Trading Safety)
- **Decision:** v1.1 foundation modules are not wired into `core/pipeline.py`; they are
  built foundation-first and integrated later only by explicit, separate authorization.
  No foundation module may bypass the Risk Manager or reach Telegram delivery.
- **Rationale:** Keeps the trading pipeline and its safety guarantees untouched while
  the Core foundation is built.
- **Related Chapters:** [07](chapters/Chapter07_NonGoalsAndTerminology.md), [18](chapters/Chapter18_CoreArchitecture.md), [36](chapters/Chapter36_RiskGovernance.md)
- **Status:** Active
- **Effective Date:** 2026-07-24
- **Superseded By:** —

## DR-005 — Acceptance Registry (MA / DD separation)
- **Decision:** Module acceptances are recorded as `MA-xxx`, kept distinct from
  architecture/governance decisions (`DD-xxx`); the two series do not collide.
- **Rationale:** Separates "this module is accepted" from "this is a governance/design
  decision," keeping the record unambiguous.
- **Related Chapters:** [15](chapters/Chapter15_DecisionProcess.md), [37](chapters/Chapter37_ComplianceFramework.md)
- **Status:** Active
- **Effective Date:** 2026-07-24
- **Superseded By:** —

## DR-006 — Canonical CandleSource Taxonomy
- **Decision:** The canonical market-data source taxonomy is STREAM / REPLAY /
  BOOTSTRAP, with RECOVERY as an additional source; components use these consistently.
- **Rationale:** One shared vocabulary for data provenance across memory, replay, and
  snapshots.
- **Related Chapters:** [20](chapters/Chapter20_MemoryArchitecture.md), [33](chapters/Chapter33_DataGovernance.md)
- **Status:** Active
- **Effective Date:** 2026-07-24
- **Superseded By:** —

## DR-007 — Live Price Service Layer
- **Decision:** Add the Live Price Service architecture layer with its `PRICE_STREAM`
  and `LIVE_PRICE` documentation, as a governed part of the market-data foundation.
- **Rationale:** Records the live-price path as an explicit, documented layer rather
  than an implicit one.
- **Related Chapters:** [20](chapters/Chapter20_MemoryArchitecture.md), [33](chapters/Chapter33_DataGovernance.md)
- **Status:** Active
- **Effective Date:** 2026-07-24
- **Superseded By:** —

## DR-008 — Replay Engine as the Core Time Layer (Module 8)
- **Decision:** Module 8 (Replay) is the Core time-control layer — LIVE/REPLAY modes, a
  virtual clock, timeline control, seamless Replay→LIVE handoff, and bookmarkable
  sessions — approved with amendments (state machine, replay events, bookmarks,
  validation, `ReplayManager` SRP, simulation source).
- **Rationale:** Gives the Core controlled, reproducible time without touching data
  consumers.
- **Related Chapters:** [22](chapters/Chapter22_ReplayArchitecture.md)
- **Status:** Active
- **Effective Date:** 2026-07-24
- **Superseded By:** —

## DR-009 — Snapshot Management Boundary (Module 9)
- **Decision:** Module 6 *creates and stores* snapshots; Module 9 *manages* them
  (catalog, registry, lifecycle, policy/cleanup, import/export, metrics), approved with
  amendments (Manifest, Lock, State machine, Compatibility check, Transactions,
  Extended events). Module 9 reuses Module 6 rather than re-implementing it.
- **Rationale:** Separates creation/storage from management and prevents duplicate
  persistence logic.
- **Related Chapters:** [23](chapters/Chapter23_SnapshotArchitecture.md)
- **Status:** Active
- **Effective Date:** 2026-07-24
- **Superseded By:** —

## DR-010 — Core Gateway Layer Scope (Module 10)
- **Decision:** Module 10 is the Core Gateway Layer — the single entry point (service
  registry/discovery, internal/external API, authentication, authorization, rate
  limiting, health/metrics/version), not a plain API layer — approved with amendments
  (Service Lifecycle, Capability Discovery, Dependency Graph, Gateway Context, Circuit
  Breaker, Service Manifest).
- **Rationale:** Establishes one governed door through which every surface reaches the
  Core.
- **Related Chapters:** [19](chapters/Chapter19_GatewayArchitecture.md), [24](chapters/Chapter24_ServiceArchitecture.md), [34](chapters/Chapter34_APIGovernance.md)
- **Status:** Active
- **Effective Date:** 2026-07-25
- **Superseded By:** —

## DR-011 — Gateway Placement
- **Decision:** The Gateway is implemented at `core_layer/gateway/` (a subpackage of the
  existing `core/` package), not as a new top-level package.
- **Rationale:** Honors the reuse principle (a new file inside an existing package over
  a new top-level folder) and matches the "Core Gateway" naming.
- **Related Chapters:** [04](chapters/Chapter04_CorePrinciples.md), [10](chapters/Chapter10_ConstitutionStructure.md), [19](chapters/Chapter19_GatewayArchitecture.md)
- **Status:** Active
- **Effective Date:** 2026-07-25
- **Superseded By:** —

## DR-012 — Gateway Transport Independence
- **Decision:** The Gateway uses in-process handlers now; HTTP / WebSocket / gRPC / IPC
  / remote transports are added later. The Gateway stays transport-independent — a
  request is a plain value.
- **Rationale:** Lets access mechanisms evolve at the edge without changing the Core or
  its contracts.
- **Related Chapters:** [19](chapters/Chapter19_GatewayArchitecture.md), [34](chapters/Chapter34_APIGovernance.md)
- **Status:** Active
- **Effective Date:** 2026-07-25
- **Superseded By:** —

---

## DR-013 — Constitution Consolidation
- **Decision:** The GoldBot Chaptered Constitution v1.0 is the primary and only
  normative governance document. `CONSTITUTION.md`, `ARTICLES.md`, and `AMENDMENTS.md`
  are retained as historical documents and are no longer independent normative sources;
  their necessary content is consolidated into the Chaptered Constitution v1.0 or
  migrated via future amendments.
- **Rationale:** Establishes a single normative source and removes ambiguity between the
  chaptered and Articles-based editions.
- **Related Chapters:** [10](chapters/Chapter10_ConstitutionStructure.md), [40](chapters/Chapter40_FinalProvisions.md)
- **Status:** Active
- **Effective Date:** 2026-07-25
- **Superseded By:** —

## DR-014 — Constitution Freeze
- **Decision:** The present 40 chapters are frozen as Constitution Baseline v1.0 (Frozen
  Baseline). Any change is made only via an ADR, the Constitution Amendment Process, and
  Director approval.
- **Rationale:** Locks a stable baseline so the ecosystem can build on it; changes become
  deliberate and governed rather than ad hoc.
- **Related Chapters:** [38](chapters/Chapter38_AmendmentProcess.md), [40](chapters/Chapter40_FinalProvisions.md)
- **Status:** Active
- **Effective Date:** 2026-07-25
- **Superseded By:** —

## DR-015 — Safety Guarantees (non-amendable)
- **Decision:** The following are confirmed as non-amendable constitutional principles:
  (1) the Risk Manager is not bypassed; (2) the AI does not independently execute trades;
  (3) human oversight is preserved; (4) Trading Safety takes precedence over all other
  modules.
- **Rationale:** Makes the user's structural protection permanent and beyond the reach of
  the amendment process.
- **Related Chapters:** [07](chapters/Chapter07_NonGoalsAndTerminology.md), [28](chapters/Chapter28_AIArchitecture.md), [36](chapters/Chapter36_RiskGovernance.md), [40](chapters/Chapter40_FinalProvisions.md)
- **Status:** Active (non-amendable)
- **Effective Date:** 2026-07-25
- **Superseded By:** — (may be strengthened, never weakened)

## DR-016 — Single Source of Truth
- **Decision:** The Constitution defines principles; operative detail is carried via
  architecture docs, ADRs, standards, policies, and specifications. Identical rules are
  not written twice.
- **Rationale:** Prevents duplicated, drifting governance and keeps one authoritative
  source per domain.
- **Related Chapters:** [10](chapters/Chapter10_ConstitutionStructure.md), [16](chapters/Chapter16_DocumentationGovernance.md), [37](chapters/Chapter37_ComplianceFramework.md)
- **Status:** Active
- **Effective Date:** 2026-07-25
- **Superseded By:** —

---

## Register Conventions

- **Append** each new ruling with the next DR number and all eight fields.
- A ruling that changes a frozen chapter's meaning also requires the Amendment Process
  ([Chapter 38](chapters/Chapter38_AmendmentProcess.md)) and is cross-referenced from the
  [Constitution Change Log](CONSTITUTION_CHANGELOG.md).
- **Superseded By** is set (not deleted) when a later ruling replaces an earlier one,
  preserving the full history.
- Safety-related rulings may **strengthen** but never weaken the DR-015 guarantees.
