# Indicators Module Map
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Indicators ichki arxitekturasini tavsiflaydi (Blueprint bosqichi — ichki submodullar implementatsiya bosqichida qo'shiladi).
---
# Module Position
```text
Drawing_Tools
↓
Indicators
↓
Analysis_Overlay
```
---
# Module Architecture (Blueprint)
```text
Indicators
        │
(ichki submodullar implementatsiya bosqichida aniqlanadi)
```
---
# Allowed Dependencies
✓ Drawing_Tools
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
Indicators GoldBot Chart Layer ichidagi Indicators moduli hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, Foundation Freeze'dan keyin ichki submodullar (papkalar) haqiqiy implementatsiya bilan to'ldiriladi.
