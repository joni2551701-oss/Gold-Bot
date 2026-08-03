# Position Sizing Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat PositionSizing Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
RiskEngine
↓
PositionSizing
↓
Calculate Risk Amount
↓
Calculate Position Size
↓
Calculate Lot Size
↓
Validate Symbol Limits
↓
Generate Position Package
↓
MoneyManagement
```
---
# Runtime Rules
1. Risk Package mavjud bo'lishi shart.
2. Entry Price mavjud bo'lishi shart.
3. Stop Loss mavjud bo'lishi shart.
4. Lot Size broker limitidan chiqmasligi kerak.
---
# State Flow
```text
Idle
↓
Receiving
↓
Calculating
↓
Validating
↓
Packaging
↓
Completed
```
---
# Summary
RiskEngine
↓
PositionSizing
↓
Position Package
↓
MoneyManagement
