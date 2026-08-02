# ContextEngine Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat ContextEngine modulining ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
Context Layer
↓
ContextEngine
↓
Context Modules
↓
ContextService
```
---
# Module Architecture
```text
ContextEngine
        │
        ├── Context Dispatcher
        ├── Module Coordinator
        ├── Context Aggregator
        ├── Validation Manager
        ├── Context Builder
        ├── State Manager
        ├── Event Generator
        └── Report Manager
```
---
# Internal Components
## Context Dispatcher
Context modullarini ishga tushiradi.
---
## Module Coordinator
Modullar bajarilishini koordinatsiya qiladi.
---
## Context Aggregator
Barcha Context natijalarini yig'adi.
---
## Validation Manager
Market Context'ni tekshiradi.
---
## Context Builder
Yakuniy Market Context obyektini yaratadi.
---
## State Manager
Runtime holatini boshqaradi.
---
## Event Generator
Context Event yaratadi.
---
## Report Manager
Runtime Report yaratadi.
---
# Dependency Map
```text
Market Data
↓
ContextEngine
↓
MarketStructure
↓
Liquidity
↓
OrderBlock
↓
FairValueGap
↓
Wyckoff
↓
AMD
↓
Session
↓
Trend
↓
VolumeProfile
↓
ContextService
```
---
# Allowed Dependencies
✓ MarketStructure
✓ Liquidity
✓ OrderBlock
✓ FairValueGap
✓ Wyckoff
✓ AMD
✓ Session
✓ Trend
✓ VolumeProfile
✓ ContextService
✓ Event System
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
ContextEngine egalik qiladi.
✓ Context Pipeline
✓ Context State
✓ Context Events
✓ Context Metadata
✓ Runtime Context
---
# Module Rules
1. ContextEngine yagona Context Orchestrator.
2. Context modullar bir-biridan mustaqil ishlaydi.
3. ContextEngine faqat koordinatsiya qiladi.
4. Indicator hisoblamaydi.
5. Signal yaratmaydi.
6. Circular Dependency taqiqlanadi.
---
# Summary
ContextEngine GoldBot Context Layer ichidagi barcha Context modullarini koordinatsiya qiluvchi Canonical Orchestrator hisoblanadi.
