# GoldBot Platform Constitution v1.0 — Index

**Status:** Approved · Completed · **Frozen Baseline** · 40 / 40 chapters
**Edition:** Chaptered Platform Constitution v1.0 — governs the Platform layer, **subordinate to** the GoldBot Constitution v1.0.

> **Constitutional hierarchy (DPR-008):** the Platform Constitution is subordinate to the
> [GoldBot Constitution v1.0](../chapters/README.md); it does not modify it and cannot conflict
> with it. Where a matter is Core, trading, or safety, the GoldBot Constitution governs.
>
> **Platform scope (DPR-009):** the Platform layer governs User Experience, Accounts,
> Subscriptions, Notifications, Payments, Analytics, Administration, and Services. **Trading
> decisions remain the Core's authority.**
>
> **Platform safety boundary (DPR-010):** the Platform never creates a signal, evaluates a
> signal, computes risk, alters AI decisions, or bypasses Core logic. It only delivers to users
> results the Core has already cleared (Chapter 31).

Related: [Platform Director Rulings Register](PLATFORM_DIRECTOR_RULINGS_REGISTER.md) · [Platform Constitution Change Log](PLATFORM_CONSTITUTION_CHANGELOG.md) · [GoldBot Constitution Index](../chapters/README.md)

---

## Blocks

| Block | Chapters | Purpose |
|---|---|---|
| **Foundation** | 01–07 | Vision, Mission, Values, Core Principles, Long-Term Goals, Scope, Terminology (platform-scoped) |
| **Governance** | 08–17 | Platform Governance, Product Philosophy, Structure, Product Director, Product Team, Review, QA, Decisions, Docs, Versions |
| **Architecture** | 18–27 | Platform Architecture, User Management, Auth, Subscription, Notification, Settings, Service, API Contracts, Integration, Lifecycle |
| **Domain** | 28–37 | User Profiles, Membership & Plans, Payments, Signal Delivery, Administration, Analytics, Security, Operations, Risk & Abuse Prevention, Compliance |
| **Closing** | 38–40 | Amendment Process, Roadmap & Evolution, Final Provisions |

## Chapters

### Foundation (01–07)
| # | Chapter | # | Chapter |
|---|---|---|---|
| 01 | [Vision](Chapter01_Vision.md) | 05 | [Long-Term Goals](Chapter05_LongTermGoals.md) |
| 02 | [Mission](Chapter02_Mission.md) | 06 | [Scope](Chapter06_Scope.md) |
| 03 | [Values](Chapter03_Values.md) | 07 | [Terminology](Chapter07_Terminology.md) |
| 04 | [Core Principles](Chapter04_CorePrinciples.md) | | |

### Governance (08–17)
| # | Chapter | # | Chapter |
|---|---|---|---|
| 08 | [Platform Governance](Chapter08_PlatformGovernance.md) | 13 | [Review Process](Chapter13_ReviewProcess.md) |
| 09 | [Product Philosophy](Chapter09_ProductPhilosophy.md) | 14 | [Quality Assurance](Chapter14_QualityAssurance.md) |
| 10 | [Platform Structure](Chapter10_PlatformStructure.md) | 15 | [Decision Process](Chapter15_DecisionProcess.md) |
| 11 | [Product Director](Chapter11_ProductDirector.md) | 16 | [Documentation Governance](Chapter16_DocumentationGovernance.md) |
| 12 | [Product Team](Chapter12_ProductTeam.md) | 17 | [Version Strategy](Chapter17_VersionStrategy.md) |

### Architecture (18–27)
| # | Chapter | # | Chapter |
|---|---|---|---|
| 18 | [Platform Architecture](Chapter18_PlatformArchitecture.md) | 23 | [Settings System](Chapter23_SettingsSystem.md) |
| 19 | [User Management](Chapter19_UserManagement.md) | 24 | [Service Architecture](Chapter24_ServiceArchitecture.md) |
| 20 | [Authentication and Authorization](Chapter20_AuthenticationAndAuthorization.md) | 25 | [API Contracts](Chapter25_APIContracts.md) |
| 21 | [Subscription System](Chapter21_SubscriptionSystem.md) | 26 | [Integration Layer](Chapter26_IntegrationLayer.md) |
| 22 | [Notification System](Chapter22_NotificationSystem.md) | 27 | [Platform Lifecycle](Chapter27_PlatformLifecycle.md) |

### Domain (28–37)
| # | Chapter | # | Chapter |
|---|---|---|---|
| 28 | [User Profiles](Chapter28_UserProfiles.md) | 33 | [Analytics](Chapter33_Analytics.md) |
| 29 | [Membership and Plans](Chapter29_MembershipAndPlans.md) | 34 | [Security](Chapter34_Security.md) |
| 30 | [Payments](Chapter30_Payments.md) | 35 | [Operations](Chapter35_Operations.md) |
| 31 | [Signal Delivery](Chapter31_SignalDelivery.md) | 36 | [Risk and Abuse Prevention](Chapter36_RiskAndAbusePrevention.md) |
| 32 | [Administration](Chapter32_Administration.md) | 37 | [Compliance](Chapter37_Compliance.md) |

### Closing (38–40)
| # | Chapter |
|---|---|
| 38 | [Amendment Process](Chapter38_AmendmentProcess.md) |
| 39 | [Roadmap and Evolution](Chapter39_RoadmapAndEvolution.md) |
| 40 | [Final Provisions](Chapter40_FinalProvisions.md) |

---

## Reading Order

- **First-time reader:** 01 → 40; read [Chapter 07 (Terminology)](Chapter07_Terminology.md) before
  the architecture and domain blocks, and note it **inherits** the GoldBot Constitution glossary.
- **Product / governance focus:** 08 → 17, then Compliance ([37](Chapter37_Compliance.md)) and the
  closing block (38–40).
- **Engineering / architecture focus:** 18 → 27, with 04 (Core Principles) for the reasoning.
- **Safety focus:** [31 (Signal Delivery)](Chapter31_SignalDelivery.md) →
  [36 (Risk and Abuse Prevention)](Chapter36_RiskAndAbusePrevention.md) →
  [40 §7 (Final Safety Affirmation)](Chapter40_FinalProvisions.md), read alongside the GoldBot
  Constitution's Risk Governance chapter.

## Cross-reference Guidance

- **Chapter-to-chapter** references are prose ("Chapter NN (Title)"), not hyperlinks.
- **GoldBot Constitution** references are by name; the GoldBot Constitution is the primary document
  (DPR-008) and its chapters live in [`../chapters/`](../chapters/README.md).
- **Operative detail** is linked to its single source of truth (platform docs, standards, policies);
  per the single-source-of-truth rule it is not restated here.
- **Rulings** are recorded in the [Platform Director Rulings Register](PLATFORM_DIRECTOR_RULINGS_REGISTER.md);
  **changes** in the [Platform Constitution Change Log](PLATFORM_CONSTITUTION_CHANGELOG.md).

## Inherited non-amendable safety principles

Per DPR-010 and the GoldBot Constitution's DR-015, the Platform layer may never: create or evaluate
a signal, compute risk, alter AI decisions, bypass Core logic, or deliver a signal the Core has not
cleared. These are inherited and non-amendable at the platform level.
