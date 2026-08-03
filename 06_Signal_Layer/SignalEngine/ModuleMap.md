# Signal Engine Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat SignalEngine ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
Strategy Layer
↓
SignalEngine
↓
Signal Service
```
---
# Module Architecture
```text
SignalEngine
        │
        ├── Pipeline Coordinator
        ├── Execution Order Manager
        ├── Runtime Controller
        ├── State Manager
        └── Event Publisher
```
---
# Internal Components
## Pipeline Coordinator
ConfluenceEngine, SignalBuilder, SignalValidator, SignalScoring, SignalFormatter'ni to'g'ri ketma-ketlikda chaqiradi.
---
## Execution Order Manager
Pipeline bosqichlarining bajarilish tartibini belgilaydi.
---
## Runtime Controller
Pipeline Runtime holatini nazorat qiladi.
---
## State Manager
Signal Lifecycle'ni boshqaradi.
---
## Event Publisher
Coordination Event yaratadi.
---
# Allowed Dependencies
✓ ConfluenceEngine
✓ SignalBuilder
✓ SignalValidator
✓ SignalScoring
✓ SignalFormatter
✓ Event System
---
# Forbidden Dependencies
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Platform Layer
---
# Summary
SignalEngine Signal Layer ichidagi Pipeline Orchestration, Module Coordination va Runtime Control'ni boshqaruvchi Canonical Orchestrator hisoblanadi. Har bir pipeline bosqichining ichki hisob-kitobi o'z modulida bajariladi.
