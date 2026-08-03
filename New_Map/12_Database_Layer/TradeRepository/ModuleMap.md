# Trade Repository Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat TradeRepository ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
DatabaseManager
↓
TradeRepository
↓
Database Storage
```
---
# Module Architecture
```text
TradeRepository
        │
        ├── Trade Writer
        ├── Trade Reader
        ├── Position Repository
        ├── Execution Repository
        ├── Query Processor
        └── Metadata Generator
```
---
# Internal Components
## Trade Writer
Trade yozadi.
---
## Trade Reader
Trade ma'lumotlarini o'qiydi.
---
## Position Repository
Position ma'lumotlarini boshqaradi.
---
## Execution Repository
Execution ma'lumotlarini boshqaradi.
---
## Query Processor
Repository Query'larini bajaradi.
---
## Metadata Generator
Repository Metadata yaratadi.
---
# Internal Storage (Real Implementations)
Domen: Savdo va risk domeni.
Repository Aggregation Rule (RAR-001): Database Layer'da repository soni biznes obyektlari soniga teng bo'lishi shart emas. Quyidagi storage implementatsiyalari alohida modul emas — ular shu Repository modulining ichki mas'uliyati hisoblanadi.
```text
TradeRepository
├── signal
├── risk_decision
├── risk_state
└── emergency
```
| Storage | Mas'uliyat |
|---|---|
| `signal` | Signal yozuvlari (SignalRecord) |
| `risk_decision` | Risk qarorlari tarixi (append-only) |
| `risk_state` | Symbol bo'yicha risk hisob holati (upsert) |
| `emergency` | Emergency holat o'tishlari (KILLED va h.k., append-only) |
---
# Allowed Dependencies
✓ DatabaseManager
✓ Database Storage
---
# Forbidden Dependencies
✗ UserRepository
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
TradeRepository GoldBot Database Layer ichidagi Trade Domain ma'lumotlarini boshqaruvchi Canonical Repository modulidir.
