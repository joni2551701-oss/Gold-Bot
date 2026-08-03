# SLTP Monitor Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat SLTPMonitor Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
TradeLifecycleManager
↓
SLTPMonitor
↓
Receive Trade Context
↓
Monitor Market Price
↓
Validate SL/TP
↓
Detect Trigger
↓
Generate Monitoring Report
↓
BreakevenManager
```
---
# Runtime Rules
1. Trade Context mavjud bo'lishi shart.
2. Current Market Price mavjud bo'lishi shart.
3. SL va TP alohida tekshirilishi shart.
4. Monitoring Report yaratilishi shart.
---
# State Flow
```text
Idle
↓
Receiving
↓
Monitoring
↓
Trigger Detection
↓
Reporting
↓
Completed
```
---
# Summary
TradeLifecycleManager
↓
SLTPMonitor
↓
BreakevenManager
