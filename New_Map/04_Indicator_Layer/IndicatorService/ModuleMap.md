# IndicatorService Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat IndicatorService modulining ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
IndicatorEngine
↓
IndicatorService
↓
Strategy Layer
```
---
# Module Architecture
```text
IndicatorService
        │
        ├── Indicator Aggregator
        ├── Validation Manager
        ├── Normalization Manager
        ├── Version Manager
        ├── Publish Manager
        ├── State Manager
        ├── Event Generator
        └── Report Manager
```
---
# Internal Components
## Indicator Aggregator
Barcha Indicator natijalarini yig'adi.
---
## Validation Manager
Indicator Context'ni tekshiradi.
---
## Normalization Manager
Indicator Context formatini standartlashtiradi.
---
## Version Manager
Har bir Indicator Context uchun Version yaratadi.
---
## Publish Manager
Indicator Context'ni Strategy Layer'ga uzatadi.
---
## State Manager
Indicator Service holatini boshqaradi.
---
## Event Generator
Indicator Update Event yaratadi.
---
## Report Manager
Runtime hisobotlarini tayyorlaydi.
---
# Dependency Map
```text
Indicator Modules
↓
IndicatorService
↓
Strategy Layer
```
---
# Allowed Dependencies
✓ IndicatorEngine
✓ TrendIndicators
✓ MomentumIndicators
✓ VolatilityIndicators
✓ VolumeIndicators
✓ MarketStructureIndicators
✓ SmartMoneyIndicators
✓ CustomIndicators
✓ Event System
---
# Forbidden Dependencies
✗ Strategy Layer (calculation)
✗ Signal Layer
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Ownership
IndicatorService egalik qiladi.
✓ Indicator Context
✓ Indicator Version
✓ Indicator Metadata
✓ Indicator Status
---
# Module Rules
1. Indicator Context yagona obyekt hisoblanadi.
2. Indicator Context immutable bo'lishi kerak.
3. Publish faqat Validation'dan keyin bajariladi.
4. Circular Dependency taqiqlanadi.
---
# Summary
IndicatorService GoldBot Indicator Layer ichidagi barcha indikator natijalarini boshqaruvchi Canonical Aggregation Service hisoblanadi.
