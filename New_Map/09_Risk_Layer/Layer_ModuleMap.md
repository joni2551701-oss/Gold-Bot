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
├── RiskValidator
│
└── Risk Approval
```
---
# Processing Pipeline
```text
RiskService
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
```
---
# Module Responsibilities
## RiskService
Risk Layer Gateway.
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
Yakuniy Risk Approval yaratadi.
---
# Summary
Risk Layer GoldBot arxitekturasidagi Canonical Capital Protection Layer hisoblanadi.
