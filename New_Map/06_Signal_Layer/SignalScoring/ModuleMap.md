# Signal Scoring Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat SignalScoring ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
Signal Validator
↓
SignalScoring
↓
Signal Formatter
```
---
# Module Architecture
```text
SignalScoring
        │
        ├── Score Calculator
        ├── Confidence Calculator
        ├── Rating Generator
        ├── Normalization Engine
        ├── Quality Evaluator
        ├── Metadata Builder
        └── Result Builder
```
---
# Internal Components
## Score Calculator
Technical Score hisoblaydi.
---
## Confidence Calculator
Technical Confidence hisoblaydi.
---
## Rating Generator
Signal Rating yaratadi.
---
## Normalization Engine
Score qiymatini standart diapazonga keltiradi.
---
## Quality Evaluator
Signal sifatini baholaydi.
---
## Metadata Builder
Score Metadata yaratadi.
---
## Result Builder
Yakuniy Scoring Result yaratadi.
---
# Allowed Dependencies
✓ SignalEngine
✓ SignalValidator
✓ ConfluenceEngine
✓ Signal Model
---
# Forbidden Dependencies
✗ SignalFormatter
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Platform Layer
---
# Summary
SignalScoring GoldBot Signal Layer ichidagi barcha Signal Result obyektlari uchun Technical Score va Confidence hisoblovchi Canonical Evaluation moduli hisoblanadi.
