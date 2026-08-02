# Trend Following Strategy Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat Trend Following Strategy ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
Indicator Layer
↓
Trend Following Strategy
↓
StrategyManager
```
---
# Module Architecture
```text
Trend Following Strategy
        │
        ├── Trend Direction Analyzer
        ├── Trend Strength Analyzer
        ├── Pullback Analyzer
        ├── Momentum Analyzer
        ├── Volume Confirmation
        ├── Continuation Analyzer
        ├── Confluence Builder
        ├── Validation Manager
        └── Result Builder
```
---
# Internal Components
## Trend Direction Analyzer
Trend yo'nalishini aniqlaydi.
---
## Trend Strength Analyzer
Trend kuchini baholaydi.
---
## Pullback Analyzer
Pullback holatini tekshiradi.
---
## Momentum Analyzer
Momentum mosligini baholaydi.
---
## Volume Confirmation
Volume orqali trendni tasdiqlaydi.
---
## Continuation Analyzer
Trend davom etishini baholaydi.
---
## Confluence Builder
Trend Confluence yaratadi.
---
## Validation Manager
Strategy natijasini tekshiradi.
---
## Result Builder
Trend Following Result yaratadi.
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
Trend Following Strategy GoldBot ichidagi Canonical Trend Analysis modulidir.
