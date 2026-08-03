# Market Structure Indicators
Status: CANONICAL
---
# Purpose
MarketStructureIndicators Indicator Layer ichidagi Market Structure asosidagi indikatorlarni hisoblovchi Canonical modul hisoblanadi.
Uning asosiy vazifasi Context Layer tomonidan yaratilgan Market Structure ma'lumotlarini sonli (numeric) indikatorlarga aylantirish va Strategy Layer uchun Structure Indicator State yaratishdir.
MarketStructureIndicators Market Structure yaratmaydi.
MarketStructureIndicators signal yaratmaydi.
MarketStructureIndicators trade ochmaydi.
MarketStructureIndicators AI ishlatmaydi.
MarketStructureIndicators faqat Market Structure asosidagi indikatorlarni hisoblaydi.
---
# Objective
MarketStructureIndicators quyidagi vazifalarni bajaradi:
• Swing Strength Calculation
• BOS Strength Calculation
• CHoCH Strength Calculation
• MSS Strength Calculation
• Trend Quality Calculation
• Breakout Quality Calculation
• Range Quality Calculation
• Structure Score Calculation
• Market Structure Indicator State Generation
---
# Layer Position
```text
Market Context
↓
IndicatorEngine
↓
MarketStructureIndicators
↓
IndicatorService
```
---
# Responsibilities
MarketStructureIndicators:
✓ Swing Strength hisoblaydi
✓ BOS Strength hisoblaydi
✓ CHoCH Strength hisoblaydi
✓ MSS Strength hisoblaydi
✓ Trend Quality hisoblaydi
✓ Breakout Quality hisoblaydi
✓ Range Quality hisoblaydi
✓ Structure Score yaratadi
✓ Structure Indicator State yaratadi
---
# Not Responsible
MarketStructureIndicators:
✗ Market Structure Detection
✗ Strategy
✗ Signal Generation
✗ AI Analysis
✗ Decision
✗ Risk
✗ Execution
---
# Input
MarketStructureIndicators qabul qiladi:
• Market Context
• Market Structure State
• Trend State
• Session State
---
# Output
MarketStructureIndicators yaratadi:
• Swing Strength
• BOS Strength
• CHoCH Strength
• MSS Strength
• Trend Quality
• Breakout Quality
• Range Quality
• Structure Score
• Structure Indicator State
---
# Workflow
```text
Market Context
↓
Load Structure State
↓
Calculate Structure Indicators
↓
Validate Indicators
↓
Generate Structure Indicator State
↓
IndicatorService
```
---
# Golden Rules
1. Market Structure Indicator'lar faqat Market Context asosida hisoblanadi.
2. Structure qayta hisoblanmaydi.
3. Natijalar immutable hisoblanadi.
4. Signal yaratilmaydi.
5. AI ishlatilmaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
MarketStructureIndicators/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
MarketStructureIndicators GoldBot Indicator Layer ichidagi Market Structure asosidagi indikatorlarni hisoblaydigan Canonical modul hisoblanadi.
