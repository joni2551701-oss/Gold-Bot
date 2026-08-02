# Risk Service Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat RiskService modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
RiskService quyidagilar uchun javobgar.
✓ Public Entry Point (Decision Layer'dan Risk Layer'ga kirish)
✓ Public Exit Point (Risk Layer'dan Execution Layer'ga chiqish)
✓ Request Validation
✓ Response Serialization
✓ Session Management
✓ API Boundary Enforcement
RiskService bajarmaydi.
✗ Risk Calculation
✗ Position Size Calculation
✗ Money Management
✗ Drawdown Monitoring
✗ Exposure Control
✗ Portfolio Analysis
✗ Risk Validation
✗ Trade Execution
✗ Database Management
---
# Module Boundary
```text
Decision Layer
↓
RiskService (Entry)
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
RiskService (Exit)
↓
Execution Layer
```
---
# Input Contract
Kirish tomonida (Decision Layer'dan):
• Decision Package
• Risk Request
• Session Metadata

Chiqish tomonida (RiskValidator'dan):
• Risk Approval
---
# Output Contract
Kirish tomonida (RiskEngine'ga):
• Validated Risk Request

Chiqish tomonida (Execution Layer'ga):
• Risk Response
• Standard Response
• Service Metadata
---
# Allowed Dependencies
✓ RiskEngine
✓ RiskValidator
---
# Forbidden Dependencies
✗ PositionSizing (to'g'ridan-to'g'ri)
✗ MoneyManagement (to'g'ridan-to'g'ri)
✗ DrawdownManager (to'g'ridan-to'g'ri)
✗ ExposureManager (to'g'ridan-to'g'ri)
✗ PortfolioManager (to'g'ridan-to'g'ri)
✗ Execution Layer'dan boshqa tashqi Layer
✗ Database Layer
✗ Platform Layer
✗ DecisionEngine
---
# Runtime Contract
1. Risk Layer'ga barcha kirish va chiqishlar RiskService orqali amalga oshirilishi shart (Boundary Gateway).
2. Har bir kirish Request Validation'dan o'tishi shart.
3. RiskService Risk hisoblamaydi — faqat Entry/Exit Boundary vazifasini bajaradi.
4. Risk javobi standart formatda qaytarilishi shart.
5. RiskValidator Layer tashqarisiga chiqmaydi — faqat RiskService orqali chiqadi.
6. Session holati boshqarilishi shart.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Decision Layer'dan Request qabul qilinadi.
✓ Validation bajariladi.
✓ RiskEngine'ga uzatiladi.
✓ RiskValidator'dan Risk Approval qabul qilinadi.
✓ Response standartlashtiriladi.
✓ Execution Layer'ga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
RiskService Contract GoldBot Risk Layer uchun ikki tomonlama (bidirectional) Boundary Gateway sifatida ishlashini — Decision Layer'dan kirish va Execution Layer'ga chiqishni — belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
