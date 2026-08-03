# Journal Repository Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat JournalRepository ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
DatabaseManager
↓
JournalRepository
↓
Database Storage
```
---
# Module Architecture
```text
JournalRepository
        │
        ├── AI Journal Repository
        ├── Decision Repository
        ├── Audit Repository
        ├── Event Repository
        ├── Query Processor
        └── Metadata Generator
```
---
# Internal Components
## AI Journal Repository
AI Analysis yozuvlarini boshqaradi.
---
## Decision Repository
Decision History'ni boshqaradi.
---
## Audit Repository
Audit Log'larni boshqaradi.
---
## Event Repository
System Event'larni boshqaradi.
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
✗ TradeRepository
✗ UserRepository
✗ MarketRepository
✗ CacheManager
✗ BackupManager
✗ Platform Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Summary
JournalRepository GoldBot Database Layer ichidagi Journal Domain ma'lumotlarini boshqaruvchi Canonical Repository modulidir.
