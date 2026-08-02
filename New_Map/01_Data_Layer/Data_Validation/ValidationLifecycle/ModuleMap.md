# ValidationLifecycle Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat ValidationLifecycle modulining ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
ValidationService
↓
ValidationLifecycle
```
---
# Module Architecture
```text
ValidationLifecycle
        │
        ├── Lifecycle Manager
        ├── State Manager
        ├── Timeout Manager
        ├── Retry Manager
        ├── Completion Manager
        ├── Cleanup Manager
        ├── Metadata Manager
        └── Event Generator
```
---
# Internal Components
## Lifecycle Manager
Validation Lifecycle boshqaradi.
---
## State Manager
Validation holatini boshqaradi.
---
## Timeout Manager
Validation Timeout kuzatadi.
---
## Retry Manager
Retry jarayonini boshqaradi.
---
## Completion Manager
Validation yakunlanganini boshqaradi.
---
## Cleanup Manager
Validation tugagandan keyin resurslarni tozalaydi.
---
## Metadata Manager
Lifecycle Metadata boshqaradi.
---
## Event Generator
Lifecycle Event yaratadi.
---
# Dependency Map
```text
ValidationService
↓
ValidationLifecycle
```
---
# Allowed Dependencies
✓ ValidationService
✓ Event System
✓ Configuration Layer
---
# Forbidden Dependencies
✗ Strategy Layer
✗ Decision Layer
✗ Risk Layer
✗ AI Layer
✗ Business Layer
---
# Ownership
ValidationLifecycle egalik qiladi.
✓ Lifecycle State
✓ Retry State
✓ Timeout State
✓ Completion State
✓ Lifecycle Metadata
---
# Module Rules
1. ValidationLifecycle yagona Lifecycle Manager.
2. Validation State qat'iy kuzatiladi.
3. Retry boshqariladi.
4. Timeout boshqariladi.
5. Circular Dependency taqiqlanadi.
---
# Summary
ValidationLifecycle Data Validation Layer ichidagi Canonical Validation Lifecycle moduli hisoblanadi.
