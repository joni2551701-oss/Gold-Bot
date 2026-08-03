# Position Sizing Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat PositionSizing modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
PositionSizing quyidagilar uchun javobgar.
✓ Risk Amount Calculation
✓ Position Size Calculation
✓ Lot Size Calculation
✓ Symbol Volume Validation
✓ Position Package Generation
✓ Position Metadata
PositionSizing bajarmaydi.
✗ Money Management
✗ Drawdown Validation
✗ Exposure Validation
✗ Risk Approval
✗ Trade Execution
✗ Portfolio Management
---
# Module Boundary
```text
RiskEngine
↓
PositionSizing
↓
MoneyManagement
```
---
# Input Contract
• Risk Package
• Account Balance
• Risk %
• Entry Price
• Stop Loss
• Symbol Specification
---
# Output Contract
• Position Size
• Lot Size
• Risk Amount
• Position Package
• Position Metadata
---
# Allowed Dependencies
✓ RiskEngine
✓ MoneyManagement
---
# Forbidden Dependencies
✗ DrawdownManager
✗ ExposureManager
✗ PortfolioManager
✗ Decision Layer
✗ Execution Layer
✗ Database Layer
✗ Platform Layer
---
# Runtime Contract
1. Risk Amount hisoblanishi shart.
2. Position Size hisoblanishi shart.
3. Lot Size broker qoidalariga mos bo'lishi shart.
4. Min Lot va Max Lot tekshirilishi shart.
5. Volume Step tekshirilishi shart.
6. Position Package MoneyManagement'ga uzatilishi shart.
7. PositionSizing Risk Approval bermaydi.
8. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Risk Amount hisoblanadi.
✓ Position Size hisoblanadi.
✓ Lot Size hisoblanadi.
✓ Broker limitlari tekshiriladi.
✓ Position Package yaratiladi.
✓ MoneyManagement'ga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
PositionSizing Contract GoldBot Risk Layer ichidagi Position Size va Lot Size hisoblash, broker cheklovlarini tekshirish hamda MoneyManagement moduliga standart Position Package uzatishni belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
