# Risk Service Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat RiskService modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
RiskService quyidagilar uchun javobgar.
✓ Risk Request Management
✓ Request Validation
✓ Risk Layer Gateway
✓ Session Management
✓ Response Formatting
✓ Service Monitoring
RiskService bajarmaydi.
✗ Risk Calculation
✗ Position Size Calculation
✗ Risk Validation
✗ Trade Execution
✗ Database Management
✗ Logging
---
# Module Boundary
```text
Decision Layer
↓
RiskService
↓
RiskEngine
↓
RiskValidator
↓
Execution Layer
```
---
# Input Contract
• Decision Package
• Risk Request
• Session Metadata
---
# Output Contract
• Risk Response
• Standard Response
• Risk Approval
• Service Metadata
---
# Allowed Dependencies
✓ RiskEngine
✓ RiskValidator
---
# Forbidden Dependencies
✗ Execution Layer
✗ Database Layer
✗ Platform Layer
✗ DecisionEngine
---
# Runtime Contract
1. Risk Layer'ga barcha kirishlar RiskService orqali amalga oshirilishi shart.
2. Har bir Request Validation'dan o'tishi shart.
3. RiskService Risk hisoblamaydi.
4. Risk javobi standart formatda qaytarilishi shart.
5. Session holati boshqarilishi shart.
6. Risk Approval Execution Layer'ga uzatilishi shart.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Request qabul qilinadi.
✓ Validation bajariladi.
✓ RiskEngine ishga tushiriladi.
✓ RiskValidator natijasi olinadi.
✓ Response standartlashtiriladi.
✓ Execution Layer'ga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
RiskService Contract GoldBot Risk Layer uchun yagona Public Interface va Service Gateway sifatida ishlashni, barcha Risk so'rovlarini boshqarishni, Risk Approval natijalarini standart formatga o'tkazishni va Execution Layer'ga uzatishni belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
