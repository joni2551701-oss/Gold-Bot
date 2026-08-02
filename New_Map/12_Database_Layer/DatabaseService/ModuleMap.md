# Database Service Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat DatabaseService ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
Trade Monitoring Layer
↓
DatabaseService
↓
DatabaseManager
↓
Repositories
```
---
# Module Architecture
```text
DatabaseService
        │
        ├── Request Receiver
        ├── Request Validator
        ├── Session Manager
        ├── Request Dispatcher
        ├── Response Formatter
        └── Service Monitor
```
---
# Internal Components
## Request Receiver
Database Request'larni qabul qiladi.
---
## Request Validator
Request formatini tekshiradi.
---
## Session Manager
Database Session'ni boshqaradi.
---
## Request Dispatcher
DatabaseManager'ga Request yuboradi.
---
## Response Formatter
Repository natijalarini standart formatga o'tkazadi.
---
## Service Monitor
DatabaseService holatini kuzatadi.
---
# Allowed Dependencies
✓ DatabaseManager
✓ TradeRepository
✓ UserRepository
✓ MarketRepository
✓ JournalRepository
✓ CacheManager
✓ BackupManager
---
# Forbidden Dependencies
✗ Platform Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Summary
DatabaseService GoldBot Database Layer uchun yagona Service Gateway va Public API modulidir.
