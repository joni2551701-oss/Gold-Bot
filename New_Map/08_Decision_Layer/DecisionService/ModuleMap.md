# Decision Service Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat DecisionService ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
External Layers
↓
DecisionService
↓
DecisionEngine
↓
DecisionLogger
```
---
# Module Architecture
```text
DecisionService
        │
        ├── Request Receiver
        ├── Request Validator
        ├── Session Manager
        ├── Request Dispatcher
        ├── Response Formatter
        └── Service Monitor
```
---
# Internal Components
## Request Receiver
Decision Request'larni qabul qiladi.
---
## Request Validator
Request formatini tekshiradi.
---
## Session Manager
Decision Session holatini boshqaradi.
---
## Request Dispatcher
Request'ni DecisionEngine'ga uzatadi.
---
## Response Formatter
Decision javobini standart formatga o'tkazadi.
---
## Service Monitor
Decision Service holatini kuzatadi.
---
# Allowed Dependencies
✓ DecisionEngine
✓ DecisionLogger
---
# Forbidden Dependencies
✗ RuleEngine
✗ Risk Layer
✗ Execution Layer
✗ Database Layer
---
# Summary
DecisionService GoldBot Decision Layer uchun yagona Service Gateway va Public API moduli hisoblanadi.
