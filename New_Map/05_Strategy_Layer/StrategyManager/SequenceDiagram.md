# Strategy Manager Sequence Diagram
Status: CANONICAL
---
# Purpose
StrategyManager Runtime Sequence.
Bu implementatsiya emas.
Bu Canonical Runtime Blueprint hisoblanadi.
---
# Runtime Sequence
```text
User Configuration
↓
StrategyManager
↓
Select Strategy
↓
Load Strategy Profile
↓
Validate Configuration
↓
Activate Strategy
↓
StrategyEngine
```
---
# Runtime Rules
1. Strategy mavjud bo'lishi kerak.
2. Strategy Profile mavjud bo'lishi kerak.
3. Validation majburiy.
4. StrategyEngine faqat Active Strategy qabul qiladi.
5. Circular Dependency taqiqlanadi.
---
# State Flow
```text
Idle
↓
Selecting
↓
Loading
↓
Validating
↓
Activating
↓
Completed
```
---
# Summary
User Configuration
↓
StrategyManager
↓
StrategyEngine
