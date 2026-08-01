# Presets Sequence Diagram
Status: CANONICAL
---
# Purpose
Preset konfiguratsiyasining Runtime Sequence.
---
# Runtime Sequence
```text
User Settings
↓
Build Configuration
↓
Validate
↓
Create Preset
↓
Save
↓
Load
↓
StrategyEngine
```
---
# Runtime Rules
1. Configuration to'liq bo'lishi kerak.
2. Validation majburiy.
3. Preset Version yaratiladi.
4. Circular Dependency taqiqlanadi.
---
# State Flow
```text
Idle
↓
Creating
↓
Validating
↓
Saving
↓
Loading
↓
Completed
```
---
# Summary
User Configuration
↓
Preset
↓
StrategyEngine
