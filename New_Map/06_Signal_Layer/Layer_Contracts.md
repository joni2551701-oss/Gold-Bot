# Signal Layer Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat Signal Layer uchun rasmiy Architecture Contract hisoblanadi.
---
# Layer Responsibility
Signal Layer quyidagilar uchun javobgar.
✓ Technical Confluence Generation
✓ Signal Construction
✓ Signal Validation
✓ Technical Scoring
✓ Signal Formatting
✓ Signal Delivery
---
# Layer Not Responsible
✗ Context Analysis
✗ Indicator Calculation
✗ Strategy Analysis
✗ AI Analysis
✗ Decision Making
✗ Risk Calculation
✗ Trade Execution
---
# Internal Modules
✓ SignalEngine
✓ ConfluenceEngine
✓ SignalBuilder
✓ SignalValidator
✓ SignalScoring
✓ SignalFormatter
✓ SignalService
---
# Input Contract
• Market Context
• Indicator Context
• Strategy Result
• Strategy Metadata
---
# Output Contract
• Signal Result
• Signal Direction
• Entry Price
• Stop Loss
• Take Profit
• Technical Score
• Technical Confidence
• Signal Metadata
---
# Allowed Dependencies
✓ Context Layer
✓ Indicator Layer
✓ Strategy Layer
✓ Event System
---
# Forbidden Dependencies
✗ AI Layer Internal Modules
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Monitoring Layer
✗ Database Layer
✗ Platform Layer
---
# Runtime Contract
1. Context mavjud bo'lishi shart.
2. Indicator natijalari mavjud bo'lishi shart.
3. Strategy Result mavjud bo'lishi shart.
4. Technical Confluence SignalBuilder'dan oldin yaratilishi shart.
5. Validation SignalScoring'dan oldin bajarilishi shart.
6. Signal Result immutable bo'lishi kerak.
7. Signal Layer AI ishlatmaydi.
8. Signal Layer yakuniy qaror qabul qilmaydi.
9. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Technical Confluence yaratiladi.
✓ Signal Result yaratiladi.
✓ Validation muvaffaqiyatli bajariladi.
✓ Technical Score hisoblanadi.
✓ Signal formatlanadi.
✓ Signal AI Layer'ga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
Signal Layer Contract GoldBot arxitekturasidagi texnik signal ishlab chiqarish uchun yagona Canonical Architecture shartnomasi hisoblanadi.
