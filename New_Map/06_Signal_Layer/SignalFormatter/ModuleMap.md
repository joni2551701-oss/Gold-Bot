# Signal Formatter Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat SignalFormatter ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
SignalScoring
↓
SignalFormatter
↓
SignalService
```
---
# Module Architecture
```text
SignalFormatter
        │
        ├── Signal Normalizer
        ├── Metadata Formatter
        ├── Output Formatter
        ├── Compatibility Adapter
        ├── Model Builder
        ├── Validation Checker
        └── Response Builder
```
---
# Internal Components
## Signal Normalizer
Signal obyektini standartlashtiradi.
---
## Metadata Formatter
Metadata formatini yaratadi.
---
## Output Formatter
Yakuniy Signal formatini yaratadi.
---
## Compatibility Adapter
Keyingi Layer bilan moslikni ta'minlaydi.
---
## Model Builder
Standard Signal Model yaratadi.
---
## Validation Checker
Formatning to'g'riligini tekshiradi.
---
## Response Builder
Yakuniy Formatted Signal yaratadi.
---
# Allowed Dependencies
✓ SignalScoring
✓ Signal Model
---
# Forbidden Dependencies
✗ SignalService
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Summary
SignalFormatter GoldBot Signal Layer ichidagi barcha Signal Result obyektlarini standart ko'rinishga o'tkazuvchi Canonical Formatter hisoblanadi.
