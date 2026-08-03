# Signal Builder Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat SignalBuilder Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu Canonical Runtime Blueprint hisoblanadi.
---
# Runtime Sequence
```text
Strategy Result
↓
Technical Confluence
↓
SignalBuilder
↓
Create Signal
↓
Create Entry
↓
Create Stop Loss
↓
Create Take Profit
↓
Create Metadata
↓
Signal Result
↓
Signal Validator
```
---
# Runtime Rules
1. Strategy Result mavjud bo'lishi kerak.
2. Technical Confluence mavjud bo'lishi kerak.
3. SignalBuilder faqat Signal yaratadi.
4. Validation keyingi bosqichda bajariladi.
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
Finalizing
↓
Completed
or
Failed
```
---
# Summary
Strategy Result
↓
SignalBuilder
↓
Signal Result
↓
Signal Validator
