# Strategy Manager Module Map
Status: CANONICAL
---
# Module Position
```text
StrategyLibrary
↓
StrategyProfiles
↓
StrategyManager
↓
StrategyEngine
```
---
# Module Architecture
```text
StrategyManager
        │
        ├── Strategy Registry
        ├── Strategy Selector
        ├── Configuration Loader
        ├── Profile Loader
        ├── Validation Manager
        ├── Lifecycle Manager
        ├── Version Manager
        └── State Manager
```
---
# Internal Components
## Strategy Registry
Barcha Strategy'larni ro'yxatdan o'tkazadi.
---
## Strategy Selector
Faol Strategy'ni tanlaydi.
---
## Configuration Loader
Strategy Configuration'ni yuklaydi.
---
## Profile Loader
Strategy Profile'ni yuklaydi.
---
## Validation Manager
Konfiguratsiyani tekshiradi.
---
## Lifecycle Manager
Strategy Lifecycle'ni boshqaradi.
---
## Version Manager
Strategy Version'larini boshqaradi.
---
## State Manager
Manager holatini boshqaradi.
---
# Allowed Dependencies
✓ StrategyLibrary
✓ StrategyProfiles
✓ StrategyEngine
---
# Forbidden Dependencies
✗ Signal Layer
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Summary
StrategyManager GoldBot ichidagi barcha Strategy va Profile boshqaruvini amalga oshiruvchi Canonical Manager hisoblanadi.
