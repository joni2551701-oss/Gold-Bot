# ICT Strategy Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat ICT Strategy ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
Indicator Layer
↓
ICT Strategy
↓
StrategyEngine
```
---
# Module Architecture
```text
ICT Strategy
        │
        ├── Market Structure Analyzer
        ├── Liquidity Analyzer
        ├── Order Block Analyzer
        ├── Fair Value Gap Analyzer
        ├── Premium / Discount Analyzer
        ├── Session Analyzer
        ├── Confluence Builder
        ├── Validation Manager
        └── Result Builder
```
---
# Internal Components
## Market Structure Analyzer
Market Structure'ni baholaydi.
---
## Liquidity Analyzer
Liquidity holatini baholaydi.
---
## Order Block Analyzer
Order Block'larni tekshiradi.
---
## Fair Value Gap Analyzer
FVG'larni tekshiradi.
---
## Premium / Discount Analyzer
Premium va Discount zonalarini baholaydi.
---
## Session Analyzer
Session mosligini tekshiradi.
---
## Confluence Builder
ICT Confluence yaratadi.
---
## Validation Manager
Strategy natijasini tekshiradi.
---
## Result Builder
ICT Execution Output yaratadi.
---
# Allowed Dependencies
✓ Market Context
✓ Indicator Context
✓ StrategyEngine
✓ Strategy Profiles
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
ICT Strategy GoldBot ichidagi Canonical ICT Analysis modulidir.
