# ContextService Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat ContextService modulining ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
ContextEngine
↓
ContextService
↓
Indicator Layer
```
---
# Module Architecture
```text
ContextService
        │
        ├── Context Aggregator
        ├── Validation Manager
        ├── Normalization Manager
        ├── Version Manager
        ├── Publish Manager
        ├── State Manager
        ├── Event Generator
        └── Report Manager
```
---
# Internal Components
## Context Aggregator
Barcha Context modullarining natijalarini yig'adi.
---
## Validation Manager
Market Context'ni tekshiradi.
---
## Normalization Manager
Market Context formatini standartlashtiradi.
---
## Version Manager
Har bir Context uchun Version yaratadi.
---
## Publish Manager
Market Context'ni keyingi Layer'ga uzatadi.
---
## State Manager
Context Service holatini boshqaradi.
---
## Event Generator
Context Update Event yaratadi.
---
## Report Manager
Runtime hisobotlarini tayyorlaydi.
---
# Dependency Map
```text
Context Modules
↓
ContextService
↓
Indicator Layer
```
---
# Allowed Dependencies
✓ ContextEngine
✓ MarketStructure
✓ Liquidity
✓ OrderBlock
✓ FairValueGap
✓ Wyckoff
✓ AMD
✓ Session
✓ Trend
✓ VolumeProfile
✓ Event System
---
# Forbidden Dependencies
✗ Strategy Layer
✗ Signal Layer
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Platform Layer
---
# Ownership
ContextService egalik qiladi.
✓ Market Context
✓ Context Version
✓ Context Metadata
✓ Context Status
---
# Module Rules
1. Market Context yagona obyekt hisoblanadi.
2. Context immutable bo'lishi kerak.
3. Publish faqat Validation'dan keyin bajariladi.
4. Circular Dependency taqiqlanadi.
---
# Summary
ContextService GoldBot Context Layer ichidagi barcha Context natijalarini boshqaruvchi Canonical Aggregation Service hisoblanadi.
