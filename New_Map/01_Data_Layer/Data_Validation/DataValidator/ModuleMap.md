# DataValidator Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat DataValidator modulining ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
Data Source
↓
DataValidator
↓
SchemaValidator
```
---
# Module Architecture
```text
DataValidator
        │
        ├── Input Manager
        ├── Rule Manager
        ├── Validation Engine
        ├── Result Builder
        ├── Event Generator
        ├── State Manager
        └── Report Manager
```
---
# Internal Components
## Input Manager
Kiruvchi Data'ni qabul qiladi.
---
## Rule Manager
Validation Rule'larni boshqaradi.
---
## Validation Engine
Asosiy Validation jarayonini bajaradi.
---
## Result Builder
Validation Result yaratadi.
---
## Event Generator
Validation Event yaratadi.
---
## State Manager
Validation holatini boshqaradi.
---
## Report Manager
Validation Report yaratadi.
---
# Dependency Map
```text
Data Source
↓
DataValidator
↓
SchemaValidator
```
---
# Allowed Dependencies
✓ SchemaValidator
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
DataValidator egalik qiladi.
✓ Validation Rules
✓ Validation State
✓ Validation Result
✓ Validation Report
---
# Module Rules
1. DataValidator Primary Validator hisoblanadi.
2. Validation Data'ni o'zgartirmaydi.
3. Validation natijasi doimo yaratiladi.
4. Circular Dependency taqiqlanadi.
---
# Summary
DataValidator Data Validation Layer ichidagi Canonical Primary Validation moduli hisoblanadi.
