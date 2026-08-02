# Money Management
Status: CANONICAL
---
# Purpose
MoneyManagement GoldBot Risk Layer ichidagi Canonical Capital Management moduli hisoblanadi.
Uning asosiy vazifasi PositionSizing natijalarini foydalanuvchining Risk Policy va Money Management qoidalari bilan solishtirib yakuniy Trading Capital Allocation yaratishdir.
MoneyManagement Risk Approval bermaydi.
MoneyManagement Trade Execution bajarmaydi.
MoneyManagement faqat Capital Management bilan shug'ullanadi.
---
# Objective
MoneyManagement quyidagi vazifalarni bajaradi.
• Capital Allocation
• Risk Per Trade Control
• Daily Risk Control
• Weekly Risk Control
• Monthly Risk Control
• Money Management Report Generation
---
# Layer Position
```text
PositionSizing
↓
MoneyManagement
↓
DrawdownManager
```
---
# Responsibilities
MoneyManagement
✓ Position Size tekshiradi
✓ Risk % tekshiradi
✓ Daily Risk hisoblaydi
✓ Weekly Risk hisoblaydi
✓ Monthly Risk hisoblaydi
✓ Capital Allocation yaratadi
---
# Not Responsible
MoneyManagement
✗ Position Size Calculation
✗ Drawdown Validation
✗ Exposure Validation
✗ Risk Approval
✗ Trade Execution
✗ Portfolio Management
---
# Input
MoneyManagement qabul qiladi.
• Position Package
• Account Balance
• Risk Policy
• Daily Statistics
• Weekly Statistics
• Monthly Statistics
---
# Output
MoneyManagement yaratadi.
• Capital Allocation
• Money Report
• Money Context
• Money Metadata
---
# Workflow
```text
Receive Position Package
↓
Validate Risk Policy
↓
Calculate Daily Risk
↓
Calculate Weekly Risk
↓
Calculate Monthly Risk
↓
Generate Capital Allocation
↓
DrawdownManager
```
---
# Golden Rules
1. Risk Policy majburiy.
2. Daily Limit buzilmasligi kerak.
3. Weekly Limit buzilmasligi kerak.
4. Monthly Limit buzilmasligi kerak.
5. Capital Protection ustuvor.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
MoneyManagement/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
MoneyManagement GoldBot Risk Layer ichidagi Capital Allocation va Money Management siyosatini boshqaruvchi Canonical modul hisoblanadi.
