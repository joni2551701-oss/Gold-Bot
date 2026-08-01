# VolumeProfile Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat VolumeProfile modulining ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
ContextEngine
↓
VolumeProfile
↓
ContextService
```
---
# Module Architecture
```text
VolumeProfile
        │
        ├── Profile Builder
        ├── POC Calculator
        ├── Value Area Calculator
        ├── HVN Detector
        ├── LVN Detector
        ├── Distribution Analyzer
        ├── State Manager
        ├── Event Generator
        └── Validation Manager
```
---
# Internal Components
## Profile Builder
Volume Profile yaratadi.
---
## POC Calculator
Point of Control hisoblaydi.
---
## Value Area Calculator
VAH va VAL hisoblaydi.
---
## HVN Detector
High Volume Node aniqlaydi.
---
## LVN Detector
Low Volume Node aniqlaydi.
---
## Distribution Analyzer
Volume Distribution'ni tahlil qiladi.
---
## State Manager
Volume Profile State boshqaradi.
---
## Event Generator
Volume Profile Event yaratadi.
---
## Validation Manager
Volume Profile Validation bajaradi.
---
# Dependency Map
```text
Market Data
↓
VolumeProfile
↓
ContextService
```
---
# Allowed Dependencies
✓ ContextEngine
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
VolumeProfile egalik qiladi.
✓ Volume Profile
✓ POC
✓ Value Area
✓ HVN
✓ LVN
✓ Volume Profile State
---
# Module Rules
1. Profile birinchi quriladi.
2. POC Profile'dan hisoblanadi.
3. Value Area POC asosida hisoblanadi.
4. Signal yaratmaydi.
5. Circular Dependency taqiqlanadi.
---
# Summary
VolumeProfile GoldBot Context Layer ichidagi Auction Market Analysis moduli hisoblanadi.
