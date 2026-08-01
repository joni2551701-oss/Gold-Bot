# Sessions Module Map
Status: CANONICAL
---
# Module Position
```text
Platform Layer
↓
Sessions
↓
StrategyEngine
```
---
# Module Architecture
```text
Sessions
        │
        ├── Asia
        ├── London
        ├── NewYork
        ├── LondonNewYorkOverlap
        ├── CustomSession
        ├── Session Loader
        ├── Session Validator
        └── Session Profile Builder
```
---
# Internal Components
## Asia
Asia Session konfiguratsiyasi.
---
## London
London Session konfiguratsiyasi.
---
## NewYork
New York Session konfiguratsiyasi.
---
## LondonNewYorkOverlap
London va New York overlap konfiguratsiyasi.
---
## CustomSession
Foydalanuvchi yaratgan Session konfiguratsiyasi.
---
## Session Loader
Session konfiguratsiyasini yuklaydi.
---
## Session Validator
Session sozlamalarini tekshiradi.
---
## Session Profile Builder
Strategy Session Profile yaratadi.
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
Sessions foydalanuvchi tanlagan Trading Session konfiguratsiyasini StrategyEngine uchun tayyorlaydi.
