# Confidence AI Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat ConfidenceAI ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
AICoordinator
↓
ConfidenceAI
↓
Decision Layer
```
---
# Module Architecture
```text
ConfidenceAI
        │
        ├── Context Evaluator
        ├── Source Evaluator
        ├── Consistency Checker
        ├── Confidence Calculator
        ├── Uncertainty Analyzer
        └── Confidence Report Builder
```
---
# Internal Components
## Context Evaluator
AI Context sifatini baholaydi.
---
## Source Evaluator
Knowledge va Provider manbalarining ishonchliligini baholaydi.
---
## Consistency Checker
Turli AI Context'lar o'rtasidagi moslikni tekshiradi.
---
## Confidence Calculator
Yakuniy Confidence Score hisoblaydi.
---
## Uncertainty Analyzer
Noaniqlik darajasini aniqlaydi.
---
## Confidence Report Builder
Decision Layer uchun standart hisobot yaratadi.
---
# Allowed Dependencies
✓ AICoordinator
✓ KnowledgeAI
✓ FundamentalAI
---
# Forbidden Dependencies
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Strategy Layer
---
# Summary
ConfidenceAI AI natijalarining ishonchlilik darajasini baholovchi Canonical modul hisoblanadi.
