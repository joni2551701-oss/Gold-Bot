# Cache Manager Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat CacheManager ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
Repositories
↓
CacheManager
↓
BackupManager
```
---
# Module Architecture
```text
CacheManager
        │
        ├── Cache Store
        ├── Cache Reader
        ├── Cache Writer
        ├── Invalidation Manager
        ├── Statistics Manager
        └── Metadata Generator
```
---
# Internal Components
## Cache Store
Cache obyektlarini saqlaydi.
---
## Cache Reader
Cache'dan ma'lumot o'qiydi.
---
## Cache Writer
Cache'ga ma'lumot yozadi.
---
## Invalidation Manager
Expired va Invalid Cache'ni boshqaradi.
---
## Statistics Manager
Cache statistikalarini yaratadi.
---
## Metadata Generator
Cache Metadata yaratadi.
---
# Allowed Dependencies
✓ TradeRepository
✓ UserRepository
✓ MarketRepository
✓ JournalRepository
✓ BackupManager
---
# Forbidden Dependencies
✗ DatabaseManager
✗ Platform Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Summary
CacheManager GoldBot Database Layer ichidagi barcha Cache operatsiyalarini boshqaruvchi Canonical modul hisoblanadi.
