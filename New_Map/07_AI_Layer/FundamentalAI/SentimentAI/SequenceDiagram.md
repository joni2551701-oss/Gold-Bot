# Sentiment AI Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat SentimentAI Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu Canonical Runtime Blueprint hisoblanadi.
---
# Runtime Sequence
```text
Market Data
↓
SentimentAI
↓
Analyze Sentiment
↓
Detect Bias
↓
Evaluate Confidence
↓
Generate Sentiment Context
↓
FundamentalAI
```
---
# Runtime Rules
1. Market Data mavjud bo'lishi kerak.
2. Sentiment hisoblanishi shart.
3. Market Bias aniqlanishi shart.
4. Confidence baholanishi shart.
5. Sentiment Context yaratilishi shart.
---
# State Flow
```text
Idle
↓
Receiving
↓
Analyzing
↓
Evaluating
↓
Completed
or
Failed
```
---
# Summary
Market Data
↓
SentimentAI
↓
Sentiment Context
↓
FundamentalAI
