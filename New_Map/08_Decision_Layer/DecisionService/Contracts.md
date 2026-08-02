# Decision Service Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat DecisionService modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
DecisionService quyidagilar uchun javobgar.
✓ Decision Request Management
✓ Request Validation
✓ Decision Layer Gateway
✓ Session Management
✓ Response Formatting
✓ Service Monitoring
DecisionService bajarmaydi.
✗ Decision Making
✗ Rule Validation
✗ Confidence Calculation
✗ Trade Execution
✗ Database Management
✗ Logging
---
# Module Boundary
```text
External Layers
↓
DecisionService
↓
DecisionEngine
↓
DecisionLogger
↓
Risk Layer
```
---
# Input Contract
• Decision Request
• Signal Package
• AI Package
• Session Metadata
---
# Output Contract
• Decision Response
• Standard Response
• Decision Metadata
• Service Metadata
---
# Allowed Dependencies
✓ DecisionEngine
✓ DecisionLogger
---
# Forbidden Dependencies
✗ RuleEngine
✗ Risk Layer
✗ Execution Layer
✗ Database Layer
---
# Runtime Contract
1. Decision Layer'ga barcha kirishlar DecisionService orqali amalga oshirilishi shart.
2. Har bir Request Validation'dan o'tishi shart.
3. DecisionService Decision yaratmaydi.
4. Decision javobi standart formatga o'tkazilishi shart.
5. Session holati boshqarilishi shart.
6. Service Monitoring doimiy ishlashi shart.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Request qabul qilinadi.
✓ Validation bajariladi.
✓ DecisionEngine'ga uzatiladi.
✓ DecisionLogger Logging bajaradi.
✓ Response standartlashtiriladi.
✓ Risk Layer'ga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
DecisionService Contract GoldBot Decision Layer uchun yagona Public Interface va Service Gateway sifatida ishlashni, barcha Decision so'rovlarini boshqarishni va standart javoblarni Risk Layer hamda boshqa tashqi qatlamlarga uzatishni belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
