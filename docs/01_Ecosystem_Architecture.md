══════════════════════════════════════════════════════════════════════════════
                            ARCHITECTURE AUTHORITY
══════════════════════════════════════════════════════════════════════════════

Status: MASTER ARCHITECTURE — the single official architecture document
for the Senior Trading AI Ecosystem (GoldBot). Formalized by
TASK-GOV-003 (docs/governance/collaboration/TASK-GOV-003.md).

This document is the authority. The principles below are binding on
every future task and every implementation:

1. Master Architecture. This document (01_Ecosystem_Architecture.md) is
   the single, official Master Architecture. Where any other document,
   diagram, or code appears to describe the ecosystem's shape, this
   document is the one that governs.

2. Basis for all technical tasks. Every technical task derives from this
   architecture. A task that cannot be located within the structure
   below is not ready to execute — its place in the architecture is
   established first.

3. Placement before implementation. Every new module is first placed
   into its position in this architecture (which layer it belongs to,
   what it may read from, what may read from it) before any code for it
   is written.

4. No contradiction. No implementation may contradict this architecture.
   Code that would violate a layer boundary, a data-flow direction, or a
   Golden Architecture Rule below is rejected, not merged and
   reconciled later.

5. Change protocol (architecture-first). Changing the architecture is
   itself a governed action, in this fixed order:
      a. an Architecture Task is written and Owner-approved;
      b. only then is the diagram/document updated;
      c. only then does implementation against the change begin.
   No implementation ever silently changes the architecture, and the
   diagram is never edited ahead of an approved Architecture Task.

Governance control chain (established by this authority):

      01_Ecosystem_Architecture.md   (this document — the authority)
                  │
                  ▼
          Architecture Tasks          (change the architecture, Owner-approved)
                  │
                  ▼
           Technical Tasks            (derive from the approved architecture)
                  │
                  ▼
          Implementation              (never contradicts the architecture)
                  │
                  ▼
             Review                   (checks conformance to this document)
                  │
                  ▼
             Merge                    (Owner-approved, per Branch rules)

Relationship to governance:
- docs/governance/collaboration/TASK-GOV-003.md — the task that
  formalized this Architecture Authority section and its governance
  linkage.
- docs/governance/collaboration/TASK-GOV-001.md — the claude/collaboration
  working rules (single dev branch, task lifecycle, Laws 1–12) under
  which architecture-derived tasks are executed.
- docs/governance/roles/Collaboration_Rules.md,
  docs/governance/policies/Branch_Policy.md — the repository-wide
  governance this authority sits alongside (Architecture First is
  already a governance principle there; this document is the concrete
  architecture it points to).

The diagram below is the authoritative architecture and is unchanged by
this section — per the change protocol (principle 5) it is edited only
under an approved Architecture Task.

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