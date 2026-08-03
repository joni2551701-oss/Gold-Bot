# Data Validation Layer Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat Data Validation Layer Runtime Sequence'ni tavsiflaydi.
---
# Complete Runtime Sequence
```text
System Start
↓
ValidationService
↓
Initialize Validators
↓
Initialize ValidationLifecycle
↓
Ready
```
---
# Runtime Validation Sequence
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
# Recovery Sequence
```text
Validation Failure
↓
ValidationService
↓
Restore Validators
↓
Restore Lifecycle
↓
Resume Validation
```
---
# Shutdown Sequence
```text
Shutdown
↓
Stop Validation
↓
Release Resources
↓
Stopped
```
---
# Runtime Rules
1. ValidationService Runtime'ni boshqaradi.
2. Validation qat'iy ketma-ket bajariladi.
3. ValidationLifecycle barcha Validation'larni kuzatadi.
4. Recovery markazlashgan boshqariladi.
5. Circular Runtime Sequence taqiqlanadi.
---
# Summary
Canonical Runtime Sequence:
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
