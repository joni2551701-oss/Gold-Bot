# Portfolio Manager Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat PortfolioManager ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
ExposureManager
↓
PortfolioManager
↓
RiskValidator
```
---
# Module Architecture
```text
PortfolioManager
        │
        ├── Portfolio Analyzer
        ├── Asset Allocator
        ├── Correlation Analyzer
        ├── Diversification Analyzer
        ├── Portfolio Heat Calculator
        ├── Portfolio Report Builder
        └── Metadata Generator
```
---
# Internal Components
## Portfolio Analyzer
Portfolio holatini umumiy baholaydi.
---
## Asset Allocator
Har bir aktiv ulushini hisoblaydi.
---
## Correlation Analyzer
Instrumentlar o'rtasidagi bog'liqlikni tekshiradi.
---
## Diversification Analyzer
Portfolio diversifikatsiyasini baholaydi.
---
## Portfolio Heat Calculator
Umumiy Portfolio Heat qiymatini hisoblaydi.
---
## Portfolio Report Builder
Portfolio Report yaratadi.
---
## Metadata Generator
Portfolio Metadata yaratadi.
---
# Allowed Dependencies
✓ ExposureManager
✓ RiskValidator
---
# Forbidden Dependencies
✗ RiskEngine
✗ Decision Layer
✗ Execution Layer
✗ Database Layer
---
# Summary
PortfolioManager GoldBot Risk Layer ichidagi Portfolio Risk Analysis va Diversification nazoratini amalga oshiruvchi Canonical modul hisoblanadi.
