# RiskProfiles Module Map
Status: CANONICAL
---
# Module Position
```text
Platform Layer
↓
RiskProfiles
↓
StrategyManager
```
---
# Module Architecture
```text
RiskProfiles
        │
        ├── Profile Selector
        ├── Configuration Loader
        ├── Validation Manager
        ├── Profile Builder
        └── Compatibility Checker
```
---
# Internal Components
## Profile Selector
Risk Profile tanlaydi.
---
## Configuration Loader
Risk konfiguratsiyasini yuklaydi.
---
## Validation Manager
Risk konfiguratsiyasini tekshiradi.
---
## Profile Builder
Strategy Risk Profile yaratadi.
---
## Compatibility Checker
Strategiya bilan mosligini tekshiradi.
---
# Allowed Dependencies
✓ StrategyProfiles
✓ StrategyManager
---
# Forbidden Dependencies
✗ Risk Layer
✗ Signal Layer
✗ AI Layer
✗ Decision Layer
✗ Execution Layer
✗ Platform Layer Logic
---
# Summary
RiskProfiles foydalanuvchi tanlagan Risk konfiguratsiyasini StrategyManager uchun tayyorlaydi.
