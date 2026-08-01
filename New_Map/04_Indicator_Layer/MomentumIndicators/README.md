# Momentum Indicators
Status: CANONICAL
---
# Purpose
MomentumIndicators Indicator Layer ichidagi Momentum Indicator'larni hisoblovchi Canonical modul hisoblanadi.
Uning asosiy vazifasi narx harakatining tezligi, kuchi va impulsini baholash hamda Momentum Indicator State yaratishdir.
MomentumIndicators signal yaratmaydi.
MomentumIndicators trade ochmaydi.
MomentumIndicators AI ishlatmaydi.
MomentumIndicators faqat Momentum Indicator'larni hisoblaydi.
---
# Objective
MomentumIndicators quyidagi vazifalarni bajaradi:
• RSI Calculation
• Stochastic Calculation
• CCI Calculation
• ROC Calculation
• Momentum Calculation
• MACD Histogram Calculation
• Momentum Strength Calculation
• Momentum Indicator State Generation
---
# Layer Position
```text
Market Context
↓
IndicatorEngine
↓
MomentumIndicators
↓
IndicatorService
```
---
# Responsibilities
MomentumIndicators:
✓ RSI hisoblaydi
✓ Stochastic hisoblaydi
✓ CCI hisoblaydi
✓ ROC hisoblaydi
✓ Momentum hisoblaydi
✓ MACD Histogram hisoblaydi
✓ Momentum Strength yaratadi
✓ Momentum Indicator State yaratadi
---
# Not Responsible
MomentumIndicators:
✗ Context Analysis
✗ Strategy
✗ Signal Generation
✗ AI Analysis
✗ Decision
✗ Risk
✗ Execution
---
# Input
MomentumIndicators qabul qiladi:
• Market Context
• OHLC Data
• Historical Data
---
# Output
MomentumIndicators yaratadi:
• RSI
• Stochastic
• CCI
• ROC
• Momentum
• MACD Histogram
• Momentum Strength
• Momentum Indicator State
---
# Workflow
```text
Market Context
↓
Load Price Data
↓
Calculate Momentum Indicators
↓
Validate Indicators
↓
Generate Momentum Indicator State
↓
IndicatorService
```
---
# Golden Rules
1. Momentum Indicator'lar faqat Market Context asosida hisoblanadi.
2. Har bir indikator mustaqil hisoblanadi.
3. Natijalar immutable hisoblanadi.
4. Signal yaratilmaydi.
5. AI ishlatilmaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
MomentumIndicators/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
MomentumIndicators GoldBot Indicator Layer ichidagi barcha Momentum Indicator'larni hisoblaydigan Canonical modul hisoblanadi.
