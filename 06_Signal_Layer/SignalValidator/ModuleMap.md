# Signal Validator Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat SignalValidator ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
Signal Builder
↓
SignalValidator
↓
Signal Scoring
```
---
# Module Architecture
```text
SignalValidator
        │
        ├── Field Validator
        ├── Technical Validator
        ├── Integrity Validator
        ├── Boundary Validator
        ├── Validation Rule Engine
        ├── Error Collector
        └── Validation Result Builder
```
---
# Internal Components
## Field Validator
Majburiy maydonlarni tekshiradi.
---
## Technical Validator
Texnik qoidalarni tekshiradi.
---
## Integrity Validator
Signal obyektining yaxlitligini tekshiradi.
---
## Boundary Validator
Entry, SL va TP qiymatlarining chegaralarini tekshiradi.
---
## Validation Rule Engine
Validation qoidalarini boshqaradi.
---
## Error Collector
Validation xatolarini yig'adi.
---
## Validation Result Builder
Validation natijasini yaratadi.
---
# Allowed Dependencies
✓ SignalEngine
✓ SignalBuilder
✓ Signal Model
✓ Validation Rules
---
# Forbidden Dependencies
✗ SignalScoring
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Platform Layer
---
# Summary
SignalValidator GoldBot Signal Layer ichidagi barcha Signal Result obyektlarini tekshiruvchi Canonical Validation moduli hisoblanadi.
