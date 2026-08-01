# SchemaValidator Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat SchemaValidator modulining ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
DataValidator
↓
SchemaValidator
↓
QualityValidator
```
---
# Module Architecture
```text
SchemaValidator
        │
        ├── Schema Loader
        ├── Structure Validator
        ├── Field Validator
        ├── Type Validator
        ├── Version Validator
        ├── Result Builder
        ├── State Manager
        └── Event Generator
```
---
# Internal Components
## Schema Loader
Schema yuklaydi.
---
## Structure Validator
Strukturani tekshiradi.
---
## Field Validator
Required va Optional Field'larni tekshiradi.
---
## Type Validator
Data Type'larni tekshiradi.
---
## Version Validator
Schema Version'ni tekshiradi.
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
DataValidator
↓
SchemaValidator
↓
QualityValidator
```
---
# Allowed Dependencies
✓ DataValidator
✓ QualityValidator
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
SchemaValidator egalik qiladi.
✓ Schema Rules
✓ Schema Metadata
✓ Validation State
✓ Validation Result
---
# Module Rules
1. SchemaValidator yagona Schema Validation komponenti.
2. Schema Validation Data mazmunini o'zgartirmaydi.
3. Validation Result majburiy.
4. Circular Dependency taqiqlanadi.
---
# Summary
SchemaValidator Data Validation Layer ichidagi Canonical Schema Validation moduli hisoblanadi.
