# Signal Scoring Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat SignalScoring Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu Canonical Runtime Blueprint hisoblanadi.
---
# Runtime Sequence
```text
Signal Validator
↓
Validated Signal
↓
SignalScoring
↓
Calculate Technical Score
↓
Calculate Confidence
↓
Normalize Score
↓
Generate Score Result
↓
Signal Formatter
```
---
# Runtime Rules
1. Signal Validation muvaffaqiyatli yakunlangan bo'lishi kerak.
2. Technical Confluence mavjud bo'lishi kerak.
3. Score deterministik hisoblanadi.
4. SignalFormatter faqat Score tayyor bo'lgandan keyin ishlaydi.
5. Circular Dependency taqiqlanadi.
---
# State Flow
```text
Idle
↓
Receiving
↓
Calculating
↓
Normalizing
↓
Completed
or
Failed
```
---
# Summary
Validated Signal
↓
SignalScoring
↓
Technical Score
↓
Signal Formatter
