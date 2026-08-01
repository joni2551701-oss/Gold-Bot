# Order Block
Status: CANONICAL
---
# Purpose
OrderBlock Context Layer ichidagi Institutional Order Block zonalarini aniqlovchi Canonical modul hisoblanadi.
Uning asosiy vazifasi Bullish va Bearish Order Block'larni aniqlash, ularning holatini kuzatish hamda Market Context uchun Institutional POI (Point of Interest) yaratishdir.
OrderBlock signal yaratmaydi.
OrderBlock trade ochmaydi.
OrderBlock AI ishlatmaydi.
OrderBlock faqat Institutional Order Block'larni aniqlaydi.
---
# Objective
OrderBlock quyidagi vazifalarni bajaradi:
• Bullish Order Block Detection
• Bearish Order Block Detection
• Internal Order Block Detection
• External Order Block Detection
• Order Block Validation
• Order Block Mitigation Detection
• Order Block Invalidation Detection
• Order Block State Generation
---
# Layer Position
```text
Market Data
↓
MarketStructure
↓
Liquidity
↓
OrderBlock
↓
ContextService
```
---
# Responsibilities
OrderBlock:
✓ Bullish Order Block aniqlaydi
✓ Bearish Order Block aniqlaydi
✓ Internal Order Block aniqlaydi
✓ External Order Block aniqlaydi
✓ Order Block Validation
✓ Mitigation Detection
✓ Invalidation Detection
✓ Order Block State yaratadi
---
# Not Responsible
OrderBlock:
✗ Indicator Calculation
✗ Strategy
✗ Signal Generation
✗ AI Analysis
✗ Decision
✗ Risk
✗ Execution
---
# Input
OrderBlock qabul qiladi:
• OHLC Data
• Candle Stream
• Market Structure
• Liquidity State
---
# Output
OrderBlock yaratadi:
• Bullish Order Blocks
• Bearish Order Blocks
• Mitigation Events
• Invalidation Events
• Order Block State
---
# Workflow
```text
Market Data
↓
Market Structure
↓
Liquidity
↓
Detect Order Blocks
↓
Validate Order Blocks
↓
Detect Mitigation
↓
Detect Invalidation
↓
Order Block State
↓
ContextService
```
---
# Golden Rules
1. Order Block Market Structure asosida aniqlanadi.
2. Liquidity Context hisobga olinadi.
3. Mitigation doim kuzatiladi.
4. Invalid Order Block Context'dan chiqariladi.
5. Signal yaratilmaydi.
6. AI ishlatilmaydi.
7. Circular Dependency taqiqlanadi.
---
# Related Documents
```text
OrderBlock/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
OrderBlock GoldBot Context Layer ichidagi Institutional Order Block'larni aniqlovchi yagona Canonical modul hisoblanadi.
