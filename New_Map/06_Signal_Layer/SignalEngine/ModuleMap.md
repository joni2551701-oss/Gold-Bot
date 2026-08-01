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
        ├── Confluence Loader
        ├── Signal Builder
        ├── Validation Manager
        ├── Scoring Manager
        ├── Formatter Manager
        ├── State Manager
        └── Event Publisher
```
---
# Internal Components
## Confluence Loader
Technical Confluence'ni qabul qiladi.
---
## Signal Builder
Signal obyektini yaratadi.
---
## Validation Manager
Signal'ni tekshiradi.
---
## Scoring Manager
Technical Score va Confidence hisoblaydi.
---
## Formatter Manager
Signal formatini yaratadi.
---
## State Manager
Signal Lifecycle'ni boshqaradi.
---
## Event Publisher
Signal Event yaratadi.
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
---
# Summary
SignalEngine Signal Layer ichidagi barcha Signal Pipeline'ni boshqaruvchi Canonical Orchestrator hisoblanadi.
