# Drawing Tools Module Map
Status: BLUEPRINT
---
# Purpose
Ushbu hujjat Drawing_Tools ichki arxitekturasini tavsiflaydi (Blueprint bosqichi — ichki submodullar implementatsiya bosqichida qo'shiladi).
---
# Module Position
```text
Objects
↓
Drawing_Tools
↓
Indicators
```
---
# Module Architecture (Blueprint)
```text
Drawing_Tools
        │
(ichki submodullar implementatsiya bosqichida aniqlanadi)
```
---
# Allowed Dependencies
✓ Objects
✓ Indicators
✓ Templates
✓ Alerts
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
Drawing_Tools GoldBot Chart Layer ichidagi Drawing Tools moduli hisoblanadi. Bu hujjat Blueprint bosqichida bo'lib, Foundation Freeze'dan keyin ichki submodullar (papkalar) haqiqiy implementatsiya bilan to'ldiriladi.
