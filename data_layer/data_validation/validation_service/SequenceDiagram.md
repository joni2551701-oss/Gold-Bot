# ValidationService Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat ValidationService modulining Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu ValidationService modulining Canonical Runtime Blueprint hisoblanadi.
---
# Complete Runtime Sequence
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
# Startup Sequence
```text
System Start
↓
ValidationService
↓
Initialize Validators
↓
Verify Validation State
↓
Ready
```
---
# Validation Sequence
```text
Validation Request
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
Validation Complete
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
ValidationService
↓
Stop Validators
↓
Release Resources
↓
Stopped
```
---
# Runtime Rules
1. ValidationService barcha Validator'larni boshqaradi.
2. Validation Pipeline ketma-ket bajariladi.
3. Recovery markazlashgan boshqariladi.
4. Runtime State doim kuzatiladi.
5. Circular Runtime Sequence taqiqlanadi.
---
# State Flow
```text
Idle
↓
Initializing
↓
Ready
↓
Running
↓
Recovering
↓
Stopping
↓
Stopped
or
Failed
```
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
