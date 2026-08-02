# Risk Layer Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat Risk Layer Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
Decision Layer
↓
RiskService
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
Risk Approval
↓
Execution Layer
```
---
# Runtime Rules
1. Decision APPROVED bo'lishi shart.
2. RiskEngine birinchi hisoblashni boshlaydi.
3. PositionSizing MoneyManagement'dan oldin ishlaydi.
4. Drawdown Exposure'dan oldin tekshiriladi.
5. Portfolio Risk Exposure natijasiga asoslanadi.
6. RiskValidator har doim oxirida ishlaydi.
7. Execution Layer faqat APPROVED Risk bilan ishga tushadi.
---
# State Flow
```text
Idle
↓
Receiving Decision
↓
Risk Assessment
↓
Risk Calculation
↓
Risk Validation
↓
Risk Approval
↓
Completed
```
---
# Summary
Decision Layer
↓
Risk Layer
↓
Execution Layer
