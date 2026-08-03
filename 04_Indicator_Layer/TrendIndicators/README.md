# Trend Indicators
Status: CANONICAL
---
# Purpose
TrendIndicators Indicator Layer ichidagi Trend Indicator'larni hisoblovchi Canonical modul hisoblanadi.
Uning asosiy vazifasi Market Context asosida bozor trendini sonli (numeric) indikatorlar orqali baholash va Trend Indicator State yaratishdir.
TrendIndicators signal yaratmaydi.
TrendIndicators trade ochmaydi.
TrendIndicators AI ishlatmaydi.
TrendIndicators faqat Trend Indicator'larni hisoblaydi.
---
# Objective
TrendIndicators quyidagi vazifalarni bajaradi:
• EMA Calculation
• SMA Calculation
• WMA Calculation
• HMA Calculation
• SuperTrend Calculation
• Ichimoku Calculation
• Trend Strength Calculation
• Trend Indicator State Generation
---
# Layer Position
```text
Market Context
↓
IndicatorEngine
↓
TrendIndicators
↓
IndicatorService
```
---
# Responsibilities
TrendIndicators:
✓ EMA hisoblaydi
✓ SMA hisoblaydi
✓ WMA hisoblaydi
✓ HMA hisoblaydi
✓ SuperTrend hisoblaydi
✓ Ichimoku hisoblaydi
✓ Trend Strength yaratadi
✓ Trend Indicator State yaratadi
---
# Not Responsible
TrendIndicators:
✗ Context Analysis
✗ Strategy
✗ Signal Generation
✗ AI Analysis
✗ Decision
✗ Risk
✗ Execution
---
# Input
TrendIndicators qabul qiladi:
• Market Context
• OHLC Data
• Historical Data
---
# Output
TrendIndicators yaratadi:
• EMA
• SMA
• WMA
• HMA
• SuperTrend
• Ichimoku
• Trend Strength
• Trend Indicator State
---
# Workflow
```text
Market Context
↓
Load Price Data
↓
Calculate Trend Indicators
↓
Validate Indicators
↓
Generate Trend Indicator State
↓
IndicatorService
```
---
# Golden Rules
1. Trend Indicator'lar faqat Market Context asosida hisoblanadi.
2. Har bir indikator mustaqil hisoblanadi.
3. Natijalar immutable hisoblanadi.
4. Signal yaratilmaydi.
5. AI ishlatilmaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
TrendIndicators/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
TrendIndicators GoldBot Indicator Layer ichidagi barcha Trend Indicator'larni hisoblaydigan Canonical modul hisoblanadi.
