# News AI Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat NewsAI modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
NewsAI quyidagilar uchun javobgar.
✓ News Collection
✓ News Filtering
✓ News Classification
✓ News Impact Analysis
✓ News Summarization
✓ News Context Generation
NewsAI bajarmaydi.
✗ Technical Analysis
✗ Sentiment Analysis
✗ Economic Calendar Analysis
✗ Signal Generation
✗ Decision Making
✗ Risk Calculation
✗ Trade Execution
---
# Module Boundary
```text
ProviderRouter
↓
NewsAI
↓
FundamentalAI
```
---
# Input Contract
• News Feed
• Market Symbol
• User Context
---
# Output Contract
• News Context
• News Summary
• Impact Level
• News Metadata
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
# Runtime Contract
1. News ishonchli manbalardan olinishi kerak.
2. Har bir News filtrlanishi shart.
3. Har bir News Impact baholanishi shart.
4. News Summary yaratilishi shart.
5. News Context FundamentalAI'ga uzatilishi shart.
6. NewsAI Signal yaratmaydi.
7. NewsAI Decision qabul qilmaydi.
8. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ News muvaffaqiyatli yig'iladi.
✓ News filtrlanadi.
✓ News kategoriyalanadi.
✓ Impact aniqlanadi.
✓ Summary yaratiladi.
✓ News Context FundamentalAI'ga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
NewsAI Contract GoldBot AI Layer ichidagi yangiliklarni yig'ish, tahlil qilish va yagona News Context yaratishni boshqaruvchi rasmiy Canonical Architecture Contract hisoblanadi.
