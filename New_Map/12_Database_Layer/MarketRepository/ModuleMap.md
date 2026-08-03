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
# Internal Storage (Real Implementations)
Domen: Market ma'lumot domeni.
Repository Aggregation Rule (RAR-001): Database Layer'da repository soni biznes obyektlari soniga teng bo'lishi shart emas. Quyidagi storage implementatsiyalari alohida modul emas — ular shu Repository modulining ichki mas'uliyati hisoblanadi.
```text
MarketRepository
├── market_snapshot
├── raw_candle
└── sync_state
```
| Storage | Mas'uliyat |
|---|---|
| `market_snapshot` | Market snapshot yozuvlari |
| `raw_candle` | Xom candle ma'lumotlari |
| `sync_state` | Tarixiy ma'lumot yig'ish sinxronizatsiya holati |
---
# Allowed Dependencies
✓ DatabaseManager
✓ Database Storage
---
# Forbidden Dependencies
✗ TradeRepository
✗ UserRepository
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
MarketRepository GoldBot Database Layer ichidagi Market Domain ma'lumotlarini boshqaruvchi Canonical Repository modulidir.
