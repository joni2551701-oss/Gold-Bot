# Database Layer Module Map
Status: CANONICAL
---
# Layer Architecture
```text
12_Database_Layer
│
├── DatabaseService
│
├── DatabaseManager
│
├── TradeRepository
│
├── UserRepository
│
├── MarketRepository
│
├── JournalRepository
├── AuditLog
│
├── CacheManager
│
└── BackupManager
```
---
# Processing Pipeline
```text
Trade Monitoring Layer
        │
        ▼
DatabaseService (Entry)
        │
        ▼
DatabaseManager
        │
        ├──────────────┬──────────────┬──────────────┐
        ▼              ▼              ▼              ▼
TradeRepository  UserRepository  MarketRepository  JournalRepository  AuditLog
        │              │              │              │
        └──────────────┴──────────────┴──────────────┘
                       │
                       ▼
                 CacheManager
                       │
                       ▼
                 BackupManager
                       │
                       ▼
                 DatabaseService (Exit)
                       │
                       ▼
                 Platform Layer
```
---
# Module Responsibilities
## DatabaseService
Database Layer'ning ikki tomonlama (bidirectional) Boundary Gateway'i — Entry va Exit.
---
## DatabaseManager
Database Infrastructure boshqaradi.
---
## TradeRepository
Trade va Position ma'lumotlarini boshqaradi.
---
## UserRepository
User va Settings ma'lumotlarini boshqaradi.
---
## MarketRepository
Market Data va Context ma'lumotlarini boshqaradi.
---
## JournalRepository
AI Journal va Audit ma'lumotlarini boshqaradi.
---
## AuditLog
Audit Trail persistence (append-only). Login, Configuration, Permission, API Access va Critical Event yozuvlari.
---
## CacheManager
Cache Infrastructure boshqaradi.
---
## BackupManager
Backup va Disaster Recovery boshqaradi. Layer tashqarisiga chiqmaydi — natijani DatabaseService orqali uzatadi.
---
# Repository Aggregation Map (RAR-001)
Real kodda 16 ta storage implementatsiyasi mavjud. Ular alohida modul emas — domen bo'yicha 5 ta Canonical Repository moduli ichida guruhlanadi (Repository Aggregation Rule).
```text
12_Database_Layer
│
├── UserRepository        (foydalanuvchi va hisob domeni)
│   ├── user
│   ├── subscription
│   ├── feedback
│   └── admin
│
├── TradeRepository       (savdo va risk domeni)
│   ├── signal
│   ├── risk_decision
│   ├── risk_state
│   └── emergency
│
├── MarketRepository      (market ma'lumot domeni)
│   ├── market_snapshot
│   ├── raw_candle
│   └── sync_state
│
├── JournalRepository     (AI Journal va tizim holati domeni)
│   ├── learning
│   ├── config_snapshot
│   └── runtime_feature
│
└── AuditLog              (audit va kuzatuv domeni)
    ├── audit_log
    └── monitoring
```
Jami: 16 storage → 5 Repository moduli. Yangi storage qo'shilganda u mos domendagi mavjud Repository ichiga kiritiladi — yangi Repository moduli yaratilmaydi.
---
# Summary
Database Layer GoldBot arxitekturasidagi Canonical Persistent Storage Layer hisoblanadi.
