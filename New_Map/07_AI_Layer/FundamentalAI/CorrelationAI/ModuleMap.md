# Correlation AI Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat CorrelationAI ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
Market Data
↓
CorrelationAI
↓
FundamentalAI
```
---
# Module Architecture
```text
CorrelationAI
        │
        ├── Asset Loader
        ├── Correlation Calculator
        ├── Strength Evaluator
        ├── Risk Analyzer
        ├── Related Asset Detector
        └── Context Builder
```
---
# Internal Components
## Asset Loader
Kerakli aktivlarni yuklaydi.
---
## Correlation Calculator
Aktivlar orasidagi Correlation koeffitsientini hisoblaydi.
---
## Strength Evaluator
Correlation kuchini baholaydi.
---
## Risk Analyzer
Correlation bilan bog'liq xavflarni aniqlaydi.
---
## Related Asset Detector
O'zaro bog'liq instrumentlarni aniqlaydi.
---
## Context Builder
Correlation Context yaratadi.
---
# Allowed Dependencies
✓ FundamentalAI
---
# Forbidden Dependencies
✗ NewsAI
✗ SentimentAI
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Platform Layer
---
# Summary
CorrelationAI aktivlar o'rtasidagi bog'liqlikni tahlil qiluvchi va Correlation Context yaratuvchi Canonical modul hisoblanadi.
