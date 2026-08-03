# Drawdown Manager Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat DrawdownManager Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
MoneyManagement
↓
DrawdownManager
↓
Calculate Current Drawdown
↓
Validate Drawdown Policy
↓
Generate Drawdown Report
↓
ExposureManager
```
---
# Runtime Rules
1. Account Equity mavjud bo'lishi shart.
2. Drawdown hisoblanishi shart.
3. Max Drawdown tekshirilishi shart.
4. Drawdown Report yaratilishi shart.
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
Reporting
↓
Completed
```
---
# Summary
MoneyManagement
↓
DrawdownManager
↓
Drawdown Report
↓
ExposureManager
