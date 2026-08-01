# RiskProfiles Sequence Diagram
Status: CANONICAL
---
# Purpose
Risk Profile konfiguratsiyasining Runtime Sequence.
---
# Runtime Sequence
```text
User Settings
↓
Select Risk Profile
↓
Load Configuration
↓
Validate
↓
Build Risk Profile
↓
StrategyEngine
```
---
# Runtime Rules
1. Risk Profile foydalanuvchi tomonidan tanlanadi.
2. Validation majburiy.
3. Risk Layer bu yerda ishlamaydi.
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
Risk Profile
↓
StrategyEngine
