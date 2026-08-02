# User Repository Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat UserRepository ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
DatabaseManager
↓
UserRepository
↓
Database Storage
```
---
# Module Architecture
```text
UserRepository
        │
        ├── User Writer
        ├── User Reader
        ├── Profile Repository
        ├── Settings Repository
        ├── Query Processor
        └── Metadata Generator
```
---
# Internal Components
## User Writer
User ma'lumotlarini yozadi.
---
## User Reader
User ma'lumotlarini o'qiydi.
---
## Profile Repository
Profile ma'lumotlarini boshqaradi.
---
## Settings Repository
User Settings boshqaradi.
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
✗ MarketRepository
✗ JournalRepository
✗ CacheManager
✗ BackupManager
---
# Summary
UserRepository GoldBot Database Layer ichidagi User Domain ma'lumotlarini boshqaruvchi Canonical Repository modulidir.
