# StrategyEngine Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat StrategyEngine ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
StrategyManager
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
        ├── Execution Manager
        ├── Pipeline Coordinator
        ├── Validation Manager
        ├── Result Builder
        ├── State Manager
        └── Event Publisher
```
---
# Internal Components
## Execution Manager
StrategyManager tomonidan faollashtirilgan strategiyani bajaradi.
---
## Pipeline Coordinator
Strategy bajarilish jarayonini muvofiqlashtiradi.
---
## Validation Manager
Natijani tekshiradi.
---
## Result Builder
Strategy Result'ni yig'adi va birlashtiradi (Aggregation).
---
## State Manager
StrategyEngine holatini boshqaradi.
---
## Event Publisher
Strategy Event yaratadi.
---
# Dependency Map
```text
StrategyManager
↓
StrategyEngine
↓
StrategyService
```
---
# Allowed Dependencies
✓ StrategyManager
✓ Indicator Layer
✓ Context Layer
✓ Event System
---
# Forbidden Dependencies
✗ StrategyLibrary (to'g'ridan-to'g'ri)
✗ StrategyProfiles (to'g'ridan-to'g'ri)
✗ Signal Layer
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Ownership
StrategyEngine egalik qiladi.
✓ Strategy Execution
✓ Strategy Pipeline Coordination
✓ Strategy Result Aggregation
✓ Strategy State

StrategyEngine egalik qilmaydi.
✗ Strategy Discovery
✗ Strategy Selection
✗ Strategy Profile Loading
---
# Module Rules
1. StrategyEngine faqat Strategy Execution, Coordination va Result Aggregation uchun yagona orchestrator hisoblanadi.
2. StrategyLibrary va StrategyProfiles bilan StrategyEngine to'g'ridan-to'g'ri ishlamaydi — bular StrategyManager orqali boshqariladi.
3. StrategyEngine faqat StrategyManager tomonidan faollashtirilgan strategiyani qabul qiladi.
4. Circular Dependency taqiqlanadi.
---
# Summary
StrategyEngine GoldBot Strategy Layer ichidagi Strategy Execution, Coordination va Result Aggregation'ni boshqaruvchi Canonical Orchestrator hisoblanadi. Strategy Discovery, Selection va Profile Loading StrategyManager vakolatida qoladi.
