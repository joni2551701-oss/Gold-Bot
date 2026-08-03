# Sentiment AI Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat SentimentAI ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
Market Data
↓
SentimentAI
↓
FundamentalAI
```
---
# Module Architecture
```text
SentimentAI
        │
        ├── Sentiment Collector
        ├── Sentiment Analyzer
        ├── Bias Detector
        ├── Confidence Evaluator
        ├── Risk Evaluator
        └── Context Builder
```
---
# Internal Components
## Sentiment Collector
Sentiment ma'lumotlarini yig'adi.
---
## Sentiment Analyzer
Bozor kayfiyatini tahlil qiladi.
---
## Bias Detector
Bullish, Bearish yoki Neutral holatini aniqlaydi.
---
## Confidence Evaluator
Sentiment ishonchliligini baholaydi.
---
## Risk Evaluator
Sentiment xavfini baholaydi.
---
## Context Builder
Sentiment Context yaratadi.
---
# Allowed Dependencies
✓ FundamentalAI
✓ NewsAI
---
# Forbidden Dependencies
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Platform Layer
---
# Summary
SentimentAI GoldBot AI Layer ichidagi Market Sentiment Analysis jarayonlarini boshqaruvchi Canonical modul hisoblanadi.
