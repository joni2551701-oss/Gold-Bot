# VolatilityIndicators Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat VolatilityIndicators modulining ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
IndicatorEngine
↓
VolatilityIndicators
↓
IndicatorService
```
---
# Module Architecture
```text
VolatilityIndicators
        │
        ├── ATR Calculator
        ├── Bollinger Bands Calculator
        ├── Keltner Channel Calculator
        ├── Donchian Channel Calculator
        ├── Standard Deviation Calculator
        ├── Volatility Score Calculator
        ├── Validation Manager
        └── State Manager
```
---
# Internal Components
## ATR Calculator
Average True Range hisoblaydi.
---
## Bollinger Bands Calculator
Bollinger Bands hisoblaydi.
---
## Keltner Channel Calculator
Keltner Channel hisoblaydi.
---
## Donchian Channel Calculator
Donchian Channel hisoblaydi.
---
## Standard Deviation Calculator
Narx dispersiyasini hisoblaydi.
---
## Volatility Score Calculator
Volatilitet darajasini baholaydi.
---
## Validation Manager
Hisoblangan indikatorlarni tekshiradi.
---
## State Manager
Volatility Indicator State boshqaradi.
---
# Dependency Map
```text
Market Context
↓
VolatilityIndicators
↓
IndicatorService
```
---
# Allowed Dependencies
✓ IndicatorEngine
✓ Market Context
✓ IndicatorService
✓ Event System
---
# Forbidden Dependencies
✗ Strategy Layer
✗ Signal Layer
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Platform Layer
---
# Ownership
VolatilityIndicators egalik qiladi.
✓ ATR
✓ Bollinger Bands
✓ Keltner Channel
✓ Donchian Channel
✓ Standard Deviation
✓ Volatility Score
✓ Volatility Indicator State
---
# Module Rules
1. Har bir indikator mustaqil hisoblanadi.
2. Volatility Score barcha indikatorlardan foydalanishi mumkin.
3. Signal yaratilmaydi.
4. Circular Dependency taqiqlanadi.
---
# Summary
VolatilityIndicators GoldBot Indicator Layer ichidagi Volatility Indicator Calculation moduli hisoblanadi.
