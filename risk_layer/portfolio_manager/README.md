# Portfolio Manager
Status: CANONICAL
---
# Purpose
PortfolioManager GoldBot Risk Layer ichidagi Canonical Portfolio Risk Management moduli hisoblanadi.
Uning asosiy vazifasi barcha aktivlar, barcha ochiq pozitsiyalar va barcha strategiyalar bo'yicha umumiy Portfolio Risk'ni boshqarishdir.
PortfolioManager bitta trade'ni emas, balki butun trading account xavfsizligini nazorat qiladi.
PortfolioManager Risk Approval bermaydi.
PortfolioManager Trade Execution bajarmaydi.
---
# Objective
PortfolioManager quyidagi vazifalarni bajaradi.
• Portfolio Risk Analysis
• Portfolio Exposure Analysis
• Asset Allocation
• Correlation Analysis
• Diversification Analysis
• Portfolio Report Generation
---
# Layer Position
```text
ExposureManager
↓
PortfolioManager
↓
RiskValidator
```
---
# Responsibilities
PortfolioManager
✓ Portfolio Risk hisoblaydi
✓ Asset Allocation nazorat qiladi
✓ Symbol Correlation tekshiradi
✓ Diversification baholaydi
✓ Portfolio Heat hisoblaydi
✓ Portfolio Report yaratadi
---
# Not Responsible
PortfolioManager
✗ Position Size Calculation
✗ Exposure Monitoring
✗ Drawdown Monitoring
✗ Risk Approval
✗ Trade Execution
✗ Decision Making
---
# Input
PortfolioManager qabul qiladi.
• Exposure Report
• Open Positions
• Portfolio Statistics
• Correlation Data
• Portfolio Policy
---
# Output
PortfolioManager yaratadi.
• Portfolio Report
• Portfolio Risk
• Portfolio Context
• Portfolio Metadata
---
# Portfolio States
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
Receive Exposure Report
↓
Analyze Portfolio
↓
Analyze Correlation
↓
Analyze Diversification
↓
Generate Portfolio Report
↓
RiskValidator
```
---
# Golden Rules
1. Portfolio Risk har doim Account darajasida hisoblanadi.
2. Correlation hisobga olinishi shart.
3. Diversification baholanishi shart.
4. Portfolio Heat limitdan oshmasligi kerak.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
PortfolioManager/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
PortfolioManager GoldBot Risk Layer ichidagi butun trading account xavfsizligini nazorat qiluvchi Canonical Portfolio Risk Management moduli hisoblanadi.
