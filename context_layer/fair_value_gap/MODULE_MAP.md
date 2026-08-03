# FairValueGap Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat FairValueGap modulining ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
ContextEngine
↓
FairValueGap
↓
ContextService
```
---
# Module Architecture
```text
FairValueGap
        │
        ├── Bullish FVG Detector
        ├── Bearish FVG Detector
        ├── Validation Manager
        ├── Gap Fill Tracker
        ├── Invalidation Tracker
        ├── State Manager
        ├── Event Generator
        └── Report Manager
```
---
# Internal Components
## Bullish FVG Detector
Bullish Fair Value Gap aniqlaydi.
---
## Bearish FVG Detector
Bearish Fair Value Gap aniqlaydi.
---
## Validation Manager
FVG zonalarini tasdiqlaydi.
---
## Gap Fill Tracker
Gap Fill holatini kuzatadi.
---
## Invalidation Tracker
Invalidation holatini kuzatadi.
---
## State Manager
FVG State boshqaradi.
---
## Event Generator
FVG Event yaratadi.
---
## Report Manager
Runtime hisobotlarini tayyorlaydi.
---
# Dependency Map
```text
MarketStructure
↓
OrderBlock
↓
FairValueGap
↓
ContextService
```
---
# Allowed Dependencies
✓ ContextEngine
✓ MarketStructure
✓ OrderBlock
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
FairValueGap egalik qiladi.
✓ Bullish FVG
✓ Bearish FVG
✓ Imbalance Zones
✓ Gap Fill State
✓ FVG Metadata
---
# Module Rules
1. FVG Market Structure asosida aniqlanadi.
2. Order Block Context hisobga olinadi.
3. Validation majburiy.
4. Circular Dependency taqiqlanadi.
---
# Summary
FairValueGap GoldBot Context Layer ichidagi Price Inefficiency Analysis moduli hisoblanadi.
