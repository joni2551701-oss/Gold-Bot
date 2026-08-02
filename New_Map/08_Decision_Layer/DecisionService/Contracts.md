# Decision Service Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat DecisionService modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
DecisionService quyidagilar uchun javobgar.
✓ Public Entry Point (AI Layer'dan Decision Layer'ga kirish)
✓ Public Exit Point (Decision Layer'dan Risk Layer'ga chiqish)
✓ Request Validation
✓ Response Serialization
✓ Session Management
✓ API Boundary Enforcement
DecisionService bajarmaydi.
✗ Decision Making
✗ Rule Validation
✗ Approval
✗ Confidence Calculation
✗ Logging
✗ Trade Execution
✗ Database Management
---
# Module Boundary
```text
AI Layer
↓
DecisionService (Entry)
↓
DecisionConfidence
↓
RuleEngine
↓
ApprovalEngine
↓
DecisionEngine
↓
DecisionLogger
↓
DecisionService (Exit)
↓
Risk Layer
```
---
# Input Contract
Kirish tomonida (AI Layer'dan):
• Decision Request
• Signal Package
• AI Package
• Session Metadata

Chiqish tomonida (DecisionLogger'dan):
• Logged Final Decision
---
# Output Contract
Kirish tomonida (DecisionConfidence'ga):
• Validated Decision Request

Chiqish tomonida (Risk Layer'ga):
• Decision Response
• Standard Response
• Decision Metadata
---
# Allowed Dependencies
✓ DecisionConfidence
✓ DecisionLogger
---
# Forbidden Dependencies
✗ RuleEngine (to'g'ridan-to'g'ri)
✗ ApprovalEngine (to'g'ridan-to'g'ri)
✗ DecisionEngine (to'g'ridan-to'g'ri)
✗ Risk Layer'dan boshqa tashqi Layer
✗ Execution Layer
✗ Database Layer
---
# Runtime Contract
1. Decision Layer'ga barcha kirish va chiqishlar DecisionService orqali amalga oshirilishi shart (Boundary Gateway).
2. Har bir kirish Request Validation'dan o'tishi shart.
3. DecisionService Decision yaratmaydi — faqat Entry/Exit Boundary vazifasini bajaradi.
4. Decision javobi standart formatga o'tkazilishi shart.
5. DecisionLogger Layer tashqarisiga chiqmaydi — faqat DecisionService orqali chiqadi.
6. Session holati boshqarilishi shart.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ AI Layer'dan Request qabul qilinadi.
✓ Validation bajariladi.
✓ DecisionConfidence'ga uzatiladi.
✓ DecisionLogger'dan yakuniy natija qabul qilinadi.
✓ Response standartlashtiriladi.
✓ Risk Layer'ga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
DecisionService Contract GoldBot Decision Layer uchun ikki tomonlama (bidirectional) Boundary Gateway sifatida ishlashini — AI Layer'dan kirish va Risk Layer'ga chiqishni — belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
