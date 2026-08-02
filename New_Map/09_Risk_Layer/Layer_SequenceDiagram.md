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
RiskService (Entry)
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
RiskService (Exit)
↓
Execution Layer
```
---
# Runtime Rules
1. Decision APPROVED bo'lishi shart.
2. RiskService Risk Layer'ning yagona Entry va Exit nuqtasi hisoblanadi.
3. RiskEngine birinchi hisoblashni boshlaydi.
4. PositionSizing MoneyManagement'dan oldin ishlaydi.
5. Drawdown Exposure'dan oldin tekshiriladi.
6. Portfolio Risk Exposure natijasiga asoslanadi.
7. RiskValidator har doim modul zanjirining oxirida ishlaydi, lekin Layer tashqarisiga chiqmaydi.
8. Execution Layer faqat APPROVED Risk bilan ishga tushadi.
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
