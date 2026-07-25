# GoldBot Constitution v1.0 — Index

**Status:** Approved · Completed · **Frozen Baseline** (DR-013, DR-014) · 40 / 40 chapters
**Edition:** Chaptered Constitution v1.0 — the single, primary governing document of GoldBot (DR-013).

> **DR-013 (Constitution Consolidation):** the Chaptered Constitution v1.0 is the
> primary and only normative governance document. The earlier
> [`CONSTITUTION.md`](../CONSTITUTION.md), [`ARTICLES.md`](../ARTICLES.md), and
> [`AMENDMENTS.md`](../AMENDMENTS.md) are retained as **historical** references
> and are no longer independent normative sources; their necessary content is
> consolidated into this edition or migrated via future amendments.
>
> **DR-014 (Freeze):** these 40 chapters are frozen as Constitution Baseline
> v1.0. Any change is made only via an ADR, the Amendment Process
> ([Chapter 38](Chapter38_AmendmentProcess.md)), and Director approval.

Related registers: [Director Rulings Register](../DIRECTOR_RULINGS_REGISTER.md) · [Constitution Change Log](../CONSTITUTION_CHANGELOG.md)

---

## Blocks

| Block | Chapters | Purpose |
|---|---|---|
| **Foundational** | 01–07 | What GoldBot is: vision, mission, values, principles, goals, scope, terminology |
| **Governance** | 08–17 | How GoldBot is governed: philosophy, structure, roles, quality, decisions, docs, versions |
| **Architecture** | 18–27 | How the Core is built: components, gateway, memory, events, replay, snapshots, services, contracts, integration, lifecycle |
| **Domain** | 28–37 | AI, platform, media, security, data, API, operations, risk, compliance |
| **Closing** | 38–40 | Amendment process, roadmap & evolution, final provisions |

## Chapters

### Foundational (01–07)
| # | Chapter | Summary |
|---|---|---|
| 01 | [Vision](Chapter01_Vision.md) | The enduring *why*: a trustworthy, platform-independent trading-intelligence Core |
| 02 | [Mission](Chapter02_Mission.md) | The standing obligation: disciplined, auditable, safe XAUUSD intelligence for a human |
| 03 | [Values](Chapter03_Values.md) | The tie-breakers: foundation, safety, and auditability over speed |
| 04 | [Core Principles](Chapter04_CorePrinciples.md) | Foundation/Gateway/Platform/Knowledge/Documentation First, Reuse, Safety, Evolution |
| 05 | [Long-Term Goals](Chapter05_LongTermGoals.md) | 5–10 year goals in architecture and governance terms |
| 06 | [Scope](Chapter06_Scope.md) | In/out of scope, boundaries, constraints, expansion rules |
| 07 | [Non-Goals & Terminology](Chapter07_NonGoalsAndTerminology.md) | Non-goals and the reserved-term glossary of record |

### Governance (08–17)
| # | Chapter | Summary |
|---|---|---|
| 08 | [Governance Philosophy](Chapter08_GovernancePhilosophy.md) | Why and how GoldBot is governed |
| 09 | [Architecture Philosophy](Chapter09_ArchitecturePhilosophy.md) | Stable interior, evolving perimeter |
| 10 | [Constitution Structure](Chapter10_ConstitutionStructure.md) | Editions, blocks, chapter anatomy, package standard |
| 11 | [Director](Chapter11_Director.md) | Authority to set direction and authorize change — and its limits |
| 12 | [Worker](Chapter12_Worker.md) | Execution discipline, no silent decisions, role limits |
| 13 | [Reviewer](Chapter13_Reviewer.md) | The check between completed work and its taking effect |
| 14 | [Quality Assurance](Chapter14_QualityAssurance.md) | Correctness as a precondition of delivery |
| 15 | [Decision Process](Chapter15_DecisionProcess.md) | No silent decisions; escalation; recording; traceability |
| 16 | [Documentation Governance](Chapter16_DocumentationGovernance.md) | Documentation-first; single source of truth |
| 17 | [Version Strategy](Chapter17_VersionStrategy.md) | Announced versions, compatibility, amend rarely/extend routinely |

### Architecture (18–27)
| # | Chapter | Summary |
|---|---|---|
| 18 | [Core Architecture](Chapter18_CoreArchitecture.md) | The stable interior and its components |
| 19 | [Gateway Architecture](Chapter19_GatewayArchitecture.md) | The single governed entry point |
| 20 | [Memory Architecture](Chapter20_MemoryArchitecture.md) | The authority for market data and state |
| 21 | [Event Architecture](Chapter21_EventArchitecture.md) | The typed publish/subscribe backbone |
| 22 | [Replay Architecture](Chapter22_ReplayArchitecture.md) | The Core time-control layer |
| 23 | [Snapshot Architecture](Chapter23_SnapshotArchitecture.md) | Durable, verifiable capture and management of state |
| 24 | [Service Architecture](Chapter24_ServiceArchitecture.md) | Core capability as governed services |
| 25 | [Contract Architecture](Chapter25_ContractArchitecture.md) | Stable interfaces between parts |
| 26 | [Integration Architecture](Chapter26_IntegrationArchitecture.md) | Integration only through the gateway |
| 27 | [Core Lifecycle](Chapter27_CoreLifecycle.md) | Startup, readiness, operation, recovery |

### Domain (28–37)
| # | Chapter | Summary |
|---|---|---|
| 28 | [AI Architecture](Chapter28_AIArchitecture.md) | Advisory intelligence, bounded by design |
| 29 | [AI Governance](Chapter29_AIGovernance.md) | The advisory-only guarantee, governed |
| 30 | [Platform Architecture](Chapter30_PlatformArchitecture.md) | One shared platform model for all surfaces |
| 31 | [Media Architecture](Chapter31_MediaArchitecture.md) | Media as a consumer surface |
| 32 | [Security Governance](Chapter32_SecurityGovernance.md) | Access controlled at the gateway boundary |
| 33 | [Data Governance](Chapter33_DataGovernance.md) | Core-owned, integrity-checked, auditable data |
| 34 | [API Governance](Chapter34_APIGovernance.md) | One governed API surface |
| 35 | [Operational Model](Chapter35_OperationalModel.md) | Observable, healthy, recoverable operations |
| 36 | [Risk Governance](Chapter36_RiskGovernance.md) | Risk Manager never bypassed (constitutional level; no risk logic) |
| 37 | [Compliance Framework](Chapter37_ComplianceFramework.md) | Verifying GoldBot follows its own Constitution |

### Closing (38–40)
| # | Chapter | Summary |
|---|---|---|
| 38 | [Amendment Process](Chapter38_AmendmentProcess.md) | How settled meaning is changed — rarely, deliberately, on the record |
| 39 | [Roadmap & Evolution](Chapter39_RoadmapAndEvolution.md) | Phase 2 work packages on top of a complete Core |
| 40 | [Final Provisions](Chapter40_FinalProvisions.md) | Ratification, precedence, severability, final safety affirmation |

---

## Non-amendable safety principles (DR-015)

These constitutional principles are permanent and may not be amended away
(Chapters 07, 36, 38, 40):

1. The **Risk Manager is never bypassed**.
2. The **AI never executes a trade** independently (advisory-only).
3. **Human oversight** is preserved (semi-automatic).
4. **Trading Safety takes precedence** over every other module and concern.

## Single Source of Truth (DR-016)

The Constitution states **principles**. Operative detail is carried in the
architecture docs, ADRs, standards, policies, and specifications, and is not
duplicated here — each governance domain has one authoritative source, which the
relevant chapters cross-link.

## Reading Order

- **First-time reader:** read the blocks in order, 01 → 40. The foundational block
  (01–07) sets the vocabulary and intent every later chapter relies on; read
  [Chapter 07](Chapter07_NonGoalsAndTerminology.md) (glossary of reserved terms)
  before the architecture and domain blocks.
- **Governance / process focus:** 08 → 17, then the compliance chapter
  ([37](Chapter37_ComplianceFramework.md)) and the closing block (38–40).
- **Engineering / architecture focus:** start at [18](Chapter18_CoreArchitecture.md),
  then 19–27; consult 04 (Core Principles) and 09 (Architecture Philosophy) for the
  reasoning behind the structure.
- **Safety focus:** [07](Chapter07_NonGoalsAndTerminology.md) →
  [28](Chapter28_AIArchitecture.md)/[29](Chapter29_AIGovernance.md) →
  [36](Chapter36_RiskGovernance.md) → [40 §7](Chapter40_FinalProvisions.md) — the
  non-amendable guarantees (DR-015) and where they are stated.
- **In every case**, the closing block (38–40) explains how the document is amended,
  where it is going, and how it takes effect.

## Cross-reference Guidance

- **Chapter-to-chapter references** are written in prose as "Chapter NN (Title)",
  not as hyperlinks, so the meaning survives regardless of where a chapter is read.
- **Operative detail** is referenced by a link to its single source of truth
  (architecture docs, ADRs, standards, policies, contracts) under the chapter
  header's *Operative sources* line — per DR-016, that source is authoritative and is
  not restated in the chapter.
- **Reserved terms** carry exactly the meaning defined in
  [Chapter 07](Chapter07_NonGoalsAndTerminology.md); when a term is used, that
  glossary is its definition.
- **Rulings** are referenced by DR number and recorded in the
  [Director Rulings Register](../DIRECTOR_RULINGS_REGISTER.md); **changes** are
  recorded in the [Constitution Change Log](../CONSTITUTION_CHANGELOG.md).
- One operative cross-reference — Chapter 09's link to the Core Gateway architecture
  document — resolves once Module 10 (the Gateway) is merged to the main line
  (milestone MA-010); until then it is referenced in prose.
