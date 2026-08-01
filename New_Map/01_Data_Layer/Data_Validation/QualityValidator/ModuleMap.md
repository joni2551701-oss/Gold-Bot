# QualityValidator Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat QualityValidator modulining ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
SchemaValidator
↓
QualityValidator
↓
IntegrityValidator
```
---
# Module Architecture
```text
QualityValidator
        │
        ├── Rule Manager
        ├── Completeness Validator
        ├── Range Validator
        ├── Freshness Validator
        ├── Score Calculator
        ├── Result Builder
        ├── State Manager
        └── Event Generator
```
---
# Internal Components
## Rule Manager
Quality Rule'larni boshqaradi.
---
## Completeness Validator
Data to'liqligini tekshiradi.
---
## Range Validator
Qiymatlar ruxsat etilgan oraliqda ekanligini tekshiradi.
---
## Freshness Validator
Data eskirmaganligini tekshiradi.
---
## Score Calculator
Quality Score hisoblaydi.
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
SchemaValidator
↓
QualityValidator
↓
IntegrityValidator
```
---
# Allowed Dependencies
✓ SchemaValidator
✓ IntegrityValidator
✓ Configuration Layer
✓ Event System
---
# Forbidden Dependencies
✗ Strategy Layer
✗ Decision Layer
✗ AI Layer
✗ Trading Logic
---
# Ownership
QualityValidator egalik qiladi.
✓ Quality Rules
✓ Quality Score
✓ Validation Result
✓ Validation State
---
# Module Rules
1. QualityValidator yagona Data Quality Validator.
2. Data o'zgartirilmaydi.
3. Quality Score majburiy.
4. Circular Dependency taqiqlanadi.
---
# Summary
QualityValidator Data Validation Layer ichidagi Canonical Data Quality Validation moduli hisoblanadi.
