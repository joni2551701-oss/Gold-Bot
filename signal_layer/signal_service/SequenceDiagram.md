# Signal Service Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat SignalService Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu Canonical Runtime Blueprint hisoblanadi.
---
# Runtime Sequence
```text
Signal Formatter
↓
SignalService
↓
Validate Request
↓
Load Signal
↓
Publish Signal
↓
AI Layer
```
---
# Runtime Rules
1. Signal mavjud bo'lishi kerak.
2. Signal Formatter yakunlangan bo'lishi kerak.
3. Signal o'zgartirilmaydi.
4. Signal AI Layer'ga uzatiladi.
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
Publishing
↓
Completed
or
Failed
```
---
# Summary
Signal Formatter
↓
SignalService
↓
AI Layer
