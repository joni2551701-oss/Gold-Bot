# Filters Sequence Diagram
Status: CANONICAL
---
# Purpose
Strategy Filter konfiguratsiyasining Runtime Sequence.
---
# Runtime Sequence
```text
User Settings
↓
Select Filters
↓
Load Filter Configuration
↓
Validate Filters
↓
Build Filter Profile
↓
StrategyEngine
```
---
# Runtime Rules
1. Bir yoki bir nechta Filter tanlanishi mumkin.
2. Validation majburiy.
3. Filterlar StrategyEngine'ga uzatiladi.
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
Filters
↓
StrategyEngine
