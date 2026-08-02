# Liquidity Sweep Strategy Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat Liquidity Sweep Strategy ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
Indicator Layer
↓
Liquidity Sweep Strategy
↓
StrategyManager
```
---
# Module Architecture
```text
Liquidity Sweep Strategy
        │
        ├── Liquidity Pool Analyzer
        ├── Equal High Analyzer
        ├── Equal Low Analyzer
        ├── Stop Hunt Analyzer
        ├── False Breakout Analyzer
        ├── Sweep Confirmation
        ├── Rejection Analyzer
        ├── Confluence Builder
        ├── Validation Manager
        └── Result Builder
```
---
# Internal Components
## Liquidity Pool Analyzer
Liquidity Pool'larni aniqlaydi.
---
## Equal High Analyzer
Equal High zonalarini tekshiradi.
---
## Equal Low Analyzer
Equal Low zonalarini tekshiradi.
---
## Stop Hunt Analyzer
Stop Hunt hodisasini aniqlaydi.
---
## False Breakout Analyzer
False Breakout holatini tekshiradi.
---
## Sweep Confirmation
Liquidity Sweep tasdiqlaydi.
---
## Rejection Analyzer
Sweep'dan keyingi Rejection'ni baholaydi.
---
## Confluence Builder
Liquidity Confluence yaratadi.
---
## Validation Manager
Strategy natijasini tekshiradi.
---
## Result Builder
Liquidity Sweep Result yaratadi.
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
Liquidity Sweep Strategy GoldBot ichidagi Canonical Liquidity Sweep Analysis modulidir.
