# News AI Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat NewsAI ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
ProviderRouter
↓
NewsAI
↓
FundamentalAI
```
---
# Module Architecture
```text
NewsAI
        │
        ├── News Collector
        ├── News Filter
        ├── News Classifier
        ├── Impact Analyzer
        ├── Summary Generator
        └── Context Builder
```
---
# Internal Components
## News Collector
Yangiliklarni yig'adi.
---
## News Filter
Keraksiz yangiliklarni chiqarib tashlaydi.
---
## News Classifier
Yangiliklarni kategoriyalarga ajratadi.
---
## Impact Analyzer
Yangilikning bozorga ta'sirini baholaydi.
---
## Summary Generator
Qisqacha xulosa yaratadi.
---
## Context Builder
News Context yaratadi.
---
# Allowed Dependencies
✓ ProviderRouter
✓ FundamentalAI
---
# Forbidden Dependencies
✗ SentimentAI
✗ EconomicCalendarAI
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Platform Layer
---
# Summary
NewsAI GoldBot AI Layer ichidagi barcha News Analysis jarayonlarini boshqaruvchi Canonical modul hisoblanadi.
