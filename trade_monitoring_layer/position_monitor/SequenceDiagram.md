# Position Monitor Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat PositionMonitor Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
MonitoringService
↓
PositionMonitor
↓
Receive Position
↓
Synchronize Position
↓
Track Position
↓
Detect Events
↓
Generate Position Report
↓
TradeLifecycleManager
```
---
# Runtime Rules
1. Position mavjud bo'lishi shart.
2. Broker Position bilan sinxronlash bajarilishi shart.
3. Position State yangilanishi shart.
4. Position Report yaratilishi shart.
---
# State Flow
```text
Idle
↓
Receiving
↓
Synchronizing
↓
Monitoring
↓
Reporting
↓
Completed
```
---
# Summary
MonitoringService
↓
PositionMonitor
↓
TradeLifecycleManager
