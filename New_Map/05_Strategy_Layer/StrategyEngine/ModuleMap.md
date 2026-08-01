# StrategyEngine Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat StrategyEngine ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
Indicator Layer
↓
StrategyEngine
↓
StrategyService
```
---
# Module Architecture
```text
StrategyEngine
        │
        ├── Strategy Loader
        ├── Strategy Selector
        ├── Profile Loader
        ├── Execution Manager
        ├── Validation Manager
        ├── Result Builder
        ├── State Manager
        └── Event Publisher
```
---
# Internal Components
## Strategy Loader
Strategy Library'dan strategiyani yuklaydi.
---
## Strategy Selector
Qaysi strategiya ishlashini aniqlaydi.
---
## Profile Loader
Trading Style, Session, Timeframe, Risk va Filter konfiguratsiyasini yuklaydi.
---
## Execution Manager
Strategiyani bajaradi.
---
## Validation Manager
Natijani tekshiradi.
---
## Result Builder
Strategy Result yaratadi.
---
## State Manager
StrategyEngine holatini boshqaradi.
---
## Event Publisher
Strategy Event yaratadi.
---
# Dependency Map
```text
Strategy Library
↓
Strategy Profiles
↓
StrategyEngine
↓
StrategyService
```
---
# Allowed Dependencies
✓ StrategyLibrary
✓ StrategyProfiles
✓ Indicator Layer
✓ Context Layer
✓ Event System
---
# Forbidden Dependencies
✗ Signal Layer
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Ownership
StrategyEngine egalik qiladi.
✓ Strategy Lifecycle
✓ Strategy Result
✓ Strategy State
---
# Module Rules
1. StrategyEngine barcha strategiyalar uchun yagona orchestrator hisoblanadi.
2. StrategyLibrary faqat StrategyEngine orqali ishlaydi.
3. StrategyProfiles faqat StrategyEngine tomonidan qo'llaniladi.
4. Circular Dependency taqiqlanadi.
---
# Summary
StrategyEngine GoldBot Strategy Layer ichidagi barcha strategiyalarni boshqaruvchi Canonical Orchestrator hisoblanadi.
