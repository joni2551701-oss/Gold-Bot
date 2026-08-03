# Session Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat Session modulining ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
ContextEngine
↓
Session
↓
ContextService
```
---
# Module Architecture
```text
Session
      │
      ├── Calendar Manager
      ├── Session Detector
      ├── Kill Zone Detector
      ├── Overlap Detector
      ├── Volatility Analyzer
      ├── State Manager
      ├── Event Generator
      └── Validation Manager
```
---
# Internal Components
## Calendar Manager
Trading Calendar boshqaradi.
---
## Session Detector
Joriy Trading Session aniqlaydi.
---
## Kill Zone Detector
Kill Zone vaqtlarini aniqlaydi.
---
## Overlap Detector
Session Overlap holatini aniqlaydi.
---
## Volatility Analyzer
Session faolligini tahlil qiladi.
---
## State Manager
Session State boshqaradi.
---
## Event Generator
Session Event yaratadi.
---
## Validation Manager
Session Validation bajaradi.
---
# Dependency Map
```text
Trading Calendar
↓
Session
↓
ContextService
```
---
# Allowed Dependencies
✓ ContextEngine
✓ ContextService
✓ Event System
✓ Trading Calendar
---
# Forbidden Dependencies
✗ Indicator Layer
✗ Strategy Layer
✗ Signal Layer
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Platform Layer
---
# Ownership
Session egalik qiladi.
✓ Session State
✓ Kill Zone
✓ Session Events
✓ Trading Calendar Context
---
# Module Rules
1. Session faqat vaqt va Calendar asosida aniqlanadi.
2. Kill Zone Session ichida hisoblanadi.
3. Signal yaratmaydi.
4. Circular Dependency taqiqlanadi.
---
# Summary
Session GoldBot Context Layer ichidagi Trading Session Analysis moduli hisoblanadi.
