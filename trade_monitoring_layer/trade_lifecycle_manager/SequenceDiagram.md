# Trade Lifecycle Manager Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat TradeLifecycleManager Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
PositionMonitor
↓
TradeLifecycleManager
↓
Receive Position Report
↓
Validate State
↓
Process Transition
↓
Update Trade State
↓
Generate Lifecycle Report
↓
SLTPMonitor
```
---
# Runtime Rules
1. Position Report mavjud bo'lishi shart.
2. State Transition tekshirilishi shart.
3. Trade State yangilanishi shart.
4. Lifecycle Report yaratilishi shart.
---
# State Flow
```text
Idle
↓
Receiving
↓
Validating
↓
Transitioning
↓
Reporting
↓
Completed
```
---
# Summary
PositionMonitor
↓
TradeLifecycleManager
↓
SLTPMonitor
