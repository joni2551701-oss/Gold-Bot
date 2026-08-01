# Timeframes Sequence Diagram
Status: CANONICAL
---
# Purpose
Timeframe konfiguratsiyasining Runtime Sequence.
---
# Runtime Sequence
```text
User Settings
↓
Select Timeframe(s)
↓
Validate Timeframe
↓
Build Timeframe Profile
↓
Apply Configuration
↓
StrategyEngine
```
---
# Runtime Rules
1. Bitta yoki bir nechta Timeframe tanlanishi mumkin.
2. Multi-Timeframe qo'llab-quvvatlanadi.
3. Validation majburiy.
4. Circular Dependency taqiqlanadi.
---
# State Flow
```text
Idle
↓
Selected
↓
Validated
↓
Configured
↓
Applied
↓
Completed
```
---
# Summary
User Configuration
↓
Timeframes
↓
StrategyEngine
