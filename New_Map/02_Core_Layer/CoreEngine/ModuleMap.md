# CoreEngine Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat CoreEngine modulining ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
GoldBot
↓
CoreEngine
↓
Pipeline
↓
GoldBot Layers
```
---
# Module Architecture
```text
CoreEngine
        │
        ├── Runtime Manager
        ├── Layer Coordinator
        ├── Startup Manager
        ├── Shutdown Manager
        ├── Recovery Manager
        ├── Health Supervisor
        ├── State Manager
        └── Event Coordinator
```
---
# Internal Components
## Runtime Manager
Runtime holatini boshqaradi.
---
## Layer Coordinator
Barcha Layer'larni koordinatsiya qiladi.
---
## Startup Manager
Startup jarayonini boshqaradi.
---
## Shutdown Manager
Shutdown jarayonini boshqaradi.
---
## Recovery Manager
Recovery jarayonini boshqaradi.
---
## Health Supervisor
Tizim sog'ligini nazorat qiladi.
---
## State Manager
Runtime State'ni boshqaradi.
---
## Event Coordinator
Core Runtime Event'larini boshqaradi.
---
# Dependency Map
```text
CoreEngine
↓
Pipeline
↓
GoldBot Layers
```
---
# Allowed Dependencies
✓ Pipeline
✓ ServiceRegistry
✓ Configuration
✓ HealthMonitor
✓ Startup
✓ Shutdown
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
CoreEngine egalik qiladi.
✓ Runtime State
✓ Layer State
✓ Lifecycle State
✓ Recovery State
✓ Health State
---
# Module Rules
1. CoreEngine yagona Runtime Engine.
2. Layer'lar CoreEngine orqali boshqariladi.
3. Runtime markazlashgan boshqariladi.
4. Circular Dependency taqiqlanadi.
---
# Summary
CoreEngine GoldBot Runtime'ning Canonical Engine moduli hisoblanadi.
