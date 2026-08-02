# Money Management Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat MoneyManagement Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
PositionSizing
↓
MoneyManagement
↓
Validate Risk Policy
↓
Calculate Daily Risk
↓
Calculate Weekly Risk
↓
Calculate Monthly Risk
↓
Generate Capital Allocation
↓
DrawdownManager
```
---
# Runtime Rules
1. Position Package mavjud bo'lishi shart.
2. Risk Policy mavjud bo'lishi shart.
3. Daily Risk hisoblanishi shart.
4. Capital Allocation yaratilishi shart.
---
# State Flow
```text
Idle
↓
Receiving
↓
Validating
↓
Calculating
↓
Allocating
↓
Completed
```
---
# Summary
PositionSizing
↓
MoneyManagement
↓
Capital Allocation
↓
DrawdownManager
