# Sentiment AI Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat SentimentAI modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
SentimentAI quyidagilar uchun javobgar.
✓ Market Sentiment Analysis
✓ Bullish/Bearish Detection
✓ Confidence Evaluation
✓ Sentiment Risk Detection
✓ Sentiment Context Generation
SentimentAI bajarmaydi.
✗ Technical Analysis
✗ News Collection
✗ Signal Generation
✗ Decision Making
✗ Risk Calculation
✗ Trade Execution
---
# Module Boundary
```text
Market Data
↓
SentimentAI
↓
FundamentalAI
```
---
# Input Contract
• Market Data
• News Context
• Social Sentiment
• Symbol
---
# Output Contract
• Sentiment Context
• Market Bias
• Confidence Level
• Sentiment Risk
• Sentiment Metadata
---
# Allowed Dependencies
✓ NewsAI
✓ FundamentalAI
---
# Forbidden Dependencies
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Platform Layer
---
# Runtime Contract
1. Sentiment har doim qayta hisoblanishi kerak.
2. Market Bias aniqlanishi shart.
3. Confidence baholanishi shart.
4. Sentiment Context yaratilishi shart.
5. Technical Signal o'zgartirilmaydi.
6. SentimentAI Signal yaratmaydi.
7. SentimentAI Decision qabul qilmaydi.
8. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Sentiment hisoblanadi.
✓ Market Bias aniqlanadi.
✓ Confidence baholanadi.
✓ Sentiment Risk aniqlanadi.
✓ Sentiment Context yaratiladi.
✓ FundamentalAI'ga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
SentimentAI Contract GoldBot AI Layer ichidagi Market Sentiment Intelligence modulining rasmiy Canonical Architecture Contract hisoblanadi.
