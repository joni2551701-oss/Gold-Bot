# Wyckoff Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat Wyckoff modulining ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
ContextEngine
↓
Wyckoff
↓
ContextService
```
---
# Module Architecture
```text
Wyckoff
      │
      ├── Phase Detector
      ├── Spring Detector
      ├── Upthrust Detector
      ├── SOS Detector
      ├── SOW Detector
      ├── State Manager
      ├── Event Generator
      └── Validation Manager
```
---
# Internal Components
## Phase Detector
Market Phase aniqlaydi.
---
## Spring Detector
Spring hodisasini aniqlaydi.
---
## Upthrust Detector
Upthrust hodisasini aniqlaydi.
---
## SOS Detector
Sign of Strength aniqlaydi.
---
## SOW Detector
Sign of Weakness aniqlaydi.
---
## State Manager
Wyckoff State boshqaradi.
---
## Event Generator
Wyckoff Event yaratadi.
---
## Validation Manager
Wyckoff Validation bajaradi.
---
# Dependency Map
```text
MarketStructure
↓
Liquidity
↓
VolumeProfile
↓
Wyckoff
↓
ContextService
```
---
# Allowed Dependencies
✓ ContextEngine
✓ MarketStructure
✓ Liquidity
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
---
# Ownership
Wyckoff egalik qiladi.
✓ Market Phase
✓ Spring Events
✓ Upthrust Events
✓ SOS Events
✓ SOW Events
✓ Wyckoff State
---
# Module Rules
1. Market Phase birinchi aniqlanadi.
2. Eventlar Phase ichida tekshiriladi.
3. Signal yaratilmaydi.
4. Circular Dependency taqiqlanadi.
---
# Summary
Wyckoff GoldBot Context Layer ichidagi Wyckoff Analysis moduli hisoblanadi.
