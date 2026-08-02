# Fundamental AI Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat FundamentalAI Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu Canonical Runtime Blueprint hisoblanadi.
---
# Runtime Sequence
```text
AIEngine
↓
FundamentalAI
↓
NewsAI
↓
SentimentAI
↓
EconomicCalendarAI
↓
CorrelationAI
↓
Fundamental Context
↓
AICoordinator
```
---
# Runtime Rules
1. News mavjud bo'lsa tahlil qilinadi.
2. Economic Calendar tekshiriladi.
3. Sentiment hisoblanadi.
4. Correlation tekshiriladi.
5. Natijalar yagona Fundamental Context'ga birlashtiriladi.
---
# State Flow
```text
Idle
↓
Receiving
↓
Analyzing
↓
Aggregating
↓
Completed
or
Failed
```
---
# Summary
AIEngine
↓
FundamentalAI
↓
Fundamental Context
↓
AICoordinator
