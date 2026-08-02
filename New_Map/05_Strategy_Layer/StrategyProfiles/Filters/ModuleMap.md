# Filters Module Map
Status: CANONICAL
---
# Module Position
```text
Platform Layer
↓
Filters
↓
StrategyManager
```
---
# Module Architecture
```text
Filters
        │
        ├── News Filter
        ├── Spread Filter
        ├── Volatility Filter
        ├── Session Filter
        ├── Weekend Filter
        ├── Holiday Filter
        ├── Trend Filter
        ├── Custom Filter
        ├── Configuration Loader
        ├── Validation Manager
        └── Profile Builder
```
---
# Internal Components
## News Filter
Yangiliklarga asoslangan filtr.
---
## Spread Filter
Spread chegaralarini tekshiradi.
---
## Volatility Filter
Bozor volatilitetini baholaydi.
---
## Session Filter
Trading Session mosligini tekshiradi.
---
## Weekend Filter
Hafta oxiri savdosini boshqaradi.
---
## Holiday Filter
Bayram kunlarini tekshiradi.
---
## Trend Filter
Trend sharoitlarini tekshiradi.
---
## Custom Filter
Foydalanuvchi yaratgan filter.
---
## Configuration Loader
Filter konfiguratsiyasini yuklaydi.
---
## Validation Manager
Filter konfiguratsiyasini tekshiradi.
---
## Profile Builder
Strategy Filter Profile yaratadi.
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
Filters foydalanuvchi tanlagan filtrlarni StrategyManager uchun tayyorlaydi.
