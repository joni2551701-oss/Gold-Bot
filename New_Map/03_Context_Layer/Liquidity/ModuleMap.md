# Liquidity Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat Liquidity modulining ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
ContextEngine
↓
Liquidity
↓
ContextService
```
---
# Module Architecture
```text
Liquidity
      │
      ├── Equal High Detector
      ├── Equal Low Detector
      ├── Liquidity Pool Builder
      ├── Sweep Detector
      ├── Grab Detector
      ├── State Manager
      ├── Event Generator
      └── Validation Manager
```
---
# Internal Components
## Equal High Detector
Equal High aniqlaydi.
---
## Equal Low Detector
Equal Low aniqlaydi.
---
## Liquidity Pool Builder
Liquidity Pool yaratadi.
---
## Sweep Detector
Liquidity Sweep aniqlaydi.
---
## Grab Detector
Liquidity Grab aniqlaydi.
---
## State Manager
Liquidity State boshqaradi.
---
## Event Generator
Liquidity Event yaratadi.
---
## Validation Manager
Liquidity Validation bajaradi.
---
# Dependency Map
```text
MarketStructure
↓
Liquidity
↓
ContextService
```
---
# Allowed Dependencies
✓ ContextEngine
✓ MarketStructure
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
---
# Ownership
Liquidity egalik qiladi.
✓ Liquidity Pools
✓ Buy-side Liquidity
✓ Sell-side Liquidity
✓ Sweep Events
✓ Liquidity State
---
# Module Rules
1. Liquidity Market Structure'ga bog'liq.
2. Pool Sweep'dan oldin yaratiladi.
3. Signal yaratilmaydi.
4. Circular Dependency taqiqlanadi.
---
# Summary
Liquidity GoldBot Context Layer ichidagi Liquidity Analysis moduli hisoblanadi.
