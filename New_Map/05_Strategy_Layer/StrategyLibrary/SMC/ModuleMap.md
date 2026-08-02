# SMC Strategy Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat SMC Strategy ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
Indicator Layer
↓
SMC Strategy
↓
StrategyEngine
```
---
# Module Architecture
```text
SMC Strategy
        │
        ├── Market Structure Analyzer
        ├── BOS Analyzer
        ├── CHoCH Analyzer
        ├── Liquidity Analyzer
        ├── Order Block Analyzer
        ├── Fair Value Gap Analyzer
        ├── Imbalance Analyzer
        ├── Premium / Discount Analyzer
        ├── Confluence Builder
        ├── Validation Manager
        └── Result Builder
```
---
# Internal Components
## Market Structure Analyzer
Market Structure holatini baholaydi.
---
## BOS Analyzer
Break Of Structure holatini tekshiradi.
---
## CHoCH Analyzer
Change Of Character holatini tekshiradi.
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
## Imbalance Analyzer
Imbalance holatini baholaydi.
---
## Premium / Discount Analyzer
Premium va Discount zonalarini baholaydi.
---
## Confluence Builder
SMC Confluence yaratadi.
---
## Validation Manager
Strategy natijasini tekshiradi.
---
## Result Builder
SMC Execution Output yaratadi.
---
# Allowed Dependencies
✓ Market Context
✓ Indicator Context
✓ StrategyEngine
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
SMC Strategy GoldBot ichidagi Canonical Smart Money Concepts Analysis modulidir.
