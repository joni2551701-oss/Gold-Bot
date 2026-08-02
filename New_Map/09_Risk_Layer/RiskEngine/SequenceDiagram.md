# Risk Engine Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat RiskEngine Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
RiskService
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
1. RiskService orqali Validated Risk Request kelishi shart.
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
RiskService
↓
RiskEngine
↓
Risk Package
↓
PositionSizing
