# Confluence Engine Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat ConfluenceEngine ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
Strategy Layer
↓
ConfluenceEngine
↓
SignalBuilder
```
---
# Module Architecture
```text
ConfluenceEngine
        │
        ├── Context Aggregator
        ├── Indicator Aggregator
        ├── Strategy Aggregator
        ├── Alignment Analyzer
        ├── Validation Manager
        ├── Confluence Builder
        └── Metadata Builder
```
---
# Internal Components
## Context Aggregator
Context Layer natijalarini yig'adi.
---
## Indicator Aggregator
Indicator Layer natijalarini yig'adi.
---
## Strategy Aggregator
Strategy Layer natijalarini yig'adi.
---
## Alignment Analyzer
Barcha texnik faktorlarning mosligini tekshiradi.
---
## Validation Manager
Confluence'ni tekshiradi.
---
## Confluence Builder
Technical Confluence yaratadi.
---
## Metadata Builder
Confluence Metadata yaratadi.
---
# Allowed Dependencies
✓ Context Layer
✓ Indicator Layer
✓ Strategy Layer
✓ Event System
---
# Forbidden Dependencies
✗ SignalBuilder
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Summary
ConfluenceEngine GoldBot Signal Layer ichidagi barcha texnik natijalarni yagona Confluence obyektiga birlashtiruvchi Canonical Engine hisoblanadi.
