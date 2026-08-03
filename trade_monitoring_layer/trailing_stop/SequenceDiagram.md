# Trailing Stop Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat TrailingStop Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
BreakevenManager
↓
TrailingStop
↓
Receive Trade Context
↓
Check Trailing Rules
↓
Track Market Price
↓
Update Stop Loss
↓
Generate Trailing Report
↓
PartialClose
```
---
# Runtime Rules
1. Trade Context mavjud bo'lishi shart.
2. Trailing Rules mavjud bo'lishi shart.
3. Market Price muntazam yangilanib turishi shart.
4. Updated Stop Loss yaratilishi shart.
---
# State Flow
```text
Idle
↓
Receiving
↓
Monitoring
↓
Updating
↓
Reporting
↓
Completed
```
---
# Summary
BreakevenManager
↓
TrailingStop
↓
PartialClose
