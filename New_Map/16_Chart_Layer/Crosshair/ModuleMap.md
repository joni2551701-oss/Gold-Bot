# Crosshair Module Map
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Crosshair ichki arxitekturasini tavsiflaydi (Blueprint bosqichi — ichki submodullar implementatsiya bosqichida qo'shiladi).
---
# Module Position
```text
Chart_Interaction
↓
Crosshair
↓
Chart_Renderer
```
---
# Module Architecture (Blueprint)
```text
Crosshair
        │
(ichki submodullar implementatsiya bosqichida aniqlanadi)
```
---
# Allowed Dependencies
✓ Chart_Interaction
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
Crosshair GoldBot Chart Layer ichidagi Crosshair moduli hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, Foundation Freeze'dan keyin ichki submodullar (papkalar) haqiqiy implementatsiya bilan to'ldiriladi.
