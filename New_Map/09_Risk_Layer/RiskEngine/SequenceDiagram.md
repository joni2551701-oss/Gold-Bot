# Risk Engine Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat RiskEngine Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
Decision Layer
↓
RiskEngine
↓
Validate Inputs
↓
Collect Risk Context
↓
Generate Risk Package
↓
PositionSizing
```
---
# Runtime Rules
1. Decision APPROVED bo'lishi shart.
2. Account ma'lumotlari mavjud bo'lishi shart.
3. Risk Context yaratilishi shart.
4. Risk Package PositionSizing'ga uzatilishi shart.
---
# State Flow
```text
Idle
↓
Receiving
↓
Validating
↓
Collecting Context
↓
Building Package
↓
Completed
```
---
# Summary
Decision Layer
↓
RiskEngine
↓
Risk Package
↓
PositionSizing
