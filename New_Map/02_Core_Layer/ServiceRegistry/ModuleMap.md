# ServiceRegistry Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat ServiceRegistry modulining ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
CoreEngine
↓
ServiceRegistry
↓
GoldBot Services
```
---
# Module Architecture
```text
ServiceRegistry
        │
        ├── Registration Manager
        ├── Discovery Manager
        ├── Resolution Manager
        ├── Dependency Manager
        ├── Metadata Manager
        ├── State Manager
        ├── Health Manager
        └── Event Generator
```
---
# Internal Components
## Registration Manager
Service'larni ro'yxatdan o'tkazadi.
---
## Discovery Manager
Service Discovery bajaradi.
---
## Resolution Manager
Service Reference qaytaradi.
---
## Dependency Manager
Service Dependency'larni boshqaradi.
---
## Metadata Manager
Service Metadata boshqaradi.
---
## State Manager
Registry holatini boshqaradi.
---
## Health Manager
Service Health holatini kuzatadi.
---
## Event Generator
Registry Event yaratadi.
---
# Dependency Map
```text
CoreEngine
↓
ServiceRegistry
↓
All Services
```
---
# Allowed Dependencies
✓ CoreEngine
✓ Configuration
✓ HealthMonitor
✓ Event System
---
# Forbidden Dependencies
✗ Data Layer
✗ Context Layer
✗ Signal Layer
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Ownership
ServiceRegistry egalik qiladi.
✓ Service Registry
✓ Dependency Graph
✓ Service Metadata
✓ Registry State
✓ Service References
---
# Module Rules
1. ServiceRegistry yagona Registry.
2. Service Discovery markazlashgan.
3. Dependency Graph saqlanadi.
4. Circular Dependency taqiqlanadi.
---
# Summary
ServiceRegistry GoldBot Runtime Service Discovery va Resolution boshqaruvini amalga oshiruvchi Canonical Registry moduli hisoblanadi.
