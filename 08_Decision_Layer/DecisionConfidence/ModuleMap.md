# Decision Confidence Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat DecisionConfidence ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
AI Layer
↓
DecisionConfidence
↓
RuleEngine
```
---
# Module Architecture
```text
DecisionConfidence
        │
        ├── Technical Evaluator
        ├── AI Confidence Integrator
        ├── Signal Quality Evaluator
        ├── Context Evaluator
        ├── Confidence Calculator
        └── Confidence Report Builder
```
---
# Internal Components
## Technical Evaluator
Technical Analysis sifatini baholaydi.
---
## AI Confidence Integrator
AI Layer'dan kelgan Confidence Score'ni integratsiya qiladi.
---
## Signal Quality Evaluator
Signal sifatini baholaydi.
---
## Context Evaluator
Market va AI Context sifatini tekshiradi.
---
## Confidence Calculator
Yakuniy Decision Confidence hisoblaydi.
---
## Confidence Report Builder
Confidence Report yaratadi.
---
# Allowed Dependencies
✓ Signal Layer
✓ AI Layer
✓ RuleEngine
---
# Forbidden Dependencies
✗ ApprovalEngine
✗ DecisionEngine
✗ Risk Layer
✗ Execution Layer
---
# Summary
DecisionConfidence GoldBot ichidagi barcha baholash natijalaridan yakuniy Decision Confidence Score hisoblovchi Canonical modul hisoblanadi.
