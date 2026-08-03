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
ExecutionService (Entry)
↓
ExecutionEngine
↓
OrderValidator
↓
OrderManager
↓
OrderRouter
↓
BrokerGateway
↓
ExecutionMonitor
↓
ExecutionService (Exit)
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
Risk Layer'dan Execution Request'larni qabul qiladi.
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
ExecutionMonitor'dan qaytgan Execution Result'ni standart formatga o'tkazadi va Trade Monitoring Layer'ga uzatadi.
---
## Service Monitor
ExecutionService holatini kuzatadi.
---
# Allowed Dependencies
✓ ExecutionEngine
✓ ExecutionMonitor
---
# Forbidden Dependencies
✗ OrderValidator (to'g'ridan-to'g'ri)
✗ OrderManager (to'g'ridan-to'g'ri)
✗ OrderRouter (to'g'ridan-to'g'ri)
✗ BrokerGateway (to'g'ridan-to'g'ri)
✗ Decision Layer
✗ Risk Layer
✗ Database Layer
✗ Platform Layer
---
# Summary
ExecutionService GoldBot Execution Layer uchun ikki tomonlama Boundary Gateway va Public API modulidir.
