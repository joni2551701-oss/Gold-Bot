# CoreService Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat CoreService modulining ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
CoreEngine
↓
CoreService
↓
Core Modules
```
---
# Module Architecture
```text
CoreService
        │
        ├── Command Manager
        ├── Service Coordinator
        ├── Lifecycle Manager
        ├── Recovery Manager
        ├── Health Coordinator
        ├── State Manager
        ├── Event Manager
        └── Response Manager
```
---
# Internal Components
## Command Manager
Runtime Command'larni boshqaradi.
---
## Service Coordinator
Core Module'larni koordinatsiya qiladi.
---
## Lifecycle Manager
Core Lifecycle boshqaradi.
---
## Recovery Manager
Recovery jarayonini boshqaradi.
---
## Health Coordinator
Health holatini muvofiqlashtiradi.
---
## State Manager
Runtime State'ni boshqaradi.
---
## Event Manager
Runtime Event'larini boshqaradi.
---
## Response Manager
Module Response'larni boshqaradi.
---
# Dependency Map
```text
CoreEngine
↓
CoreService
↓
Pipeline
↓
Scheduler
↓
ServiceRegistry
↓
Configuration
↓
HealthMonitor
↓
Startup
↓
Shutdown
```
---
# Allowed Dependencies
✓ Pipeline
✓ Scheduler
✓ ServiceRegistry
✓ Configuration
✓ HealthMonitor
✓ Startup
✓ Shutdown
✓ Event System
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
CoreService egalik qiladi.
✓ Runtime State
✓ Core Service State
✓ Lifecycle State
✓ Runtime Events
✓ Core Metadata
---
# Module Rules
1. CoreService yagona Core Service Orchestrator.
2. Core Module'lar bevosita bir-birini boshqarmaydi.
3. Runtime Coordination markazlashgan.
4. Circular Dependency taqiqlanadi.
---
# Summary
CoreService GoldBot Core Layer ichidagi barcha Runtime Service koordinatsiyasini amalga oshiruvchi Canonical Service moduli hisoblanadi.
