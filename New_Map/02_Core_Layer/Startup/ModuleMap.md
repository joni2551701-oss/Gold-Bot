# Startup Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat Startup modulining ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
System Boot
↓
Startup
↓
CoreEngine
```
---
# Module Architecture
```text
Startup
      │
      ├── Boot Manager
      ├── Configuration Loader
      ├── Dependency Verifier
      ├── Initialization Manager
      ├── Validation Manager
      ├── State Manager
      ├── Event Generator
      └── Report Generator
```
---
# Internal Components
## Boot Manager
Boot jarayonini boshqaradi.
---
## Configuration Loader
Configuration yuklaydi.
---
## Dependency Verifier
Dependency tekshiradi.
---
## Initialization Manager
Service va Layer'larni initialize qiladi.
---
## Validation Manager
Startup Validation bajaradi.
---
## State Manager
Startup State boshqaradi.
---
## Event Generator
Startup Event yaratadi.
---
## Report Generator
Startup Report yaratadi.
---
# Dependency Map
```text
System Boot
↓
Startup
↓
CoreEngine
```
---
# Allowed Dependencies
✓ Configuration
✓ ServiceRegistry
✓ Event System
✓ CoreEngine
---
# Forbidden Dependencies
✗ Data Layer internals
✗ Context Layer
✗ Signal Layer
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Platform Layer
---
# Ownership
Startup egalik qiladi.
✓ Startup State
✓ Initialization Order
✓ Dependency Validation
✓ Startup Metadata
---
# Module Rules
1. Startup yagona Boot Manager.
2. Initialization Order o'zgarmaydi.
3. Dependency tekshiruvi majburiy.
4. Circular Dependency taqiqlanadi.
---
# Summary
Startup GoldBot Runtime Initialization boshqaruvini amalga oshiruvchi Canonical Startup moduli hisoblanadi.
