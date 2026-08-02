# Execution Engine Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat ExecutionEngine ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
ExecutionService
↓
ExecutionEngine
↓
OrderValidator
```
---
# Module Architecture
```text
ExecutionEngine
        │
        ├── Request Validator
        ├── Context Builder
        ├── Pipeline Coordinator
        ├── Execution State Manager
        ├── Execution Report Builder
        └── Metadata Generator
```
---
# Internal Components
## Request Validator
Execution Request tekshiradi.
---
## Context Builder
Execution Context yaratadi.
---
## Pipeline Coordinator
Execution modullarini boshqaradi.
---
## Execution State Manager
Execution holatini boshqaradi.
---
## Execution Report Builder
Execution Report yaratadi.
---
## Metadata Generator
Execution Metadata yaratadi.
---
# Allowed Dependencies
✓ ExecutionService
✓ OrderValidator
✓ OrderManager
✓ OrderRouter
✓ BrokerGateway
✓ ExecutionMonitor
---
# Forbidden Dependencies
✗ Decision Layer
✗ Risk Layer
✗ Database Layer
✗ Platform Layer
---
# Summary
ExecutionEngine GoldBot Execution Layer ichidagi barcha Execution modullarini koordinatsiya qiluvchi Canonical Controller hisoblanadi.
