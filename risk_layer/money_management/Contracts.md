# Money Management Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat MoneyManagement modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
MoneyManagement quyidagilar uchun javobgar.
✓ Capital Allocation
✓ Risk Policy Validation
✓ Daily Risk Control
✓ Weekly Risk Control
✓ Monthly Risk Control
✓ Money Report Generation
MoneyManagement bajarmaydi.
✗ Position Size Calculation
✗ Drawdown Validation
✗ Exposure Validation
✗ Portfolio Validation
✗ Risk Approval
✗ Trade Execution
---
# Module Boundary
```text
PositionSizing
↓
MoneyManagement
↓
DrawdownManager
```
---
# Input Contract
• Position Package
• Account Balance
• Risk Policy
• Daily Statistics
• Weekly Statistics
• Monthly Statistics
---
# Output Contract
• Capital Allocation
• Money Report
• Money Context
• Money Metadata
---
# Allowed Dependencies
✓ PositionSizing
✓ DrawdownManager
---
# Forbidden Dependencies
✗ ExposureManager
✗ PortfolioManager
✗ Execution Layer
✗ Decision Layer
✗ Database Layer
✗ Platform Layer
---
# Runtime Contract
1. Risk Policy tekshirilishi shart.
2. Daily Risk hisoblanishi shart.
3. Weekly Risk hisoblanishi shart.
4. Monthly Risk hisoblanishi shart.
5. Capital Allocation yaratilishi shart.
6. MoneyManagement Risk Approval bermaydi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Position Package qabul qilinadi.
✓ Risk Policy tekshiriladi.
✓ Daily, Weekly va Monthly Risk hisoblanadi.
✓ Capital Allocation yaratiladi.
✓ Money Report yaratiladi.
✓ DrawdownManager'ga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
MoneyManagement Contract GoldBot Risk Layer ichidagi Capital Allocation va Risk Policy boshqaruvi, kunlik, haftalik va oylik risk nazorati hamda DrawdownManager moduliga standart Money Context uzatishni belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
