# Pipeline Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat Pipeline modulining ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
CoreEngine
↓
Pipeline
↓
GoldBot Layers
```
---
# Module Architecture
```text
Pipeline
      │
      ├── Request Manager
      ├── Stage Manager
      ├── Flow Controller
      ├── Execution Manager
      ├── Recovery Manager
      ├── State Manager
      ├── Event Manager
      └── Result Manager
```
---
# Internal Components
## Request Manager
Pipeline Request'larni boshqaradi.
---
## Stage Manager
Pipeline Stage'larni boshqaradi.
---
## Flow Controller
Execution Flow'ni boshqaradi.
---
## Execution Manager
Stage'larni ishga tushiradi.
---
## Recovery Manager
Pipeline Recovery boshqaradi.
---
## State Manager
Pipeline Runtime State'ni boshqaradi.
---
## Event Manager
Pipeline Event'larini boshqaradi.
---
## Result Manager
Pipeline natijalarini boshqaradi.
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
✓ CoreEngine
✓ Scheduler
✓ ServiceRegistry
✓ Event System
✓ Configuration
---
# Forbidden Dependencies
✗ Data Layer internals
✗ Context Logic
✗ Signal Logic
✗ AI Logic
✗ Decision Logic
✗ Risk Logic
✗ Execution Logic
---
# Ownership
Pipeline egalik qiladi.
✓ Pipeline State
✓ Execution Order
✓ Runtime Flow
✓ Pipeline Metadata
---
# Module Rules
1. Pipeline yagona Runtime Flow Manager.
2. Execution Order qat'iy saqlanadi.
3. Pipeline State markazlashgan boshqariladi.
4. Circular Dependency taqiqlanadi.
---
# Summary
Pipeline GoldBot Runtime Execution Flow'ni boshqaruvchi Canonical Pipeline moduli hisoblanadi.
