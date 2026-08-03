# ValidationService Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat ValidationService modulining ichki arxitekturasi va komponentlarini tavsiflaydi.
---
# Module Position
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
```
---
# Module Architecture
```text
ValidationService
        │
        ├── Request Manager
        ├── Validation Coordinator
        ├── Runtime Manager
        ├── Lifecycle Manager
        ├── Recovery Manager
        ├── Health Monitor
        ├── State Manager
        └── Event Generator
```
---
# Internal Components
## Request Manager
Validation Request qabul qiladi.
---
## Validation Coordinator
Barcha Validator'larni boshqaradi.
---
## Runtime Manager
Validation Runtime'ni boshqaradi.
---
## Lifecycle Manager
Validation Lifecycle bilan ishlaydi.
---
## Recovery Manager
Recovery jarayonini boshqaradi.
---
## Health Monitor
Validation Layer sog'ligini kuzatadi.
---
## State Manager
Runtime holatini boshqaradi.
---
## Event Generator
Validation Runtime Event'larini yaratadi.
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
```
---
# Allowed Dependencies
✓ DataValidator
✓ SchemaValidator
✓ QualityValidator
✓ IntegrityValidator
✓ ValidationLifecycle
✓ Event System
✓ Configuration Layer
---
# Forbidden Dependencies
✗ Context Layer
✗ Strategy Layer
✗ Decision Layer
✗ Risk Layer
✗ AI Layer
✗ Platform Layer
✗ Business Layer
✗ Learning Layer
✗ Media Layer
✗ Future Expansion Layer
---
# Ownership
ValidationService egalik qiladi.
✓ Validation Workflow
✓ Runtime State
✓ Lifecycle State
✓ Recovery State
✓ Health State
---
# Module Rules
1. ValidationService yagona Canonical Orchestrator.
2. Validation Pipeline markazlashgan boshqariladi.
3. Validator'lar mustaqil ishlamaydi.
4. Circular Dependency taqiqlanadi.
---
# Summary
ValidationService Data Validation Layer ichidagi barcha Validation modullarini boshqaruvchi yagona Canonical Orchestrator moduli hisoblanadi.
