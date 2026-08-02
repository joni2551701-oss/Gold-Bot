# Signal Validator Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat SignalValidator modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
SignalValidator quyidagilar uchun javobgar.
✓ Signal Validation
✓ Field Validation
✓ Technical Rule Validation
✓ Boundary Validation
✓ Signal Integrity Validation
✓ Validation Result Generation
SignalValidator bajarmaydi.
✗ Signal Generation
✗ Signal Formatting
✗ Signal Scoring
✗ AI Analysis
✗ Decision Making
✗ Risk Calculation
✗ Trade Execution
---
# Module Boundary
```text
Signal Builder
↓
SignalValidator
↓
Signal Scoring
```
---
# Input Contract
• Signal Result
• Technical Metadata
---
# Output Contract
• Validation Result
• Validation Status
• Validation Errors
• Valid Signal Result
---
# Allowed Dependencies
✓ SignalEngine
✓ SignalBuilder
✓ Signal Model
✓ Validation Rules
---
# Forbidden Dependencies
✗ SignalScoring
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Platform Layer
---
# Runtime Contract
1. Signal Result mavjud bo'lishi shart.
2. Required Field Validation majburiy.
3. Technical Validation majburiy.
4. Validation Signal Result'ni o'zgartirmaydi.
5. Faqat Approved Signal SignalScoring moduliga uzatiladi.
6. Validation deterministik bo'lishi kerak.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Required Field tekshiriladi.
✓ Technical Rule tekshiriladi.
✓ Boundary tekshiriladi.
✓ Validation Result yaratiladi.
✓ Approved Signal SignalScoring moduliga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
SignalValidator Contract GoldBot Signal Layer ichidagi barcha Signal Result obyektlarini tekshiruvchi rasmiy Canonical Architecture Contract hisoblanadi.
