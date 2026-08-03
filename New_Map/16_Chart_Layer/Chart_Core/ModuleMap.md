# Chart Core Module Map
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Chart_Core ichki arxitekturasini tavsiflaydi (Blueprint bosqichi — ichki submodullar implementatsiya bosqichida qo'shiladi).
---
# Module Position
```text
Chart_API
↓
Chart_Core
↓
Chart_Data
```
---
# Module Architecture (Blueprint)
```text
Chart_Core
        │
(ichki submodullar implementatsiya bosqichida aniqlanadi)
```
---
# Allowed Dependencies
✓ Chart_API
✓ Chart_Data
✓ Templates
✓ Layout
✓ Settings
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
Chart_Core GoldBot Chart Layer ichidagi Chart Core moduli hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, Foundation Freeze'dan keyin ichki submodullar (papkalar) haqiqiy implementatsiya bilan to'ldiriladi.
