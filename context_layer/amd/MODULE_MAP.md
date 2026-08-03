# AMD Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat AMD modulining ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
Wyckoff
↓
AMD
↓
Session
```
---
# Module Architecture
```text
AMD
      │
      ├── Accumulation Detector
      ├── Manipulation Detector
      ├── Distribution Detector
      ├── Phase Manager
      ├── Validation Manager
      ├── State Manager
      ├── Event Generator
      └── Report Manager
```
---
# Internal Components
## Accumulation Detector
Accumulation bosqichini aniqlaydi.
---
## Manipulation Detector
Manipulation bosqichini aniqlaydi.
---
## Distribution Detector
Distribution bosqichini aniqlaydi.
---
## Phase Manager
AMD Phase almashinishini boshqaradi.
---
## Validation Manager
AMD Validation bajaradi.
---
## State Manager
AMD State boshqaradi.
---
## Event Generator
AMD Event yaratadi.
---
## Report Manager
Runtime hisobotlarini tayyorlaydi.
---
# Dependency Map
```text
MarketStructure
↓
Liquidity
↓
AMD
↓
ContextService
```
---
# Allowed Dependencies
✓ ContextEngine
✓ MarketStructure
✓ Liquidity
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
AMD egalik qiladi.
✓ AMD Phase
✓ Accumulation Zone
✓ Manipulation Zone
✓ Distribution Zone
✓ AMD Metadata
---
# Module Rules
1. Phase ketma-ketligi saqlanadi.
2. Manipulation Liquidity bilan tasdiqlanadi.
3. Distribution Manipulation'dan keyin aniqlanadi.
4. Circular Dependency taqiqlanadi.
---
# Summary
AMD GoldBot Context Layer ichidagi Institutional Market Cycle Analysis moduli hisoblanadi.
