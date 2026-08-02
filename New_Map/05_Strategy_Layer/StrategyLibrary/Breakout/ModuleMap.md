# Breakout Strategy Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat Breakout Strategy ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
Indicator Layer
↓
Breakout Strategy
↓
StrategyManager
```
---
# Module Architecture
```text
Breakout Strategy
        │
        ├── Range Analyzer
        ├── Consolidation Analyzer
        ├── Support Analyzer
        ├── Resistance Analyzer
        ├── Breakout Detector
        ├── Volume Confirmation
        ├── Retest Analyzer
        ├── Confluence Builder
        ├── Validation Manager
        └── Result Builder
```
---
# Internal Components
## Range Analyzer
Trading Range'ni aniqlaydi.
---
## Consolidation Analyzer
Consolidation zonalarini aniqlaydi.
---
## Support Analyzer
Support darajalarini baholaydi.
---
## Resistance Analyzer
Resistance darajalarini baholaydi.
---
## Breakout Detector
Breakout hodisasini aniqlaydi.
---
## Volume Confirmation
Volume orqali Breakout'ni tasdiqlaydi.
---
## Retest Analyzer
Breakout'dan keyingi Retest'ni baholaydi.
---
## Confluence Builder
Breakout Confluence yaratadi.
---
## Validation Manager
Natijani tekshiradi.
---
## Result Builder
Breakout Strategy Result yaratadi.
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
---
# Summary
Breakout Strategy GoldBot ichidagi Canonical Breakout Analysis modulidir.
