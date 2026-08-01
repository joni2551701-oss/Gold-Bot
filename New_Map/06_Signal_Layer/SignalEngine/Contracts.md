# Signal Engine Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat SignalEngine modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
SignalEngine quyidagilar uchun javobgar.
✓ Signal Pipeline Management
✓ Signal Generation
✓ Signal Validation
✓ Signal Scoring
✓ Signal Formatting
✓ Signal Lifecycle Management
✓ Signal Result Generation
SignalEngine bajarmaydi.
✗ Market Analysis
✗ Context Analysis
✗ Indicator Calculation
✗ Strategy Analysis
✗ AI Analysis
✗ Decision Making
✗ Risk Calculation
✗ Trade Execution
---
# Module Boundary
```text
Strategy Layer
↓
SignalEngine
↓
Signal Service
```
---
# Input Contract
• Strategy Result
• Technical Confluence
• Strategy Metadata
---
# Output Contract
• Signal Result
• Technical Score
• Technical Confidence
• Signal Metadata
---
# Allowed Dependencies
✓ ConfluenceEngine
✓ SignalBuilder
✓ SignalValidator
✓ SignalScoring
✓ SignalFormatter
✓ Event System
---
# Forbidden Dependencies
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Platform Layer
---
# Runtime Contract
1. Strategy Result mavjud bo'lishi shart.
2. Confluence mavjud bo'lishi shart.
3. Validation majburiy.
4. Signal Result immutable bo'lishi kerak.
5. AI ishlatilmaydi.
6. Decision qabul qilinmaydi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Signal muvaffaqiyatli yaratiladi.
✓ Validation bajariladi.
✓ Score hisoblanadi.
✓ Signal formatlanadi.
✓ Signal Result SignalService'ga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
SignalEngine Contract GoldBot Signal Layer ichidagi barcha Signal Generation jarayonini boshqaruvchi rasmiy Canonical Architecture Contract hisoblanadi.
