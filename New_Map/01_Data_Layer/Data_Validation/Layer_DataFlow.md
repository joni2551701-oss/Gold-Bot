# Data Validation Layer Data Flow
Status: CANONICAL
---
# Purpose
Ushbu hujjat Data Validation Layer ichidagi barcha Runtime Data Flow'ni tavsiflaydi.
Data Validation Layer GoldBot Runtime davomida kiruvchi ma'lumotlarning to'liq validatsiyasini amalga oshiruvchi yagona Canonical Validation Layer hisoblanadi.
Bu implementatsiya emas.
Bu Data Validation Layer'ning Canonical Runtime Data Flow hujjati hisoblanadi.
---
# Layer Position
```text
Runtime Data
↓
Data Validation Layer
↓
Validated Data
```
---
# Complete Validation Flow
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
# Runtime Validation Flow
```text
Receive Runtime Data
↓
Validate Input
↓
Validate Schema
↓
Validate Quality
↓
Validate Integrity
↓
Complete Validation
↓
Validated Data
```
---
# Failure Flow
```text
Runtime Data
↓
Validation Failed
↓
ValidationLifecycle
↓
Retry
or
Reject Data
```
---
# Recovery Flow
```text
Validation Failure
↓
Recovery
↓
Restore Validation State
↓
Resume Validation
```
---
# Layer Rules
1. DataValidator birinchi Validation bosqichi.
2. SchemaValidator strukturani tekshiradi.
3. QualityValidator sifatni tekshiradi.
4. IntegrityValidator yaxlitlikni tekshiradi.
5. ValidationLifecycle barcha Validation jarayonini kuzatadi.
6. ValidationService barcha Validator'larni boshqaradi.
7. Invalid Data keyingi Layer'ga uzatilmaydi.
8. Circular Validation Flow taqiqlanadi.
---
# Summary
Canonical Validation Flow:
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
