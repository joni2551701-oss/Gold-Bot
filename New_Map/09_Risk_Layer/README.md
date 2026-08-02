# Risk Layer
Status: CANONICAL
---
# Purpose
Risk Layer GoldBot arxitekturasidagi Capital Protection va Risk Control qatlami hisoblanadi.
Uning asosiy vazifasi Decision Layer tomonidan APPROVED qilingan Trade'ni risk nuqtai nazaridan baholash va faqat xavfsiz bo'lgan Trade'larga Execution Layer'ga o'tishga ruxsat berishdir.
Risk Layer'dan o'tmagan hech qanday Trade Execution Layer'ga uzatilmaydi.
---
# Objective
Risk Layer quyidagi vazifalarni bajaradi.
• Position Size Calculation
• Money Management
• Drawdown Protection
• Exposure Control
• Portfolio Risk Management
• Risk Validation
---
# Layer Position
```text
Decision Layer
↓
Risk Layer
↓
Execution Layer
```
---
# Internal Modules
```text
Risk Layer
├── RiskEngine
├── PositionSizing
├── MoneyManagement
├── DrawdownManager
├── ExposureManager
├── PortfolioManager
├── RiskValidator
└── RiskService
```
---
# Responsibilities
Risk Layer
✓ Position Size hisoblaydi
✓ Lot Size hisoblaydi
✓ Risk % tekshiradi
✓ Drawdown nazorat qiladi
✓ Exposure nazorat qiladi
✓ Portfolio Risk nazorat qiladi
✓ Risk Validation bajaradi
✓ Execution uchun Risk Approval yaratadi
---
# Not Responsible
Risk Layer
✗ Signal Generation
✗ AI Analysis
✗ Final Decision
✗ Market Analysis
✗ Order Execution
✗ Position Monitoring
---
# Input
Risk Layer qabul qiladi.
• Final Decision
• Decision Confidence
• Signal Package
• Account Information
• Portfolio Information
---
# Output
Risk Layer yaratadi.
• Risk Approval
• Position Size
• Lot Size
• Risk Report
• Risk Metadata
---
# Risk States
```text
APPROVED
Trade xavfsiz.
↓
REJECTED
Risk juda yuqori.
↓
REDUCE
Lot yoki Risk kamaytirilsin.
↓
BLOCKED
Trading vaqtincha bloklandi.
```
---
# Workflow
```text
Receive Decision
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
RiskService
↓
Execution Layer
```
---
# Golden Rules
1. Decision APPROVED bo'lmasa Risk Layer ishlamaydi.
2. Risk Layer Final Decision'ni o'zgartirmaydi.
3. Har bir Trade Risk Validation'dan o'tishi shart.
4. RiskValidator yakuniy Risk Approval yaratadi.
5. Risk REJECT bo'lsa Execution Layer ishga tushmaydi.
6. Capital Protection har doim ustuvor.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
09_Risk_Layer/
├── README.md
├── RiskEngine/
├── PositionSizing/
├── MoneyManagement/
├── DrawdownManager/
├── ExposureManager/
├── PortfolioManager/
├── RiskValidator/
├── RiskService/
├── Layer_DataFlow.md
├── Layer_SequenceDiagram.md
├── Layer_ModuleMap.md
└── Layer_Contracts.md
```
---
# Summary
Risk Layer GoldBot arxitekturasidagi Canonical Capital Protection Layer hisoblanadi.
Decision Layer savdoga ruxsat beradi.
Risk Layer esa ushbu savdoni kapital xavfsizligi nuqtai nazaridan baholab, faqat xavfsiz Trade'larnigina Execution Layer'ga uzatadi.
