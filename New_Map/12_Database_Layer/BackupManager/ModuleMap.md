# Backup Manager Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat BackupManager ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
CacheManager
↓
BackupManager
↓
DatabaseService
```
---
# Module Architecture
```text
BackupManager
        │
        ├── Backup Scheduler
        ├── Backup Creator
        ├── Restore Manager
        ├── Snapshot Manager
        ├── Verification Manager
        └── Metadata Generator
```
---
# Internal Components
## Backup Scheduler
Backup vaqtlarini boshqaradi.
---
## Backup Creator
Backup fayllarini yaratadi.
---
## Restore Manager
Restore jarayonini boshqaradi.
---
## Snapshot Manager
Snapshot yaratadi va boshqaradi.
---
## Verification Manager
Backup yaxlitligini tekshiradi.
---
## Metadata Generator
Backup Metadata yaratadi.
---
# Allowed Dependencies
✓ CacheManager
✓ DatabaseService
---
# Forbidden Dependencies
✗ DatabaseManager
✗ TradeRepository
✗ UserRepository
✗ MarketRepository
✗ JournalRepository
✗ AuditLog
✗ Platform Layer (to'g'ridan-to'g'ri)
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Summary
BackupManager GoldBot Database Layer ichidagi barcha Backup va Restore operatsiyalarini boshqaruvchi Canonical modul hisoblanadi.
