# Risk Service Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat RiskService ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
Decision Layer
↓
RiskService
↓
RiskEngine
↓
RiskValidator
↓
Execution Layer
```
---
# Module Architecture
```text
RiskService
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
Risk Request'larni qabul qiladi.
---
## Request Validator
Request formatini tekshiradi.
---
## Session Manager
Risk Session holatini boshqaradi.
---
## Request Dispatcher
RiskEngine'ga so'rov yuboradi.
---
## Response Formatter
Risk javobini standart formatga o'tkazadi.
---
## Service Monitor
RiskService holatini kuzatadi.
---
# Allowed Dependencies
✓ RiskEngine
✓ RiskValidator
---
# Forbidden Dependencies
✗ Execution Layer
✗ Database Layer
✗ Platform Layer
✗ DecisionEngine
---
# Summary
RiskService GoldBot Risk Layer uchun yagona Service Gateway va Public API modulidir.
