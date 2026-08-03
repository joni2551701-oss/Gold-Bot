# Database Manager Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat DatabaseManager ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
DatabaseService
↓
DatabaseManager
↓
Repositories
```
---
# Module Architecture
```text
DatabaseManager
        │
        ├── Configuration Loader
        ├── Connection Pool Manager
        ├── Transaction Manager
        ├── Migration Manager
        ├── Health Monitor
        └── Metadata Generator
```
---
# Internal Components
## Configuration Loader
Database konfiguratsiyasini yuklaydi.
---
## Connection Pool Manager
Connection Pool yaratadi va boshqaradi.
---
## Transaction Manager
Database Transaction'larni boshqaradi.
---
## Migration Manager
Migration'larni boshqaradi.
---
## Health Monitor
Database holatini kuzatadi.
---
## Metadata Generator
Database Metadata yaratadi.
---
# Allowed Dependencies
✓ DatabaseService
✓ TradeRepository
✓ UserRepository
✓ MarketRepository
✓ JournalRepository
---
# Forbidden Dependencies
✗ CacheManager
✗ BackupManager
✗ Platform Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Summary
DatabaseManager GoldBot Database Layer ichidagi Database Infrastructure boshqaruvini amalga oshiruvchi Canonical modul hisoblanadi.
