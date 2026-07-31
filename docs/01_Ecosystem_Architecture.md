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
        └── docs/01_Ecosystem_Architecture.md   <- THIS document: the wider
              (this document)                       ecosystem vision (media,
                                                      business, learning,
                                                      platform expansion,
                                                      future expansion) that
                                                      the set above does not
                                                      cover, plus the gap
                                                      analysis / roadmap tying
                                                      the two together.
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
                              LEARNING LAYER
══════════════════════════════════════════════════════════════════════════════

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
not the current state of the repository**, and Section 18 (Gap
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
| Market Memory | The Single Source of Truth every consumer reads (Section 4; real, as `data/memory/`, MA-001). |
| GoldBot Core | The deterministic pipeline — see `ARCHITECTURE_MASTER.md` for the authoritative version of this layer. |
| Application Services | The service boundary between Core and every product surface (mostly not yet built — Section 6). |
| AI Layer | Advisory-only explanation/analysis; real as a single `ai/` package today, not the five-persona split the diagram shows (Section 7, and the Conflicts section). |
| Platform Layer | Telegram is real; Web/Mobile/Desktop/Mini App/Public API are not (Section 8). |
| User Experience | Chart/Journal/Analytics/Notifications as user-facing features — largely not built as standalone products yet (Section 9). |
| Business Layer | Subscription tiers exist; Payment/Wallet/Billing/Referral do not (Section 10). |
| Learning Layer | An ML "learning" loop exists (`learning/`); a learner-facing Academy does not (Section 11). |
| Media Layer | A content-generation foundation exists (`ai/persona/`, `broadcast/`, `media/`, `translation/`, Phase 63.0, contract-only); no live channel integration (Section 12). |
| Future Expansion | Entirely vision — Section 13. |
| Security & Infrastructure | Partially real (`monitoring/`, `core/gateway/`); much of the list is vision — Section 14. |

**Data flow between layers, one line:** raw price → validated candles →
Market Memory → Core computes a decision → (once Application Services
exist) a service formats it for a platform → a platform delivers it to
a user → the user's action/outcome feeds back into Memory/learning.
Section 15 gives the full, honest version of this loop.

## 3. Architecture Principles

Listed once; where a principle is already a Constitution Article, this
document points to it rather than restating it (avoids the exact
duplication the Owner instructed against).

| Principle | Status |
|---|---|
| Single Source of Truth | Market Memory (`data/memory/`, MA-001) is the one in-RAM store every consumer reads through (`MemoryReader`, MA-002). Real today, for candle data; not yet the source for every layer above Core (Section 18). |
| Separation of Concerns | Each layer above does one job — see `docs/architecture/SYSTEM_LAYERS.md`'s 7-layer responsibility-cluster view for the real, current version inside the Trading Core/AI/Telegram system. |
| Layer Isolation | = Constitution Article 2 (Dependency Law) + Article 3 (Import Rules). Not restated here. |
| Composition over Duplication | = Constitution Article 7 (Reuse Principle). Not restated here. |
| Reuse First | = Constitution Article 7, and `docs/governance/collaboration/TASK-GOV-001.md` Law 2 for `claude/collaboration` work specifically. |
| Dependency Direction | = Constitution Article 2: dependency flows forward through the pipeline only, never backward. |
| Fail Safe | Every foundation module audited for this task (Section 4/5) degrades to an empty/None/neutral result rather than raising into its caller — a repository-wide convention, not a single Article, evidenced consistently in `data/`, `ai/`, and the Phase 60.8 Safe Integration Layer. |
| Open for Extension | = Constitution Article 13 (Future First Principle) — design accounts for future platforms/providers from the start without requiring their code today. |
| Backward Compatibility | = Constitution Article 9 (Version Compatibility Law). Not restated here. |
| Architecture First, Implementation Second | = Constitution Article 8 (Change Management Law): Constitution → Architecture → Roadmap → Policy → Audit → Code. This is the exact order this task itself was run under (TASK-GOV-003's correction, then this task). |

## 4. Data Layer

Full module-by-module detail already exists and is not restated here:
`data/README.md`, `docs/architecture/MARKET_DATA_FOUNDATION.md`,
`docs/architecture/PRICE_STREAM.md`, `docs/architecture/LIVE_PRICE.md`.
Ecosystem-level summary (What/Reads/Writes/Wired-or-foundation), from
this task's own audit:

| Module | Role | Wired into live pipeline? |
|---|---|---|
| `data/market_data.py` (`MarketDataNormalizer`) | Fetch/validate/dedupe TwelveData candles | **Yes** — the pipeline's real data source |
| `data/data_quality.py` | Scores fetched candles, observational only | **Yes** |
| `data/market_data_service.py` (`MarketDataService`, TASK-DATA-001/004) | Facade unifying candles/snapshot/history; optional MarketMemory hydrate | **Yes**, but pipeline constructs it bare (no memory registry) — memory-write path dormant |
| `data/stream/price_stream_service.py` (`PriceStreamService`, TASK-DATA-001/004) | Unified live-tick API + optional MarketMemory write via `CandleBuilder` | **No** — not imported by `core/` at all; foundation only |
| `data/memory/` (`MarketMemory`, MA-001; `MemoryReader`, MA-002) | The Single Source of Truth for candle data | Exists, Director-accepted, **not yet the pipeline's read path** |
| `data/candle_builder.py` | Single writer aggregating ticks into `MarketMemory` OHLC | Foundation only — no production driver ticks it |
| `data/events/event_bus.py` | Central pub/sub (`PRICE.UPDATED`, `MARKET.*`, `STREAM.*`, ...) | Foundation only — never constructed in `core/pipeline.py` |
| `data/providers/` | Per-vendor `MarketDataProvider` adapters (TwelveData real; MT5/Binance/Bitget/FRED stubs) | TwelveData used indirectly by historical collection, not by the live cycle |
| `data/persistence/`, `data/snapshots/`, `data/replay/`, `data/bootstrap/` | Durable storage, snapshot lifecycle, replay, historical bootstrap | All foundation only |
| `data/current_price_provider.py` | Phase-1/3 current-price read facade (now backed by `PriceStreamService`) | Used outside the pipeline (Telegram-facing), not by `core/pipeline.py` |

**Who writes, who reads (Golden Rule 6):** Providers (`data/providers/`,
`data/twelve_data_client.py`) are the only writers of raw external
data; every layer above only reads (`MarketDataNormalizer`,
`MarketMemory`, `MemoryReader`) — verified true today, no counter-
example found in this audit.

## 5. GoldBot Core

Full per-engine Responsibility/Input/Output/Dependencies/Forbidden
detail is `docs/architecture/ARCHITECTURE_MASTER.md`'s "Per-Layer
Responsibility" section and `docs/architecture/LAYER_CONTRACT.md` — the
authoritative, Constitution-governed version. Not restated here.
Ecosystem-level summary and the one genuine finding this audit adds
(the three named engines that do not exist as separate modules):

| Ecosystem diagram box | Real module | Note |
|---|---|---|
| Market Engine | *(no separate module)* | Absorbed into `data/` (fetch) + `context/` (structure) |
| Context Engine | `context/context_orchestrator.py` | Real, matches `ARCHITECTURE_MASTER.md` |
| Analysis Engine | *(no separate module)* | Absorbed into `context/`'s detectors (Wyckoff/Regime/Session) + `signals/signal_quality.py` |
| Strategy Engine | `strategies/strategy_manager.py` | Real |
| Confluence Engine | *(no separate module)* | Confluence logic lives inside each strategy in `strategies/*.py`, reinforced by `signals/signal_quality.py` |
| Decision Engine | `decision/decision_engine.py` | Real |
| Risk Engine | `risk/risk_manager.py` | Real |
| Signal Engine | `signals/signal_engine.py` | Real |
| Monitoring | `monitoring/` | Real, matches by name |
| Simulation | `backtesting/` + `execution/simulator/` | Real, different name |

This "Market/Analysis/Confluence Engine absorbed, not separate" finding
is logged again in Section 18 (Gap Analysis) and is a genuine
diagram-vs-code discrepancy — listed, not resolved here, per the
Owner's instruction (Section 21).

## 6. Application Services

**Status: mostly not built.** The diagram's Application Services layer
(Signal/Chart/AI/Notification/Replay/Analytics/Portfolio/Gateway
Service, behind an API/WebSocket Gateway) is the boundary between Core
and every product surface. Real findings:

| Service | Status |
|---|---|
| Signal Service | Not a standalone service — signal output is currently formatted and delivered directly by `telegram/signal_formatter.py`/`notifier.py` inside the pipeline, not through a separate service boundary. |
| Chart Service | Partial — `ai/chart_intelligence/` exists but is AI-vision-oriented (chart image analysis), not a chart-rendering/serving service. |
| AI Service | Real and substantial — `ai/runtime/ai_service.py` is production-wired (Phase 62.2; see `docs/PHASE62_2_RUNTIME_FREEZE.md`) with lifecycle gating, circuit-breaker failover, response validation, audit logging, and cost protection. This is the one Application Service that is genuinely real. |
| Notification Service | Real, beyond `telegram/notifier.py` — `telegram/notification_service.py`, `telegram/owner/runtime_notifications.py`, plus a `broadcast/` package for multi-channel delivery (contract-only, Phase 63.0). |
| Replay Service | Real as foundation — `data/replay/` (module 8), plus `telegram/owner/replay_commands.py`. Not wired into the live pipeline. |
| Analytics Service | Real as an internal reporting package — `analytics/` (benchmark, equity curve, execution/gap/performance/signal/strategy reports). Internal, not a customer-facing service. |
| Portfolio Service | Partial — `ai/portfolio/` exists but is scoped inside the AI layer (feeds AI reasoning), not a standalone user-facing service. |
| API / WebSocket Gateway | `core/gateway/` (Module 10) exists as an internal Core Gateway — single entry point into Core services (auth, rate limiting, circuit breaking, dependency graph). It is **not** a public-facing API/WebSocket server; no such server exists in the repository. |

## 7. AI Layer

Full detail: `docs/architecture/ARCHITECTURE_MASTER.md`'s AI Layer
section (five tracks: Infrastructure/Runtime/Intelligence/Product/
Broadcast) and `docs/architecture/AI_FLOW.md`. Not restated here.

**What the diagram names vs. what exists:** the diagram above lists
Senior / Seniorita / Trading AI / Learning AI / Voice AI / Vision AI as
if they were six separate systems. In the actual repository this is
**one** `ai/` package (confirmed by this audit — no separate top-level
module per name), organized into the five ARCHITECTURE_MASTER.md
tracks plus a `voice/` package and `ai/chart_intelligence/` (the
closest thing to "Vision AI"). This is a genuine naming/structure gap
between the ecosystem vision and the real code — logged in Section 18
and Section 21, not resolved here.

**What AI does / does not do** (Constitution Article 1 — restated only
because it is this ecosystem's single most important boundary, so it
is worth stating in both documents): the AI layer explains, analyzes,
summarizes, and educates. It never approves or rejects a trade, never
calls `decision/decision_engine.py` or `risk/risk_manager.py`, never
executes an order, and never sends a Telegram message that bypasses
the pipeline's own eligibility filter. This boundary is permanent
(Constitution Article 1: "It will never give the AI a vote"), not a
temporary limitation.

## 8. Platform Layer

**Status: one platform is real.** Telegram (`telegram/`) is fully
built — Command Router → Permission Check → Handler → Service →
Repository, plus an Owner-only subsystem (`telegram/owner/`). None of
Web, Desktop, Android, iOS, or a Mini App exist in the repository —
no `web/`, no frontend server, no mobile app code, no Mini App/webview
integration was found. A Public API does not exist (`core/gateway/` is
internal-only, Section 6). Constitution Article 13 (Future First
Principle) already requires that architecture account for all
platforms from the start without requiring their code today — this
section is that accounting, made explicit and honest rather than
implied.

## 9. User Experience Layer

**Status: not built as standalone products.** Chart, Replay, Journal,
Analytics, Notifications, Portfolio, and Learning as *user-facing
experiences* (as opposed to the internal packages with similar names
audited in Sections 6/7/11) do not exist as their own UX layer — there
is no separate presentation/UX code beyond what Telegram's message
formatting already does. This layer depends entirely on Section 8's
Platform Layer existing first (a Web/Mobile client to render it), which
it does not yet.

## 10. Business Layer

**Status: mostly not built.** Subscription tiers exist
(`database/subscription_repository.py`, `telegram/subscription_service.py`)
as access-tier gating, not billing. Identity exists, but as
`assistant/identity*.py` — the AI assistant's own identity model, not
a user-authentication/business-identity system. Payment, Wallet,
Billing, and Referral were not found anywhere in the codebase. Future
monetization (per the diagram) is therefore entirely a roadmap item
(Section 19), not a present capability.

## 11. Learning Layer

**Status: real as ML, not real as education.** `learning/`
(`confidence.py`, `outcome_analyzer.py`, `pattern_detector.py`,
`regime_memory.py`, `trade_event_bridge.py`) plus
`database/learning_repository.py` and `ai/learning/`/
`ai/learning_context.py` are a genuine adaptive-learning loop — the
system learning from its own trade outcomes. This is a different thing
from the diagram's Academy (Interactive Lessons, Simulator, AI Coach,
Challenge, Tournament, PvP, Certification, Career Mode) — a
learner-facing education product, which does not exist. The naming
overlap ("Learning") between the real ML loop and the vision's Academy
is itself worth flagging as a source of future confusion (Section 21).

## 12. Media Layer

**Status: contract-only foundation, no live channel.** Phase 63.0
already built `ai/persona/` (identity data), `broadcast/`
(`BroadcastRequest`/`ExplanationOutput` value objects, channel/media-
type/language intent flags), `media/` (`media_adapter.py`,
`media_manager.py`, `media_pipeline.py`, `media_registry.py`,
`media_types.py`), and `translation/` — all explicitly contract-first
per `docs/PHASE63_0_FREEZE.md`: they hold data, never call a prompt,
never call `AIService` or a provider, never call a YouTube/OBS/RTMP/
Twitch/Kick client, never synthesize voice/image/video. This is a real,
deliberate foundation for the diagram's Media Hub (YouTube, Telegram
Broadcast, TikTok, Shorts, Podcast, Weekly Market Review, AI Content
Studio, Live Streaming) — but no live channel integration exists yet.
This is the one layer in this section where "not built" would
understate the real, already-approved foundation work.

## 13. Future Expansion

**Status: pure vision, by design.** Marketplace, Strategy Builder,
Indicator Store, Plugin System, Developer SDK, Enterprise Platform,
Research Center, Broker Integration, Multi Broker, Cloud Sync, Team
Workspace — none exist in the repository, and none are expected to at
this stage. This section exists in the diagram precisely so that a
future Architecture Task has a named place to go, per Constitution
Article 13's Future First Principle — the point is that placement
happens before implementation, not that implementation happens now.

## 14. Infrastructure

**Status: partially real.** Security/Authentication/Authorization exist
inside `core/gateway/` (internal-only, Section 6) and `core/secrets.py`.
Monitoring is real and substantial (`monitoring/` — system, market,
error, resource, provider-health, risk, signal, performance monitors).
Logging exists throughout (`core/logger.py`, used everywhere). Storage
is `database/` (SQLite, Constitution Article 4) plus `data/persistence/`
(foundation only). Scheduler is the GitHub Actions workflow
(`trading_bot.yml`) that runs the pipeline every 5 minutes — not an
in-process scheduler. Queue System, dedicated Cache (beyond
`SmartDataCache`, foundation-only), Backup, Disaster Recovery, Metrics/
Observability as a distinct product, and Audit Logs as a first-class
system (beyond `database/audit_log`, which does exist) are largely not
built as named, standalone infrastructure.

## 15. Complete Data Flow

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
      │                                          path yet — see Section 4]
      ▼
Core (the real 16-stage pipeline; DATA_FLOW.md is authoritative)
      │
      ▼
Services  ──▶  [mostly do not exist yet — Section 6]
      │
      ▼
Platform  ──▶  Telegram only (real); the rest do not exist — Section 8
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
              see Section 18]
```

## 16. Dependency Rules

The real, mechanically-checked dependency graph for the Trading Core/
AI/Telegram system is `docs/architecture/MODULE_DEPENDENCIES.md` and
`docs/architecture/IMPORT_RULES.md` — authoritative, not restated here.
Constitution Article 2 (Dependency Law) is the rule those two documents
enforce: dependency flows forward through the pipeline only, never
backward. Ecosystem-level addition (layers that set does not cover, all
"may depend downward only, never upward" per the same Article 2
principle):

- Application Services (Section 6) may depend on GoldBot Core; GoldBot
  Core may never depend on Application Services.
- Platform Layer (Section 8) may depend on Application Services; not
  the reverse.
- User Experience (Section 9) may depend on Platform Layer; not the
  reverse.
- Business, Learning, and Media Layers (Sections 10–12) may depend on
  Application Services and Core (read-only, through the same services
  everything else uses); none of them may be depended on by Core,
  Application Services, or each other directly — cross-layer
  communication among Business/Learning/Media, if it is ever needed,
  goes through the Event Bus (Golden Rule 7), not a direct import.
- Infrastructure (Section 14) is cross-cutting and may be depended on
  by any layer; it depends on nothing above Configuration.

## 17. Refactoring Audit

Per-module comparison of the ecosystem diagram against the real
repository, from this task's own three-part codebase audit. "Diagram
match" = the module exists and does what its diagram box says.
"Absorbed" = the responsibility exists but inside a different, already-
correct module (not a defect — see Section 21, no refactor is
proposed for these). "Missing" = genuinely not built.

| Module (diagram) | Current | Target | Priority | Impact | Risk |
|---|---|---|---|---|---|
| Market Engine | Absorbed into `data/` + `context/` | No change proposed — see Section 21 | N/A | N/A | N/A |
| Analysis Engine | Absorbed into `context/` + `signals/signal_quality.py` | No change proposed — see Section 21 | N/A | N/A | N/A |
| Confluence Engine | Absorbed into each `strategies/*.py` | No change proposed — see Section 21 | N/A | N/A | N/A |
| Application Services boundary | Mostly missing (Section 6) | A real service boundary between Core and Telegram, so a future Web/Mobile client doesn't need its own copy of `telegram/signal_formatter.py`'s logic | Medium (blocks Platform Layer expansion, not urgent while Telegram is the only platform) | High once a second platform is planned | Low — additive, no existing consumer needs to change |
| MarketMemory as the pipeline's read path | Not wired (`core/pipeline.py` uses `MarketDataService()` bare, no registry — Section 4) | Inject a shared `MarketMemoryRegistry` into the pipeline's `MarketDataService`/future `PriceStreamService` construction | Medium | Closes the "Single Source of Truth" gap (Golden Rule 1) for real | Medium — touches `core/pipeline.py` construction; needs its own Owner-approved technical task, explicit test coverage, and Trading Safety review (out of scope for this doc-only task) |
| Public API / Gateway | `core/gateway/` is internal-only; no public server | Not proposed here — depends on Platform Layer roadmap (Section 19) | Low today | High once Web/Mobile exist | N/A until then |

No refactor above is implemented by this task (Forbidden: no `.py`
changes) — this table is the proposal only, per the brief's own
instruction ("Faqat ro'yxat").

## 18. Architecture Gap Analysis

**In diagram, not in code:**
- Market Engine, Analysis Engine, Confluence Engine as separate modules
  (Section 5, 17) — responsibilities exist, absorbed elsewhere.
- Application Services layer as a real service boundary (Section 6) —
  mostly absent; AI Service and Notification Service are the
  exceptions.
- Platform Layer beyond Telegram (Web/Desktop/Mobile/Mini App/Public
  API) — entirely absent (Section 8).
- User Experience as standalone products (Section 9) — absent.
- Business Layer's Payment/Wallet/Billing/Referral (Section 10) —
  absent.
- Learning Layer's Academy (lessons/simulator/tournament/PvP/
  certification/career) (Section 11) — absent; a different "Learning"
  (ML loop) exists under the same name.
- Media Layer's live channel integration (Section 12) — absent; the
  contract-first foundation is real.
- Future Expansion (Section 13) — entirely absent, by design.
- Much of Infrastructure's named list (Section 14) — partially absent.
- The ecosystem Feedback loop closing back into Memory (Section 15) —
  not confirmed wired.

**In code, not in diagram:**
- `core/gateway/` (Core Gateway Layer, Module 10) — an internal service
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
  foundation (Section 12) is considerably more built-out than the
  diagram's single "Media Hub" box implies.
- `monitoring/`'s real breadth (system/market/error/resource/provider-
  health/risk/signal/performance monitors) exceeds what the diagram's
  single "Health Monitoring" line under Infrastructure suggests.

## 19. Future Roadmap

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
  entirely Future Expansion (Section 13) territory; no architecture
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
  subscription tiers can support it — currently blocked on Section 10's
  gap, not an architecture blocker.

## 20. Golden Rules (extended)

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
    never resolved by a Worker alone — it is listed (Section 21) and
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
    document, Section 11), that collision is documented explicitly
    rather than left to cause confusion later.

## 21. Conflicts Requiring Owner Decision

Per the Owner's explicit instruction: found, listed, not resolved.

1. **Diagram pipeline-order mismatch.** This document's diagram (GoldBot
   Core section) lists `Market Engine → Context Engine → Analysis
   Engine → Strategy Engine → Confluence Engine → Decision Engine`.
   `docs/architecture/ARCHITECTURE_MASTER.md`'s diagram lists
   `Market Data → Context Engine → Strategy Engine → Signal Engine →
   Decision Engine → Risk Manager → Execution → Trade Monitor` — a
   different box set (no Market/Analysis/Confluence Engine; includes
   Signal Engine, Risk Manager, Execution, Trade Monitor that this
   document's diagram omits from that specific chain, though Signal/
   Risk/Execution do appear elsewhere in this document's fuller
   diagram). Both diagrams describe the same real code (Section 5's
   table shows exactly which). Whether to ever reconcile the two
   diagrams into one, and if so which one changes, is an Owner
   decision — not made here.
2. **AI Layer naming.** This document's diagram names Senior /
   Seniorita / Trading AI / Learning AI / Voice AI / Vision AI as
   separate boxes; `ARCHITECTURE_MASTER.md` and the real code organize
   the same territory as one `ai/` package with five tracks
   (Infrastructure/Runtime/Intelligence/Product/Broadcast) plus a
   separate `voice/` package. Whether the ecosystem-vision naming is a
   future intended restructuring or simply a different vocabulary for
   the same tracks is an Owner decision.
3. **"Learning" naming collision** (Section 11, Golden Rule 15) — same
   word, two different systems (ML loop vs. Academy). Not a contradiction
   in code, but a documentation clarity risk flagged for an Owner call
   on whether to rename one of them in a future Architecture Task.
4. **File location.** `01_Ecosystem_Architecture.md` lives at `docs/`;
   `ARCHITECTURE_MASTER.md` and its siblings live at
   `docs/architecture/`. Whether this document should move under
   `docs/architecture/` for consistency (flagged already in
   `TASK-GOV-003.md` §3) remains an open Owner decision, not acted on
   here.

## 22. Self-Test — "Can a new developer understand the system from this document alone?"

**Honest answer: partially, and this section states exactly which part
is and is not covered, rather than claiming an unqualified "yes."**

A new developer reading only this document would correctly understand:
the ecosystem's full intended shape and vision (Sections 1–2), which
layers are real vs. vision today (Sections 6–14, the single most
load-bearing content in this document), the ecosystem-level ("outer
loop") data flow (Section 15), the dependency rules for layers beyond
the Trading Core (Section 16), a concrete gap list (Section 18), and
where the architecture is headed (Section 19).

They would **not** correctly understand, from this document alone: the
real, code-verified layer contracts, dependency graph, and pipeline
stage order of the Trading Core/AI/Telegram system — that requires
`docs/architecture/ARCHITECTURE_MASTER.md`, `LAYER_CONTRACT.md`,
`MODULE_DEPENDENCIES.md`, and `DATA_FLOW.md`, which this document
deliberately does not duplicate (Section 21's Division of Authority is
exactly this trade-off, made on purpose, per Constitution Article 7 and
the Owner's explicit instruction on this task).

So the honest, literal answer to the brief's own question is: **read
this document plus `ARCHITECTURE_MASTER.md`, and the answer becomes
yes.** Neither document alone is sufficient by design — this document
is the ecosystem's vision-and-gap layer, not a replacement for the
Constitution-governed, code-verified architecture layer. This
constraint is itself the most important finding of this task, and is
why Section 21 exists rather than a single, larger, self-contained
document that would have duplicated ~2,000 lines of already-correct,
mechanically-verified documentation.
