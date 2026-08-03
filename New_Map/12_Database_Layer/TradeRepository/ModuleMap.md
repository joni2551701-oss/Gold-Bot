# Trade Repository Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat TradeRepository ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
DatabaseManager
↓
TradeRepository
↓
Database Storage
```
---
# Module Architecture
```text
TradeRepository
        │
        ├── Trade Writer
        ├── Trade Reader
        ├── Position Repository
        ├── Execution Repository
        ├── Query Processor
        └── Metadata Generator
```
---
# Internal Components
## Trade Writer
Trade yozadi.
---
## Trade Reader
Trade ma'lumotlarini o'qiydi.
---
## Position Repository
Position ma'lumotlarini boshqaradi.
---
## Execution Repository
Execution ma'lumotlarini boshqaradi.
---
## Query Processor
Repository Query'larini bajaradi.
---
## Metadata Generator
Repository Metadata yaratadi.
---
# Allowed Dependencies
✓ DatabaseManager
✓ Database Storage
---
# Forbidden Dependencies
✗ UserRepository
✗ MarketRepository
✗ JournalRepository
✗ AuditLog
✗ CacheManager
✗ BackupManager
✗ Platform Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Summary
TradeRepository GoldBot Database Layer ichidagi Trade Domain ma'lumotlarini boshqaruvchi Canonical Repository modulidir.
