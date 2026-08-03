# Signal Validator Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat SignalValidator Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu Canonical Runtime Blueprint hisoblanadi.
---
# Runtime Sequence
```text
Signal Builder
↓
Signal Result
↓
SignalValidator
↓
Field Validation
↓
Technical Validation
↓
Integrity Validation
↓
Approve / Reject
↓
Signal Scoring
```
---
# Runtime Rules
1. Signal Result mavjud bo'lishi kerak.
2. Required Field Validation majburiy.
3. Technical Validation majburiy.
4. Validation muvaffaqiyatli bo'lsa SignalScoring ishga tushadi.
5. Circular Dependency taqiqlanadi.
---
# State Flow
```text
Idle
↓
Receiving
↓
Validating
↓
Approved
or
Rejected
```
---
# Summary
Signal Builder
↓
SignalValidator
↓
Validation Result
↓
Signal Scoring
