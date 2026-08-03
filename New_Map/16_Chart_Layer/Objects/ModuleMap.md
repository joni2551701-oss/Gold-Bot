# Objects Module Map
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Objects ichki arxitekturasini tavsiflaydi (Blueprint bosqichi — ichki submodullar implementatsiya bosqichida qo'shiladi).
---
# Module Position
```text
Chart_Interaction
↓
Objects
↓
Drawing_Tools
```
---
# Module Architecture (Blueprint)
```text
Objects
        │
(ichki submodullar implementatsiya bosqichida aniqlanadi)
```
---
# Allowed Dependencies
✓ Chart_Interaction
✓ Drawing_Tools
✓ Chart_Renderer
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
Objects GoldBot Chart Layer ichidagi Objects moduli hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, Foundation Freeze'dan keyin ichki submodullar (papkalar) haqiqiy implementatsiya bilan to'ldiriladi.
