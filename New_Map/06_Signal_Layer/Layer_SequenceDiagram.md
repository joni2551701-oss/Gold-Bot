# Signal Layer Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat Signal Layer Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu Canonical Runtime Blueprint hisoblanadi.
---
# Runtime Sequence
```text
Strategy Layer
↓
SignalEngine (Pipeline Orchestration)
↓
Context Layer
↓
Indicator Layer
↓
ConfluenceEngine
↓
SignalBuilder
↓
SignalValidator
↓
SignalScoring
↓
SignalFormatter
↓
SignalService
↓
AI Layer
```
---
# Runtime Rules
1. Context tayyor bo'lishi kerak.
2. Indicator tayyor bo'lishi kerak.
3. Strategy Result tayyor bo'lishi kerak.
4. Validation Score hisoblashdan oldin bajariladi.
5. Formatter Validation'dan keyin ishlaydi.
6. SignalService oxirgi bosqich hisoblanadi.
7. Circular Dependency qat'iyan taqiqlanadi.
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
Publishing
↓
Completed
or
Failed
```
---
# Summary
Context
↓
Indicators
↓
Strategies
↓
Signal
↓
AI
