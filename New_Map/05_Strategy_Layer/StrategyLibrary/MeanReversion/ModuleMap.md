# Mean Reversion Strategy Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat Mean Reversion Strategy ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
Indicator Layer
↓
Mean Reversion Strategy
↓
StrategyManager
```
---
# Module Architecture
```text
Mean Reversion Strategy
        │
        ├── Mean Value Analyzer
        ├── Deviation Analyzer
        ├── Overbought Analyzer
        ├── Oversold Analyzer
        ├── Reversal Analyzer
        ├── Momentum Confirmation
        ├── Volume Confirmation
        ├── Confluence Builder
        ├── Validation Manager
        └── Result Builder
```
---
# Internal Components
## Mean Value Analyzer
Bozorning muvozanat qiymatini aniqlaydi.
---
## Deviation Analyzer
Narxning Mean'dan og'ishini hisoblaydi.
---
## Overbought Analyzer
Overbought holatini baholaydi.
---
## Oversold Analyzer
Oversold holatini baholaydi.
---
## Reversal Analyzer
Reversal tasdiqlanishini tekshiradi.
---
## Momentum Confirmation
Momentum mosligini baholaydi.
---
## Volume Confirmation
Volume orqali tasdiqlaydi.
---
## Confluence Builder
Mean Reversion Confluence yaratadi.
---
## Validation Manager
Strategy natijasini tekshiradi.
---
## Result Builder
Mean Reversion Result yaratadi.
---
# Allowed Dependencies
✓ Market Context
✓ Indicator Context
✓ StrategyManager
✓ StrategyProfiles
---
# Forbidden Dependencies
✗ Signal Layer
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Platform Layer
---
# Summary
Mean Reversion Strategy GoldBot ichidagi Canonical Mean Reversion Analysis modulidir.
