# Decision Service Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat DecisionService ichki arxitekturasini tavsiflaydi.
---
# Module Position
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
# Module Architecture
```text
DecisionService
        │
        ├── Request Receiver
        ├── Request Validator
        ├── Session Manager
        ├── Request Dispatcher
        ├── Response Formatter
        └── Service Monitor
```
---
# Internal Components
## Request Receiver
AI Layer'dan Decision Request'larni qabul qiladi.
---
## Request Validator
Request formatini tekshiradi.
---
## Session Manager
Decision Session holatini boshqaradi.
---
## Request Dispatcher
Request'ni DecisionConfidence'ga uzatadi.
---
## Response Formatter
DecisionLogger'dan qaytgan Decision javobini standart formatga o'tkazadi va Risk Layer'ga uzatadi.
---
## Service Monitor
Decision Service holatini kuzatadi.
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
# Summary
DecisionService GoldBot Decision Layer uchun ikki tomonlama Boundary Gateway va Public API moduli hisoblanadi.
