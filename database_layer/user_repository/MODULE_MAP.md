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
# Internal Storage (Real Implementations)
Domen: Foydalanuvchi va hisob domeni.
Repository Aggregation Rule (RAR-001): Database Layer'da repository soni biznes obyektlari soniga teng bo'lishi shart emas. Quyidagi storage implementatsiyalari alohida modul emas — ular shu Repository modulining ichki mas'uliyati hisoblanadi.
```text
UserRepository
├── user
├── subscription
├── feedback
└── admin
```
| Storage | Mas'uliyat |
|---|---|
| `user` | Foydalanuvchi yozuvlari |
| `subscription` | Obuna holati va tarixi |
| `feedback` | Foydalanuvchi fikr-mulohazalari |
| `admin` | Admin yozuvlari (telegram_id, role) |
---
# Allowed Dependencies
✓ DatabaseManager
✓ Database Storage
---
# Forbidden Dependencies
✗ TradeRepository
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
UserRepository GoldBot Database Layer ichidagi User Domain ma'lumotlarini boshqaruvchi Canonical Repository modulidir.
