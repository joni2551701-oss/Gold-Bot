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