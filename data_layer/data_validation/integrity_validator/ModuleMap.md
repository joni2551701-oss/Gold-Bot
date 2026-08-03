# IntegrityValidator Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat IntegrityValidator modulining ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
QualityValidator
↓
IntegrityValidator
↓
Validated Data
```
---
# Module Architecture
```text
IntegrityValidator
        │
        ├── Duplicate Validator
        ├── Timestamp Validator
        ├── Sequence Validator
        ├── Consistency Validator
        ├── Cross Reference Validator
        ├── Result Builder
        ├── State Manager
        └── Event Generator
```
---
# Internal Components
## Duplicate Validator
Duplicate yozuvlarni tekshiradi.
---
## Timestamp Validator
Timestamp izchilligini tekshiradi.
---
## Sequence Validator
Ketma-ketlikni tekshiradi.
---
## Consistency Validator
Ma'lumotlar o'rtasidagi izchillikni tekshiradi.
---
## Cross Reference Validator
Bog'langan obyektlarni tekshiradi.
---
## Result Builder
Validation Result yaratadi.
---
## State Manager
Validator holatini boshqaradi.
---
## Event Generator
Validation Event yaratadi.
---
# Dependency Map
```text
QualityValidator
↓
IntegrityValidator
↓
Validated Data
```
---
# Allowed Dependencies
✓ QualityValidator
✓ ValidationService
✓ Configuration Layer
✓ Event System
---
# Forbidden Dependencies
✗ Strategy Layer
✗ Decision Layer
✗ Risk Layer
✗ AI Layer
✗ Business Layer
---
# Ownership
IntegrityValidator egalik qiladi.
✓ Integrity Rules
✓ Validation State
✓ Validation Result
✓ Validation Report
---
# Module Rules
1. IntegrityValidator yagona Data Integrity Validator.
2. Data o'zgartirilmaydi.
3. Validation Result majburiy.
4. Circular Dependency taqiqlanadi.
---
# Summary
IntegrityValidator Data Validation Layer ichidagi Canonical Data Integrity Validation moduli hisoblanadi.
