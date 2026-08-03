# Trend Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat Trend modulining ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
MarketStructure
↓
Session
↓
Trend
↓
ContextService
```
---
# Module Architecture
```text
Trend
     │
     ├── Trend Detector
     ├── Structure Analyzer
     ├── Strength Analyzer
     ├── Premium/Discount Analyzer
     ├── Continuation Detector
     ├── Reversal Detector
     ├── State Manager
     ├── Event Generator
     └── Validation Manager
```
---
# Internal Components
## Trend Detector
Asosiy trendni aniqlaydi.
---
## Structure Analyzer
Market Structure asosida trendni tahlil qiladi.
---
## Strength Analyzer
Trend kuchini baholaydi.
---
## Premium / Discount Analyzer
Premium va Discount zonalarini hisoblaydi.
---
## Continuation Detector
Trend davom etayotganini aniqlaydi.
---
## Reversal Detector
Trend o'zgarishini aniqlaydi.
---
## State Manager
Trend State boshqaradi.
---
## Event Generator
Trend Event yaratadi.
---
## Validation Manager
Trend Validation bajaradi.
---
# Dependency Map
```text
MarketStructure
↓
Session
↓
Trend
↓
ContextService
```
---
# Allowed Dependencies
✓ ContextEngine
✓ MarketStructure
✓ Session
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
Trend egalik qiladi.
✓ Trend Direction
✓ Trend Strength
✓ Premium Zone
✓ Discount Zone
✓ Trend Events
✓ Trend State
---
# Module Rules
1. Trend faqat Market Structure asosida aniqlanadi.
2. Premium / Discount har doim hisoblanadi.
3. Signal yaratmaydi.
4. Circular Dependency taqiqlanadi.
---
# Summary
Trend GoldBot Context Layer ichidagi Market Trend Analysis moduli hisoblanadi.
