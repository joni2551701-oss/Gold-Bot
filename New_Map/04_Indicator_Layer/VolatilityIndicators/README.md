# Volatility Indicators
Status: CANONICAL
---
# Purpose
VolatilityIndicators Indicator Layer ichidagi Volatility Indicator'larni hisoblovchi Canonical modul hisoblanadi.
Uning asosiy vazifasi bozorning volatilitet darajasini, narx diapazonini va kengayish/qisqarish holatini baholash hamda Volatility Indicator State yaratishdir.
VolatilityIndicators signal yaratmaydi.
VolatilityIndicators trade ochmaydi.
VolatilityIndicators AI ishlatmaydi.
VolatilityIndicators faqat Volatility Indicator'larni hisoblaydi.
---
# Objective
VolatilityIndicators quyidagi vazifalarni bajaradi:
• ATR Calculation
• Bollinger Bands Calculation
• Keltner Channel Calculation
• Donchian Channel Calculation
• Standard Deviation Calculation
• Volatility Score Calculation
• Volatility State Generation
---
# Layer Position
```text
Market Context
↓
IndicatorEngine
↓
VolatilityIndicators
↓
IndicatorService
```
---
# Responsibilities
VolatilityIndicators:
✓ ATR hisoblaydi
✓ Bollinger Bands hisoblaydi
✓ Keltner Channel hisoblaydi
✓ Donchian Channel hisoblaydi
✓ Standard Deviation hisoblaydi
✓ Volatility Score yaratadi
✓ Volatility Indicator State yaratadi
---
# Not Responsible
VolatilityIndicators:
✗ Context Analysis
✗ Strategy
✗ Signal Generation
✗ AI Analysis
✗ Decision
✗ Risk
✗ Execution
---
# Input
VolatilityIndicators qabul qiladi:
• Market Context
• OHLC Data
• Historical Data
---
# Output
VolatilityIndicators yaratadi:
• ATR
• Bollinger Bands
• Keltner Channel
• Donchian Channel
• Standard Deviation
• Volatility Score
• Volatility Indicator State
---
# Workflow
```text
Market Context
↓
Load Price Data
↓
Calculate Volatility Indicators
↓
Validate Indicators
↓
Generate Volatility Indicator State
↓
IndicatorService
```
---
# Golden Rules
1. Volatility Indicator'lar faqat Market Context asosida hisoblanadi.
2. Har bir indikator mustaqil hisoblanadi.
3. Natijalar immutable hisoblanadi.
4. Signal yaratilmaydi.
5. AI ishlatilmaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
VolatilityIndicators/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
VolatilityIndicators GoldBot Indicator Layer ichidagi barcha Volatility Indicator'larni hisoblaydigan Canonical modul hisoblanadi.
