# Trend
Status: CANONICAL
---
# Purpose
Trend Context Layer ichidagi bozor trendini aniqlovchi Canonical modul hisoblanadi.
Uning asosiy vazifasi Market Structure asosida bozorning umumiy yo'nalishini aniqlash va Market Context uchun Trend State yaratishdir.
Trend signal yaratmaydi.
Trend trade ochmaydi.
Trend AI ishlatmaydi.
Trend faqat bozor trendini aniqlaydi.
---
# Objective
Trend quyidagi vazifalarni bajaradi:
• Primary Trend Detection
• Secondary Trend Detection
• Internal Trend Detection
• External Trend Detection
• Trend Strength Analysis
• Trend Continuation Detection
• Trend Reversal Detection
• Premium / Discount Analysis
• Trend State Generation
---
# Layer Position
```text
Market Data
↓
MarketStructure
↓
Trend
↓
ContextService
```
---
# Responsibilities
Trend:
✓ Primary Trend aniqlaydi
✓ Secondary Trend aniqlaydi
✓ Internal Trend aniqlaydi
✓ External Trend aniqlaydi
✓ Trend Strength baholaydi
✓ Trend Continuation aniqlaydi
✓ Trend Reversal aniqlaydi
✓ Premium / Discount Zone aniqlaydi
✓ Trend State yaratadi
---
# Not Responsible
Trend:
✗ Indicator Calculation
✗ Strategy
✗ Signal Generation
✗ AI Analysis
✗ Decision
✗ Risk
✗ Execution
---
# Input
Trend qabul qiladi:
• OHLC Data
• Market Structure
• Session State
---
# Output
Trend yaratadi:
• Trend Direction
• Trend Strength
• Premium Zone
• Discount Zone
• Trend Events
• Trend State
---
# Workflow
```text
Market Data
↓
Market Structure
↓
Detect Trend
↓
Analyze Strength
↓
Detect Premium / Discount
↓
Generate Trend State
↓
ContextService
```
---
# Golden Rules
1. Trend Market Structure asosida aniqlanadi.
2. Premium / Discount doimo hisoblanadi.
3. Trend State har bir yangi Candle bilan yangilanadi.
4. Signal yaratilmaydi.
5. AI ishlatilmaydi.
6. Circular Dependency taqiqlanadi.
---
# Related Documents
```text
Trend/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
Trend GoldBot Context Layer ichidagi bozor trendini aniqlovchi yagona Canonical modul hisoblanadi.
