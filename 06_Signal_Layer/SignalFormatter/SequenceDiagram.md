# Signal Formatter Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat SignalFormatter Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu Canonical Runtime Blueprint hisoblanadi.
---
# Runtime Sequence
```text
SignalScoring
↓
Receive Signal Result
↓
Normalize Data
↓
Format Signal
↓
Format Metadata
↓
Build Standard Signal Model
↓
Signal Service
```
---
# Runtime Rules
1. Signal Result mavjud bo'lishi kerak.
2. Technical Score mavjud bo'lishi kerak.
3. Metadata mavjud bo'lishi kerak.
4. Formatting deterministik bo'lishi kerak.
5. Circular Dependency taqiqlanadi.
---
# State Flow
```text
Idle
↓
Receiving
↓
Formatting
↓
Building
↓
Completed
or
Failed
```
---
# Summary
Signal Result
↓
SignalFormatter
↓
Standard Signal Model
↓
Signal Service
