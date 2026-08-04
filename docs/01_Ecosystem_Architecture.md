══════════════════════════════════════════════════════════════════════════════
                         GOLDBOT V3 — PROFESSIONAL STRUCTURE
══════════════════════════════════════════════════════════════════════════════

                                 GoldBot Start
                                       │
                                       ▼
══════════════════════════════════════════════════════════════════════════════
                           FOUNDATION LAYER
══════════════════════════════════════════════════════════════════════════════

   Configuration ──► Infrastructure ──► Provider Factory ──► Data Sources
   (.env, secrets,      (logger, DB,        (TwelveData,       (historical,
    features, version)   cache, queue,       Bitget, future)    live stream)
                         scheduler, bus)

                                       │
                                       ▼
══════════════════════════════════════════════════════════════════════════════
                              DATA LAYER
══════════════════════════════════════════════════════════════════════════════

                    Data Validation ──► Market Memory (SSOT)
                     (filter, normalize,      (single source
                      deduplicate)             of truth)

                                       │
               ┌───────────────────────┼────────────────────────┐
               ▼                       ▼                        ▼
        Current Price             Candle Builder           Historical DB
               │                                                │
               └──────────────────────────┬─────────────────────┘
                                          ▼
                                     Event Bus
                                          │
                                          ▼
══════════════════════════════════════════════════════════════════════════════
                                   GOLDBOT
══════════════════════════════════════════════════════════════════════════════

┌──────────────────────────────────────────────────────────────────────────────┐
│                              GOLD BOT CORE                                  │
│                                                                              │
│  Market Engine ─► Context Engine ─► Analysis Engine ─► Indicator Engine      │
│        │                                                                      │
│        ▼                                                                      │
│  Strategy Engine ─► Confluence Engine ─► Decision Engine                     │
│                                              │                               │
│                             ┌────────────────┴───────────────┐               │
│                             ▼                                ▼               │
│                       Risk Engine                     Signal Engine          │
│                             │                                │               │
│                             └───────────────┬────────────────┘               │
│                                             ▼                                │
│                                    Execution Engine                          │
│                                             │                                │
│                                             ▼                                │
│                                   Trade Monitoring                           │
│                                             │                                │
│                                             ▼                                │
│                                   GoldBot Core API                           │
│                                                                              │
│  Core mas'uliyati:                                                            │
│  - bozorni tahlil qilish                                                     │
│  - qaror chiqarish                                                           │
│  - riskni hisoblash                                                          │
│  - signal ishlab chiqish                                                     │
│  - execution va monitoring                                                   │
└──────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│                              CHART SERVICE                                   │
│                                                                              │
│  Chart Engine ─► Renderer ─► Multi TF ─► Drawing Tools ─► Indicators        │
│                         │                                │                   │
│                         ├────────────► Replay ───────────┤                   │
│                         ├────────────► Templates ────────┤                   │
│                         └────────────► Alerts ────────────┘                   │
│                                                                              │
│  Chart mas'uliyati:                                                          │
│  - narxni vizual ko‘rsatish                                                  │
│  - drawing tool’lar                                                          │
│  - indikatorlar                                                              │
│  - replay                                                                    │
│  - elite chart view                                                          │
└──────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│                              PERSONAL AI CORE                                │
│                                                                              │
│                    Shared Brain / Memory / Knowledge / Reasoning             │
│                                      │                                       │
│                   ┌──────────────────┴──────────────────┐                    │
│                   ▼                                     ▼                    │
│            Senior Persona                        Seniorita Persona           │
│               (Male)                                 (Female)                │
│                   │                                     │                    │
│                   └──────────────┬──────────────────────┘                    │
│                                  ▼                                           │
│                        AI Explanation Engine                                 │
│                                                                              │
│  AI mas'uliyati:                                                             │
│  - tushuntirish                                                             │
│  - tahlil                                                                   │
│  - xulosa                                                                   │
│  - user bilan muloqot                                                       │
│  - trading qarorini o‘zi qilmaydi                                           │
└──────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│                             BACKTESTING ENGINE                               │
│                                                                              │
│  Historical Replay ─► Strategy Testing ─► AI Evaluation ─► Metrics          │
│                             │                                │               │
│                             └──────────────┬─────────────────┘               │
│                                            ▼                                 │
│                                   Optimization / Reports                     │
│                                                                              │
│  Backtesting mas'uliyati:                                                    │
│  - strategiyani qayta sinash                                                 │
│  - natijani baholash                                                         │
│  - performance metrics                                                       │
│  - report chiqarish                                                          │
└──────────────────────────────────────────────────────────────────────────────┘

══════════════════════════════════════════════════════════════════════════════
                           GOLD BOT PUBLIC API
══════════════════════════════════════════════════════════════════════════════

                           GoldBot Core API / Gateway
                                       │
       ┌───────────────────────────────┼───────────────────────────────┐
       ▼                               ▼                               ▼
    Signal API                      Chart API                        AI API
       │                               │                               │
       └───────────────┬───────────────┼───────────────┬───────────────┘
                       ▼                               ▼
               Notification API                 Replay / Analytics API
                       │                               │
                       └───────────────┬───────────────┘
                                       ▼
                                 Portfolio API

══════════════════════════════════════════════════════════════════════════════
                         APPLICATION / SERVICE LAYER
══════════════════════════════════════════════════════════════════════════════

                API Gateway ─► Services ─► Orchestrators ─► Integrations
                       │
       ┌───────────────┼───────────────┬───────────────┬───────────────┐
       ▼               ▼               ▼               ▼               ▼
   Signal Service   Chart Service   AI Service   Notification      Replay /
                                                        Service      Analytics

══════════════════════════════════════════════════════════════════════════════
                              PLATFORM LAYER
══════════════════════════════════════════════════════════════════════════════

        ┌──────────────┬──────────────┬──────────────┬──────────────┐
        ▼              ▼              ▼              ▼
    Telegram         Mobile         Desktop          Web
        │              │              │              │
        └──────────────┼──────────────┼──────────────┘
                       ▼
                    End User

══════════════════════════════════════════════════════════════════════════════
                         BUSINESS / LEARNING / MEDIA
══════════════════════════════════════════════════════════════════════════════

Business Layer    ─► Identity / Profile / Subscription / Payment / Referral
Learning Layer    ─► Academy / Replay / Simulator / AI Coach / Certification
Media Layer       ─► Broadcast / YouTube / TikTok / Podcast / Live Content

══════════════════════════════════════════════════════════════════════════════
                       SECURITY & INFRASTRUCTURE
══════════════════════════════════════════════════════════════════════════════

Security / Auth / Encryption / Storage / Cache / Logging / Metrics / Observability
Health Monitoring / Backup / Disaster Recovery / Scheduler / Queue / Audit Logs

══════════════════════════════════════════════════════════════════════════════