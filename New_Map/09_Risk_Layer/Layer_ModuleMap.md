# Risk Layer Module Map
Status: CANONICAL
---
# Layer Architecture
```text
09_Risk_Layer
│
├── RiskService
│
├── RiskEngine
│
├── PositionSizing
│
├── MoneyManagement
│
├── DrawdownManager
│
├── ExposureManager
│
├── PortfolioManager
│
└── RiskValidator
```
---
# Processing Pipeline
```text
Decision Layer
        │
        ▼
RiskService (Entry)
        │
        ▼
RiskEngine
        │
        ▼
PositionSizing
        │
        ▼
MoneyManagement
        │
        ▼
DrawdownManager
        │
        ▼
ExposureManager
        │
        ▼
PortfolioManager
        │
        ▼
RiskValidator
        │
        ▼
RiskService (Exit)
        │
        ▼
Execution Layer
```
---
# Module Responsibilities
## RiskService
Risk Layer'ning ikki tomonlama (bidirectional) Boundary Gateway'i — Entry va Exit.
---
## RiskEngine
Risk Assessment boshlaydi.
---
## PositionSizing
Position Size va Lot Size hisoblaydi.
---
## MoneyManagement
Capital Allocation va Risk Policy nazorat qiladi.
---
## DrawdownManager
Drawdown limitlarini nazorat qiladi.
---
## ExposureManager
Exposure va Position Concentration nazorat qiladi.
---
## PortfolioManager
Portfolio Risk va Correlation nazorat qiladi.
---
## RiskValidator
Yakuniy Risk Approval yaratadi. Layer tashqarisiga chiqmaydi — natijani RiskService orqali uzatadi.
---
# Summary
Risk Layer GoldBot arxitekturasidagi Canonical Capital Protection Layer hisoblanadi.
