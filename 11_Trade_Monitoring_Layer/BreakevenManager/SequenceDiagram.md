# Breakeven Manager Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat BreakevenManager Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
SLTPMonitor
↓
BreakevenManager
↓
Receive Trade Context
↓
Check Break Even Rules
↓
Validate Trigger
↓
Move Stop Loss
↓
Generate Break Even Report
↓
TrailingStop
```
---
# Runtime Rules
1. Trade Context mavjud bo'lishi shart.
2. Break Even Rules mavjud bo'lishi shart.
3. Trigger tasdiqlanishi shart.
4. Updated Stop Loss yaratilishi shart.
---
# State Flow
```text
Idle
↓
Receiving
↓
Checking
↓
Activating
↓
Reporting
↓
Completed
```
---
# Summary
SLTPMonitor
↓
BreakevenManager
↓
TrailingStop
