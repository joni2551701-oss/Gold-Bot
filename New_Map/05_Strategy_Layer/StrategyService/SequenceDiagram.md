# Strategy Service Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat StrategyService Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu Canonical Runtime Blueprint hisoblanadi.
---
# Runtime Sequence
```text
Signal Layer
↓
StrategyService
↓
Validate Request
↓
StrategyEngine
↓
Strategy Result
↓
Publish Result
↓
Signal Layer
```
---
# Runtime Rules
1. Request valid bo'lishi kerak.
2. Strategy faqat StrategyEngine orqali ishlaydi.
3. Natija o'zgartirilmaydi.
4. Circular Dependency taqiqlanadi.
---
# State Flow
```text
Idle
↓
Receiving
↓
Validating
↓
Processing
↓
Publishing
↓
Completed
```
---
# Summary
Signal Layer
↓
StrategyService
↓
StrategyEngine
↓
Strategy Result
↓
Signal Layer
