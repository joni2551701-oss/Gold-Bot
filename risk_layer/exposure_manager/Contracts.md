# Exposure Manager Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat ExposureManager modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
ExposureManager quyidagilar uchun javobgar.
✓ Open Position Analysis
✓ Pending Order Analysis
✓ Symbol Exposure Calculation
✓ Direction Exposure Calculation
✓ Exposure Validation
✓ Exposure Report Generation
ExposureManager bajarmaydi.
✗ Portfolio Risk Analysis
✗ Position Size Calculation
✗ Drawdown Validation
✗ Risk Approval
✗ Trade Execution
✗ Decision Making
---
# Module Boundary
```text
DrawdownManager
↓
ExposureManager
↓
PortfolioManager
```
---
# Input Contract
• Drawdown Context
• Open Positions
• Pending Orders
• Current Trade
• Exposure Policy
---
# Output Contract
• Exposure Report
• Exposure Status
• Exposure Context
• Exposure Metadata
---
# Allowed Dependencies
✓ DrawdownManager
✓ PortfolioManager
---
# Forbidden Dependencies
✗ RiskValidator
✗ Execution Layer
✗ Decision Layer
✗ Database Layer
✗ Platform Layer
---
# Runtime Contract
1. Barcha Open Positionlar hisobga olinishi shart.
2. Pending Orderlar Exposure hisobiga qo'shilishi shart.
3. Symbol Exposure tekshirilishi shart.
4. Direction Exposure tekshirilishi shart.
5. Exposure Policy buzilsa LIMIT_REACHED yoki BLOCKED holati yaratilishi shart.
6. Exposure Report PortfolioManager'ga uzatilishi shart.
7. ExposureManager Risk Approval bermaydi.
8. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Open Positionlar tahlil qilinadi.
✓ Pending Orderlar hisobga olinadi.
✓ Exposure hisoblanadi.
✓ Exposure limitlari tekshiriladi.
✓ Exposure Report yaratiladi.
✓ PortfolioManager'ga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
ExposureManager Contract GoldBot Risk Layer ichidagi Market Exposure nazorati, Symbol va Direction Exposure hisoblash, Exposure Report yaratish hamda PortfolioManager moduliga standart Exposure Context uzatishni belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
