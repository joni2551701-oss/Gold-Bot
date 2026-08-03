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
# Summary
Database Layer GoldBot arxitekturasidagi Canonical Persistent Storage Layer hisoblanadi.
