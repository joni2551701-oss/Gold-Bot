# Execution Service Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat ExecutionService ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
Risk Layer
↓
ExecutionService
↓
ExecutionEngine
↓
ExecutionMonitor
↓
Trade Monitoring Layer
```
---
# Module Architecture
```text
ExecutionService
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
Execution Request'larni qabul qiladi.
---
## Request Validator
Request formatini tekshiradi.
---
## Session Manager
Execution Session'ni boshqaradi.
---
## Request Dispatcher
ExecutionEngine'ga Request yuboradi.
---
## Response Formatter
Execution natijasini standart formatga o'tkazadi.
---
## Service Monitor
ExecutionService holatini kuzatadi.
---
# Allowed Dependencies
✓ ExecutionEngine
✓ ExecutionMonitor
---
# Forbidden Dependencies
✗ BrokerGateway
✗ OrderRouter
✗ Decision Layer
✗ Database Layer
---
# Summary
ExecutionService GoldBot Execution Layer uchun yagona Service Gateway va Public API modulidir.
