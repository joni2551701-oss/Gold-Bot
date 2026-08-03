# Chart Data Module Map
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Chart_Data ichki arxitekturasini tavsiflaydi (Blueprint bosqichi — ichki submodullar implementatsiya bosqichida qo'shiladi).
---
# Module Position
```text
Chart_Core
↓
Chart_Data
↓
Chart_Renderer
```
---
# Module Architecture (Blueprint)
```text
Chart_Data
        │
(ichki submodullar implementatsiya bosqichida aniqlanadi)
```
---
# Allowed Dependencies
✓ Chart_Core
✓ Chart_Renderer
✓ Replay
✓ Timeframe
✓ Symbols
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
Chart_Data GoldBot Chart Layer ichidagi Chart Data moduli hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, Foundation Freeze'dan keyin ichki submodullar (papkalar) haqiqiy implementatsiya bilan to'ldiriladi.
