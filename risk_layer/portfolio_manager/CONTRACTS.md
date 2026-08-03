# Portfolio Manager Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat PortfolioManager modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
PortfolioManager quyidagilar uchun javobgar.
✓ Portfolio Risk Analysis
✓ Asset Allocation
✓ Correlation Analysis
✓ Diversification Analysis
✓ Portfolio Heat Calculation
✓ Portfolio Report Generation
PortfolioManager bajarmaydi.
✗ Position Size Calculation
✗ Exposure Monitoring
✗ Drawdown Monitoring
✗ Risk Approval
✗ Trade Execution
✗ Decision Making
---
# Module Boundary
```text
ExposureManager
↓
PortfolioManager
↓
RiskValidator
```
---
# Input Contract
• Exposure Report
• Open Positions
• Portfolio Statistics
• Correlation Data
• Portfolio Policy
---
# Output Contract
• Portfolio Report
• Portfolio Risk
• Portfolio Context
• Portfolio Metadata
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
✗ Platform Layer
---
# Runtime Contract
1. Portfolio Risk hisoblanishi shart.
2. Asset Allocation tekshirilishi shart.
3. Correlation Analysis bajarilishi shart.
4. Diversification baholanishi shart.
5. Portfolio Heat hisoblanishi shart.
6. Portfolio Report RiskValidator'ga uzatilishi shart.
7. PortfolioManager Risk Approval bermaydi.
8. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Portfolio tahlil qilinadi.
✓ Correlation tekshiriladi.
✓ Diversification baholanadi.
✓ Portfolio Heat hisoblanadi.
✓ Portfolio Report yaratiladi.
✓ RiskValidator'ga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
PortfolioManager Contract GoldBot Risk Layer ichidagi umumiy Portfolio Risk, Asset Allocation, Correlation va Diversification nazoratini amalga oshirish hamda RiskValidator moduliga standart Portfolio Report uzatishni belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
