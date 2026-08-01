# Liquidity
Status: CANONICAL
---
# Purpose
Liquidity Context Layer ichidagi bozordagi likvidlikni aniqlovchi Canonical modul hisoblanadi.
Uning asosiy vazifasi Buy-side va Sell-side Liquidity zonalarini, Liquidity Pool'larni hamda Liquidity Sweep hodisalarini aniqlashdir.
Liquidity signal yaratmaydi.
Liquidity trade ochmaydi.
Liquidity AI ishlatmaydi.
Liquidity faqat bozor likvidligini tahlil qiladi.
---
# Objective
Liquidity quyidagi vazifalarni bajaradi:
• Buy-side Liquidity Detection
• Sell-side Liquidity Detection
• Equal High Detection
• Equal Low Detection
• Liquidity Pool Detection
• Liquidity Sweep Detection
• Liquidity Grab Detection
• Resting Liquidity Detection
• Liquidity State Generation
---
# Layer Position
```text
Market Data
↓
ContextEngine
↓
Liquidity
↓
ContextService
```
---
# Responsibilities
Liquidity:
✓ Buy-side Liquidity aniqlaydi
✓ Sell-side Liquidity aniqlaydi
✓ Equal High aniqlaydi
✓ Equal Low aniqlaydi
✓ Liquidity Pool yaratadi
✓ Liquidity Sweep aniqlaydi
✓ Liquidity Grab aniqlaydi
✓ Liquidity State yaratadi
---
# Not Responsible
Liquidity:
✗ Indicator Calculation
✗ Strategy
✗ Signal Generation
✗ AI Analysis
✗ Decision
✗ Risk
✗ Execution
---
# Input
Liquidity qabul qiladi:
• OHLC Data
• Candle Stream
• Historical Candles
• Market Structure
---
# Output
Liquidity yaratadi:
• Buy-side Liquidity
• Sell-side Liquidity
• Liquidity Pools
• Liquidity Sweep Events
• Liquidity Grab Events
• Liquidity State
---
# Workflow
```text
Market Data
↓
Market Structure
↓
Equal High / Low
↓
Liquidity Pools
↓
Liquidity Sweep
↓
Liquidity Grab
↓
Liquidity State
↓
ContextService
```
---
# Golden Rules
1. Liquidity Market Structure asosida hisoblanadi.
2. Equal High va Equal Low avval aniqlanadi.
3. Liquidity Sweep faqat mavjud Liquidity Pool ustida aniqlanadi.
4. Liquidity State doimo yangilanadi.
5. Signal yaratilmaydi.
6. AI ishlatilmaydi.
7. Circular Dependency taqiqlanadi.
---
# Related Documents
```text
Liquidity/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
Liquidity GoldBot Context Layer ichidagi bozordagi likvidlikni aniqlovchi yagona Canonical modul hisoblanadi.
