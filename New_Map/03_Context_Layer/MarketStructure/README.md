# Market Structure
Status: CANONICAL
---
# Purpose
MarketStructure Context Layer ichidagi bozor strukturasini aniqlovchi Canonical modul hisoblanadi.
Uning asosiy vazifasi narx harakatini tahlil qilish va Market Structure holatini yaratishdir.
MarketStructure signal yaratmaydi.
MarketStructure trade ochmaydi.
MarketStructure AI ishlatmaydi.
MarketStructure faqat bozor strukturasini aniqlaydi.
---
# Objective
MarketStructure quyidagi vazifalarni bajaradi:
• Swing Detection
• HH Detection
• HL Detection
• LH Detection
• LL Detection
• BOS Detection
• CHoCH Detection
• MSS Detection
• Internal Structure Analysis
• External Structure Analysis
• Structure State Generation
---
# Layer Position
```text
Market Data
↓
ContextEngine
↓
MarketStructure
↓
ContextService
```
---
# Responsibilities
MarketStructure:
✓ Swing aniqlaydi
✓ HH/HL/LH/LL aniqlaydi
✓ BOS aniqlaydi
✓ CHoCH aniqlaydi
✓ MSS aniqlaydi
✓ Internal Structure yaratadi
✓ External Structure yaratadi
✓ Structure State yaratadi
---
# Not Responsible
MarketStructure:
✗ Indicator Calculation
✗ Strategy
✗ Signal Generation
✗ AI Analysis
✗ Decision
✗ Risk
✗ Execution
---
# Input
MarketStructure qabul qiladi:
• OHLC Data
• Candle Stream
• Historical Candles
• Market Events
---
# Output
MarketStructure yaratadi:
• Swing Points
• Market Structure
• BOS Events
• CHoCH Events
• MSS Events
• Structure State
---
# Workflow
```text
Market Data
↓
Swing Detection
↓
HH HL LH LL
↓
BOS
↓
CHoCH
↓
MSS
↓
Market Structure
↓
ContextService
```
---
# Golden Rules
1. Structure faqat narxdan hisoblanadi.
2. BOS Structure Break hisoblanadi.
3. CHoCH Trend Change hisoblanadi.
4. Swing tasdiqlanmaguncha Structure yaratilmaydi.
5. Signal yaratilmaydi.
6. AI ishlatilmaydi.
7. Circular Dependency taqiqlanadi.
---
# Related Documents
```text
MarketStructure/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
MarketStructure GoldBot Context Layer ichidagi bozor strukturasini yaratadigan yagona Canonical modul hisoblanadi.
