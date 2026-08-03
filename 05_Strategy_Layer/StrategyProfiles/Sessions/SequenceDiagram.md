# Sessions Sequence Diagram
Status: CANONICAL
---
# Purpose
Trading Session konfiguratsiyasining Runtime Sequence.
---
# Runtime Sequence
```text
User Settings
↓
Select Session
↓
Load Session Configuration
↓
Validate Session
↓
Apply Session Filter
↓
StrategyManager
```
---
# Runtime Rules
1. Session foydalanuvchi tomonidan tanlanadi.
2. Session Configuration yuklanadi.
3. Session Filter qo'llaniladi.
4. Circular Dependency taqiqlanadi.
---
# State Flow
```text
Idle
↓
Selected
↓
Loaded
↓
Validated
↓
Applied
↓
Completed
```
---
# Summary
User Configuration
↓
Trading Session
↓
StrategyManager
