# Decision Engine Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat DecisionEngine ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
ApprovalEngine
↓
DecisionEngine
↓
DecisionLogger
```
---
# Module Architecture
```text
DecisionEngine
        │
        ├── Input Validator
        ├── Decision Aggregator
        ├── Decision Builder
        ├── Decision Status Manager
        ├── Context Builder
        └── Metadata Generator
```
---
# Internal Components
## Input Validator
Barcha kiruvchi ma'lumotlarni tekshiradi.
---
## Decision Aggregator
Signal, AI va Rule natijalarini birlashtiradi.
---
## Decision Builder
Yakuniy Decision yaratadi.
---
## Decision Status Manager
APPROVE, REJECT, HOLD yoki WAIT holatini belgilaydi.
---
## Context Builder
Decision Context yaratadi.
---
## Metadata Generator
Decision Metadata yaratadi.
---
# Allowed Dependencies
✓ ApprovalEngine
✓ DecisionConfidence
✓ RuleEngine
✓ DecisionLogger
---
# Forbidden Dependencies
✗ Risk Layer
✗ Execution Layer
✗ Database Layer
✗ Platform Layer
---
# Summary
DecisionEngine GoldBot ichidagi Final Decision Pipeline'ni boshqaruvchi Canonical modul hisoblanadi.
