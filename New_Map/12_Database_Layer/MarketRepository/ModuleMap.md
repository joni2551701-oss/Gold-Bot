# Market Repository Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat MarketRepository ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
DatabaseManager
↓
MarketRepository
↓
Database Storage
```
---
# Module Architecture
```text
MarketRepository
        │
        ├── Candle Repository
        ├── Tick Repository
        ├── Indicator Repository
        ├── Context Repository
        ├── Query Processor
        └── Metadata Generator
```
---
# Internal Components
## Candle Repository
OHLCV Candle ma'lumotlarini boshqaradi.
---
## Tick Repository
Tick Data'ni boshqaradi.
---
## Indicator Repository
Indicator natijalarini saqlaydi.
---
## Context Repository
Market Context va Signal History ma'lumotlarini boshqaradi.
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
✗ JournalRepository
✗ CacheManager
✗ BackupManager
✗ Platform Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Summary
MarketRepository GoldBot Database Layer ichidagi Market Domain ma'lumotlarini boshqaruvchi Canonical Repository modulidir.
