# Presets Module Map
Status: CANONICAL
---
# Module Position
```text
Platform Layer
↓
Presets
↓
StrategyEngine
```
---
# Module Architecture
```text
Presets
        │
        ├── Preset Builder
        ├── Preset Loader
        ├── Preset Saver
        ├── Version Manager
        ├── Validation Manager
        ├── Configuration Builder
        └── Profile Builder
```
---
# Internal Components
## Preset Builder
Yangi Preset yaratadi.
---
## Preset Loader
Saqlangan Preset'ni yuklaydi.
---
## Preset Saver
Preset'ni saqlaydi.
---
## Version Manager
Preset versiyalarini boshqaradi.
---
## Validation Manager
Preset konfiguratsiyasini tekshiradi.
---
## Configuration Builder
Strategy Configuration yaratadi.
---
## Profile Builder
Strategy Profile yaratadi.
---
# Allowed Dependencies
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
Presets foydalanuvchi va tizim tomonidan yaratilgan Strategy Configuration'larni StrategyEngine uchun tayyorlaydi.
