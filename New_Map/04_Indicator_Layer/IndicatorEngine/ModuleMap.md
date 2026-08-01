# IndicatorEngine Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat IndicatorEngine modulining ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
Market Context
↓
IndicatorEngine
↓
Indicator Modules
↓
IndicatorService
```
---
# Module Architecture
```text
IndicatorEngine
        │
        ├── Configuration Manager
        ├── Dependency Manager
        ├── Pipeline Manager
        ├── Execution Manager
        ├── Validation Manager
        ├── State Manager
        ├── Event Generator
        └── Report Manager
```
---
# Internal Components
## Configuration Manager
Indicator konfiguratsiyalarini yuklaydi.
---
## Dependency Manager
Modullar orasidagi bog'liqlikni tekshiradi.
---
## Pipeline Manager
Indicator Pipeline'ni boshqaradi.
---
## Execution Manager
Barcha indikator modullarini ishga tushiradi.
---
## Validation Manager
Hisoblangan natijalarni tekshiradi.
---
## State Manager
Runtime holatini boshqaradi.
---
## Event Generator
Indicator Runtime Event yaratadi.
---
## Report Manager
Runtime hisobotlarini tayyorlaydi.
---
# Dependency Map
```text
Market Context
↓
IndicatorEngine
↓
Indicator Modules
↓
IndicatorService
```
---
# Allowed Dependencies
✓ Context Layer
✓ Event System
✓ Indicator Modules
✓ IndicatorService
---
# Forbidden Dependencies
✗ Strategy Layer
✗ Signal Layer
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Monitoring Layer
---
# Ownership
IndicatorEngine egalik qiladi.
✓ Pipeline State
✓ Execution State
✓ Runtime Metadata
✓ Execution Events
---
# Module Rules
1. IndicatorEngine faqat Orchestrator hisoblanadi.
2. Indicator formulalari bu modulda bo'lmaydi.
3. Indicator Pipeline deterministik bo'lishi kerak.
4. Circular Dependency taqiqlanadi.
---
# Summary
IndicatorEngine Indicator Layer ichidagi barcha indikator modullarini boshqaruvchi Canonical Orchestrator hisoblanadi.
