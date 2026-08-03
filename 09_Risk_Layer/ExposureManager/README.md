# Exposure Manager
Status: CANONICAL
---
# Purpose
ExposureManager GoldBot Risk Layer ichidagi Canonical Market Exposure Control moduli hisoblanadi.
Uning asosiy vazifasi Account'dagi ochiq va rejalashtirilayotgan pozitsiyalarni tahlil qilish, umumiy Exposure darajasini nazorat qilish va bitta instrument yoki yo'nalishda ortiqcha Risk to'planishining oldini olishdir.
ExposureManager Trade Decision qabul qilmaydi.
ExposureManager Portfolio Risk hisoblamaydi.
ExposureManager faqat Market Exposure nazoratini amalga oshiradi.
---
# Objective
ExposureManager quyidagi vazifalarni bajaradi.
• Symbol Exposure Monitoring
• Direction Exposure Monitoring
• Open Position Analysis
• Pending Order Analysis
• Exposure Limit Validation
• Exposure Report Generation
---
# Layer Position
```text
DrawdownManager
↓
ExposureManager
↓
PortfolioManager
```
---
# Responsibilities
ExposureManager
✓ Symbol Exposure hisoblaydi
✓ BUY/SELL Exposure hisoblaydi
✓ Open Positionlarni tekshiradi
✓ Pending Orderlarni hisobga oladi
✓ Exposure Limit tekshiradi
✓ Exposure Report yaratadi
---
# Not Responsible
ExposureManager
✗ Portfolio Risk Analysis
✗ Position Size Calculation
✗ Drawdown Validation
✗ Risk Approval
✗ Trade Execution
✗ Decision Making
---
# Input
ExposureManager qabul qiladi.
• Drawdown Context
• Open Positions
• Pending Orders
• Current Trade
• Exposure Policy
---
# Output
ExposureManager yaratadi.
• Exposure Report
• Exposure Context
• Exposure Status
• Exposure Metadata
---
# Exposure States
NORMAL
↓
WARNING
↓
LIMIT_REACHED
↓
BLOCKED
---
# Workflow
```text
Receive Drawdown Context
↓
Analyze Open Positions
↓
Calculate Exposure
↓
Validate Exposure Limits
↓
Generate Exposure Report
↓
PortfolioManager
```
---
# Golden Rules
1. Barcha Open Positionlar hisobga olinadi.
2. Pending Orderlar ham Exposure'ga qo'shiladi.
3. Symbol Exposure limiti buzilmasligi kerak.
4. Direction Exposure limiti buzilmasligi kerak.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
ExposureManager/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
ExposureManager GoldBot Risk Layer ichidagi Market Exposure va Position Concentration nazoratini amalga oshiruvchi Canonical modul hisoblanadi.
