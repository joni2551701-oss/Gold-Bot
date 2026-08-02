# Risk Engine Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat RiskEngine modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
RiskEngine quyidagilar uchun javobgar.
✓ Risk Assessment
✓ Risk Context Generation
✓ Account Evaluation
✓ Risk Package Generation
✓ Risk Report
✓ Risk Metadata
RiskEngine bajarmaydi.
✗ Final Decision
✗ Position Size Calculation
✗ Money Management
✗ Trade Execution
✗ Portfolio Management
✗ Position Monitoring
---
# Module Boundary
```text
RiskService
↓
RiskEngine
↓
PositionSizing
```
---
# Input Contract
• Validated Risk Request
• Account Information
• Market Context
• Symbol Information
• Risk Preferences
---
# Output Contract
• Risk Package
• Risk Context
• Risk Report
• Risk Metadata
---
# Allowed Dependencies
✓ RiskService
✓ PositionSizing
✓ MoneyManagement
---
# Forbidden Dependencies
✗ Decision Layer
✗ Execution Layer
✗ Database Layer
✗ Platform Layer
---
# Runtime Contract
1. Faqat RiskService orqali kelgan Validated Risk Request qabul qilinadi.
2. Account Information tekshirilishi shart.
3. Risk Context yaratilishi shart.
4. Risk Package standart formatda yaratilishi shart.
5. RiskEngine Lot Size hisoblamaydi.
6. RiskEngine Decision yaratmaydi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Validated Risk Request qabul qilinadi.
✓ Account tekshiriladi.
✓ Risk Context yaratiladi.
✓ Risk Report yaratiladi.
✓ Risk Package PositionSizing'ga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
RiskEngine Contract GoldBot Risk Layer ichidagi barcha Risk Assessment jarayonlarini boshqarish, Risk Context va Risk Package yaratish hamda ularni PositionSizing moduliga uzatishni belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
