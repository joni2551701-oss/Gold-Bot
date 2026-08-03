# Risk Service Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat RiskService Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
Decision Layer
↓
RiskService (Entry)
↓
Validate Request
↓
RiskEngine
↓
PositionSizing
↓
MoneyManagement
↓
DrawdownManager
↓
ExposureManager
↓
PortfolioManager
↓
RiskValidator
↓
RiskService (Exit)
↓
Standardize Response
↓
Execution Layer
```
---
# Runtime Rules
1. Decision APPROVED bo'lishi shart.
2. Request Validation bajarilishi shart.
3. RiskValidator yakunlanishi shart.
4. RiskValidator natijasi RiskService orqali Execution Layer'ga uzatiladi.
5. Standard Response yaratilishi shart.
---
# State Flow
```text
Idle
↓
Receiving
↓
Validating
↓
Forwarding
↓
Receiving Response
↓
Completed
```
---
# Summary
Decision Layer
↓
RiskService
↓
Risk Layer
↓
Execution Layer
