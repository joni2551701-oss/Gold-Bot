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
RiskService
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
Receive Risk Approval
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
4. Standard Response yaratilishi shart.
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
