# Drawdown Manager
Status: CANONICAL
---
# Purpose
DrawdownManager GoldBot Risk Layer ichidagi Canonical Drawdown Protection moduli hisoblanadi.
Uning asosiy vazifasi Account Drawdown darajasini kuzatish, Risk Policy bilan solishtirish va kapitalni ortiqcha yo'qotishdan himoya qilishdir.
DrawdownManager Trade Decision qabul qilmaydi.
DrawdownManager Trade Execution bajarmaydi.
DrawdownManager faqat Drawdown Protection bilan shug'ullanadi.
---
# Objective
DrawdownManager quyidagi vazifalarni bajaradi.
• Current Drawdown Calculation
• Daily Drawdown Monitoring
• Weekly Drawdown Monitoring
• Monthly Drawdown Monitoring
• Maximum Drawdown Protection
• Drawdown Report Generation
---
# Layer Position
```text
MoneyManagement
↓
DrawdownManager
↓
ExposureManager
```
---
# Responsibilities
DrawdownManager
✓ Current Drawdown hisoblaydi
✓ Daily Drawdown tekshiradi
✓ Weekly Drawdown tekshiradi
✓ Monthly Drawdown tekshiradi
✓ Max Drawdown tekshiradi
✓ Drawdown Report yaratadi
---
# Not Responsible
DrawdownManager
✗ Position Size Calculation
✗ Exposure Validation
✗ Portfolio Validation
✗ Risk Approval
✗ Trade Execution
✗ Decision Making
---
# Input
DrawdownManager qabul qiladi.
• Money Context
• Account Balance
• Equity
• Closed PnL
• Floating PnL
• Drawdown Policy
---
# Output
DrawdownManager yaratadi.
• Drawdown Report
• Drawdown Context
• Drawdown Status
• Drawdown Metadata
---
# Drawdown States
NORMAL
↓
WARNING
↓
LIMIT_REACHED
↓
LOCKED
---
# Workflow
```text
Receive Money Context
↓
Calculate Drawdown
↓
Validate Drawdown Limits
↓
Generate Drawdown Report
↓
ExposureManager
```
---
# Golden Rules
1. Equity asosiy hisoblash manbai hisoblanadi.
2. Max Drawdown buzilmasligi kerak.
3. Drawdown limiti oshsa Trading bloklanadi.
4. Drawdown Status standart formatda yaratiladi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
DrawdownManager/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
DrawdownManager GoldBot Risk Layer ichidagi kapitalni Drawdown'dan himoya qiluvchi Canonical modul hisoblanadi.
