# MarketStructure Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat MarketStructure modulining ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
ContextEngine
↓
MarketStructure
↓
ContextService
```
---
# Module Architecture
```text
MarketStructure
        │
        ├── Swing Detector
        ├── Structure Builder
        ├── BOS Detector
        ├── CHoCH Detector
        ├── MSS Detector
        ├── State Manager
        ├── Event Generator
        └── Validation Manager
```
---
# Internal Components
## Swing Detector
Swing High va Swing Low aniqlaydi.
---
## Structure Builder
HH, HL, LH, LL yaratadi.
---
## BOS Detector
Break of Structure aniqlaydi.
---
## CHoCH Detector
Change of Character aniqlaydi.
---
## MSS Detector
Market Structure Shift aniqlaydi.
---
## State Manager
Structure State boshqaradi.
---
## Event Generator
Structure Event yaratadi.
---
## Validation Manager
Structure Validation bajaradi.
---
# Dependency Map
```text
Market Data
↓
MarketStructure
↓
ContextService
```
---
# Allowed Dependencies
✓ ContextEngine
✓ Event System
✓ ContextService
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
MarketStructure egalik qiladi.
✓ Swing Points
✓ Structure State
✓ BOS Events
✓ CHoCH Events
✓ MSS Events
---
# Module Rules
1. Swing har doim birinchi hisoblanadi.
2. Structure Swing asosida quriladi.
3. BOS va CHoCH Structure'dan keyin aniqlanadi.
4. Signal yaratilmaydi.
5. Circular Dependency taqiqlanadi.
---
# Summary
MarketStructure GoldBot Context Layer ichidagi bozor strukturasini hisoblovchi Canonical modul hisoblanadi.
