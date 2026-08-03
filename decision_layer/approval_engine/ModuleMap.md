# Approval Engine Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat ApprovalEngine ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
DecisionConfidence
↓
RuleEngine
↓
ApprovalEngine
↓
DecisionEngine
```
---
# Module Architecture
```text
ApprovalEngine
        │
        ├── Rule Validator
        ├── Confidence Validator
        ├── Approval Evaluator
        ├── Reject Reason Builder
        ├── Approval Context Builder
        └── Metadata Generator
```
---
# Internal Components
## Rule Validator
RuleEngine natijalarini tekshiradi.
---
## Confidence Validator
Decision Confidence qiymatini tekshiradi.
---
## Approval Evaluator
APPROVED, REJECTED, HOLD yoki WAIT holatini belgilaydi.
---
## Reject Reason Builder
Rad etish sabablarini yaratadi.
---
## Approval Context Builder
Approval Context yaratadi.
---
## Metadata Generator
Approval Metadata yaratadi.
---
# Allowed Dependencies
✓ RuleEngine
✓ DecisionConfidence
✓ DecisionEngine
---
# Forbidden Dependencies
✗ Risk Layer
✗ Execution Layer
✗ Database Layer
✗ Platform Layer
---
# Summary
ApprovalEngine GoldBot Decision Layer ichidagi Trade Approval jarayonini boshqaruvchi Canonical modul hisoblanadi.
