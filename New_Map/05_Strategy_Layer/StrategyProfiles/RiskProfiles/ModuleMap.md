# RiskProfiles Module Map
Status: CANONICAL
---
# Module Position
```text
Platform Layer
↓
RiskProfiles
↓
StrategyEngine
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
✓ StrategyEngine
---
# Forbidden Dependencies
✗ Risk Layer
✗ Signal Layer
✗ AI Layer
✗ Decision Layer
✗ Execution Layer
---
# Summary
RiskProfiles foydalanuvchi tanlagan Risk konfiguratsiyasini StrategyEngine uchun tayyorlaydi.
