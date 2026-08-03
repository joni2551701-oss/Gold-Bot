# Economic Calendar AI Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat EconomicCalendarAI ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
Calendar Provider
↓
EconomicCalendarAI
↓
FundamentalAI
```
---
# Module Architecture
```text
EconomicCalendarAI
        │
        ├── Calendar Loader
        ├── Event Filter
        ├── Impact Analyzer
        ├── Time Analyzer
        ├── News Lock Evaluator
        └── Context Builder
```
---
# Internal Components
## Calendar Loader
Economic Calendar ma'lumotlarini yuklaydi.
---
## Event Filter
Kerakli voqealarni saralaydi.
---
## Impact Analyzer
High / Medium / Low Impact darajasini baholaydi.
---
## Time Analyzer
Voqea vaqtini va qolgan vaqtni hisoblaydi.
---
## News Lock Evaluator
Savdoni vaqtincha cheklash tavsiyasini ishlab chiqadi.
---
## Context Builder
Economic Context yaratadi.
---
# Allowed Dependencies
✓ FundamentalAI
---
# Forbidden Dependencies
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Platform Layer
---
# Summary
EconomicCalendarAI iqtisodiy voqealarni tahlil qiluvchi va Economic Context yaratuvchi Canonical modul hisoblanadi.
