# Confluence Engine Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat ConfluenceEngine modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
ConfluenceEngine quyidagilar uchun javobgar.
✓ Context Aggregation
✓ Indicator Aggregation
✓ Strategy Aggregation
✓ Technical Alignment
✓ Confluence Validation
✓ Technical Confluence Generation
ConfluenceEngine bajarmaydi.
✗ Signal Generation
✗ Signal Validation
✗ Signal Scoring
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
Context Layer
↓
Indicator Layer
↓
ConfluenceEngine
↓
SignalBuilder
```
---
# Input Contract
• Market Context
• Indicator Context
• Strategy Result
• Technical Metadata
---
# Output Contract
• Technical Confluence
• Confluence Score
• Confluence Metadata
---
# Allowed Dependencies
✓ SignalEngine
✓ Context Layer
✓ Indicator Layer
✓ Strategy Layer
✓ Event System
---
# Forbidden Dependencies
✗ SignalBuilder
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Platform Layer
---
# Runtime Contract
1. Context mavjud bo'lishi shart.
2. Indicator Context mavjud bo'lishi shart.
3. Strategy Result mavjud bo'lishi shart.
4. Alignment Validation majburiy.
5. Technical Confluence immutable bo'lishi kerak.
6. AI ishlatilmaydi.
7. Decision qabul qilinmaydi.
8. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Context yig'iladi.
✓ Indicator natijalari yig'iladi.
✓ Strategy Result qo'shiladi.
✓ Technical Alignment tekshiriladi.
✓ Technical Confluence yaratiladi.
✓ SignalBuilder'ga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
ConfluenceEngine Contract GoldBot Signal Layer ichidagi barcha texnik faktorlarni yagona Technical Confluence obyektiga birlashtiruvchi rasmiy Canonical Architecture Contract hisoblanadi.
