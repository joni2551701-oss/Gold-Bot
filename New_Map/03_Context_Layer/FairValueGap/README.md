# Fair Value Gap
Status: CANONICAL
---
# Purpose
FairValueGap Context Layer ichidagi Fair Value Gap (FVG) va Imbalance zonalarini aniqlovchi Canonical modul hisoblanadi.
Uning asosiy vazifasi bozordagi narx samarasizligini (Price Inefficiency) aniqlash, Fair Value Gap zonalarini yaratish va ularning Runtime holatini kuzatishdir.
FairValueGap signal yaratmaydi.
FairValueGap trade ochmaydi.
FairValueGap AI ishlatmaydi.
FairValueGap faqat Price Inefficiency'ni aniqlaydi.
---
# Objective
FairValueGap quyidagi vazifalarni bajaradi:
• Bullish FVG Detection
• Bearish FVG Detection
• Internal FVG Detection
• External FVG Detection
• Imbalance Detection
• Gap Validation
• Gap Fill Detection
• Gap Invalidation Detection
• Fair Value Gap State Generation
---
# Layer Position
```text
Market Data
↓
MarketStructure
↓
OrderBlock
↓
FairValueGap
↓
ContextService
```
---
# Responsibilities
FairValueGap:
✓ Bullish FVG aniqlaydi
✓ Bearish FVG aniqlaydi
✓ Imbalance aniqlaydi
✓ Gap Validation
✓ Gap Fill aniqlaydi
✓ Gap Invalidation aniqlaydi
✓ FVG State yaratadi
---
# Not Responsible
FairValueGap:
✗ Indicator Calculation
✗ Strategy
✗ Signal Generation
✗ AI Analysis
✗ Decision
✗ Risk
✗ Execution
---
# Input
FairValueGap qabul qiladi:
• OHLC Data
• Candle Stream
• Market Structure
• Order Block State
---
# Output
FairValueGap yaratadi:
• Bullish FVG
• Bearish FVG
• Imbalance Zones
• Gap Fill Events
• Gap Invalidation Events
• Fair Value Gap State
---
# Workflow
```text
Market Data
↓
Read Market Structure
↓
Read Order Blocks
↓
Detect FVG
↓
Validate FVG
↓
Detect Gap Fill
↓
Detect Invalidation
↓
FVG State
↓
ContextService
```
---
# Golden Rules
1. Fair Value Gap faqat Market Structure asosida aniqlanadi.
2. Har bir Gap Validation'dan o'tadi.
3. Gap Fill doim kuzatiladi.
4. Invalid FVG Context'dan chiqariladi.
5. Signal yaratilmaydi.
6. AI ishlatilmaydi.
7. Circular Dependency taqiqlanadi.
---
# Related Documents
```text
FairValueGap/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
FairValueGap GoldBot Context Layer ichidagi Fair Value Gap va Imbalance zonalarini aniqlovchi yagona Canonical modul hisoblanadi.
