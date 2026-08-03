# TradingStyles Sequence Diagram
Status: CANONICAL
---
# Purpose
Trading Style konfiguratsiyasining Runtime Sequence.
---
# Runtime Sequence
```text
User Settings
↓
Select Trading Style
↓
Load Trading Profile
↓
Apply Configuration
↓
StrategyManager
```
---
# Runtime Rules
1. Trading Style foydalanuvchi tomonidan tanlanadi.
2. Strategy Logic o'zgarmaydi.
3. Configuration StrategyManager'ga uzatiladi.
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
Applied
↓
Completed
```
---
# Summary
User Configuration
↓
Trading Style
↓
StrategyManager
