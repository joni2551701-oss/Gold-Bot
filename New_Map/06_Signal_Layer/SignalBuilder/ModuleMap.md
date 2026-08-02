# Signal Builder Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat SignalBuilder ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
Confluence Engine
↓
SignalBuilder
↓
Signal Validator
```
---
# Module Architecture
```text
SignalBuilder
        │
        ├── Direction Builder
        ├── Entry Builder
        ├── Stop Loss Builder
        ├── Take Profit Builder
        ├── Metadata Builder
        ├── Signal Factory
        └── Result Builder
```
---
# Internal Components
## Direction Builder
BUY / SELL / NONE yo'nalishini yaratadi.
---
## Entry Builder
Entry narxini yaratadi.
---
## Stop Loss Builder
Stop Loss qiymatini yaratadi.
---
## Take Profit Builder
Take Profit qiymatini yaratadi.
---
## Metadata Builder
Signal Metadata yaratadi.
---
## Signal Factory
Standard Signal obyektini yaratadi.
---
## Result Builder
Yakuniy Signal Result yaratadi.
---
# Allowed Dependencies
✓ SignalEngine
✓ Strategy Result
✓ Confluence Engine
✓ Signal Model
---
# Forbidden Dependencies
✗ Signal Validator
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Platform Layer
---
# Summary
SignalBuilder Signal Result obyektini yaratadigan Canonical Builder modulidir.
