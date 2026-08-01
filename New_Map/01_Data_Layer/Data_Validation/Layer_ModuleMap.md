# Data Validation Layer Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat Data Validation Layer ichidagi barcha modullar va ularning o'zaro bog'lanishini tavsiflaydi.
---
# Layer Architecture
```text
Data Validation Layer
          │
          ▼
  ValidationService
          │
 ┌────────┼─────────┐
 ▼        ▼         ▼
DataValidator
SchemaValidator
QualityValidator
IntegrityValidator
ValidationLifecycle
```
---
# Layer Modules
## ValidationService
Layer Orchestrator.
---
## DataValidator
Primary Validation.
---
## SchemaValidator
Schema Validation.
---
## QualityValidator
Data Quality Validation.
---
## IntegrityValidator
Data Integrity Validation.
---
## ValidationLifecycle
Validation Lifecycle Management.
---
# Dependency Map
```text
Runtime Data
↓
ValidationService
↓
DataValidator
↓
SchemaValidator
↓
QualityValidator
↓
IntegrityValidator
↓
ValidationLifecycle
↓
Validated Data
```
---
# Ownership
Layer egalik qiladi.
✓ Validation Pipeline
✓ Validation Workflow
✓ Validation Lifecycle
✓ Runtime Validation State
✓ Validation Results
---
# Rules
1. ValidationService yagona Orchestrator.
2. DataValidator yagona Primary Validator.
3. SchemaValidator faqat Schema tekshiradi.
4. QualityValidator faqat Quality tekshiradi.
5. IntegrityValidator faqat Integrity tekshiradi.
6. ValidationLifecycle Lifecycle boshqaradi.
7. Circular Dependency taqiqlanadi.
---
# Summary
Data Validation Layer GoldBot Runtime davomida barcha Validation jarayonlarini boshqaruvchi Canonical Validation Layer hisoblanadi.
