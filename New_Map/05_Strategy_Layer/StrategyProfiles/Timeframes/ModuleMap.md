# Timeframes Module Map
Status: CANONICAL
---
# Module Position
```text
Platform Layer
↓
Timeframes
↓
StrategyManager
```
---
# Module Architecture
```text
Timeframes
        │
        ├── Timeframe Selector
        ├── Multi-Timeframe Manager
        ├── Validation Manager
        ├── Configuration Builder
        ├── Profile Builder
        └── Compatibility Checker
```
---
# Internal Components
## Timeframe Selector
Foydalanuvchi tanlagan timeframe'larni qabul qiladi.
---
## Multi-Timeframe Manager
Bir nechta timeframe bilan ishlashni boshqaradi.
---
## Validation Manager
Timeframe mosligini tekshiradi.
---
## Configuration Builder
Timeframe konfiguratsiyasini yaratadi.
---
## Profile Builder
Strategy Timeframe Profile yaratadi.
---
## Compatibility Checker
Strategiya va Timeframe mosligini tekshiradi.
---
# Allowed Dependencies
✓ StrategyProfiles
✓ StrategyManager
---
# Forbidden Dependencies
✗ Signal Layer
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Summary
Timeframes foydalanuvchi tanlagan timeframe konfiguratsiyasini StrategyManager uchun tayyorlaydi.
