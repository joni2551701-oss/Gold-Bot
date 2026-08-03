# Audit Log Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat AuditLog ichki arxitekturasini tavsiflaydi (ichki submodullar implementatsiya bosqichida to'ldiriladi).
---
# Internal Architecture (Planned)
```text
AuditLog
├── AuditEntryModel
├── AuditWriter
├── AuditReader
└── AuditQuery
```
---
# Module Position
```text
DatabaseManager
↓
AuditLog
↓
Database Storage
```
---
# Processing Pipeline (Planned)
```text
AuditEntryModel → AuditWriter → AuditReader → AuditQuery
```
---
# Dependency Map
```text
DatabaseManager
↓
AuditLog
↓
Database Storage
```
---
# Internal Storage (Real Implementations)
Domen: Audit va kuzatuv domeni.
Repository Aggregation Rule (RAR-001): Database Layer'da repository soni biznes obyektlari soniga teng bo'lishi shart emas. Quyidagi storage implementatsiyalari alohida modul emas — ular shu Repository modulining ichki mas'uliyati hisoblanadi.
```text
AuditLog
├── audit_log
└── monitoring
```
| Storage | Mas'uliyat |
|---|---|
| `audit_log` | Owner/Admin harakatlari (append-only) |
| `monitoring` | Runtime kuzatuv yozuvlari (append-only) |
---
# Allowed Dependencies
✓ DatabaseManager
✓ Database Storage
---
# Forbidden Dependencies
✗ TradeRepository
✗ UserRepository
✗ MarketRepository
✗ JournalRepository
✗ CacheManager
✗ BackupManager
✗ Platform Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Runtime Flow
```text
Receive Input
↓
Process (AuditLog)
↓
Emit Output
↓
Database Storage
```
---
# Summary
AuditLog AuditLog GoldBot'dagi barcha Owner/Admin harakatlari va Critical Event'lar uchun Canonical append-only Audit Trail repository moduli hisoblanadi.
