# Layout Module Map
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Layout ichki arxitekturasini tavsiflaydi (Blueprint bosqichi — ichki submodullar implementatsiya bosqichida qo'shiladi).
---
# Module Position
```text
Chart_API
↓
Layout
↓
Chart_Core
```
---
# Module Architecture (Blueprint)
```text
Layout
        │
(ichki submodullar implementatsiya bosqichida aniqlanadi)
```
---
# Allowed Dependencies
✓ Chart_API
✓ Chart_Core
✓ Templates
---
# Forbidden Dependencies
✗ Signal Layer
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Database Layer
✗ Platform Layer
---
# Summary
Layout GoldBot Chart Layer ichidagi Layout moduli hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, Foundation Freeze'dan keyin ichki submodullar (papkalar) haqiqiy implementatsiya bilan to'ldiriladi.
