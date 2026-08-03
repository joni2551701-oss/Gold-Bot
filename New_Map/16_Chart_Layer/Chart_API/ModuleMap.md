# Chart API Module Map
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Chart_API ichki arxitekturasini tavsiflaydi (Blueprint bosqichi — ichki submodullar implementatsiya bosqichida qo'shiladi).
---
# Module Position
```text
GoldBot Core
↓
Chart_API
↓
Chart_Core
```
---
# Module Architecture (Blueprint)
```text
Chart_API
        │
(ichki submodullar implementatsiya bosqichida aniqlanadi)
```
---
# Allowed Dependencies
✓ Chart_Core
✓ Analysis_Overlay
✓ Plugins
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
Chart_API GoldBot Chart Layer ichidagi Chart API moduli hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, Foundation Freeze'dan keyin ichki submodullar (papkalar) haqiqiy implementatsiya bilan to'ldiriladi.
