# Validation Engine Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat ValidationEngine ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
ProviderRouter
↓
ValidationEngine
↓
LearningEngine
```
---
# Module Architecture
```text
ValidationEngine
        │
        ├── Source Validator
        ├── Fact Checker
        ├── Duplicate Detector
        ├── Confidence Evaluator
        ├── Approval Manager
        └── Validation Reporter
```
---
# Internal Components
## Source Validator
Manba ishonchliligini tekshiradi.
---
## Fact Checker
Faktlarning to'g'riligini tekshiradi.
---
## Duplicate Detector
Takroriy Knowledge'ni aniqlaydi.
---
## Confidence Evaluator
Ishonchlilik darajasini hisoblaydi.
---
## Approval Manager
Approve yoki Reject qarorini beradi.
---
## Validation Reporter
Validation hisobotini yaratadi.
---
# Allowed Dependencies
✓ ProviderRouter
✓ LearningEngine
---
# Forbidden Dependencies
✗ MemoryManager
✗ MemorySearch
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Summary
ValidationEngine GoldBot AI ichidagi Knowledge Validation jarayonini boshqaruvchi Canonical modul hisoblanadi.
