# Risk Validator Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat RiskValidator Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
PortfolioManager
↓
RiskValidator
↓
Receive Risk Reports
↓
Validate All Modules
↓
Validate Risk Policy
↓
Generate Risk Approval
↓
Create Validation Report
↓
RiskService
```
---
# Runtime Rules
1. Barcha Risk Reportlar mavjud bo'lishi shart.
2. Risk Policy tekshirilishi shart.
3. Risk Approval yaratilishi shart.
4. Validation Report yaratilishi shart.
---
# State Flow
```text
Idle
↓
Receiving
↓
Validating
↓
Approving
↓
Completed
```
---
# Summary
PortfolioManager
↓
RiskValidator
↓
Risk Approval
↓
RiskService
