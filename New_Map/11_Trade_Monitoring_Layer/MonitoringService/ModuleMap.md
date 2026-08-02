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
MonitoringService (Entry)
↓
PositionMonitor
↓
TradeLifecycleManager
↓
SLTPMonitor
↓
BreakevenManager
↓
TrailingStop
↓
PartialClose
↓
RecoveryManager
↓
MonitoringService (Exit)
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
Execution Layer'dan Monitoring Request'larni qabul qiladi.
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
RecoveryManager'dan qaytgan Monitoring Result'ni standart formatga o'tkazadi va Database Layer'ga uzatadi.
---
## Service Monitor
MonitoringService holatini kuzatadi.
---
# Allowed Dependencies
✓ PositionMonitor
✓ RecoveryManager
---
# Forbidden Dependencies
✗ TradeLifecycleManager (to'g'ridan-to'g'ri)
✗ SLTPMonitor (to'g'ridan-to'g'ri)
✗ BreakevenManager (to'g'ridan-to'g'ri)
✗ TrailingStop (to'g'ridan-to'g'ri)
✗ PartialClose (to'g'ridan-to'g'ri)
✗ ExecutionEngine
✗ BrokerGateway
✗ Decision Layer
✗ Risk Layer
---
# Summary
MonitoringService GoldBot Trade Monitoring Layer uchun ikki tomonlama Boundary Gateway va Public API modulidir.
