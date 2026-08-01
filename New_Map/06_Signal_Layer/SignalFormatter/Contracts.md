# Signal Formatter Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat SignalFormatter modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
SignalFormatter quyidagilar uchun javobgar.
✓ Signal Formatting
✓ Metadata Formatting
✓ Standard Signal Model Generation
✓ Output Normalization
✓ Layer Compatibility
✓ Formatted Signal Generation
SignalFormatter bajarmaydi.
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
SignalScoring
↓
SignalFormatter
↓
SignalService
```
---
# Input Contract
• Signal Result
• Technical Score
• Technical Confidence
• Signal Metadata
---
# Output Contract
• Standard Signal Model
• Formatted Signal
• Formatted Metadata
---
# Allowed Dependencies
✓ SignalScoring
✓ Signal Model
---
# Forbidden Dependencies
✗ SignalService
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Platform Layer
---
# Runtime Contract
1. Signal Result mavjud bo'lishi shart.
2. Signal mazmuni o'zgartirilmaydi.
3. Faqat format o'zgartiriladi.
4. Standard Signal Model yaratilishi shart.
5. Formatting deterministik bo'lishi kerak.
6. Signal Result immutable bo'lishi kerak.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Signal standart formatga o'tkaziladi.
✓ Metadata formatlanadi.
✓ Standard Signal Model yaratiladi.
✓ Formatted Signal SignalService'ga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
SignalFormatter Contract GoldBot Signal Layer ichidagi barcha Signal Result obyektlarini yagona standart formatga o'tkazuvchi rasmiy Canonical Architecture Contract hisoblanadi.
