# Fundamental AI Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat FundamentalAI modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
FundamentalAI quyidagilar uchun javobgar.
✓ News Analysis
✓ Sentiment Analysis
✓ Economic Calendar Analysis
✓ Correlation Analysis
✓ Fundamental Context Generation
✓ Fundamental Risk Detection
FundamentalAI bajarmaydi.
✗ Technical Analysis
✗ Indicator Calculation
✗ Strategy
✗ Signal Generation
✗ Decision Making
✗ Risk Calculation
✗ Trade Execution
---
# Module Boundary
```text
AIEngine
↓
FundamentalAI
↓
AICoordinator
```
---
# Input Contract
• Signal Result
• Market Context
• News Data
• Economic Events
• Sentiment Data
---
# Output Contract
• Fundamental Context
• News Summary
• Sentiment Result
• Event Impact
• Correlation Result
• Fundamental Risk
---
# Allowed Dependencies
✓ NewsAI
✓ SentimentAI
✓ EconomicCalendarAI
✓ CorrelationAI
✓ AIEngine
✓ AICoordinator
---
# Forbidden Dependencies
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Platform Layer
---
# Runtime Contract
1. FundamentalAI faqat fundamental ma'lumotlarni tahlil qiladi.
2. Technical Signal o'zgartirilmaydi.
3. Har bir modul mustaqil ishlaydi.
4. Natijalar yagona Fundamental Context'ga birlashtiriladi.
5. AI yakuniy Decision qabul qilmaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ News tahlil qilinadi.
✓ Sentiment hisoblanadi.
✓ Economic Calendar tekshiriladi.
✓ Correlation aniqlanadi.
✓ Fundamental Context yaratiladi.
✓ Natijalar AICoordinator'ga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
FundamentalAI Contract GoldBot AI Layer ichidagi barcha fundamental tahlillarni yagona Fundamental Context obyektiga birlashtiruvchi rasmiy Canonical Architecture Contract hisoblanadi.
