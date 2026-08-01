# Wyckoff Strategy Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat Wyckoff Strategy ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
Indicator Layer
↓
Wyckoff Strategy
↓
StrategyEngine
```
---
# Module Architecture
```text
Wyckoff Strategy
        │
        ├── Market Cycle Analyzer
        ├── Accumulation Analyzer
        ├── Distribution Analyzer
        ├── Phase Analyzer
        ├── Spring Analyzer
        ├── Upthrust Analyzer
        ├── Volume Confirmation
        ├── Confluence Builder
        ├── Validation Manager
        └── Result Builder
```
---
# Internal Components
## Market Cycle Analyzer
Bozor siklini aniqlaydi.
---
## Accumulation Analyzer
Accumulation zonasini baholaydi.
---
## Distribution Analyzer
Distribution zonasini baholaydi.
---
## Phase Analyzer
Wyckoff Phase (A-E) ni aniqlaydi.
---
## Spring Analyzer
Spring hodisasini tekshiradi.
---
## Upthrust Analyzer
Upthrust hodisasini tekshiradi.
---
## Volume Confirmation
Volume orqali tasdiqlashni bajaradi.
---
## Confluence Builder
Wyckoff Confluence yaratadi.
---
## Validation Manager
Natijani tekshiradi.
---
## Result Builder
Wyckoff Strategy Result yaratadi.
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
---
# Summary
Wyckoff Strategy GoldBot ichidagi Canonical Wyckoff Analysis modulidir.
