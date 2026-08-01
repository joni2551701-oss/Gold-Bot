# Signal Scoring Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat SignalScoring modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
SignalScoring quyidagilar uchun javobgar.
✓ Technical Score Calculation
✓ Technical Confidence Calculation
✓ Score Normalization
✓ Signal Rating Generation
✓ Quality Evaluation
✓ Score Metadata Generation
SignalScoring bajarmaydi.
✗ Signal Generation
✗ Signal Validation
✗ Signal Formatting
✗ AI Analysis
✗ Decision Making
✗ Risk Calculation
✗ Trade Execution
---
# Module Boundary
```text
Signal Validator
↓
SignalScoring
↓
Signal Formatter
```
---
# Input Contract
• Valid Signal Result
• Technical Confluence
• Validation Result
---
# Output Contract
• Technical Score
• Technical Confidence
• Signal Rating
• Score Metadata
---
# Allowed Dependencies
✓ SignalValidator
✓ ConfluenceEngine
✓ Signal Model
---
# Forbidden Dependencies
✗ SignalFormatter
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Platform Layer
---
# Runtime Contract
1. Signal Validation muvaffaqiyatli yakunlangan bo'lishi shart.
2. Technical Confluence mavjud bo'lishi shart.
3. Technical Score deterministik hisoblanishi kerak.
4. Technical Confidence Score asosida hisoblanadi.
5. Score Result immutable bo'lishi kerak.
6. AI ishlatilmaydi.
7. Decision qabul qilinmaydi.
8. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Technical Score hisoblanadi.
✓ Technical Confidence hisoblanadi.
✓ Score Normalization bajariladi.
✓ Signal Rating yaratiladi.
✓ Score Metadata yaratiladi.
✓ SignalFormatter moduliga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
SignalScoring Contract GoldBot Signal Layer ichidagi barcha Signal Result obyektlarini texnik jihatdan baholovchi va Technical Score hamda Technical Confidence yaratuvchi rasmiy Canonical Architecture Contract hisoblanadi.
