# Custom Indicators
Status: CANONICAL
---
# Purpose
CustomIndicators Indicator Layer ichidagi GoldBot'ga xos maxsus indikatorlarni hisoblovchi Canonical modul hisoblanadi.
Uning asosiy vazifasi klassik texnik indikatorlar va Smart Money indikatorlaridan tashqari GoldBot uchun ishlab chiqilgan proprietary indikatorlarni hisoblash hamda Custom Indicator State yaratishdir.
CustomIndicators signal yaratmaydi.
CustomIndicators trade ochmaydi.
CustomIndicators AI ishlatmaydi.
CustomIndicators faqat GoldBot indikatorlarini hisoblaydi.
---
# Objective
CustomIndicators quyidagi vazifalarni bajaradi:
• Senior Trend Score
• Market Confidence Index
• Liquidity Pressure Index
• Institutional Strength Index
• Smart Trend Index
• Risk Environment Index
• Composite Market Score
• Custom Indicator State Generation
---
# Layer Position
```text
Market Context
↓
IndicatorEngine
↓
CustomIndicators
↓
IndicatorService
```
---
# Responsibilities
CustomIndicators:
✓ Proprietary indikatorlarni hisoblaydi
✓ Composite Score yaratadi
✓ Market Score yaratadi
✓ Confidence Index yaratadi
✓ Indicator State yaratadi
---
# Not Responsible
CustomIndicators:
✗ Market Context Analysis
✗ Strategy
✗ Signal Generation
✗ AI Analysis
✗ Decision
✗ Risk
✗ Execution
---
# Input
CustomIndicators qabul qiladi:
• Market Context
• Trend Indicators
• Momentum Indicators
• Volatility Indicators
• Volume Indicators
• Market Structure Indicators
• Smart Money Indicators
---
# Output
CustomIndicators yaratadi:
• Senior Trend Score
• Market Confidence Index
• Liquidity Pressure Index
• Institutional Strength Index
• Smart Trend Index
• Risk Environment Index
• Composite Market Score
• Custom Indicator State
---
# Workflow
```text
Market Context
↓
Load Indicator Context
↓
Calculate Proprietary Indicators
↓
Validate Indicators
↓
Generate Custom Indicator State
↓
IndicatorService
```
---
# Golden Rules
1. Faqat GoldBot indikatorlari hisoblanadi.
2. Klassik indikatorlar qayta hisoblanmaydi.
3. Natijalar immutable hisoblanadi.
4. Signal yaratilmaydi.
5. AI ishlatilmaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
CustomIndicators/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
CustomIndicators GoldBot Indicator Layer ichidagi proprietary indikatorlarni hisoblaydigan Canonical modul hisoblanadi.
