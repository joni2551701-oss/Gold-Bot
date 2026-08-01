# OrderBlock Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat OrderBlock modulining ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
ContextEngine
↓
OrderBlock
↓
ContextService
```
---
# Module Architecture
```text
OrderBlock
        │
        ├── Bullish Detector
        ├── Bearish Detector
        ├── Validation Manager
        ├── Mitigation Tracker
        ├── Invalidation Tracker
        ├── State Manager
        ├── Event Generator
        └── Report Manager
```
---
# Internal Components
## Bullish Detector
Bullish Order Block aniqlaydi.
---
## Bearish Detector
Bearish Order Block aniqlaydi.
---
## Validation Manager
Order Block'larni tasdiqlaydi.
---
## Mitigation Tracker
Mitigation holatini kuzatadi.
---
## Invalidation Tracker
Invalidation holatini kuzatadi.
---
## State Manager
Order Block State boshqaradi.
---
## Event Generator
Order Block Event yaratadi.
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
OrderBlock
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
---
# Ownership
OrderBlock egalik qiladi.
✓ Bullish Order Blocks
✓ Bearish Order Blocks
✓ Mitigation State
✓ Invalidation State
✓ Order Block Metadata
---
# Module Rules
1. Order Block Market Structure asosida yaratiladi.
2. Liquidity Validation majburiy.
3. Mitigation doim kuzatiladi.
4. Circular Dependency taqiqlanadi.
---
# Summary
OrderBlock GoldBot Context Layer ichidagi Institutional Order Block Analysis moduli hisoblanadi.
