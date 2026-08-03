══════════════════════════════════════════════════════════════════════════════
                            ARCHITECTURE AUTHORITY
══════════════════════════════════════════════════════════════════════════════

**Revision 2 (TASK-ARCH-001 correction).** Revision 1 (TASK-GOV-003)
declared this document "the single official Master Architecture...
where any other document appears to describe the ecosystem's shape,
this document is the one that governs." **That claim was wrong and is
withdrawn here.** `docs/constitution/CONSTITUTION.md` already exists,
predates this document, and states in its own opening line: "This is
the single highest-authority governance document in this repository."
Under it, `docs/architecture/ARCHITECTURE_MASTER.md`,
`LAYER_CONTRACT.md`, `MODULE_DEPENDENCIES.md`, `DATA_FLOW.md`,
`SYSTEM_LAYERS.md`, `IMPORT_RULES.md` and their siblings already exist
as the Constitution-governed, code-verified architecture of the
Trading Core + AI + Telegram system. Revision 1 was written without
checking for `docs/constitution/` or `docs/architecture/` first — a
Reuse-First failure (Constitution Article 7), corrected here by
Owner instruction rather than repeated.

**Status: ECOSYSTEM ARCHITECTURE** — the architecture-tier document
(Constitution Article 8's "Constitution → Architecture → Roadmap →
Policy → Audit → Code" order) for the full, long-horizon **Senior
Trading AI Ecosystem** vision — the layers beyond the Trading
Core/AI/Telegram system `ARCHITECTURE_MASTER.md` already covers in
depth (media, business, learning, platform expansion, future
expansion). It sits **beside**, not above, the existing
Constitution-governed architecture set, and never restates content
that set already owns — see "Division of authority" below.

1. **Ecosystem scope.** This document is the architecture reference for
   the ecosystem's full intended shape — vision, layer inventory,
   ecosystem-wide data flow, gap analysis against the current
   repository, and the roadmap. For the Trading Core/AI/Telegram
   system's real, code-verified layer contracts, dependency graph, and
   pipeline stage order, `docs/architecture/ARCHITECTURE_MASTER.md`
   (+ `LAYER_CONTRACT.md`/`MODULE_DEPENDENCIES.md`/`DATA_FLOW.md`) are
   authoritative — this document references them, never restates them.
2. **Basis for ecosystem-level tasks.** A task that adds a layer or
   module not yet covered by the Constitution-governed set (Platform
   apps beyond Telegram, Business/Billing, Academy, Media Hub, Future
   Expansion) derives from this document. A task inside the Trading
   Core/AI/Telegram system derives from `ARCHITECTURE_MASTER.md` and
   the Constitution first.
3. **Placement before implementation.** Every new module is first
   placed into its position in the applicable architecture document
   before any code for it is written (Constitution Article 7/11).
4. **No contradiction.** No implementation may contradict the
   Constitution, `ARCHITECTURE_MASTER.md`, or this document. A
   perceived conflict between this document and the Constitution-
   governed set is resolved in the Constitution-governed set's favor
   (it is more specific and code-verified) — never silently, and never
   by a Worker alone (Constitution Article 8, STOP → AUDIT → Owner
   Decision). Any such conflict actually found is listed, not resolved,
   in "Conflicts Requiring Owner Decision" below.
5. **Change protocol (architecture-first).** Changing this document
   follows Constitution Article 8's order: an Architecture Task is
   Owner-approved first, only then is the diagram/document updated,
   only then does implementation begin.

## Division of authority (added, Revision 2)

```
docs/constitution/CONSTITUTION.md         <- supreme (Article 8's own order)
        │
        ├── docs/architecture/ARCHITECTURE_MASTER.md   } Trading Core / AI /
        │   docs/architecture/LAYER_CONTRACT.md         } Telegram system —
        │   docs/architecture/MODULE_DEPENDENCIES.md     } real, code-verified,
        │   docs/architecture/DATA_FLOW.md                } authoritative for
        │   docs/architecture/SYSTEM_LAYERS.md              } their own scope.
        │
        └── docs/architecture/01_Ecosystem_Architecture.md   <- THIS document: the wider
              (this document, high-level map)         ecosystem vision, gap
                    │                                 analysis, roadmap.
                    ▼
              docs/architecture/02_Data_Layer.md .. 11_Infrastructure.md
              <- per-layer ecosystem-level detail (TASK-GOV-004 restructure,
                 Owner-directed, Option A: these summarize and cross-
                 reference the set above where it overlaps them; they do
                 not duplicate or absorb it — see "Layer Detail Documents"
                 below).
```

Both branches report to the Constitution; neither branch overrides the
other. Where this document's diagram (below, unchanged from Revision 1
per the change protocol) names a box the Constitution-governed set
already names differently or not at all, that is logged in "Conflicts
Requiring Owner Decision," not silently reconciled.

Governance control chain (a Worker follows this to place a new task):

      Constitution                (supreme; Article 8 order)
            │
            ▼
      ARCHITECTURE_MASTER.md  ── or ──  01_Ecosystem_Architecture.md
      (Trading Core/AI/Telegram)        (wider ecosystem layers)
            │                                  │
            └──────────────┬───────────────────┘
                            ▼
                    Architecture Tasks          (Owner-approved)
                            │
                            ▼
                     Technical Tasks
                            │
                            ▼
                    Implementation
                            │
                            ▼
                       Review
                            │
                            ▼
                       Merge                    (Owner-approved, per Branch rules)

Relationship to governance:
- docs/governance/collaboration/TASK-GOV-003.md — Revision 1's task
  record (the overclaim corrected above).
- docs/governance/collaboration/TASK-ARCH-001.md — this revision's task
  record; the full documentation set (Vision through Golden Rules) this
  task added is appended below the existing diagram.
- docs/governance/collaboration/TASK-GOV-001.md — the claude/collaboration
  working rules (single dev branch, task lifecycle, Laws 1–12) under
  which architecture-derived tasks are executed.
- docs/governance/roles/Collaboration_Rules.md,
  docs/governance/policies/Branch_Policy.md — the repository-wide
  governance this document sits alongside.

The diagram below is unchanged from Revision 1 — per the change
protocol (principle 5) and the Owner's explicit instruction not to
resolve the diagram-vs-`ARCHITECTURE_MASTER.md` discrepancy
unilaterally, it is edited only under an approved Architecture Task.

══════════════════════════════════════════════════════════════════════════════
                         SENIOR TRADING AI ECOSYSTEM
══════════════════════════════════════════════════════════════════════════════

                               GoldBot Start
                                     │
                                     ▼
                           Configuration Layer
                 (Environment • Features • Secrets • Version)
                                     │
                                     ▼
                             Provider Factory
                                     │
                ┌────────────────────┴────────────────────┐
                ▼                                         ▼
      Historical Data Service                 Price Stream Service
      (Bootstrap / Recovery)                   (Live Streaming)
                │                                         │
                ▼                                         ▼
     Twelve Data / Providers                Bitget / Exchange APIs
                │                                         │
                └────────────────────┬────────────────────┘
                                     ▼
                            Data Validation Layer
                                     │
                                     ▼
                               Market Memory
                        (Single Source of Truth)
                                     │
      ┌──────────────┬──────────────┬──────────────┬──────────────┐
      ▼              ▼              ▼              ▼
 Current Price   Candle Builder  Historical DB  Event Bus
                                     │
══════════════════════════════════════════════════════════════════════════════
                               GOLDBOT CORE
══════════════════════════════════════════════════════════════════════════════

                              Market Engine
                                     │
                              Context Engine
                                     │
                              Analysis Engine
                                     │
                              Strategy Engine
                                     │
                            Confluence Engine
                                     │
                             Decision Engine
                                     │
        ┌──────────────┬──────────────┬──────────────┬──────────────┐
        ▼              ▼              ▼              ▼
   Risk Engine   Signal Engine   Monitoring   Simulation
                                     │
                                     ▼
                              GoldBot Core API

══════════════════════════════════════════════════════════════════════════════
                           APPLICATION SERVICES
══════════════════════════════════════════════════════════════════════════════

                        API / WebSocket Gateway
                                     │
     ┌──────────────┬──────────────┬──────────────┬──────────────┐
     ▼              ▼              ▼              ▼
 Signal Service  Chart Service  AI Service  Notification Service
     │              │              │              │
     ├──────────────┼──────────────┼──────────────┤
     ▼              ▼              ▼              ▼
 Replay Service Analytics Service User Service Portfolio Service

══════════════════════════════════════════════════════════════════════════════
                                 AI LAYER
══════════════════════════════════════════════════════════════════════════════

                              Senior AI
                             Seniorita AI
                                   │
      ┌──────────────┬──────────────┬──────────────┬──────────────┐
      ▼              ▼              ▼              ▼
 Trading AI     Learning AI     Voice AI     Vision AI
                                   │
                         AI Explanation Engine

══════════════════════════════════════════════════════════════════════════════
                              PLATFORM LAYER
══════════════════════════════════════════════════════════════════════════════

     ┌──────────────┬──────────────┬──────────────┬──────────────┐
     ▼              ▼              ▼              ▼
 Telegram      Mobile App      Desktop App      Web Platform
                                     │
                                     ▼
                                Public API

══════════════════════════════════════════════════════════════════════════════
                           USER EXPERIENCE LAYER
══════════════════════════════════════════════════════════════════════════════

     ┌──────────────┬──────────────┬──────────────┬──────────────┐
     ▼              ▼              ▼              ▼
 Chart Engine   Trade Journal   Analytics   Notifications
     │              │              │              │
     ▼              ▼              ▼              ▼
 Multi TF       Replay         Portfolio      Push
 Drawing        Notes          Statistics     Telegram
 SMC Layer      History        Reports        Email
 Elite View

══════════════════════════════════════════════════════════════════════════════
                              BUSINESS LAYER
══════════════════════════════════════════════════════════════════════════════

     ┌──────────────┬──────────────┬──────────────┬──────────────┐
     ▼              ▼              ▼              ▼
 Identity      Subscription     Payment      Referral
     │              │              │              │
     ▼              ▼              ▼              ▼
 User Profile   FREE / PRO     Wallet      Rewards
 Roles          ELITE          Billing

══════════════════════════════════════════════════════════════════════════════
                          ACADEMY LAYER (User Education)
══════════════════════════════════════════════════════════════════════════════

Renamed from "LEARNING LAYER" (Owner ruling, TASK-ARCH-001 Conflict 3):
this box is the user-facing education product. It is a distinct thing
from "Learning Engine" — the real, existing `learning/` ML/feedback
package inside GoldBot Core (Section 5) that learns from trade
outcomes. Same word, two different systems; see Section 11.

Academy
│
├── Interactive Lessons
├── Replay
├── Simulator
├── AI Coach
├── Challenge
├── Tournament
├── PvP / AI vs AI
├── Certification
└── Career Mode

══════════════════════════════════════════════════════════════════════════════
                                MEDIA LAYER
══════════════════════════════════════════════════════════════════════════════

Media Hub
│
├── YouTube
├── Telegram Broadcast
├── TikTok
├── Shorts
├── Podcast
├── Weekly Market Review
├── AI Content Studio
└── Live Streaming

══════════════════════════════════════════════════════════════════════════════
                           FUTURE EXPANSION
══════════════════════════════════════════════════════════════════════════════

Marketplace
Strategy Builder
Indicator Store
Plugin System
Developer SDK
Enterprise Platform
Research Center
Broker Integration
Multi Broker
Cloud Sync
Team Workspace

══════════════════════════════════════════════════════════════════════════════
                    SECURITY & INFRASTRUCTURE LAYER
══════════════════════════════════════════════════════════════════════════════

Security
Authentication
Authorization
Encryption
Storage
Cache
Logging
Metrics
Observability
Health Monitoring
Backup
Disaster Recovery
Scheduler
Queue System
Audit Logs

══════════════════════════════════════════════════════════════════════════════
                           GOLDEN ARCHITECTURE RULES
══════════════════════════════════════════════════════════════════════════════

1. Market Memory — Single Source of Truth.
2. GoldBot Core faqat hisoblaydi.
3. AI qaror qabul qilmaydi, faqat tahlil va tushuntirish beradi.
4. Platformlar faqat Application Services orqali ishlaydi.
5. Barcha platformalar bitta GoldBot Core API'dan foydalanadi.
6. Providerlar yozadi, Consumerlar faqat o'qiydi.
7. Event Bus modullarni bog'laydi, ular bir-biriga to'g'ridan-to'g'ri bog'lanmaydi.
8. Reuse First — dublikat logika yaratilmaydi.
9. Har bir qatlam faqat o'z vazifasi uchun javobgar.
10. Core mustaqil qoladi va kelajakdagi barcha platformalar uning ustiga quriladi.
══════════════════════════════════════════════════════════════════════════════
                    MASTER ARCHITECTURE DOCUMENTATION (TASK-ARCH-001)
══════════════════════════════════════════════════════════════════════════════

Owner's roadmap sketch (added directly, concurrently with this task's
own restructure below — kept as-is, not overwritten; reconciled with
what was actually built in "Layer Detail Documents" just below):

Roadmap
01. DATA LAYER
02. GOLDBOT CORE
03. APPLICATION SERVICES
04. AI LAYER
05. PLATFORM LAYER
06. USER EXPERIENCE
07. BUSINESS LAYER
08. LEARNING LAYER
09. MEDIA LAYER
10. ECOSYSTEM ROADMAP

(This sketch predates the Learning→Academy rename and the final
`01_Ecosystem_Architecture.md`/`02`–`11` numbering below, where `01`
itself is the high-level document rather than a numbered layer, and
Infrastructure has its own file. Not force-reconciled here — flagged,
per this branch's own Laws, for the Owner to confirm or adjust.)

Everything below expands the diagram and Golden Rules above into a full
architecture document, per TASK-ARCH-001. Where a topic is already
covered in depth by the Constitution-governed set
(`docs/constitution/CONSTITUTION.md`, `docs/architecture/*.md`), this
document references it rather than restating it (Constitution Article
7, Reuse Principle; Owner instruction on this task). Sections below are
original content only where the referenced set does not already cover
the ground — most visibly Sections 6, 8–14 (layers beyond the Trading
Core/AI/Telegram system), and Sections 17–19 (audit/gap/roadmap, which
are new synthesis by definition).

## Layer Detail Documents (TASK-GOV-004 restructure)

Full detail for each ecosystem layer now lives in its own file
under this directory, split out of this document's former Sections
4-12/14 (Owner-directed restructure, Option A: ecosystem-level
summaries, not a duplicate of `ARCHITECTURE_MASTER.md`'s Trading-
Core/AI/Telegram mechanical detail). This document (01) stays the
high-level map: Vision, Overview, Principles, Future Expansion,
Data Flow, Dependency Rules, Refactoring Audit, Gap Analysis,
Roadmap, Golden Rules, Conflicts, and the Self-Test.

- `02_Data_Layer.md` — Data Layer
- `03_GoldBot_Core.md` — GoldBot Core
- `04_Application_Services.md` — Application Services
- `05_AI_Layer.md` — AI Layer
- `06_Platform_Layer.md` — Platform Layer
- `07_User_Experience.md` — User Experience Layer
- `08_Business_Layer.md` — Business Layer
- `09_Academy_Layer.md` — Academy Layer
- `10_Media_Layer.md` — Media Layer
- `11_Infrastructure.md` — Infrastructure

## 1. Vision

**What is the Senior Trading AI Ecosystem?** GoldBot today is a
semi-automatic XAUUSD trading-signal bot: a deterministic pipeline
(`core/pipeline.py`) that reads market data, builds context, generates
and grades signal candidates, gets an advisory AI read, makes a
rule-based APPROVE/REJECT/NO_TRADE decision, validates risk geometry,
and — at most once per cycle — delivers a Telegram message. That system
is real, tested, and Constitution-governed (`ARCHITECTURE_MASTER.md`).

The diagram above this section describes something larger: GoldBot as
the trading core of a full ecosystem — live multi-asset data, an AI
layer that can eventually explain in a human voice, a platform layer
reaching Telegram/Web/Mobile/Desktop, a business layer supporting
subscriptions, a learning layer teaching the methodology the bot
trades, and a media layer broadcasting it. **This is the vision; it is
not the current state of the repository**, and Section 8 (Gap
Analysis) states exactly which parts are real and which are not, so
this document never overstates capability (Constitution Article 8's
honesty requirement; `docs/governance/roles/Collaboration_Rules.md`
§17 "Honesty over completeness").

**Why is it being built?** To turn a single trading-signal bot into a
platform: one deterministic, auditable core that many products (a
Telegram bot, a future app, an education product, a media presence)
can be built on top of without ever duplicating or bypassing the core's
decision logic.

**10-year goal.** A Trading Core that has not changed its fundamental
guarantee (Article 1: the Trading Engine decides, the AI never does) is
still running, now serving multiple platforms, funding an education and
media business, with the AI layer's role having grown from "explain a
signal" toward richer analysis and voice — but never toward "decide a
trade." The core's auditability and the Article 1 boundary are the
one guarantee that must survive all ten years unchanged; everything
above it is expected to grow.

**Core principles** (see Section 3 for the full, non-duplicated list):
Single Source of Truth (Market Memory), Trading Engine ≠ AI Engine
(Constitution Article 1), Reuse First (Constitution Article 7), and
Architecture First (Constitution Article 8) are the four that every
other principle in this ecosystem ultimately serves.

## 2. Ecosystem Overview

The full diagram is reproduced above this section (unchanged from
Revision 1). Layer-by-layer one-line summary, top to bottom:

| Layer | One line |
|---|---|
| Configuration | Environment, feature flags, secrets, version — read by everything, written by nothing above it. |
| Provider Factory → Data Validation | Fetches and validates raw market data from external providers (TwelveData, Bitget/exchange APIs). |
| Market Memory | The Single Source of Truth every consumer reads (`02_Data_Layer.md`; real, as `data/memory/`, MA-001). |
| GoldBot Core | The deterministic pipeline — see `ARCHITECTURE_MASTER.md` for the authoritative version of this layer. |
| Application Services | The service boundary between Core and every product surface (mostly not yet built — `04_Application_Services.md`). |
| AI Layer | Advisory-only explanation/analysis; real as a single `ai/` package today, not the five-persona split the diagram shows (`05_AI_Layer.md`, and the Conflicts section). |
| Platform Layer | Telegram is real; Web/Mobile/Desktop/Mini App/Public API are not (`06_Platform_Layer.md`). |
| User Experience | Chart/Journal/Analytics/Notifications as user-facing features — largely not built as standalone products yet (`07_User_Experience.md`). |
| Business Layer | Subscription tiers exist; Payment/Wallet/Billing/Referral do not (`08_Business_Layer.md`). |
| Learning Layer | An ML "learning" loop exists (`learning/`); a learner-facing Academy does not (`09_Academy_Layer.md`). |
| Media Layer | A content-generation foundation exists (`ai/persona/`, `broadcast/`, `media/`, `translation/`, Phase 63.0, contract-only); no live channel integration (`10_Media_Layer.md`). |
| Future Expansion | Entirely vision — Section 4. |
| Security & Infrastructure | Partially real (`monitoring/`, `core_layer/gateway/`); much of the list is vision — `11_Infrastructure.md`. |

**Data flow between layers, one line:** raw price → validated candles →
Market Memory → Core computes a decision → (once Application Services
exist) a service formats it for a platform → a platform delivers it to
a user → the user's action/outcome feeds back into Memory/learning.
Section 5 gives the full, honest version of this loop.

## 3. Architecture Principles

Listed once; where a principle is already a Constitution Article, this
document points to it rather than restating it (avoids the exact
duplication the Owner instructed against).

| Principle | Status |
|---|---|
| Single Source of Truth | Market Memory (`data/memory/`, MA-001) is the one in-RAM store every consumer reads through (`MemoryReader`, MA-002). Real today, for candle data; not yet the source for every layer above Core (Section 8). |
| Separation of Concerns | Each layer above does one job — see `docs/architecture/SYSTEM_LAYERS.md`'s 7-layer responsibility-cluster view for the real, current version inside the Trading Core/AI/Telegram system. |
| Layer Isolation | = Constitution Article 2 (Dependency Law) + Article 3 (Import Rules). Not restated here. |
| Composition over Duplication | = Constitution Article 7 (Reuse Principle). Not restated here. |
| Reuse First | = Constitution Article 7, and `docs/governance/collaboration/TASK-GOV-001.md` Law 2 for `claude/collaboration` work specifically. |
| Dependency Direction | = Constitution Article 2: dependency flows forward through the pipeline only, never backward. |
| Fail Safe | Every foundation module audited for this task (`02_Data_Layer.md`/5) degrades to an empty/None/neutral result rather than raising into its caller — a repository-wide convention, not a single Article, evidenced consistently in `data/`, `ai/`, and the Phase 60.8 Safe Integration Layer. |
| Open for Extension | = Constitution Article 13 (Future First Principle) — design accounts for future platforms/providers from the start without requiring their code today. |
| Backward Compatibility | = Constitution Article 9 (Version Compatibility Law). Not restated here. |
| Architecture First, Implementation Second | = Constitution Article 8 (Change Management Law): Constitution → Architecture → Roadmap → Policy → Audit → Code. This is the exact order this task itself was run under (TASK-GOV-003's correction, then this task). |

## 4. Future Expansion

**Status: pure vision, by design.** Marketplace, Strategy Builder,
Indicator Store, Plugin System, Developer SDK, Enterprise Platform,
Research Center, Broker Integration, Multi Broker, Cloud Sync, Team
Workspace — none exist in the repository, and none are expected to at
this stage. This section exists in the diagram precisely so that a
future Architecture Task has a named place to go, per Constitution
Article 13's Future First Principle — the point is that placement
happens before implementation, not that implementation happens now.

## 5. Complete Data Flow

The diagram's high-level loop (GoldBot Start → Provider → Memory →
Core → Services → Platform → User → Feedback → Memory) is the
**ecosystem-level** flow — complementary to, not a replacement for,
`docs/architecture/DATA_FLOW.md`'s real, verified **pipeline-internal**
stage order (`market_data → data_quality → htf_bias → context →
market_phase → signal → signal_quality → explainability → features →
ai → decision → risk → signal_history → telegram_format →
telegram_delivery → database`, verified against
`TradingPipeline._log_stage()`'s actual call sites).

Honest version of the ecosystem loop as it exists today:

```
GoldBot Start (GitHub Actions, every 5 min)
      │
      ▼
Provider (TwelveData)  ──▶  data_quality  ──▶  [Memory: NOT the read
      │                                          path yet — see `02_Data_Layer.md`]
      ▼
Core (the real 16-stage pipeline; DATA_FLOW.md is authoritative)
      │
      ▼
Services  ──▶  [mostly do not exist yet — `04_Application_Services.md`]
      │
      ▼
Platform  ──▶  Telegram only (real); the rest do not exist — `06_Platform_Layer.md`
      │
      ▼
User  ──▶  reads the Telegram message
      │
      ▼
Feedback  ──▶  [no user-outcome feedback loop back into Memory/learning
                 was found wired into the live pipeline; learning/'s
                 loop exists but its trigger/wiring into this cycle was
                 not confirmed in this audit — flagged as an open
                 question for a future, narrower Architecture Task]
      │
      ▼
Memory  ──▶  [the loop does not currently close through MarketMemory —
              see Section 8]
```

## 6. Dependency Rules

The real, mechanically-checked dependency graph for the Trading Core/
AI/Telegram system is `docs/architecture/MODULE_DEPENDENCIES.md` and
`docs/architecture/IMPORT_RULES.md` — authoritative, not restated here.
Constitution Article 2 (Dependency Law) is the rule those two documents
enforce: dependency flows forward through the pipeline only, never
backward. Ecosystem-level addition (layers that set does not cover, all
"may depend downward only, never upward" per the same Article 2
principle):

- Application Services (`04_Application_Services.md`) may depend on GoldBot Core; GoldBot
  Core may never depend on Application Services.
- Platform Layer (`06_Platform_Layer.md`) may depend on Application Services; not
  the reverse.
- User Experience (`07_User_Experience.md`) may depend on Platform Layer; not the
  reverse.
- Business, Learning, and Media Layers (Sections 10–12) may depend on
  Application Services and Core (read-only, through the same services
  everything else uses); none of them may be depended on by Core,
  Application Services, or each other directly — cross-layer
  communication among Business/Learning/Media, if it is ever needed,
  goes through the Event Bus (Golden Rule 7), not a direct import.
- Infrastructure (`11_Infrastructure.md`) is cross-cutting and may be depended on
  by any layer; it depends on nothing above Configuration.

## 7. Refactoring Audit

Per-module comparison of the ecosystem diagram against the real
repository, from this task's own three-part codebase audit. "Diagram
match" = the module exists and does what its diagram box says.
"Absorbed" = the responsibility exists but inside a different, already-
correct module (not a defect — see Section 11, no refactor is
proposed for these). "Missing" = genuinely not built.

| Module (diagram) | Current | Target | Priority | Impact | Risk |
|---|---|---|---|---|---|
| Market Engine | Absorbed into `data/` + `context/` | No change proposed — see Section 11 | N/A | N/A | N/A |
| Analysis Engine | Absorbed into `context/` + `signals/signal_quality.py` | No change proposed — see Section 11 | N/A | N/A | N/A |
| Confluence Engine | Absorbed into each `strategies/*.py` | No change proposed — see Section 11 | N/A | N/A | N/A |
| Application Services boundary | Mostly missing (`04_Application_Services.md`) | A real service boundary between Core and Telegram, so a future Web/Mobile client doesn't need its own copy of `telegram/signal_formatter.py`'s logic | Medium (blocks Platform Layer expansion, not urgent while Telegram is the only platform) | High once a second platform is planned | Low — additive, no existing consumer needs to change |
| MarketMemory as the pipeline's read path | Not wired (`core/pipeline.py` uses `MarketDataService()` bare, no registry — `02_Data_Layer.md`) | Inject a shared `MarketMemoryRegistry` into the pipeline's `MarketDataService`/future `PriceStreamService` construction | Medium | Closes the "Single Source of Truth" gap (Golden Rule 1) for real | Medium — touches `core/pipeline.py` construction; needs its own Owner-approved technical task, explicit test coverage, and Trading Safety review (out of scope for this doc-only task) |
| Public API / Gateway | `core_layer/gateway/` is internal-only; no public server | Not proposed here — depends on Platform Layer roadmap (Section 9) | Low today | High once Web/Mobile exist | N/A until then |

No refactor above is implemented by this task (Forbidden: no `.py`
changes) — this table is the proposal only, per the brief's own
instruction ("Faqat ro'yxat").

## 8. Architecture Gap Analysis

**In diagram, not in code:**
- Market Engine, Analysis Engine, Confluence Engine as separate modules
  (`03_GoldBot_Core.md`, 17) — responsibilities exist, absorbed elsewhere.
- Application Services layer as a real service boundary (`04_Application_Services.md`) —
  mostly absent; AI Service and Notification Service are the
  exceptions.
- Platform Layer beyond Telegram (Web/Desktop/Mobile/Mini App/Public
  API) — entirely absent (`06_Platform_Layer.md`).
- User Experience as standalone products (`07_User_Experience.md`) — absent.
- Business Layer's Payment/Wallet/Billing/Referral (`08_Business_Layer.md`) —
  absent.
- Learning Layer's Academy (lessons/simulator/tournament/PvP/
  certification/career) (`09_Academy_Layer.md`) — absent; a different "Learning"
  (ML loop) exists under the same name.
- Media Layer's live channel integration (`10_Media_Layer.md`) — absent; the
  contract-first foundation is real.
- Future Expansion (Section 4) — entirely absent, by design.
- Much of Infrastructure's named list (`11_Infrastructure.md`) — partially absent.
- The ecosystem Feedback loop closing back into Memory (Section 5) —
  not confirmed wired.

**In code, not in diagram:**
- `core_layer/gateway/` (Core Gateway Layer, Module 10) — an internal service
  gateway the ecosystem diagram never names as its own box (the
  diagram's "GoldBot Core API" box is the closest match, but the real
  module is considerably more developed — auth, rate limiting, circuit
  breaking, dependency graph, health/metrics/version services — than a
  single diagram box suggests).
- `assets/` (Asset Registry) — a dedicated multi-asset metadata layer,
  not named in the diagram at all.
- `features/` (Feature Engineering) — a standardization layer between
  Signal Quality/Explainability and AI, not named in the diagram.
- The full Phase 63.0 Media/Persona/Broadcast/Translation contract
  foundation (`10_Media_Layer.md`) is considerably more built-out than the
  diagram's single "Media Hub" box implies.
- `monitoring/`'s real breadth (system/market/error/resource/provider-
  health/risk/signal/performance monitors) exceeds what the diagram's
  single "Health Monitoring" line under Infrastructure suggests.

## 9. Future Roadmap

Architecture-tier only (no timeline commitment — that is a Roadmap/
Policy-tier decision per Constitution Article 8, out of this document's
scope):

- **v1 (current):** Trading Core + AI advisory layer + Telegram, all
  Constitution-governed and real, per `ARCHITECTURE_MASTER.md`.
- **v2:** Close the MarketMemory single-source-of-truth gap (Section
  17's proposed change); stand up the Application Services boundary
  for at least Signal/Chart/Notification, so a second platform becomes
  additive rather than a rewrite.
- **v3:** A second Platform Layer surface (most likely Web, per
  Constitution Article 13's platform-neutral design intent) built
  against the now-real Application Services boundary.
- **Enterprise / Cloud:** Multi-tenant, multi-broker, cloud-sync —
  entirely Future Expansion (Section 4) territory; no architecture
  commitment made here beyond "placement before implementation" still
  applying when that day comes.
- **AI:** Grow the AI layer's explanation depth and (per the diagram)
  eventually voice — never its decision authority (Constitution
  Article 1, permanent).
- **Media:** Activate the Phase 63.0 foundation against a real channel
  (YouTube/Telegram Broadcast most likely first, per the existing
  `broadcast/`/`media/` contracts) once Business Layer monetization
  exists to justify the operational cost.
- **Education:** A learner-facing Academy, once Business Layer
  subscription tiers can support it — currently blocked on `08_Business_Layer.md`'s
  gap, not an architecture blocker.

## 10. Golden Rules (extended)

The original 10 rules above are unchanged (see the diagram section).
Extension, numbered onward, covering ground the original 10 (and the
Constitution Articles they don't duplicate) leave open:

11. **Architecture before code, always.** No implementation begins
    before its place in the applicable architecture document (this one,
    or `ARCHITECTURE_MASTER.md`) is established — Constitution Article
    8, restated here because it is this ecosystem's own operating
    method, demonstrated by this very task's STOP → AUDIT → Owner
    Decision sequence.
12. **Two architecture documents, one Constitution.** A perceived
    conflict between this document and the Constitution-governed set is
    never resolved by a Worker alone — it is listed (Section 11) and
    returned to the Owner (Constitution Article 8).
13. **Honesty over completeness.** A layer that does not exist yet is
    documented as not existing, not implied into being by inclusion in
    a diagram — every "Status" line in Sections 6–14 is this rule in
    practice.
14. **Foundation before consumer.** A layer is built foundation-first,
    consumer-second (Constitution Article 11) — MarketMemory (real,
    unconsumed) and the Phase 63.0 Media contracts (real, uncalled) are
    both examples already in the repository, not hypothetical.
15. **Naming collisions are architecture debt.** Where the same word
    names two different things (e.g. "Learning" = the ML loop in
    `learning/` vs. the vision's learner-facing Academy in this
    document, `09_Academy_Layer.md`), that collision is documented explicitly
    rather than left to cause confusion later.

## 11. Conflicts Requiring Owner Decision

Found and listed per the Owner's original instruction (not resolved
unilaterally). The Owner has since ruled on all four; each entry below
records the ruling and its status.

1. **Diagram pipeline-order mismatch** (`Market Engine → Context Engine
   → Analysis Engine → Strategy Engine → Confluence Engine → Decision
   Engine` here vs. `ARCHITECTURE_MASTER.md`'s different chain for the
   same real code — `03_GoldBot_Core.md`'s table shows exactly which). **Owner
   ruling: RETAINED, status "Accepted as Future Architecture."** This
   diagram is the target architecture; the code has not reached it yet,
   but the diagram is not lowered to match current code — the code is
   expected to grow toward the diagram instead (per the Owner's own
   words: "kod hali u darajaga yetmagan bo'lsa ham, diagrammani kodga
   tushirib yubormaymiz"). No diagram edit made. `03_GoldBot_Core.md`'s table
   continues to show the real absorbed-elsewhere mapping honestly
   alongside this status.
2. **AI Layer naming** (Senior/Seniorita/Trading AI/Learning AI/Voice
   AI/Vision AI here vs. one real `ai/` package with five tracks).
   **Owner ruling: RETAINED, status "Accepted."** The six names are
   **logical services**, not physical packages/folders — the diagram
   was never claiming a 1:1 folder mapping, and `05_AI_Layer.md`'s honest
   "one real package, five tracks" status stands as the correct
   implementation-level description underneath these logical names. No
   diagram edit made.
3. **"Learning" naming collision** (ML loop vs. Academy sharing one
   name). **Owner ruling: renamed. Status: RESOLVED.** The diagram
   section is now "ACADEMY LAYER (User Education)"; `09_Academy_Layer.md` is
   retitled to match and explicitly names the real ML package "Learning
   Engine" (part of GoldBot Core, `03_GoldBot_Core.md`) as the distinct other
   thing. See `09_Academy_Layer.md` for the full split.
4. **File location** (`01_Ecosystem_Architecture.md` was at `docs/` vs.
   the Constitution-governed set at `docs/architecture/`). **Owner
   ruling: restructure to a single `docs/architecture/` directory,
   numbered `01_Ecosystem_Architecture.md` (high-level) through
   `11_Infrastructure.md` (per-layer detail), with `docs/constitution/
   CONSTITUTION.md` staying separate at the governance tier above it.**
   Owner confirmed Option A (ecosystem-level summaries splitting this
   document's own former Sections 4–14 into separate files, still
   cross-referencing `ARCHITECTURE_MASTER.md`/`MODULE_DEPENDENCIES.md`/
   etc. for Trading-Core mechanical detail — Division of Authority
   unchanged, no absorption of that content). **Status: RESOLVED.**
   This document now lives at
   `docs/architecture/01_Ecosystem_Architecture.md`; its former
   Sections 4–12/14 are `02_Data_Layer.md` through `11_Infrastructure.md`
   (see "Layer Detail Documents" near the top of this file). Full
   record: `docs/governance/collaboration/TASK-GOV-004.md`.

## 12. Self-Test — "Can a new developer understand the system from this document alone?"

**Honest answer: partially, and this section states exactly which part
is and is not covered, rather than claiming an unqualified "yes."**

A new developer reading only this document would correctly understand:
the ecosystem's full intended shape and vision (Sections 1–2), which
layers are real vs. vision today (Sections 6–14, the single most
load-bearing content in this document), the ecosystem-level ("outer
loop") data flow (Section 5), the dependency rules for layers beyond
the Trading Core (Section 6), a concrete gap list (Section 8), and
where the architecture is headed (Section 9).

They would **not** correctly understand, from this document alone: the
real, code-verified layer contracts, dependency graph, and pipeline
stage order of the Trading Core/AI/Telegram system — that requires
`docs/architecture/ARCHITECTURE_MASTER.md`, `LAYER_CONTRACT.md`,
`MODULE_DEPENDENCIES.md`, and `DATA_FLOW.md`, which this document
deliberately does not duplicate (Section 11's Division of Authority is
exactly this trade-off, made on purpose, per Constitution Article 7 and
the Owner's explicit instruction on this task).

So the honest, literal answer to the brief's own question is: **read
this document plus `ARCHITECTURE_MASTER.md`, and the answer becomes
yes.** Neither document alone is sufficient by design — this document
is the ecosystem's vision-and-gap layer, not a replacement for the
Constitution-governed, code-verified architecture layer. This
constraint is itself the most important finding of this task, and is
why Section 11 exists rather than a single, larger, self-contained
document that would have duplicated ~2,000 lines of already-correct,
mechanically-verified documentation.
