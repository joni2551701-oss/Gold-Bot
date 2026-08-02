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
DatabaseService (Entry)
↓
DatabaseManager
↓
TradeRepository / UserRepository / MarketRepository / JournalRepository
↓
CacheManager
↓
BackupManager
↓
DatabaseService (Exit)
↓
Platform Layer
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
Trade Monitoring Layer'dan Database Request'larni qabul qiladi.
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
BackupManager'dan qaytgan natijani standart formatga o'tkazadi va Platform Layer'ga uzatadi.
---
## Service Monitor
DatabaseService holatini kuzatadi.
---
# Allowed Dependencies
✓ DatabaseManager
✓ BackupManager
---
# Forbidden Dependencies
✗ TradeRepository (to'g'ridan-to'g'ri)
✗ UserRepository (to'g'ridan-to'g'ri)
✗ MarketRepository (to'g'ridan-to'g'ri)
✗ JournalRepository (to'g'ridan-to'g'ri)
✗ CacheManager (to'g'ridan-to'g'ri)
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Summary
DatabaseService GoldBot Database Layer uchun ikki tomonlama Boundary Gateway va Public API modulidir.
