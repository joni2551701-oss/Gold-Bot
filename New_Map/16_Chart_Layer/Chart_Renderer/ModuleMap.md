# Chart Renderer Module Map
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Chart_Renderer ichki arxitekturasini tavsiflaydi (Blueprint bosqichi — ichki submodullar implementatsiya bosqichida qo'shiladi).
---
# Module Position
```text
Chart_Data
↓
Chart_Renderer
↓
Chart_Interaction
```
---
# Module Architecture (Blueprint)
```text
Chart_Renderer
        │
(ichki submodullar implementatsiya bosqichida aniqlanadi)
```
---
# Allowed Dependencies
✓ Chart_Data
✓ Chart_Interaction
✓ Objects
✓ Theme
✓ Crosshair
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
Chart_Renderer GoldBot Chart Layer ichidagi Chart Renderer moduli hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, Foundation Freeze'dan keyin ichki submodullar (papkalar) haqiqiy implementatsiya bilan to'ldiriladi.
