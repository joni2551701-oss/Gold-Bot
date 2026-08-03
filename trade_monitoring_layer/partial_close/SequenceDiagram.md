# Partial Close Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat PartialClose Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
TrailingStop
↓
PartialClose
↓
Receive Trade Context
↓
Check Partial Close Rules
↓
Calculate Close Volume
↓
Update Position
↓
Generate Partial Close Report
↓
RecoveryManager
```
---
# Runtime Rules
1. Trade Context mavjud bo'lishi shart.
2. Partial Close Rules mavjud bo'lishi shart.
3. Close Volume hisoblanishi shart.
4. Remaining Position aniqlanishi shart.
---
# State Flow
```text
Idle
↓
Receiving
↓
Evaluating
↓
Closing
↓
Reporting
↓
Completed
```
---
# Summary
TrailingStop
↓
PartialClose
↓
RecoveryManager
