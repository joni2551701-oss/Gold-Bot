# Templates Module Map
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Templates ichki arxitekturasini tavsiflaydi (Blueprint bosqichi — ichki submodullar implementatsiya bosqichida qo'shiladi).
---
# Module Position
```text
Chart_API
↓
Templates
↓
Chart_Core
```
---
# Module Architecture (Blueprint)
```text
Templates
        │
(ichki submodullar implementatsiya bosqichida aniqlanadi)
```
---
# Allowed Dependencies
✓ Chart_API
✓ Chart_Core
✓ Layout
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
Templates GoldBot Chart Layer ichidagi Templates moduli hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, Foundation Freeze'dan keyin ichki submodullar (papkalar) haqiqiy implementatsiya bilan to'ldiriladi.
