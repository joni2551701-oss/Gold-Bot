# Trade Monitoring Layer Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat Trade Monitoring Layer Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
Execution Layer
↓
MonitoringService
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
Database Layer
```
---
# Runtime Rules
1. Execution Result mavjud bo'lishi shart.
2. Position Monitoring boshlanishi shart.
3. Trade Lifecycle boshqarilishi shart.
4. SL/TP Trigger tekshirilishi shart.
5. Break Even va Trailing ketma-ket ishlashi shart.
6. Recovery faqat Restart holatida ishlaydi.
7. Monitoring natijalari Database Layer'ga uzatiladi.
---
# State Flow
```text
Idle
↓
Receiving Position
↓
Monitoring
↓
Managing Trade
↓
Updating Position
↓
Recovering (optional)
↓
Completed
```
---
# Summary
Execution Layer
↓
Trade Monitoring Layer
↓
Database Layer
