# Monitoring Service Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat MonitoringService ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
Execution Layer
↓
MonitoringService
↓
PositionMonitor
↓
RecoveryManager
↓
Database Layer
```
---
# Module Architecture
```text
MonitoringService
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
Monitoring Request'larni qabul qiladi.
---
## Request Validator
Request formatini tekshiradi.
---
## Session Manager
Monitoring Session'ni boshqaradi.
---
## Request Dispatcher
PositionMonitor'ga Request yuboradi.
---
## Response Formatter
Monitoring natijasini standart formatga o'tkazadi.
---
## Service Monitor
MonitoringService holatini kuzatadi.
---
# Allowed Dependencies
✓ PositionMonitor
✓ RecoveryManager
---
# Forbidden Dependencies
✗ ExecutionEngine
✗ BrokerGateway
✗ Decision Layer
✗ Risk Layer
---
# Summary
MonitoringService GoldBot Trade Monitoring Layer uchun yagona Service Gateway va Public API modulidir.
