# Risk Validator Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat RiskValidator modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
RiskValidator quyidagilar uchun javobgar.
✓ Final Risk Validation
✓ Risk Policy Validation
✓ Capital Protection Validation
✓ Risk Approval Generation
✓ Risk Policy Generation
✓ Reject Reason Generation
✓ Validation Report Generation
RiskValidator bajarmaydi.
✗ Position Size Calculation
✗ Money Management
✗ Drawdown Monitoring
✗ Exposure Monitoring
✗ Portfolio Management
✗ Trade Execution
---
# Module Boundary
```text
PortfolioManager
↓
RiskValidator
↓
RiskService
```
---
# Input Contract
• Risk Context
• Position Package
• Money Report
• Drawdown Report
• Exposure Report
• Portfolio Report
---
# Output Contract
• Risk Approval
• Risk Policy
• Risk Status
• Reject Reason
• Validation Report
• Risk Metadata
---
# Allowed Dependencies
✓ PortfolioManager
✓ RiskService
---
# Forbidden Dependencies
✗ Execution Layer
✗ Decision Layer
✗ Database Layer
✗ Platform Layer
---
# Runtime Contract
1. Barcha Risk Reportlar mavjud bo'lishi shart.
2. Risk Policy to'liq tekshirilishi shart.
3. Yakuniy Risk Approval yaratilishi shart.
4. REJECT holatida Reject Reason majburiy.
5. APPROVED natijasi RiskService'ga uzatilishi shart.
6. RiskValidator Risk qiymatlarini qayta hisoblamaydi.
7. Risk Policy (Allow BE, Allow Trailing, Allow Partial Close, Max Partial %, Trailing Rules, BreakEven Rules) Risk Approval bilan birga yaratilishi shart — Trade Monitoring Layer faqat shu Policy doirasida harakat qiladi va qayta risk hisoblamaydi.
8. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Barcha Risk Reportlar qabul qilinadi.
✓ Risk Policy tekshiriladi.
✓ Risk Approval yaratiladi.
✓ Validation Report yaratiladi.
✓ Reject Reason yaratiladi (zarur bo'lsa).
✓ RiskService'ga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
RiskValidator Contract GoldBot Risk Layer ichidagi barcha Risk Assessment natijalarini yakuniy tekshirish, Risk Approval yaratish va Execution Layer oldidan RiskService orqali standart Validation Report uzatishni belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
