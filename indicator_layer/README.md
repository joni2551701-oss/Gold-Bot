# Indicator Layer
Status: CANONICAL
---
# Purpose
Indicator Layer GoldBot arxitekturasidagi barcha texnik va maxsus indikatorlarni hisoblaydigan Canonical Layer hisoblanadi.
Ushbu Layer Market Context asosida indikatorlarni hisoblaydi va Strategy Layer uchun yagona Indicator Context yaratadi.
Indicator Layer signal yaratmaydi.
Indicator Layer trade ochmaydi.
Indicator Layer AI ishlatmaydi.
Indicator Layer faqat indikatorlarni hisoblaydi.
---
# Objective
Indicator Layer quyidagi vazifalarni bajaradi:
• Trend Indicators Calculation
• Momentum Indicators Calculation
• Volatility Indicators Calculation
• Volume Indicators Calculation
• Market Structure Indicators Calculation
• Smart Money Indicators Calculation
• Custom Indicators Calculation
• Indicator Context Generation
---
# Layer Position
```text
Data Layer
↓
Context Layer
↓
Indicator Layer
↓
Strategy Layer
```
---
# Layer Modules
```text
IndicatorEngine
TrendIndicators
MomentumIndicators
VolatilityIndicators
VolumeIndicators
MarketStructureIndicators
SmartMoneyIndicators
CustomIndicators
IndicatorService
```
---
# Responsibilities
Indicator Layer:
✓ Technical Indicators hisoblaydi
✓ Smart Money Indicators hisoblaydi
✓ Structure Indicators hisoblaydi
✓ Indicator Validation bajaradi
✓ Indicator Context yaratadi
✓ Indicator Context publish qiladi
---
# Not Responsible
Indicator Layer:
✗ Context Analysis
✗ Strategy
✗ Signal Generation
✗ AI Analysis
✗ Decision
✗ Risk
✗ Execution
---
# Input
Indicator Layer qabul qiladi:
• Market Context
• Historical Data
• Candle Data
• Volume Data
---
# Output
Indicator Layer yaratadi:
• Trend Indicators
• Momentum Indicators
• Volatility Indicators
• Volume Indicators
• Market Structure Indicators
• Smart Money Indicators
• Custom Indicators
• Indicator Context
---
# Workflow
```text
Market Context
↓
IndicatorEngine
↓
Indicator Modules
↓
Indicator Validation
↓
IndicatorService
↓
Indicator Context
↓
Strategy Layer
```
---
# Golden Rules
1. Indicator Layer faqat Market Context asosida ishlaydi.
2. Indicator natijalari immutable hisoblanadi.
3. IndicatorService yagona publish nuqtasi hisoblanadi.
4. Indicator Layer signal yaratmaydi.
5. AI ishlatilmaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
04_Indicator_Layer/
├── README.md
├── IndicatorEngine/
├── TrendIndicators/
├── MomentumIndicators/
├── VolatilityIndicators/
├── VolumeIndicators/
├── MarketStructureIndicators/
├── SmartMoneyIndicators/
├── CustomIndicators/
├── IndicatorService/
├── Layer_DataFlow.md
├── Layer_SequenceDiagram.md
├── Layer_ModuleMap.md
└── Layer_Contracts.md
```
---
# Summary
Indicator Layer GoldBot arxitekturasidagi barcha texnik va Smart Money indikatorlarini hisoblaydigan Canonical Layer hisoblanadi.
Uning yakuniy natijasi Strategy Layer tomonidan foydalaniladigan yagona **Indicator Context** obyektidir.
