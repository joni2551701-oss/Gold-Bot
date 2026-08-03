# Fundamental AI Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat FundamentalAI ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
AIEngine
↓
FundamentalAI
↓
AICoordinator
```
---
# Module Architecture
```text
FundamentalAI
        │
        ├── NewsAI
        ├── SentimentAI
        ├── EconomicCalendarAI
        ├── CorrelationAI
        ├── Context Builder
        └── Risk Evaluator
```
---
# Internal Components
## NewsAI
Yangiliklarni tahlil qiladi.
---
## SentimentAI
Bozor kayfiyatini aniqlaydi.
---
## EconomicCalendarAI
Muhim iqtisodiy voqealarni baholaydi.
---
## CorrelationAI
Bozorlar o'rtasidagi bog'liqlikni tahlil qiladi.
---
## Context Builder
Fundamental Context yaratadi.
---
## Risk Evaluator
Fundamental xavfni baholaydi.
---
# Allowed Dependencies
✓ AIEngine
✓ AICoordinator
✓ NewsAI
✓ SentimentAI
✓ EconomicCalendarAI
✓ CorrelationAI
---
# Forbidden Dependencies
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Platform Layer
---
# Summary
FundamentalAI GoldBot AI Layer ichidagi barcha Fundamental Analysis modullarini boshqaruvchi Canonical modul hisoblanadi.
