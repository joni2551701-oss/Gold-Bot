# Monitoring Service Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat MonitoringService Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
Execution Layer
↓
MonitoringService
↓
Validate Request
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
Receive Monitoring Result
↓
Standardize Response
↓
Database Layer
```
---
# Runtime Rules
1. Execution Result mavjud bo'lishi shart.
2. Request Validation bajarilishi shart.
3. Monitoring Pipeline muvaffaqiyatli yakunlanishi shart.
4. Standard Response yaratilishi shart.
---
# State Flow
```text
Idle
↓
Receiving
↓
Validating
↓
Forwarding
↓
Receiving Result
↓
Completed
```
---
# Summary
Execution Layer
↓
MonitoringService
↓
Trade Monitoring Layer
↓
Database Layer
