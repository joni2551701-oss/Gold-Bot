# AMD Strategy Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat AMD Strategy ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
Indicator Layer
↓
AMD Strategy
↓
StrategyEngine
```
---
# Module Architecture
```text
AMD Strategy
        │
        ├── Accumulation Analyzer
        ├── Manipulation Analyzer
        ├── Liquidity Sweep Analyzer
        ├── Distribution Analyzer
        ├── Expansion Analyzer
        ├── Session Analyzer
        ├── Confluence Builder
        ├── Validation Manager
        └── Result Builder
```
---
# Internal Components
## Accumulation Analyzer
Accumulation fazasini baholaydi.
---
## Manipulation Analyzer
Manipulation fazasini aniqlaydi.
---
## Liquidity Sweep Analyzer
Liquidity Sweep mavjudligini tekshiradi.
---
## Distribution Analyzer
Distribution fazasini baholaydi.
---
## Expansion Analyzer
Manipulation'dan keyingi Expansion holatini baholaydi.
---
## Session Analyzer
AMD uchun mos Session'ni tekshiradi.
---
## Confluence Builder
AMD Confluence yaratadi.
---
## Validation Manager
Strategy natijasini tekshiradi.
---
## Result Builder
AMD Execution Output yaratadi.
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
AMD Strategy GoldBot ichidagi Canonical AMD Analysis modulidir.
