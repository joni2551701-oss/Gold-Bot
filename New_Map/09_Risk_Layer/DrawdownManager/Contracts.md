# Drawdown Manager Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat DrawdownManager modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
DrawdownManager quyidagilar uchun javobgar.
✓ Current Drawdown Calculation
✓ Daily Drawdown Monitoring
✓ Weekly Drawdown Monitoring
✓ Monthly Drawdown Monitoring
✓ Maximum Drawdown Validation
✓ Drawdown Report Generation
DrawdownManager bajarmaydi.
✗ Position Size Calculation
✗ Exposure Validation
✗ Portfolio Validation
✗ Risk Approval
✗ Trade Execution
✗ Decision Making
---
# Module Boundary
```text
MoneyManagement
↓
DrawdownManager
↓
ExposureManager
```
---
# Input Contract
• Money Context
• Account Balance
• Equity
• Closed PnL
• Floating PnL
• Drawdown Policy
---
# Output Contract
• Drawdown Report
• Drawdown Status
• Drawdown Context
• Drawdown Metadata
---
# Allowed Dependencies
✓ MoneyManagement
✓ ExposureManager
---
# Forbidden Dependencies
✗ PortfolioManager
✗ RiskValidator
✗ Execution Layer
✗ Decision Layer
---
# Runtime Contract
1. Current Drawdown hisoblanishi shart.
2. Daily, Weekly va Monthly Drawdown tekshirilishi shart.
3. Maximum Drawdown limiti tekshirilishi shart.
4. LIMIT_REACHED va LOCKED holatlari yaratilishi mumkin.
5. Drawdown Report ExposureManager'ga uzatilishi shart.
6. DrawdownManager Risk Approval bermaydi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Drawdown hisoblanadi.
✓ Limitlar tekshiriladi.
✓ Drawdown Status yaratiladi.
✓ Drawdown Report yaratiladi.
✓ ExposureManager'ga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
DrawdownManager Contract GoldBot Risk Layer ichidagi Drawdown Monitoring va Capital Protection qoidalarini, Drawdown Report yaratish hamda ExposureManager moduliga standart Drawdown Context uzatishni belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
