# Context Layer Sequence Diagram
Status: CANONICAL
---
# Purpose
Context Layer Runtime Sequence.
---
# Runtime Sequence
```text
Validated Market Data
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
↓
Market Context
↓
Indicator Layer
```
---
# Runtime Rules
1. ContextEngine Pipeline'ni boshqaradi.
2. Har bir modul Context yaratadi.
3. ContextService barcha natijalarni birlashtiradi.
4. Validation Publish'dan oldin bajariladi.
