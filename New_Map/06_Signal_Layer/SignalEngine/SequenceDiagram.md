# Signal Engine Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat SignalEngine Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu Canonical Runtime Blueprint hisoblanadi.
---
# Runtime Sequence
```text
Strategy Result
↓
Confluence Engine
↓
SignalEngine
↓
Signal Builder
↓
Signal Validator
↓
Signal Scoring
↓
Signal Formatter
↓
Signal Result
↓
Signal Service
```
---
# Runtime Rules
1. Strategy Result mavjud bo'lishi kerak.
2. Confluence tayyor bo'lishi kerak.
3. Validation Score hisoblashdan oldin bajariladi.
4. Signal Formatter oxirgi bosqich hisoblanadi.
5. Circular Dependency taqiqlanadi.
---
# State Flow
```text
Idle
↓
Receiving
↓
Building
↓
Validating
↓
Scoring
↓
Formatting
↓
Completed
or
Failed
```
---
# Summary
Strategy Result
↓
SignalEngine
↓
Signal Result
↓
Signal Service
