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
## Event Repository
System Event'larni boshqaradi.
---
## Query Processor
Repository Query'larini bajaradi.
---
## Metadata Generator
Repository Metadata yaratadi.
---
# Internal Storage (Real Implementations)
Domen: AI Journal va tizim holati domeni.
Repository Aggregation Rule (RAR-001): Database Layer'da repository soni biznes obyektlari soniga teng bo'lishi shart emas. Quyidagi storage implementatsiyalari alohida modul emas — ular shu Repository modulining ichki mas'uliyati hisoblanadi.
```text
JournalRepository
├── learning
├── config_snapshot
└── runtime_feature
```
| Storage | Mas'uliyat |
|---|---|
| `learning` | Learning Loop yozuvlari (append-only) |
| `config_snapshot` | Konfiguratsiya snapshot'lari (append-only) |
| `runtime_feature` | Runtime Feature Toggle holati (upsert, feature/enabled/updated_by) |
---
# Allowed Dependencies
✓ DatabaseManager
✓ Database Storage
---
# Forbidden Dependencies
✗ AuditLog
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
