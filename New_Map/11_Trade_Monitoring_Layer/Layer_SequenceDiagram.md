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
# Runtime Rules
1. Execution Result mavjud bo'lishi shart.
2. MonitoringService Trade Monitoring Layer'ning yagona Entry va Exit nuqtasi hisoblanadi.
3. Position Monitoring boshlanishi shart.
4. Trade Lifecycle boshqarilishi shart.
5. SL/TP Trigger tekshirilishi shart.
6. Break Even va Trailing ketma-ket ishlashi shart.
7. Recovery faqat Restart holatida ishlaydi, lekin Layer tashqarisiga chiqmaydi.
8. Monitoring natijalari MonitoringService orqali Database Layer'ga uzatiladi.
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
