══════════════════════════════════════════════════════════════════════════════
                               GOLDBOT AI ECOSYSTEM
══════════════════════════════════════════════════════════════════════════════

                                   GoldBot Start
                                         │
                                         ▼
                              Configuration Layer
                    (Environment • Features • Secrets • Version)
                                         │
                                         ▼
                                Provider Factory Layer
                                         │
                  ┌──────────────────────┴──────────────────────┐
                  ▼                                             ▼
     Historical Data Layer                             Price Stream Layer
      (Bootstrap / Recovery)                           (Live Streaming)
                  │                                             │
                  ▼                                             ▼
        Twelve Data / Providers                     Exchange / Broker APIs
                  │                                             │
                  └──────────────────────┬──────────────────────┘
                                         ▼
                              Data Validation Layer
                                         │
                                         ▼
                              Market Memory Layer
                      (Single Source of Truth — SSOT)
                                         │
        ┌──────────────────┬──────────────────┬──────────────────┬──────────────────┐
        ▼                  ▼                  ▼                  ▼
   Current Price       Candle Builder     Historical DB        Event Bus
                                         │
══════════════════════════════════════════════════════════════════════════════
                                  GOLDBOT CORE
══════════════════════════════════════════════════════════════════════════════

                                Market Engine
                                         │
                                         ▼
                               Context Engine
                                         │
                                         ▼
                               Analysis Engine
                                         │
                                         ▼
                              Indicator Engine
                                         │
                                         ▼
                               Strategy Engine
                                         │
                                         ▼
                              Confluence Engine
                                         │
                                         ▼
                               Decision Engine
                                         │
                      ┌──────────────────┴──────────────────┐
                      ▼                                     ▼
                Risk Engine                            Signal Engine
                      │                                     │
                      └──────────────┬──────────────────────┘
                                     ▼
                               Execution Engine
                                     │
                                     ▼
                          Trade Monitoring Layer
                                     │
                                     ▼
                           GoldBot Core API Layer

══════════════════════════════════════════════════════════════════════════════
                            APPLICATION SERVICES LAYER
══════════════════════════════════════════════════════════════════════════════

                            API / WebSocket Gateway
                                     │
       ┌──────────────┬──────────────┬──────────────┬──────────────┐
       ▼              ▼              ▼              ▼
   Signal API      Chart API       AI API     Notification API
       │              │              │              │
       └──────────────┼──────────────┼──────────────┘
                      ▼              ▼
                Replay Service   Analytics Service
                      │
                      ▼
                 Portfolio Service

══════════════════════════════════════════════════════════════════════════════
                                 AI LAYER
══════════════════════════════════════════════════════════════════════════════

                              Senior AI
                            Seniorita AI
                                   │
       ┌──────────────┬──────────────┬──────────────┬──────────────┐
       ▼              ▼              ▼              ▼
   Trading AI     Learning AI     Voice AI      Vision AI
                                   │
                                   ▼
                       AI Explanation Engine

══════════════════════════════════════════════════════════════════════════════
                               PLATFORM LAYER
══════════════════════════════════════════════════════════════════════════════

      ┌──────────────┬──────────────┬──────────────┬──────────────┐
      ▼              ▼              ▼              ▼
   Telegram         Mobile         Desktop          Web
                                           │
                                           ▼
                                      Public API

══════════════════════════════════════════════════════════════════════════════
                             CHART LAYER
══════════════════════════════════════════════════════════════════════════════

                               Chart Engine
                                     │
      ┌──────────────┬──────────────┬──────────────┬──────────────┐
      ▼              ▼              ▼              ▼
    Multi TF     Drawing Tools     Indicators        Replay
       │              │               │              │
       ▼              ▼               ▼              ▼
    SMC Layer      Elite View      Templates       Alerts

══════════════════════════════════════════════════════════════════════════════
                           BACKTESTING LAYER
══════════════════════════════════════════════════════════════════════════════

                               Replay Engine
                                     │
        ┌──────────────┬──────────────┬──────────────┬──────────────┐
        ▼              ▼              ▼              ▼
 Historical Replay  Strategy Testing  AI Evaluation  Performance Metrics
        │              │              │              │
        └──────────────┴──────────────┴──────────────┴──────────────┘
                                     │
                                     ▼
                           Optimization / Reports

══════════════════════════════════════════════════════════════════════════════
                              BUSINESS LAYER
══════════════════════════════════════════════════════════════════════════════

      ┌──────────────┬──────────────┬──────────────┬──────────────┐
      ▼              ▼              ▼              ▼
    Identity     Subscription      Payment       Referral
      │              │              │              │
      ▼              ▼              ▼              ▼
  User Profile    FREE / PRO        Wallet        Rewards
      │
      ▼
     Roles
     ELITE

══════════════════════════════════════════════════════════════════════════════
                              LEARNING LAYER
══════════════════════════════════════════════════════════════════════════════

                                  Academy
                                     │
     ┌──────────────┬──────────────┬──────────────┬──────────────┐
     ▼              ▼              ▼              ▼
Interactive Lessons  Replay      Simulator      AI Coach
     │
     ├──────────────┬──────────────┬──────────────┬──────────────┐
     ▼              ▼              ▼              ▼
  Challenge      Tournament   PvP / AI vs AI  Certification
                                     │
                                     ▼
                                Career Mode

══════════════════════════════════════════════════════════════════════════════
                                MEDIA LAYER
══════════════════════════════════════════════════════════════════════════════

                                  Media Hub
                                     │
     ┌──────────────┬──────────────┬──────────────┬──────────────┐
     ▼              ▼              ▼              ▼
Telegram Broadcast   YouTube       TikTok        Shorts
     │              │              │              │
     └──────────────┼──────────────┼──────────────┘
                    ▼              ▼
                Podcast      Weekly Market Review
                    │
                    └──────────────┬──────────────┐
                                   ▼              ▼
                           AI Content Studio   Live Streaming

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
                           GOVERNANCE & STANDARDS
══════════════════════════════════════════════════════════════════════════════

1. GEL-001 — Har bir canonical module alohida package bo‘lishi shart.
2. GLS-001 — Barcha docs va hisobotlar O‘zbek tilida yoziladi.
3. DD-005 — Compatibility Exception faqat empirik isbot bilan yuritiladi.
4. GDS — Development Workflow va Definition of Done majburiy.
5. RFC / ADR — katta o‘zgarishlar avval hujjatlashtiriladi.
6. Release Standard — beta → RC → production tartibi saqlanadi.
7. Deployment Authority — deployment faqat belgilangan vakolat bilan.
8. Empirical Verification — qonunlar real platformada sinov bilan tasdiqlanadi.

══════════════════════════════════════════════════════════════════════════════
                           GOLDEN ARCHITECTURE RULES
══════════════════════════════════════════════════════════════════════════════

1. Market Memory — Single Source of Truth (SSOT).
2. GoldBot Core faqat hisoblaydi.
3. AI yakuniy qaror qabul qilmaydi, faqat tahlil va tushuntirish beradi.
4. Decision faqat Technical + Risk + Rules asosida qabul qilinadi.
5. Platformlar faqat GoldBot Core API orqali ishlaydi.
6. Provider yozadi, Consumer faqat o‘qiydi.
7. Event Bus qatlamlarni bog‘laydi, ular bir-biriga to‘g‘ridan-to‘g‘ri bog‘lanmaydi.
8. Reuse First — dublikat logika taqiqlanadi.
9. Har bir qatlam faqat o‘z vazifasi uchun javobgar.
10. Core Platform va AI’dan mustaqil bo‘ladi.
11. File-by-File Development Workflow majburiy.
12. Documentation va Audit GLS-001 bo‘yicha O‘zbek tilida yuritiladi.
13. Compatibility Exception faqat DD-005 orqali boshqariladi.
14. Foundation Rule faqat Empirical Verification orqali tasdiqlanadi.
15. Development v1 — faqat real, production-ready kod.
16. Hujjatlar, loglar va reviewlar append-only yuritiladi.
17. Har bir modulning hayot sikli: Blueprint → Implemented → Testing → Stable.
══════════════════════════════════════════════════════════════════════════════