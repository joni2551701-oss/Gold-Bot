# Risk Layer Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat Risk Layer uchun rasmiy Architecture Contract hisoblanadi.
---
# Layer Responsibility
Risk Layer quyidagilar uchun javobgar.
✓ Risk Assessment
✓ Position Size Calculation
✓ Money Management
✓ Drawdown Protection
✓ Exposure Control
✓ Portfolio Risk Management
✓ Final Risk Validation
✓ Risk Approval
---
# Layer Does NOT
✗ Signal Generation
✗ AI Analysis
✗ Decision Making
✗ Market Analysis
✗ Order Execution
✗ Position Monitoring
---
# Input Contract
Risk Layer qabul qiladi.
• Decision Package
• Account Information
• Symbol Information
• Open Positions
• Portfolio Information
• Risk Policy
---
# Output Contract
Risk Layer yaratadi.
• Risk Approval
• Position Size
• Lot Size
• Risk Report
• Portfolio Report
• Risk Metadata
---
# Layer Pipeline
```text
RiskService
↓
RiskEngine
↓
PositionSizing
↓
MoneyManagement
↓
DrawdownManager
↓
ExposureManager
↓
PortfolioManager
↓
RiskValidator
↓
Execution Layer
```
---
# Layer Rules
1. Decision APPROVED bo'lmasa Risk Layer ishlamaydi.
2. RiskEngine Risk Pipeline'ni boshlaydi.
3. PositionSizing Lot Size hisoblaydi.
4. MoneyManagement Capital Allocation'ni tekshiradi.
5. DrawdownManager Drawdown limitlarini nazorat qiladi.
6. ExposureManager Exposure limitlarini tekshiradi.
7. PortfolioManager umumiy Portfolio Risk'ni baholaydi.
8. RiskValidator yakuniy Risk Approval yaratadi.
9. Execution Layer faqat APPROVED Risk natijasini qabul qiladi.
10. Barcha tashqi aloqalar RiskService orqali amalga oshiriladi.
11. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Decision Package qabul qilinadi.
✓ Risk Assessment bajariladi.
✓ Position Size hisoblanadi.
✓ Money Management tekshiriladi.
✓ Drawdown tekshiriladi.
✓ Exposure tekshiriladi.
✓ Portfolio Risk baholanadi.
✓ Risk Approval yaratiladi.
✓ Execution Layer'ga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
Risk Layer Contract GoldBot arxitekturasidagi Canonical Capital Protection qatlami sifatida ishlashini, barcha Risk modullarini ketma-ket boshqarishini, yakuniy Risk Approval yaratishini va faqat xavfsiz Trade'larni Execution Layer'ga uzatishini belgilovchi rasmiy Architecture Contract hisoblanadi.
